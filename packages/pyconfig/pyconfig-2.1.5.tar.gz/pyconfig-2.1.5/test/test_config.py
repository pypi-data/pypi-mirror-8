"""
Tests for pyconfig
"""
from __future__ import print_function, unicode_literals

import mock

import pyconfig
from nose.tools import eq_


def test_namespace_attr():
    ns = pyconfig.Namespace()
    ns.test = True
    eq_(ns.test, True)


def test_namespace_get_config():
    ns = pyconfig.Namespace()
    ns.test = True
    eq_(dict(ns._get_config('ns')), {'ns.test': True})


def test_namespace_nested_attr():
    ns = pyconfig.Namespace()
    ns.nest = pyconfig.Namespace()
    ns.nest.test = True
    eq_(ns.nest.test, True)


def test_namespace_nested_get_config():
    ns = pyconfig.Namespace()
    ns.nest = pyconfig.Namespace()
    ns.nest.test = True
    eq_(dict(ns._get_config('ns')), {'ns.nest.test': True})


def test_namespace_deep_nested():
    ns = pyconfig.Namespace()
    ns.test = True
    ns.nest = pyconfig.Namespace()
    ns.nest.test = True
    ns.nest.deep = pyconfig.Namespace()
    ns.nest.deep.test = True
    eq_(dict(ns._get_config('ns')), {'ns.nest.test': True, 'ns.test': True,
        'ns.nest.deep.test': True})


def test_namespace_implicit_nesting():
    ns = pyconfig.Namespace()
    ns.test = True
    ns.nest.test = True
    ns.nest.deep.test = True
    eq_(dict(ns._get_config('ns')), {'ns.nest.test': True, 'ns.test': True,
        'ns.nest.deep.test': True})


def test_set_and_get():
    pyconfig.set('set_and_get', 'tested')
    eq_(pyconfig.get('set_and_get'), 'tested')


def test_set_get_change():
    pyconfig.set('set_get_change', 'testing')
    eq_(pyconfig.get('set_get_change'), 'testing')
    pyconfig.set('set_get_change', 'tested')
    eq_(pyconfig.get('set_get_change'), 'tested')


def test_setting():
    class Test(object):
        setting = pyconfig.Setting('test', 'value')
    eq_(Test.setting, 'value')
    eq_(Test().setting, 'value')


def test_setting_change():
    class Test(object):
        setting = pyconfig.Setting('test_setting_change', 'value')
    eq_(Test.setting, 'value')
    eq_(Test().setting, 'value')
    pyconfig.set('test_setting_change', 'value2')
    eq_(Test.setting, 'value2')
    eq_(Test().setting, 'value2')


def test_config_update():
    conf = pyconfig.Config()
    conf.settings = {}
    conf._update({'test_config_update': 'test_value'}, 'ns')
    eq_(conf.settings, {'ns.test_config_update': 'test_value'})
    eq_(conf.get('ns.test_config_update', None), 'test_value')


def test_config_update_sans_private():
    conf = pyconfig.Config()
    conf.settings = {}
    conf._update({'_test_private': 'private', 'other': 'nonprivate'}, 'ns')
    eq_(conf.settings, {'ns.other': 'nonprivate'})
    eq_(conf.get('ns.other', None), 'nonprivate')
    eq_(conf.get('ns._test_private', None), None)


def test_config_update_skip_namespace_class():
    conf = pyconfig.Config()
    conf.settings = {}
    conf._update({'Namespace': pyconfig.Namespace})
    eq_(conf.settings, {})


def test_config_update_nested_namespace():
    conf = pyconfig.Config()
    conf.settings = {}
    ns = pyconfig.Namespace()
    ns.value = 'value'
    conf._update({'test': ns}, 'ns')
    eq_(conf.get('ns.test.value', None), 'value')


def test_config_update_callable():
    conf = pyconfig.Config()
    conf.settings = {}
    call = lambda: 'value'
    conf._update({'test_callable': call}, 'ns')
    eq_(conf.get('ns.test_callable', None), 'value')


def test_reload_hook():
    hook = mock.MagicMock()
    pyconfig.reload_hook(hook)
    pyconfig.reload()
    hook.assert_called_with()


def test_setting_shortcut():
    class Test(object):
        setting = pyconfig.setting('test_setting_shortcut', 'tested')
    eq_(Test.setting, 'tested')
    eq_(Test().setting, 'tested')


def test_get_default_with_various_values():
    eq_(pyconfig.get('default_num', 1), 1)
    eq_(pyconfig.get('default_num', 1.0), 1.0)
    eq_(pyconfig.get('default_none', None), None)
    eq_(pyconfig.get('default_true', True), True)
    eq_(pyconfig.get('default_false', False), False)
    eq_(pyconfig.get('default_unicode', 'Test'), 'Test')
    eq_(pyconfig.get('default_expr', 60*24), 60*24)
    eq_(pyconfig.get('ns.test_namespace', 'pyconfig'), 'pyconfig')


def test_localconfig_py_actually_works():
    eq_(pyconfig.get('conf.local', False), True)

