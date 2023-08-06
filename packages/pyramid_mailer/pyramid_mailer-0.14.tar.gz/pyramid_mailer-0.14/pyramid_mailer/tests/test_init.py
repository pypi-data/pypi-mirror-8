import unittest
from pyramid import testing

class TestGetMailer(unittest.TestCase):

    def _get_mailer(self, arg):
        from pyramid_mailer import get_mailer
        return get_mailer(arg)

    def test_arg_is_registry(self):
        mailer = object()
        registry = DummyRegistry(mailer)
        result = self._get_mailer(registry)
        self.assertEqual(result, mailer)

    def test_arg_is_request(self):
        class Dummy(object):
            pass
        mailer = object()
        registry = DummyRegistry(mailer)
        request = Dummy()
        request.registry = registry
        result = self._get_mailer(request)
        self.assertEqual(result, mailer)


class Test_includeme(unittest.TestCase):
    def _do_includeme(self, config):
        from pyramid_mailer import includeme
        includeme(config)

    def test_with_default_prefix(self):
        from pyramid_mailer.interfaces import IMailer
        registry = DummyRegistry()
        settings = {'mail.default_sender': 'sender'}
        config = DummyConfig(registry, settings)
        self._do_includeme(config)
        self.assertEqual(registry.registered[IMailer].default_sender, 'sender')

    def test_with_specified_prefix(self):
        from pyramid_mailer.interfaces import IMailer
        registry = DummyRegistry()
        settings = {'pyramid_mailer.prefix': 'foo.',
                    'foo.default_sender': 'sender'}
        config = DummyConfig(registry, settings)
        self._do_includeme(config)
        self.assertEqual(registry.registered[IMailer].default_sender, 'sender')

class TestFunctional(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_get_mailer_realthing(self):
        from pyramid_mailer import get_mailer
        from pyramid_mailer.mailer import Mailer
        self.config.include('pyramid_mailer')
        request = testing.DummyRequest()
        mailer = get_mailer(request)
        self.assertEqual(mailer.__class__, Mailer)

    def test_get_mailer_dummy(self):
        from pyramid_mailer import get_mailer
        from pyramid_mailer.testing import DummyMailer
        self.config.include('pyramid_mailer.testing')
        request = testing.DummyRequest()
        mailer = get_mailer(request)
        self.assertEqual(mailer.__class__, DummyMailer)


class DummyRegistry(object):
    def __init__(self, result=None):
        self.result = result
        self.registered = {}

    def getUtility(self, iface):
        return self.result

    def registerUtility(self, impl, iface):
        self.registered[iface] = impl


class DummyConfig(object):
    def __init__(self, registry, settings):
        self.registry = registry
        self.registry.settings = settings


