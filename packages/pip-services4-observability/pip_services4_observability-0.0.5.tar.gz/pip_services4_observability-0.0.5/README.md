# <img src="https://uploads-ssl.webflow.com/5ea5d3315186cf5ec60c3ee4/5edf1c94ce4c859f2b188094_logo.svg" alt="Pip.Services Logo" width="200"> <br/> Observability Components for Python

This module is a part of the [Pip.Services](http://pipservices.org) polyglot microservices toolkit.

The Observability module contains observability component definitions that can be used to build applications and services.

The module contains the following packages:
- **Count** - performance counters
- **Log** - basic logging components that provide console and composite logging, as well as an interface for developing custom loggers
- **Trace** - tracing components

<a name="links"></a> Quick links:

* [Logging](https://www.pipservices.org/recipies/logging)
* [API Reference](https://pip-services3-python.github.io/pip-services4-observability-python/index.html)
* [Change Log](CHANGELOG.md)
* [Get Help](https://www.pipservices.org/community/help)
* [Contribute](https://www.pipservices.org/community/contribute)

## Use

Install the Python package as
```bash
pip install pip_services4_observability
```

Example how to use Logging and Performance counters.
Here we are going to use CompositeLogger and CompositeCounters components.
They will pass through calls to loggers and counters that are set in references.

```python
class MyComponent(IConfigurable, IReferenceable):
    __logger = CompositeLogger()
    __counters = CompositeCounters()

    def configure(self, config):
        self.__logger.configure(config)

    def set_references(self, references):
        self.__logger.set_references(references)
        self.__counters.set_references(references)

    def my_method(self, context, param1):
        try:
            self.__logger.trace(context, "Executed method mycomponent.mymethod")
            self.__counters.increment("mycomponent.mymethod.exec_count", 1)
            timing = self.__counters.begin_timing("mycomponent.mymethod.exec_time")
            # ...
            timing.end_timing()
        except Exception as ex:
            self.__logger.error(context, ex, "Failed to execute mycomponent.mymethod")
            self.__counters.increment("mycomponent.mymethod.error_count", 1)
```

## Develop

For development you shall install the following prerequisites:
* Python 3.7+
* Visual Studio Code or another IDE of your choice
* Docker

Install dependencies:
```bash
pip install -r requirements.txt
```

Run automated tests:
```bash
python test.py
```

Generate API documentation:
```bash
./docgen.ps1
```

Before committing changes run dockerized build and test as:
```bash
./build.ps1
./test.ps1
./clear.ps1
```

## Contacts

The initial implementation is done by **Sergey Seroukhov**. Pip.Services team is looking for volunteers to 
take ownership over Python implementation in the project.
