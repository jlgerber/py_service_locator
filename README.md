# ServiceLocator
This is a service locator implementation, inspired by the need for an alternative IoC pattern to simple dependency injection via class __init__s. Using the service locator is a two step affair:

1. Import the service proxy into each module that requires a service, and look up said service using `get_service` or `get_service_proxy`.
2. Configure the service locator and register service implmentations with it.

## Configuration

The service locator has a couple of options, depending upon your use case. The simpest way of using the service locator has you register dependency classes or instances name via `service_locator.register`, and then look them up with corresponding calls to `service_locator.get_service_proxy`.

### Example 1
The simple path. Here we have the main.py

#### example1/__main__.py
```python
# in main
import service_locator
from example1.myservice import Service1
from example1.myservice import Service1

from consumer import Consumer
from consumer2 import Consumer2

service_locator.register("service1", Service1)
service_locator.register("service2", Service2)

def main():
    c1 = Consumer1("stuff")
    c2 = Consumer2("some other thing")
    c1.things()
    c2.foobar()
if __name__ == "__main__":
    main()
```

### example1/consumer.py
```python
# in consumer.py
from service_locator import get_service_proxy

class Consumer(object):
    service1 = get_service_proxy('service1', __name__ + ".Consumer")()

    def __init__(self, stuff):
        self.stuff = stuff

    def things(self):
        return self.service1.something_interesting(self.stuff)
```

### example1/consumer2.py
```python
# in consumer.py
from service_locator import gt_service_proxy

class Consumer2(object):
    service2 = get_service_proxy('service1', __name__ + ".Consumer2")()

    def __init__(self, otherthing)
        self.otherthing  = otherthing

    def foobar(self):
        self.service2.barfoo(self.otherthing)
...
```

