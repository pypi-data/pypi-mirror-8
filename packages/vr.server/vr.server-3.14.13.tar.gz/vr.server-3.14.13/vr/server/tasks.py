import contextlib
import datetime
import functools
import logging
import traceback
import time
import json

from hashlib import md5
from collections import defaultdict

from six.moves import range

import yaml
import fabric.network
import redis
from celery.task import subtask, chord, task
from fabric.api import env
from django.conf import settings
from django.utils import timezone
from django.core.files import File

from vr.builder.main import BuildData
from vr.common import utils
from vr.common.models import Proc
from vr.common.utils import tmpdir
from vr.server import events, balancer, remote
from vr.server.models import (
    Release, Build, Swarm, Host, PortLock, TestRun, TestResult, BuildPack,
)


logger = logging.getLogger('velociraptor')


def send_event(title, msg, tags=None, **kw):
    logger.info(msg)
    # Create and discard connections when needed.  More robust than trying to
    # hold them open for a long time.
    sender = events.EventSender(
        settings.EVENTS_PUBSUB_URL,
        settings.EVENTS_PUBSUB_CHANNEL,
        settings.EVENTS_BUFFER_KEY,
        settings.EVENTS_BUFFER_LENGTH,
    )
    sender.publish(msg, title=title, tags=tags, **kw)
    sender.close()


def send_debug_event(title, msg=''):
    if settings.DEBUG:
        send_event(title, msg, tags=['debug'])


class event_on_exception(object):
    """
    Decorator that puts a message on the pubsub for any exception raised in the
    decorated function.
    """
    def __init__(self, tags=None):
        self.tags = tags or []
        self.tags.append('failed')

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except remote.Error as e:

                swarm_trace_id = kwargs.get('swarm_trace_id')

                try:
                    send_event(title=e.title, msg=e.out, tags=self.tags,
                               swarm_trace_id=swarm_trace_id)
                finally:
                    raise
            except (Exception, SystemExit) as e:
                try:
                    send_event(title=str(e), msg=traceback.format_exc(),
                               tags=self.tags,
                               swarm_trace_id=swarm_trace_id)
                finally:
                    raise
        return wrapper


def build_proc_info(release, config_name, hostname, proc, port):
    """
    Return a dictionary with exhaustive metadata about a proc.  This is saved
    as the proc.yaml file that is given to the runner.
    """

    build = release.build
    app = build.app
    proc_info = {
        'release_hash': release.hash,
        'config_name': config_name,
        'settings': release.config_yaml or {},
        'env': release.env_yaml or {},
        'version': build.tag,
        'build_md5': build.file_md5,
        'build_url': build.file.url,
        'buildpack_url': build.buildpack_url,
        'buildpack_version': build.buildpack_version,
        'app_name': app.name,
        'app_repo_url': app.repo_url,
        'app_repo_type': app.repo_type,
        'host': hostname,
        'proc_name': proc,
        'port': port,
        'user': release.run_as or 'nobody',
        'group': 'nogroup',
        'volumes': release.volumes or [],
        'mem_limit': release.mem_limit,
        'memsw_limit': release.memsw_limit,
    }

    if build.os_image is not None:
        proc_info.update({
            'image_name': build.os_image.name,
            'image_url': build.os_image.file.url,
            'image_md5': build.os_image.file_md5,
        })

    return proc_info


@task
@event_on_exception(['deploy'])
def deploy(release_id, config_name, hostname, proc, port, swarm_trace_id=None):
    with remove_port_lock(hostname, port):
        release = Release.objects.get(id=release_id)
        msg_title = '%s-%s-%s' % (release.build.app.name, release.build.tag, proc)
        logging.info('beginning deploy of %s-%s-%s to %s' % (release, proc,
                                                             port,
                                                             hostname))

        msg = 'deploying %s-%s-%s to %s' % (release, proc, port, hostname)
        send_event(title=msg_title, msg=msg, tags=['deploy'],
                   swarm_id=swarm_trace_id)

        assert release.build.file, "Build %s has no file" % release.build
        assert release.hash, "Release %s has not been hashed" % release

        # Set up env for Fabric
        env.host_string = hostname
        env.abort_on_prompts = True
        env.task = deploy
        env.user = settings.DEPLOY_USER
        env.password = settings.DEPLOY_PASSWORD
        env.linewise = True

        with tmpdir():

            # write the proc.yaml locally
            with open('proc.yaml', 'wb') as f:
                info = build_proc_info(release, config_name, hostname, proc, port)
                f.write(yaml.safe_dump(info, default_flow_style=False))

            with always_disconnect():
                remote.deploy_proc('proc.yaml')


@task
@event_on_exception(['build'])
def build_app(build_id, callback=None, swarm_trace_id=None):
    build = Build.objects.get(id=build_id)
    build.start()
    build.save()

    build_yaml = BuildData(get_build_parameters(build)).as_yaml()
    build_msg = "Started build %s" % build + '\n\n' + build_yaml
    send_event(str(build), build_msg, tags=['build'],
               swarm_id=swarm_trace_id)

    _do_build(build, build_yaml)

    # start callback if there is one.
    if callback is not None:
        subtask(callback).delay()

    # If there were any other swarms waiting on this build, kick them off
    build_start_waiting_swarms(build.id)


def _do_build(build, build_yaml):
    # enter a temp folder
    with tmpdir():
        try:
            with open('build_job.yaml', 'wb') as f:
                f.write(build_yaml)
            # call the fabric build task to ssh to self and do the build
            env.host_string = 'localhost'
            env.abort_on_prompts = True
            env.task = build_app
            env.user = settings.DEPLOY_USER
            env.password = settings.DEPLOY_PASSWORD
            env.linewise = True
            remote.build_app('build_job.yaml')

            # store the build file and metadata in the database.  There should
            # now be a build.tar.gz and build_result.yaml in the current folder
            with open('build_result.yaml', 'rb') as f:
                build_result = BuildData(yaml.safe_load(f))

            build_name = '-'.join([
                build_result.app_name,
                build_result.version,
                build_result.build_md5
            ])
            filepath = 'builds/' + build_name + '.tar.gz'
            with open('build.tar.gz', 'rb') as localfile:
                build.file.save(filepath, File(localfile))
            build.file_md5 = build_result.build_md5
            build.env_yaml = build_result.release_data.get('config_vars', {})
            build.buildpack_url = build_result.buildpack_url
            build.buildpack_version = build_result.buildpack_version
            build.status = 'success'
        except:
            build.status = 'failed'
            raise
        finally:
            try:
                # grab and store the compile log.
                with open('compile.log', 'rb') as f:
                    logname = 'builds/build_%s_compile.log' % build.id
                    build.compile_log.save(logname, File(f))
            except:
                logger.info('Could not retrieve compile.log for %s' % build)
            finally:
                build.end_time = timezone.now()
                build.save()

    send_event(str(build), "Completed build %s" % build, tags=['build',
                                                               'success'])


def get_build_parameters(build):
    """Return a dictionary of Heroku-style build parameters."""
    app = build.app
    os_image = build.os_image

    build_params = {
        'app_name': app.name,
        'app_repo_url': app.repo_url,
        'app_repo_type': app.repo_type,
        'version': build.tag,
    }

    if os_image is not None:
        build_params.update({
            'image_name': os_image.name,
            'image_url': os_image.file.url,
            'image_md5': os_image.file_md5,
        })

    if app.buildpack:
        build_params['buildpack_url'] = app.buildpack.repo_url
    else:
        buildpacks = BuildPack.objects.order_by('order')
        urls = [bp.repo_url for bp in buildpacks]
        build_params['buildpack_urls'] = urls

    return build_params


@task
@event_on_exception(['proc', 'deleted'])
def delete_proc(host, proc, callback=None, swarm_trace_id=None):
    env.host_string = host
    env.abort_on_prompts = True
    env.user = settings.DEPLOY_USER
    env.password = settings.DEPLOY_PASSWORD
    env.linewise = True
    with always_disconnect():
        remote.delete_proc(host, proc)

    send_event(Proc.name_to_shortname(proc),
               'deleted %s on %s' % (proc, host),
               tags=['proc', 'deleted'],
               swarm_id=swarm_trace_id)

    if callback:
        subtask(callback).delay()


def create_wait_value(swarm_id, swarm_trace_id=None):
    swarm_trace_id = swarm_trace_id or ''
    return json.dumps({'swarm_id': swarm_id,
                       'swarm_trace_id': swarm_trace_id})


def read_wait_value(key):
    # If we can't parse assume the key is the swarm_id
    doc = {'swarm_id': key, 'swarm_trace_id': None}
    try:
        doc = json.loads(key)
    except:
        pass

    return doc['swarm_id'], doc['swarm_trace_id']


def swarm_wait_for_build(swarm, build, swarm_trace_id=None):
    """
    Given a swarm that you want to have swarmed ASAP, and a build that the
    swarm is waiting to finish, push the swarm's ID onto the build's waiting
    list.
    """
    msg = 'Swarm %s waiting for completion of build %s' % (swarm, build)
    send_event('%s waiting' % swarm, msg, ['wait'], swarm_trace_id=swarm_trace_id)
    with tmpredis() as r:
        key = getattr(settings, 'BUILD_WAIT_PREFIX', 'buildwait_') + str(build.id)
        r.lpush(key, create_wait_value(swarm.id, swarm_trace_id))
        r.expire(key, getattr(settings, 'BUILD_WAIT_AGE', 3600))


def build_start_waiting_swarms(build_id):
    """
    Check Redis for the list of swarms waiting on a particular build.  Pop each
    off the list and call swarm_start for it.
    """
    with tmpredis() as r:
        key = getattr(settings, 'BUILD_WAIT_PREFIX', 'buildwait_') + str(build_id)
        swarm_id, swarm_trace_id = read_wait_value(r.lpop(key))
        while swarm_id:
            swarm_start.delay(swarm_id, swarm_trace_id)
            swarm_id = r.lpop(key)


@task
def swarm_start(swarm_id, swarm_trace_id=None):
    """
    Given a swarm_id, kick off the chain of tasks necessary to get this swarm
    deployed.
    """
    swarm = Swarm.objects.get(id=swarm_id)
    build = swarm.release.build

    if not swarm_trace_id:
        swarm_trace_id = md5(str(swarm) + str(time.time())).hexdigest()

    if build.is_usable():
        # Build is good.  Do a release.
        swarm_release.delay(swarm_id, swarm_trace_id)
    elif build.in_progress():
        # Another swarm call already started a build for this app/tag.  Instead
        # of starting a duplicate, just push the swarm ID onto the build's
        # waiting list.
        swarm_wait_for_build(swarm, build, swarm_trace_id)
    else:
        # Build hasn't been kicked off yet.  Do that now.
        callback = swarm_release.subtask((swarm.id, swarm_trace_id))
        build_app.delay(build.id, callback, swarm_trace_id)


# This task should only be used as a callback after swarm_start
@task
def swarm_release(swarm_id, swarm_trace_id=None):
    """
    Assuming the swarm's build is complete, this task will ensure there's a
    release with that build + current config, and call subtasks to make sure
    there are enough deployments.
    """
    send_debug_event('swarm release')
    swarm = Swarm.objects.get(id=swarm_id)
    build = swarm.release.build

    # Bail out if the build doesn't have a file
    assert build.file, "Build %s has no file" % build

    # swarm.get_current_release(tag) will check whether there's a release with
    # the right build and config, and create one if not.
    swarm.release = swarm.get_current_release(build.os_image, build.tag)
    swarm.save()

    # OK we have a release.  Next: see if we need to do a deployment.
    # Query squad for list of procs.
    all_procs = swarm.get_procs()
    current_procs = [p for p in all_procs if p.hash == swarm.release.hash]

    procs_needed = swarm.size - len(current_procs)

    if procs_needed > 0:
        hosts = swarm.get_prioritized_hosts()
        hostcount = len(hosts)

        # Build up a dictionary where the keys are hostnames, and the
        # values are lists of ports.
        new_procs_by_host = defaultdict(list)
        for x in range(procs_needed):
            host = hosts[x % hostcount]
            port = host.get_next_port()
            new_procs_by_host[host.name].append(port)

            # Ports need to be locked here in the synchronous loop, before
            # fanning out the async subtasks, in order to prevent collisions.
            pl = PortLock(host=host, port=port)
            pl.save()

        # Now loop over the hosts and fan out a task to each that needs it.
        subtasks = []
        for host in hosts:
            if host.name in new_procs_by_host:
                subtasks.append(
                    swarm_deploy_to_host.subtask((
                        swarm.id,
                        host.id,
                        new_procs_by_host[host.name],
                        swarm_trace_id
                    ))
                )
        callback = swarm_post_deploy.subtask((swarm.id, swarm_trace_id))
        chord(subtasks)(callback)
    elif procs_needed < 0:
        # We need to delete some procs

        # reverse prioritized list so the most loaded hosts get things removed
        # first.
        hosts = swarm.get_prioritized_hosts()
        hosts.reverse()
        hostcount = len(hosts)
        subtasks = []
        for x in range(procs_needed * -1):
            host = hosts[x % hostcount]
            proc = host.swarm_procs.pop()
            subtasks.append(
                swarm_delete_proc.subtask(
                    (swarm.id, host.name, proc.name, proc.port),
                    {'swarm_trace_id': swarm_trace_id}
                )

            )
        callback = swarm_post_deploy.subtask((swarm.id, swarm_trace_id))
        chord(subtasks)(callback)
    else:
        # We have just the right number of procs.  Uptest and route them.
        swarm_assign_uptests(swarm.id, swarm_trace_id)


@task
def swarm_deploy_to_host(swarm_id, host_id, ports, swarm_trace_id=None):
    """
    Given a swarm, a host, and a list of ports, deploy the swarm's current
    release to the host, one instance for each port.
    """
    # This function allows a swarm's deployments to be parallel across
    # different hosts, but synchronous on a per-host basis, which solves the
    # problem of two deployments both trying to copy the release over at the
    # same time.

    swarm = Swarm.objects.get(id=swarm_id)
    host = Host.objects.get(id=host_id)
    for port in ports:
        deploy(
            swarm.release.id,
            swarm.config_name,
            host.name,
            swarm.proc_name,
            port,
            swarm_trace_id,
        )

    procnames = ["%s-%s-%s" % (swarm.release, swarm.proc_name, port) for port
                 in ports]

    return host.name, procnames


@task
def swarm_post_deploy(deploy_results, swarm_id, swarm_trace_id):
    """
    Chord callback run after deployments.  Should check for exceptions, then
    launch uptests.
    """
    if any(isinstance(r, Exception) for r in deploy_results):
        swarm = Swarm.objects.get(id=swarm_id)
        msg = "Error in deployments for swarm %s" % swarm
        send_event('Swarm %s aborted' % swarm, msg,
                   tags=['failed'], swarm_id=swarm_trace_id)
        raise Exception(msg)

    swarm_assign_uptests(swarm_id, swarm_trace_id)


@task
def swarm_assign_uptests(swarm_id, swarm_trace_id=None):
    swarm = Swarm.objects.get(id=swarm_id)
    all_procs = swarm.get_procs()
    current_procs = [p for p in all_procs if p.hash == swarm.release.hash]

    # Organize procs by host
    host_procs = defaultdict(list)
    for proc in current_procs:
        host_procs[proc.host.name].append(proc.name)

    header = [uptest_host_procs.subtask((h, ps)) for h, ps in
              host_procs.items()]

    if len(header):
        this_chord = chord(header)
        callback = swarm_post_uptest.s(swarm_id, swarm_trace_id)
        this_chord(callback)
    else:
        # There are no procs, so there are no uptests to run.  Call
        # swarm_post_uptest with an empty list of uptest results.
        swarm_post_uptest([], swarm_id, swarm_trace_id)


@task
def uptest_host_procs(hostname, procs):
    env.host_string = hostname
    env.abort_on_prompts = True
    env.user = settings.DEPLOY_USER
    env.password = settings.DEPLOY_PASSWORD
    env.linewise = True

    with always_disconnect():
        results = {
            p: remote.run_uptests(hostname, p, settings.PROC_USER)
            for p in procs
        }
    return hostname, results


@task
def uptest_host(hostname, test_run_id=None):
    """
    Given a hostname, look up all its procs and then run uptests on them.
    """

    host = Host.objects.get(name=hostname)
    procs = host.get_procs()
    _, results = uptest_host_procs(hostname, [p.name for p in procs])

    if test_run_id:
        run = TestRun.objects.get(id=test_run_id)
        for procname, resultlist in results.items():
            testcount = len(resultlist)
            if testcount:
                passed = all(r['Passed'] for r in resultlist)
            else:
                # There were no tests :(
                passed = True

            tr = TestResult(
                run=run,
                time=timezone.now(),
                hostname=hostname,
                procname=procname,
                passed=passed,
                testcount=testcount,
                results=yaml.safe_dump(resultlist)
            )
            tr.save()
    return hostname, results


class FailedUptest(Exception):
    pass


@task
def swarm_post_uptest(uptest_results, swarm_id, swarm_trace_id):
    """
    Chord callback that runs after uptests have completed.  Checks that they
    were successful, and then calls routing function.
    """

    # uptest_results will be a list of tuples in form (host, results), where
    # 'results' is a list of dictionaries, one for each test script.

    swarm = Swarm.objects.get(id=swarm_id)
    test_counter = 0
    for host_results in uptest_results:
        if isinstance(host_results, Exception):
            raise host_results
        host, proc_results = host_results

        # results is now a dict
        for proc, results in proc_results.items():
            for result in results:
                test_counter += 1
                # This checking/formatting relies on each uptest result being a
                # dict with 'Passed', 'Name', and 'Output' keys.
                if result['Passed'] is not True:
                    msg = (proc + ": {Name} failed:"
                           "{Output}".format(**result))
                    send_event(str(swarm), msg,
                               tags=['failed', 'uptest'],
                               swarm_id=swarm_trace_id)

                    raise FailedUptest(msg)

    # Don't congratulate swarms that don't actually have any uptests.
    if test_counter > 0:
        send_event("Uptests passed", 'Uptests passed for swarm %s' % swarm,
                   tags=['success', 'uptest'], swarm_id=swarm_trace_id)
    else:
        send_event("No uptests!", 'No uptests for swarm %s' % swarm,
                   tags=['warning', 'uptest'], swarm_id=swarm_trace_id)

    # Also check for captured failures in the results
    correct_nodes = set()
    for host, results in uptest_results:
        # results is now a dictionary keyed by procname
        for procname in results:
            correct_nodes.add('%s:%s' % (host, procname.split('-')[-1]))

    callback = swarm_cleanup.subtask((swarm_id, swarm_trace_id))
    swarm_route.delay(swarm_id, list(correct_nodes), callback,
                      swarm_trace_id=swarm_trace_id)


@task
@event_on_exception(['route'])
def swarm_route(swarm_id, correct_nodes, callback=None, swarm_trace_id=None):
    """
    Given a list of nodes for the current swarm, make sure those nodes and
    only those nodes are in the swarm's routing pool, if it has one.
    """
    # It's important that the correct_nodes list be passed to this function
    # from the uptest finisher, rather than having this function build that
    # list itself, because if it built the list itself it couldn't be sure that
    # all the nodes had been uptested.  It's possible that one could have crept
    # in throuh a non-swarm deployment, for example.

    swarm = Swarm.objects.get(id=swarm_id)
    if swarm.pool:
        # There's just the right number of procs.  Make sure the balancer is up
        # to date, but only if the swarm has a pool specified.

        current_nodes = set(balancer.get_nodes(swarm.balancer, swarm.pool))

        correct_nodes = set(correct_nodes)

        new_nodes = correct_nodes.difference(current_nodes)

        stale_nodes = current_nodes.difference(correct_nodes)

        if new_nodes:
            balancer.add_nodes(swarm.balancer, swarm.pool,
                               list(new_nodes))

        if stale_nodes:
            balancer.delete_nodes(swarm.balancer, swarm.pool,
                                  list(stale_nodes))
        send_event(str(swarm),
                   'Routed swarm %s.  New nodes: %s' % (swarm, list(correct_nodes)),
                   tags=['route'], swarm_id=swarm_trace_id)

    if callback is not None:
        subtask(callback).delay()


@task
def swarm_cleanup(swarm_id, swarm_trace_id):
    """
    Delete any procs in the swarm that aren't from the current release.
    """
    swarm = Swarm.objects.get(id=swarm_id)
    all_procs = swarm.get_procs()
    current_procs = [p for p in all_procs if p.hash == swarm.release.hash]
    stale_procs = [p for p in all_procs if p.hash != swarm.release.hash]

    delete_subtasks = []

    # Only delete old procs if the deploy of the new ones was successful.
    if stale_procs and len(current_procs) >= swarm.size:
        for p in stale_procs:
            # We don't need to worry about removing these nodes from a pool at
            # this point, so just call delete_proc instead of swarm_delete_proc
            delete_subtasks.append(
                delete_proc.subtask((p.host.name, p.name),
                                    {'swarm_trace_id': swarm_trace_id})
            )

    if delete_subtasks:
        chord(delete_subtasks)(swarm_finished.subtask((swarm_id, swarm_trace_id,)))
    else:
        swarm_finished.delay([], swarm_id, swarm_trace_id)


@task
def swarm_finished(result, swarm_id, swarm_trace_id):
    swarm = Swarm.objects.get(id=swarm_id)
    title = msg = 'Swarm %s finished' % swarm
    send_event(title, msg,
               tags=['swarm', 'deploy', 'done'],
               swarm_id=swarm_trace_id)


@task
def swarm_delete_proc(swarm_id, hostname, procname, port, swarm_trace_id=None):
    # wrap the regular delete_proc, but first ensure the proc is removed from
    # the routing pool.  This is done on a per-proc basis because sometimes
    # it's called when deleting old procs, and other times it's called when we
    # just have too many of the current proc.  If it handles its own routing,
    # this function can be used in both places.
    swarm = Swarm.objects.get(id=swarm_id)
    if swarm.pool:
        node = '%s:%s' % (hostname, port)
        if node in balancer.get_nodes(swarm.balancer, swarm.pool):
            balancer.delete_nodes(swarm.balancer, swarm.pool, [node])

    delete_proc(hostname, procname, swarm_trace_id=swarm_trace_id)


@task
def uptest_all_procs():
    # Fan out a task for each active host
    # callback post_uptest_all_procs at the end
    hosts = Host.objects.filter(active=True)

    # Only bother doing anything if there are active hosts
    if hosts:
        # Create a test run record.
        run = TestRun(start=timezone.now())
        run.save()

        def make_test_task(host):
            return uptest_host.subtask((host.name, run.id), expires=120)
        chord((make_test_task(h) for h in hosts))(post_uptest_all_procs.subtask((run.id,)))


@task
def post_uptest_all_procs(results, test_run_id):
    # record test run end time
    run = TestRun.objects.get(id=test_run_id)
    run.end = timezone.now()
    run.save()

    if run.has_failures():
        # Get just the failed TestResult objects.
        fail_results = run.tests.filter(passed=False)

        # Show output for each failed test in each failed result
        msg = '\n\n'.join(f.get_formatted_fails() for f in fail_results)

        send_event('scheduled uptest failures', msg,
                   tags=['scheduled', 'failed'])


@task
def _clean_host(hostname):
    env.host_string = hostname
    env.abort_on_prompts = True
    env.user = settings.DEPLOY_USER
    env.password = settings.DEPLOY_PASSWORD
    env.linewise = True

    with always_disconnect():
        remote.clean_builds_folders()


@task
def scooper():
    # Clean up all active hosts
    for host in Host.objects.filter(active=True):
        _clean_host.apply_async((host.name,), expires=120)


@task
def clean_old_builds():
    # select all builds older than BUILD_EXPIRATION_DAYS where file is not
    # None
    if settings.BUILD_EXPIRATION_DAYS is not None:
        cutoff = (timezone.now() -
                  datetime.timedelta(days=settings.BUILD_EXPIRATION_DAYS))

        old_builds = Build.objects.filter(end_time__lt=cutoff,
                                          file__isnull=False).order_by('-end_time')
        old_builds = set(old_builds)

        # Now filter out any builds that are currently in use
        all_procs = set()
        for host in Host.objects.filter(active=True):
            all_procs.update(host.get_procs())

        builds_in_use = set()
        for p in all_procs:
            rs = Release.objects.filter(hash=p.hash)
            if rs:
                builds_in_use.add(rs[0].build)
        old_builds.difference_update(builds_in_use)

        # Filter out any builds that are still within BUILD_EXPIRATION_COUNT
        def is_recent(build):
            newer_builds = Build.objects.filter(id__gte=build.id,
                                                app=build.app)
            rcnt = newer_builds.count() < settings.BUILD_EXPIRATION_COUNT
            return rcnt
        old_builds.difference_update([b for b in old_builds if is_recent(b)])

        # OK, we now have a set of builds that are older than both our cutoffs,
        # and definitely not in use.  Delete their files to free up space.
        for build in old_builds:
            # TODO: ensure that the mongo storage honors the delete method
            build.file.delete()
            build.status = 'expired'
            build.save()


@contextlib.contextmanager
def always_disconnect():
    """
    to address #18366, disconnect every time.
    """
    try:
        yield
    finally:
        fabric.network.disconnect_all()


class tmpredis(object):
    def __enter__(self):
        self.conn = redis.StrictRedis(
            **utils.parse_redis_url(settings.EVENTS_PUBSUB_URL))
        return self.conn

    def __exit__(self, type, value, tb):
        self.conn.connection_pool.disconnect()


class remove_port_lock(object):
    """
    Context manager for removing a port lock on a host.  Requires a hostname
    and port on init.
    """

    # This used just during deployment.  In general the host itself is the
    # source of truth about what ports are in use. But when deployments are
    # still in flight, port locks are necessary to prevent collisions.

    def __init__(self, hostname, port):
        self.host = Host.objects.get(name=hostname)
        self.port = int(port)

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        try:
            self.lock = PortLock.objects.get(host=self.host, port=self.port)
            self.lock.delete()
        except PortLock.DoesNotExist:
            pass
