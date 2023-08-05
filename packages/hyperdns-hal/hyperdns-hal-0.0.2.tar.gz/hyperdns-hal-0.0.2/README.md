# HAL Navigator and Renderer

This module provides a HAL generation and consumption library similar to dougrain and
rest_navigator, but with the goal of making an object model that can be transparently
used as if one were using the remote object model locally.  This allows the HAL output
from the server to be consumed by any HAL compliant system, such as hyperagent.


The render and navigator components are complimentary and include some
minor, non-intrusive additions to HAL to assist, specifically, in building
transparent client models.

Rendering is pretty simple but not totally functional

Navigation is a thin wrapper around https://github.com/deontologician/rest_navigator

## Rendering

## Navigator & HALRoot

A HALRoot object is the base of an API, but is, itself a Navigator.  A Navigator is a wrapper around deontologician's HALNavigator class, which supports lazy loading and hides the underlying HAL representation.


### Conventions

Properties that start with a leading '_' are considered system control properties.  All other properties
become first level members of the navigator object.

Collection representation.... https://phlyrestfully.readthedocs.org/en/latest/halprimer.html

### Extending Behaviour

The library provides an annotation which will causes methods to be attached to Navigators corresponding
to specific points in the API.  This requires a small extension to HAL, the _class_name pseudo property, which is described below.

The @attach annotation is used like this
```
@hyperdns.hal.navigator.attach('myClass')
def instanceMethod(self):
	pass
```

which will be attached to resources with _class_name='myClass' so that the resulting objects will
have the instanceMethod.

### Breaking RESTfulness

Navigators provide a means of posting and getting relative to a resource, which allow us to accommodate
HTTP services which are not captured by HAL or the REST model - for whatever reason.  Of course, we should
try not to use these, but sometimes this activity is required.

### Lazy Loading

Once the HALRoot is established, resources will be lazy loaded on demand.



# HAL Extensions/MetaData

While every attempt was made to adhere to the HAL specification without modification, two specific components were added.  The HAL produced by the rendering module includes a _class_name attribute on each HAL object, for use by the @attach annotation mentioned above.  This will appear as a regular property for other HAL clients, and represents meta information about the resource being delivered.  The second extension is the inclusion of standard meta information in collections, including pagination data and, most importantly, the name of the property of the embedded resources that is used to index the collection.