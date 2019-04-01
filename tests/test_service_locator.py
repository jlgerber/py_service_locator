import unittest
from .context import service_locator

class UseSuperclassCM(object):
    """
    contect manager to ensure that the key_is_superclass is turned on and off during the
    execution
    """
    def __init__(self):
        self.is_super = service_locator.key_is_superclass

    def __enter__(self):
        service_locator.key_is_superclass()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        service_locator.key_is_superclass(self.is_super)


class TestServiceLocator(unittest.TestCase):

    def test_can_store_instance(self):
        class Foo(object):
            def test(self):
                return "success"

        service_locator.register("foo", Foo())
        foo = service_locator.get_service("foo")
        expect = "success"
        self.assertEquals(expect, foo.test())

    def test_can_store_class(self):
        class Foo(object):
            def test(self):
                return "success"

        service_locator.register("foo", Foo)
        foo = service_locator.get_service("foo")
        expect = "success"
        self.assertEquals(expect, foo().test())

    def test_enforces_instance_when_configured(self):
        class BaseFoo(object):
            def test(self):
                raise NotImplementedError()

        class Foo(BaseFoo):
            def test(self):
                return "success"

        with UseSuperclassCM() as sclass:
            #service_locator.key_is_superclass()
            service_locator.register(BaseFoo, Foo())
            foo = service_locator.get_service(BaseFoo)
            expect = "success"
            self.assertEquals(expect, foo.test())

    def test_raises_exception_when_key_is_not_instance_when_configured(self):
        class BaseFoo(object):
            def test(self):
                raise NotImplementedError()

        class Foo(BaseFoo):
            def test(self):
                return "success"
        #service_locator.key_is_superclass()
        with UseSuperclassCM() as sclass:
            with self.assertRaises(Exception) as context:
                service_locator.register("BaseFoo", Foo())
            self.assertTrue( context.exception is not None)

    def test_enforces_subclass_when_configured(self):
        class BaseFoo(object):
            def test(self):
                raise NotImplementedError()

        class Foo(BaseFoo):
            def test(self):
                return "success"

        with UseSuperclassCM() as sclass:
            service_locator.register(BaseFoo, Foo)
            foo = service_locator.get_service(BaseFoo)
            expect = "success"
            self.assertEquals(expect, foo().test())

    def test_raises_exception_when_key_is_not_superclass_when_configured(self):
        class BaseFoo(object):
            def test(self):
                raise NotImplementedError()

        class Foo(BaseFoo):
            def test(self):
                return "success"

        with UseSuperclassCM() as sclass:
            with self.assertRaises(Exception) as context:
                service_locator.register("BaseFoo", Foo)
            self.assertTrue( context.exception is not None)
