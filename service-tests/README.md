# Testing code in zato services

So you should see a `example-service.py` file here with three service classes.

- MyServiceUsingOutgoingSoapConnection
- MyServiceUsingOutgoingHTTPConnection
- MyServiceUsingInvoke

These simple services do a very basic call to an external api as well as a local service. But how do we test them?

### Preperation
First things first, you need an environment to work on and install some requirements
```
mkvirtualenv zato
pip install -r requirements.pip
```
The requirements file is just _some_ libraries that zato uses and that you will need in your tests.

### What are we trying to achieve

Its very hard to test code for zato services because we need to remember the following.

- Services you write are used in zato itself
- Testing code here will not ensure that it works in zato. This is because cannot replicate the flow zato uses to test code.

With that in mind, we need to remember the following with all our testing

1. We are testing code. Not funcionality, that comes later.
2. Since we are NOT working inside zato for this, we need to replicate zato IO on services. Meaning we are testing assuming we are in a zato environment and testing code based on events. We'll get into this in a sec.

So lets look at the service imports. (this is all in `example-service.py`)
```
try:
    from zato.server.service import Service
except ImportError:
    # Override for unit tests
    from mock import Mock
    class Service:
        ...
```
The try catch block is what sets us free from being constrained to having to be in a zato environment to run tests. Basically we cannot import `zato.server.service` so we throw it in a `try` `catch`. This is where the magic happens.

We can use the `mock.py` library here! I specifically like the mock library because my goal is to test code under different circumstances, not functionality, that comes later.

Using mock and understanding the flow of zato and services, you can easily test code. Let me show you.

Lets take the `MyServiceUsingInvoke` service. The handle of this service is super simple, we are calling a service using `self.invoke` and then we are setting it as the `response.payload`.

Lets use this scenario, what will the code do if we had an error was raised on the section `json.loads(self.invoke('get-date-time'))`.

To test this we use mock. 

```
def test_error_on_invoke(self):
    service = MyServiceUsingInvoke()
    service.invoke.side_effect = Exception("This is a forced error")
    service.handle()
    self.assert_equal(service.response.payload, None)
```
Now this test would break because we are not catching any errors in the service. However the fact is that we have a code test to check for things like this for us. You can also test values that are inputed and values output in these unit tests. You want to test as much as possible. More tests = less bugs reported.

I've added some things in the `tests.py` file that may help you with your tests. I have also added some sample services that are in the `example_services.py` file which may be similar to services you write.
