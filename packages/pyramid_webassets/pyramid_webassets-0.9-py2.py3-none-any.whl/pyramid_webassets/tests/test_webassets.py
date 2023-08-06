import hashlib
import unittest
import os
import re

from mock import Mock
from pyramid import testing
import pytest
from webassets import __version__ as webassets_version
from webassets.test import TempDirHelper as WebassetsTempDirHelper


def _urls(bundle, env):
    if webassets_version > (0, 9):
        with bundle.bind(env):
            return bundle.urls()
    else:
        return bundle.urls(env=env)


class TempDirHelper(WebassetsTempDirHelper):
    def setup(self):
        super(TempDirHelper, self).setup()
        import sys
        sys.path.append(self.tempdir)

    def teardown(self):
        super(TempDirHelper, self).teardown()

        import sys
        # remove tempdir path elements
        for pth in sys.path:
            if pth.startswith(self.tempdir):
                sys.path.remove(pth)

        sys_modules_items = sys.modules.copy()
        # remove tempdir modules
        for name, module in sys_modules_items.items():
            if module is not None:
                if getattr(module, '__file__', '').startswith(self.tempdir):
                    del sys.modules[name]


class TestWebAssets(unittest.TestCase):
    def test_asset_interface(self):
        from pyramid_webassets import IWebAssetsEnvironment

        def make_env():
            IWebAssetsEnvironment('1')

        self.assertRaises(TypeError, make_env)

    def test_add_web_asset(self):
        from pyramid_webassets import add_webasset

        config = Mock()
        config.registry = Mock()
        queryUtility = Mock()
        env = Mock()
        register = Mock()
        env.register = register
        queryUtility.return_value = env

        config.registry.queryUtility = queryUtility

        add_webasset(config, 'foo', 'bar')
        register.assert_called_with('foo', 'bar')

    def test_add_setting(self):
        from pyramid_webassets import add_setting

        config = Mock()
        config.registry = Mock()
        queryUtility = Mock()
        env = Mock()
        env.config = {}
        register = Mock()
        env.register = register
        queryUtility.return_value = env

        config.registry.queryUtility = queryUtility

        add_setting(config, 'foo', 'bar')
        assert env.config['foo'] == 'bar'

    def test_add_path(self):
        from pyramid_webassets import add_path

        config = Mock()
        config.registry = Mock()
        queryUtility = Mock()
        env = Mock()
        env.config = {}
        register = Mock()
        env.register = register
        queryUtility.return_value = env

        config.registry.queryUtility = queryUtility

        add_path(config, 'foo', '/bar')
        env.append_path.assert_called_with('foo', '/bar')

    def test_get_webassets_env(self):
        from pyramid_webassets import get_webassets_env
        from pyramid_webassets import IWebAssetsEnvironment

        config = Mock()
        config.registry = Mock()
        queryUtility = Mock()

        config.registry.queryUtility = queryUtility

        env = get_webassets_env(config)
        queryUtility.assert_called_with(IWebAssetsEnvironment)

        assert env is not None

    def test_get_webassets_env_from_settings_no_config(self):
        from pyramid_webassets import get_webassets_env_from_settings

        settings = {}

        with self.assertRaises(Exception) as cm:
            get_webassets_env_from_settings(settings)

        assert str(cm.exception) == "You need to provide webassets.base_dir in your configuration"

    def test_get_webassets_env_from_settings_no_base_dir(self):
        from pyramid_webassets import get_webassets_env_from_settings

        settings = {'webassets.base_url': 'static'}

        with self.assertRaises(Exception) as cm:
            get_webassets_env_from_settings(settings)

        assert str(cm.exception) == "You need to provide webassets.base_dir in your configuration"

    def test_get_webassets_env_from_settings_no_base_url(self):
        from pyramid_webassets import get_webassets_env_from_settings

        settings = {'webassets.base_dir': '/home'}

        with self.assertRaises(Exception) as cm:
            get_webassets_env_from_settings(settings)

        assert str(cm.exception) == "You need to provide webassets.base_url in your configuration"

    def test_get_webassets_env_from_settings_minimal(self):
        from pyramid_webassets import get_webassets_env_from_settings

        settings = {
            'webassets.base_url': 'static',
            'webassets.base_dir': os.getcwd(),
        }

        env = get_webassets_env_from_settings(settings)

        assert env.directory == settings['webassets.base_dir']
        assert env.url == '/' + settings['webassets.base_url']
        self.assertEqual(env.url_mapping, {})
        self.assertEqual(env.load_path, [])

    def test_get_webassets_env_from_settings_asset_spec_dir(self):
        import pyramid_webassets
        from pyramid_webassets import get_webassets_env_from_settings

        settings = {
            'webassets.base_url': 'static',
            'webassets.base_dir': 'pyramid_webassets:static',
        }

        env = get_webassets_env_from_settings(settings)
        expected = os.path.join(pyramid_webassets.__path__[0], 'static')

        assert env.directory == expected

    def test_get_webassets_env_from_settings_dir_with_colon(self):
        import pyramid_webassets
        from pyramid_webassets import get_webassets_env_from_settings

        settings = {
            'webassets.base_url': 'static',
            'webassets.base_dir': 'here:static',
        }

        env = get_webassets_env_from_settings(settings)
        expected = os.path.abspath('here:static')

        assert env.directory == expected

    def test_get_webassets_env_from_settings_paths(self):
        from pyramid_webassets import get_webassets_env_from_settings

        settings = {
            'webassets.base_url': 'static',
            'webassets.base_dir': os.getcwd(),
            'webassets.paths': '{"/path/to/scripts": "/js", "/path/to/styles": "/css"}',
        }

        env = get_webassets_env_from_settings(settings)

        assert env.directory == settings['webassets.base_dir']
        assert env.url == '/' + settings['webassets.base_url']
        self.assertEqual(env.url_mapping, {
            '/path/to/scripts': '/js',
            '/path/to/styles':  '/css',
            })
        self.assertEqual(sorted(env.load_path), sorted([
            '/path/to/styles',
            '/path/to/scripts',
            ]))

    def test_get_webassets_env_from_settings_paths_null_url(self):
        from pyramid_webassets import get_webassets_env_from_settings

        settings = {
            'webassets.base_url': 'static',
            'webassets.base_dir': os.getcwd(),
            'webassets.paths': '{"/path/to/scripts": null, "/path/to/styles": "/css"}',
        }

        env = get_webassets_env_from_settings(settings)

        assert env.directory == settings['webassets.base_dir']
        assert env.url == '/' + settings['webassets.base_url']
        self.assertEqual(env.url_mapping, {
            '/path/to/styles':  '/css',
            })
        self.assertEqual(sorted(env.load_path), sorted([
            '/path/to/styles',
            '/path/to/scripts',
            ]))

    def test_get_webassets_env_from_settings_autobuild_disabled(self):
        from pyramid_webassets import get_webassets_env_from_settings

        settings = {
            'webassets.base_url': 'static',
            'webassets.base_dir': os.getcwd(),
            'webassets.auto_build': 'false'
        }

        env = get_webassets_env_from_settings(settings)

        assert env.directory == settings['webassets.base_dir']
        assert env.url == '/' + settings['webassets.base_url']
        assert env.auto_build is False

    def test_get_webassets_env_from_settings_complete(self):
        from pyramid_webassets import get_webassets_env_from_settings
        import webassets

        settings = {
            'webassets.base_url': 'static',
            'webassets.base_dir': os.getcwd(),
            'webassets.debug': 'true',
            'webassets.cache': 'false',
            'webassets.updater': 'always',
            'webassets.jst_compiler': 'Handlebars.compile',
            'webassets.jst_namespace': 'window.Ember.TEMPLATES'
        }

        env = get_webassets_env_from_settings(settings)

        assert env.directory == settings['webassets.base_dir']
        assert env.url == '/' + settings['webassets.base_url']
        assert env.debug is True
        assert isinstance(env.updater, webassets.updater.AlwaysUpdater)
        assert env.config['JST_COMPILER'] == settings['webassets.jst_compiler']
        assert env.config['JST_NAMESPACE'] == settings['webassets.jst_namespace']
        assert env.cache is None
        assert env.auto_build is True

    def test_get_webassets_env_from_settings_with_cache(self):
        from pyramid_webassets import get_webassets_env_from_settings

        settings = {
            'webassets.base_url': 'static',
            'webassets.base_dir': os.getcwd(),
            'webassets.cache': 'true',
        }

        env = get_webassets_env_from_settings(settings)

        assert env.cache is not None

    def test_get_webassets_env_from_settings_with_cache_directory(self):
        from pyramid_webassets import get_webassets_env_from_settings
        from uuid import uuid4
        import shutil

        tmpdir = os.path.join(os.getcwd(), 'test-cache-dir-' + str(uuid4()))

        settings = {
            'webassets.base_url': 'static',
            'webassets.base_dir': os.getcwd(),
            'webassets.cache': tmpdir,
        }

        assert not os.path.isdir(tmpdir)

        env = get_webassets_env_from_settings(settings)

        assert env.cache is not None
        assert env.cache == tmpdir
        assert os.path.isdir(tmpdir)

        shutil.rmtree(tmpdir)

    def test_get_webassets_env_from_settings_prefix_change(self):
        from pyramid_webassets import get_webassets_env_from_settings

        settings = {
            'foo.base_url': 'static',
            'foo.base_dir': os.getcwd(),
        }

        env = get_webassets_env_from_settings(settings, prefix='foo')

        assert env is not None
        assert env.directory == settings['foo.base_dir']
        assert env.url == '/' + settings['foo.base_url']

    def test_get_webassets_env_from_settings_prefix_bad_change(self):
        from pyramid_webassets import get_webassets_env_from_settings

        settings = {
            'foo.base_url': 'static',
            'foo.base_dir': os.getcwd(),
        }

        with self.assertRaises(Exception) as cm:
            get_webassets_env_from_settings(settings, prefix='webassets')

        assert str(cm.exception) == "You need to provide webassets.base_dir in your configuration"

    def test_includeme(self):
        from pyramid_webassets import includeme
        from pyramid_webassets import add_webasset
        from pyramid_webassets import get_webassets_env
        from pyramid_webassets import add_setting
        from pyramid_webassets import get_webassets_env_from_request

        config = Mock()
        add_directive = Mock()
        registerUtility = Mock()
        set_request_property = Mock()

        config.registry = Mock()
        config.registry.registerUtility = registerUtility
        config.add_directive = add_directive
        config.set_request_property = set_request_property

        settings = {
            'webassets.base_url': 'static',
            'webassets.base_dir': os.getcwd(),
        }

        config.registry.settings = settings

        includeme(config)

        expected1 = ('add_webasset', add_webasset)
        expected2 = ('get_webassets_env', get_webassets_env)
        expected3 = ('add_webassets_setting', add_setting)

        assert add_directive.call_args_list[0][0] == expected1
        assert add_directive.call_args_list[1][0] == expected2
        assert add_directive.call_args_list[2][0] == expected3

        assert set_request_property.call_args_list[0][0] == \
            (get_webassets_env_from_request, 'webassets_env')

    def test_get_webassets_env_from_request(self):
        from pyramid_webassets import get_webassets_env_from_request
        from pyramid_webassets import IWebAssetsEnvironment

        request = Mock()
        request.registry = Mock()
        queryUtility = Mock()
        request.registry.queryUtility = queryUtility

        env = get_webassets_env_from_request(request)
        queryUtility.assert_called_with(IWebAssetsEnvironment)

        assert env is not None

    def test_webassets_static_view_setting(self):
        from pyramid_webassets import get_webassets_env_from_settings

        settings = {
            'webassets.base_url': 'static',
            'webassets.base_dir': os.getcwd(),
            'webassets.static_view': True,
        }

        env = get_webassets_env_from_settings(settings)

        assert env is not None
        assert env.config['static_view'] == settings['webassets.static_view']

    def test_webassets_static_view_cache_control_setting(self):
        from pyramid_webassets import get_webassets_env_from_settings

        settings = {
            'webassets.base_url': 'static',
            'webassets.base_dir': os.getcwd(),
            'webassets.static_view': True,
            'webassets.cache_max_age': 3600,
        }

        env = get_webassets_env_from_settings(settings)

        assert env is not None
        assert env.config['static_view'] == settings['webassets.static_view']
        assert env.config['cache_max_age'] == settings['webassets.cache_max_age']

    def test_get_webassets_env_from_settings_load_path(self):
        from pyramid_webassets import get_webassets_env_from_settings

        settings = {
            'webassets.base_url': 'static',
            'webassets.base_dir': os.getcwd(),
            'webassets.load_path': '/foo bar/\nbaz'
        }

        env = get_webassets_env_from_settings(settings)

        assert env.load_path == ['/foo', 'bar/', 'baz']

    def test_auto_bool(self):
        from pyramid_webassets import get_webassets_env_from_settings
        settings = {
            'webassets.base_url': 'static',
            'webassets.base_dir': os.getcwd(),
            'webassets.less_run_in_debug': 'true',
        }
        env = get_webassets_env_from_settings(settings)
        assert env.config['less_run_in_debug'] is True

    def test_auto_json(self):
        from pyramid_webassets import get_webassets_env_from_settings
        settings = {
            'webassets.base_url': 'static',
            'webassets.base_dir': os.getcwd(),
            'webassets.less_extra_args': 'json:["--foo", "--bar"]',
        }
        env = get_webassets_env_from_settings(settings)
        assert env.config['less_extra_args'] == ['--foo', '--bar']


class TestAssetSpecs(TempDirHelper, unittest.TestCase):
    # Mask the methods from TempDirHelper, pytest will try to call them without
    # instantiating the class...
    setup = None
    teardown = None

    def setUp(self):
        from pyramid_webassets import get_webassets_env

        TempDirHelper.setup(self)

        self.create_files({
            'static/__init__.py': '',
            'static/assets/zing.css': '* { text-decoration: underline }'})

        self.request = testing.DummyRequest()
        self.config = testing.setUp(request=self.request, settings={
            'webassets.base_url': 'static',
            'webassets.base_dir': 'static:assets',
            'webassets.static_view': True,
        })
        self.config.include('pyramid_webassets')

        self.env = get_webassets_env(self.config)
        # Disable cache busting
        self.env.url_expire = False

        import sys
        sys.path.append(self.tempdir)

    def tearDown(self):
        TempDirHelper.teardown(self)
        testing.tearDown()

    def test_asset_spec_passthru_uses_static_url(self):
        from webassets import Bundle
        from pyramid.path import AssetResolver

        asset_spec = 'static:assets/zing.css'
        bundle = Bundle(asset_spec)
        self.request.static_url = Mock(return_value='http://example.com/foo/')

        urls = _urls(bundle, self.env)
        path = AssetResolver(None).resolve(asset_spec).abspath()
        self.request.static_url.assert_called_with(path)
        assert urls == ['http://example.com/foo/']

    def test_asset_spec_source_is_resolved(self):
        from webassets import Bundle

        asset_spec = 'static:assets/zing.css'
        bundle = Bundle(asset_spec, output='zung.css')

        urls = _urls(bundle, self.env)
        assert urls == ['http://example.com/static/zung.css']

        fname = os.path.join(self.tempdir, 'static', 'assets', 'zung.css')
        with open(fname) as f:
            assert f.read() == '* { text-decoration: underline }'

    def test_asset_spec_output_is_resolved(self):
        from webassets import Bundle

        asset_spec = 'static:assets/zing.css'
        bundle = Bundle(asset_spec, output='static:assets/zung.css')

        urls = _urls(bundle, self.env)
        assert urls == ['http://example.com/static/zung.css']

        fname = os.path.join(self.tempdir, 'static', 'assets', 'zung.css')
        with open(fname) as f:
            assert f.read() == '* { text-decoration: underline }'

    def test_asset_spec_missing_file(self):
        from webassets import Bundle
        from webassets.exceptions import BundleError

        asset_spec = 'static:assets/bogus.css'
        bundle = Bundle(asset_spec)

        with self.assertRaises(BundleError) as cm:
            _urls(bundle, self.env)

        fname = self.tempdir+'/static/assets/bogus.css'
        assert str(cm.exception) == ("'%s' does not exist" % (fname,))

    def test_asset_spec_missing_package(self):
        from webassets import Bundle
        from webassets.exceptions import BundleError

        asset_spec = 'rabbits:static/zing.css'
        bundle = Bundle(asset_spec)

        with self.assertRaises(BundleError) as cm:
            _urls(bundle, self.env)

        assert re.search('rabbits', str(cm.exception)) is not None

    def test_asset_spec_static_view(self):
        from webassets import Bundle

        asset_spec = 'static:assets/zing.css'
        bundle = Bundle(asset_spec)

        # webassets will copy the file into a place that it can generate
        # a url for
        urls = _urls(bundle, self.env)
        assert self.request.static_url(asset_spec) in urls

    def test_asset_spec_no_static_view(self):
        from webassets import Bundle

        self.create_files({
            'dotted/__init__.py': '',
            'dotted/package/__init__.py': '',
            'dotted/package/name/__init__.py': '',
            'dotted/package/name/static/zing.css':
            '* { text-decoration: underline }'})

        asset_spec = 'dotted.package.name:static/zing.css'
        bundle = Bundle(asset_spec)

        # webassets will copy the file into a place that it can generate
        # a url for
        urls = _urls(bundle, self.env)
        domain = 'http://example.com/static/webassets-external/'

        assert domain in urls[0]
        assert len(urls) == 1

    def test_asset_spec_globbing(self):
        from webassets import Bundle

        self.create_files({
            'static/assets/zang.css':
            '* { text-decoration: underline }'})
        asset_spec = 'static:assets/z*ng.css'
        bundle = Bundle(asset_spec)

        urls = _urls(bundle, self.env)
        assert len(urls) == 2
        assert 'http://example.com/static/zing.css' in urls
        assert 'http://example.com/static/zang.css' in urls

    def test_asset_spec_load_path_and_mapping(self):
        from webassets import Bundle

        asset_path = self.tempdir + '/dotted/package/name/static/'
        self.env.append_path(asset_path, 'http://static.example.com')

        self.create_files({
            'dotted/__init__.py': '',
            'dotted/package/__init__.py': '',
            'dotted/package/name/__init__.py': '',
            'dotted/package/name/static/zing.css':
            '* { text-decoration: underline }'})
        asset_spec = 'dotted.package.name:static/zing.css'
        bundle = Bundle(asset_spec, output=asset_spec.replace('zing', 'zung'))

        urls = _urls(bundle, self.env)
        assert urls == ['http://static.example.com/zung.css']

    def test_bundles_yamlloader_file(self):
        try:
            import yaml
        except ImportError:
            raise unittest.SkipTest('PyYAML not installed')
        from pyramid_webassets import get_webassets_env_from_settings
        settings = {
            'webassets.base_url': 'static',
            'webassets.base_dir': os.getcwd(),
            'webassets.bundles': self.tempdir + '/foo/bar.yaml',
        }
        self.create_files({'foo/bar.yaml': 'mycss: {contents: style/mycss.css}'})
        env = get_webassets_env_from_settings(settings)
        self.assertEqual(env.config.get('bundles'), None)
        self.assertIsNotNone(env['mycss'])
        self.assertEqual(list(env._named_bundles.keys()), ['mycss'])

    def test_bundles_yamlloader_list(self):
        try:
            import yaml
        except ImportError:
            raise unittest.SkipTest('PyYAML not installed')
        from pyramid_webassets import get_webassets_env_from_settings
        settings = {
            'webassets.base_url': 'static',
            'webassets.base_dir': os.getcwd(),
            'webassets.bundles': 'dotted.package.name:foo/bar.yaml '
                                 'dotted.package.name:foo/baz.yaml',
        }
        self.create_files({
            'dotted/__init__.py': '',
            'dotted/package/__init__.py': '',
            'dotted/package/name/__init__.py': '',
            'dotted/package/name/foo/bar.yaml': 'mycss: {contents: style/mycss.css}',
            'dotted/package/name/foo/baz.yaml': 'myjs: {contents js/myjs.js}',
        })
        env = get_webassets_env_from_settings(settings)
        self.assertEqual(env.config.get('bundles'), None)
        self.assertIsNotNone(env['mycss'])
        self.assertEqual(sorted(env._named_bundles.keys()), ['mycss', 'myjs'])

    def test_bundles_yamlloader_asset(self):
        try:
            import yaml
        except ImportError:
            raise unittest.SkipTest('PyYAML not installed')
        from pyramid_webassets import get_webassets_env_from_settings
        settings = {
            'webassets.base_url': 'static',
            'webassets.base_dir': os.getcwd(),
            'webassets.bundles': (
                'dotted.package.name:foo/bar.yaml\n'
                'dotted.package.name:foo/baz.yaml'
            ),
        }
        self.create_files({
            'dotted/__init__.py': '',
            'dotted/package/__init__.py': '',
            'dotted/package/name/__init__.py': '',
            'dotted/package/name/foo/bar.yaml': (
                'mycss: {contents: style/mycssoverride.css}'
            ),
            'dotted/package/name/foo/baz.yaml': (
                'mycss: {contents: style/mycss.css}\n'
                'myjs: {contents: js/myjs.js}'
            ),
        })
        env = get_webassets_env_from_settings(settings)
        self.assertEqual(env.config.get('bundles'), None)
        self.assertIsNotNone(env['mycss'])
        self.assertEqual(sorted(env._named_bundles.keys()), ['mycss', 'myjs'])
        self.assertIn('style/mycssoverride.css', env['mycss'].contents)


class TestBaseUrlBehavior(object):
    """
    Tests related to the base_url with asset specs and static_view
    """
    view_actions = {
        None: (False, False),
        'automatic': (True, False),
        'manual': (False, True)}

    def setup_method(self, method):
        self.temp = TempDirHelper()
        self.temp.setup()
        empty_css = '* {color:black}'
        self.temp.create_files({
            'static/__init__.py': '',
            'static/t.css': empty_css,
            'static/some/__init__.py': '',
            'static/some/t.css': empty_css,
            'mypkg/__init__.py': '',
            'mypkg/static/t.css': empty_css})

    def teardown_method(self, method):
        testing.tearDown()
        self.temp.teardown()

    def build_env(self, base_dir, static_view):
        from pyramid_webassets import get_webassets_env

        automatic_view, manual_view = self.view_actions[static_view]

        if not ':' in base_dir:
            base_dir = os.path.join(self.temp.tempdir, base_dir)

        self.request = testing.DummyRequest()
        self.config = testing.setUp(request=self.request, settings={
            'webassets.base_url': 'static',
            'webassets.base_dir': base_dir,
            'webassets.static_view': automatic_view,
            'webassets.url_expire': False,
        })
        self.config.include('pyramid_webassets')

        if manual_view:
            self.config.add_static_view('static', 'mypkg:static')

        return get_webassets_env(self.config)

    def format_expected(self, expected, webasset):
        """
        Formats the expected url when the webasset is external
        """
        from pyramid.path import AssetResolver

        if '%' not in expected:
            return expected

        if ':' in webasset:
            name = AssetResolver(None).resolve(webasset).abspath()
        else:
            name = self.temp.tempdir + '/static/' + webasset

        if webassets_version > (0, 9):
            hashed_filename = hashlib.md5(name.encode("utf-8")).hexdigest()
        else:
            hashed_filename = hash(name) & ((1 << 64) - 1)
        external = 'webassets-external/%s_' % hashed_filename
        return expected % {'external': external}

    @pytest.mark.parametrize(
        ('base_dir', 'static_view', 'webasset', 'expected'),
        [('static', None, 't.css', '/static/t.css'),
         ('static', 'automatic', 't.css', 'http://example.com/static/t.css'),
         ('static', None, 'mypkg:static/t.css', '/static/%(external)st.css'),
         ('static', None, 'static:t.css', '/static/t.css'),

         # If base_dir is an asset spec, but webassets are files
         ('static:some', 'manual', 't.css', '/static/t.css'),
         ('static:some', None, 't.css', '/static/t.css'),

         # base_dir as asset spec, but webasset is asset spec with route
         ('mypkg:some', 'manual', 'mypkg:static/t.css',
          'http://example.com/static/t.css'),

         # base_dir as asset spec, but webasset is asset spec without route
         ('static:some', None, 'static:some/t.css', '/static/t.css'),
         # base_dir as asset spec, but webasset is asset spec automatic route
         ('static:some', 'automatic', 'static:some/t.css',
          'http://example.com/static/t.css'),

         # Work a bit the resolve output (o.css will activate the output=o.css)
         ('mypkg:static', 'manual', 'mypkg:static/t.css',
          'http://example.com/static/o.css'),

         # Test the string joins when using a package root as the asset spec
         # The expected output is relative until/unless Pyramid merges
         # https://github.com/Pylons/pyramid/pull/1377
         # As such, this is not really a recommended setup.
         ('mypkg:', 'automatic', 'mypkg:static/t.css', '/static/o.css')],
    )
    def test_url(self, base_dir, static_view, webasset, expected):
        """
        Test final urls.

        If the expected output ends in o.css, it setups output in the bundle.
        """
        from webassets import Bundle

        expected = self.format_expected(expected, webasset)
        params = {} if not 'o.css' in expected else {'output': 'o.css'}
        bundle = Bundle(webasset, **params)
        res = _urls(bundle, self.build_env(base_dir, static_view))
        assert [expected] == res
