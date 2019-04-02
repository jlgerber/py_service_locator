# ServiceLocator
This is a service locator implementation, inspired by the need for an alternative IoC pattern to simple dependency injection via class __init__s. Using the service locator is a two step affair:

1. Import the service proxy into each module that requires a service, and look up said service using `get_service` or `get_service_proxy`.
2. Configure the service locator and register service implmentations with it.

## Simple Useage

The service locator has a couple of options, depending upon our use case. The simpest way of using the service locator has us register dependency classes or instances  via `service_locator.register` in our executable, and look them up with corresponding calls to `service_locator.get_service` in our modules.

By default, `service_locator.register` takes a key, which can be any hashable object, and a service, which may be any python class or instance. The `service_locator.get_service_proxy` call takes a key, which should correspond with a registered key, and returns a ServiceProxy wrapping the registered class or instance. This is a simple workflow, but has a couple of drawbacks.

First, there is no way of establishing a contract between the service consumer and service provider. How do the producer and consumer express requirements for what is being produced / consumed?

Second, there is no way to guarantee that the producer has registered sufficient services to cover all of the registered requests. Failures in this regard will manifest at runtime.

So how do we fix this?

Here are some guidelines.

## Prefered Usage

First, we need to establish a *contract* between the consumer and the producer of each service. We do this by implementing base classes for our services, and using the base classes as keys when We register with `service_provider.register`, and when we look up via `get_service_proxy`.

Second, we have to instruct the service_proxy to require that each registered class is a subclass of the key, which should be one of those base classes from above. We do this by feeding a configuration dictionary to `service_locator.configure`, specifying `key_is_superclass` as True. This will cause `service_locator.register` to raise an exception should we fail to register a subclass of the key's class.

Third, we have to restrict usage of `get_service_proxy` to module constants and class variables. This will allow the system to validate the registration immediately subsquent to it, but before the runtime is in full swing allowing us to fail early and consistently.

Fourth, after registering all our services, validate that no ServiceProxy requests have been neglected by running `service_locator.unbound_services()`. This call returns a list of any unregistered service dependencies.
