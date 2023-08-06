import mock
from django.utils import timezone

from vr.server.models import (App, Build, OSImage, OSStack, Release, Swarm,
                              Squad, release_eq)
from vr.common.utils import randchars


class TestCurrentRelease(object):

    def setup(self):
        self.stack = OSStack(name=randchars(), desc=randchars())
        self.stack.save()

        self.os_image = OSImage(name=randchars(), stack=self.stack,
                                active=True)
        with mock.patch.object(OSImage, '_compute_file_md5',
                               return_value='abcdef1234567890'):
            self.os_image.save()

        self.app = App(name=randchars(), repo_url=randchars(), repo_type='hg',
                      stack=self.stack)
        self.app.save()


        self.version = 'v1'
        self.build = Build(app=self.app, os_image=self.os_image,
                           start_time=timezone.now(), end_time=timezone.now(),
                           tag=self.version, status='success',
                           buildpack_url=randchars(),
                           buildpack_version=randchars(), hash=randchars())
        self.build.save()

        self.env = {'a': 1}
        self.config = {'b': 2}
        self.volumes = [['/foo', '/bar'], ['/baz', '/quux']]

    def test_save_creates_hash(self):
        release = Release(build=self.build, env_yaml=self.env,
                          config_yaml=self.config, volumes=self.volumes)
        release.save()
        assert release.hash  # must not be None or blank.

    def test_release_eq(self):
        r = Release(build=self.build, env_yaml=self.env,
                    config_yaml=self.config, volumes=self.volumes)
        assert release_eq(r, self.config, self.env, self.volumes)

    def test_release_not_eq(self):
        r = Release(build=self.build, env_yaml=self.env,
                    config_yaml=self.config, volumes=self.volumes)
        assert not release_eq(r, {'no': 'match'}, self.env, self.volumes)

    def test_release_eq_empty_config(self):
        r = Release(build=self.build)
        assert release_eq(r, {}, {}, [])

    def test_swarm_with_stack_reuses_release(self):
        squad = Squad(name=randchars())
        squad.save()

        release = Release(build=self.build, env_yaml=self.env,
                          config_yaml=self.config, volumes=self.volumes)
        release.save()

        swarm = Swarm(
            app=self.app,
            release=release,
            config_name=randchars(),
            proc_name=randchars(),
            squad=squad,
            size=1,
            config_yaml=self.config,
            env_yaml=self.env,
            volumes=self.volumes
        )
        swarm.save()

        assert swarm.get_current_release(self.version) == release

    def test_swarm_without_stack_reuses_release(self):
        self.app = App(name=randchars(), repo_url=randchars(), repo_type='hg')
        self.app.save()

        self.build = Build(app=self.app, os_image=None,
                           start_time=timezone.now(), end_time=timezone.now(),
                           tag=self.version, status='success',
                           buildpack_url=randchars(),
                           buildpack_version=randchars(), hash=randchars())
        self.build.save()

        squad = Squad(name=randchars())
        squad.save()

        release = Release(build=self.build, env_yaml=self.env,
                          config_yaml=self.config, volumes=self.volumes)
        release.save()

        swarm = Swarm(
            app=self.app,
            release=release,
            config_name=randchars(),
            proc_name=randchars(),
            squad=squad,
            size=1,
            config_yaml=self.config,
            env_yaml=self.env,
            volumes=self.volumes
        )
        swarm.save()

        assert swarm.get_current_release(self.version) == release


    def test_swarm_creates_release(self):

        # Make an existing release to save with the swarm.
        squad = Squad(name=randchars())
        squad.save()

        release = Release(build=self.build, env_yaml=self.env,
                          config_yaml=self.config, volumes=self.volumes)
        release.save()

        release_count = Release.objects.count()

        swarm = Swarm(
            app=self.app,
            release=release,
            config_name=randchars(),
            proc_name=randchars(),
            squad=squad,
            size=1,
            config_yaml=self.config,
            env_yaml=self.env,
            volumes=self.volumes
        )
        swarm.save()

        # update the swarm with new config.
        swarm.config_yaml = self.config.update({'c': 3})
        swarm.save()

        # get_current_release should make a new release for us from the new
        # config.
        r = swarm.get_current_release(self.version)
        assert Release.objects.count() == release_count + 1
        assert r.id != release.id

    def test_new_osimage_invalidates_release(self):
        # If you have a swarm with a current release, and you get a new OS
        # image on the app's stack, then call get_current_release on the swarm,
        # it should give you a new release with a build linked to the new OS
        # image.
        squad = Squad(name=randchars())
        squad.save()

        release = Release(build=self.build, env_yaml=self.env,
                          config_yaml=self.config, volumes=self.volumes)
        release.save()

        swarm = Swarm(
            app=self.app,
            release=release,
            config_name=randchars(),
            proc_name=randchars(),
            squad=squad,
            size=1,
            config_yaml=self.config,
            env_yaml=self.env,
            volumes=self.volumes
        )
        swarm.save()

        assert swarm.get_current_release(self.version) == release

        # Now save a new OS Image to the stack, and assert that we get a new
        # release.
        new_image = OSImage(name=randchars(), file=randchars(),
                            stack=self.stack, active=True)
        with mock.patch.object(OSImage, '_compute_file_md5',
                               return_value='abcdef1234567890'):
            new_image.save()

        new_release = swarm.get_current_release(self.version)
        assert new_release != release

        assert new_release.build.os_image == new_image
