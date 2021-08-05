# detection
Intro to component here


## Configuration parameters
As any other component, *detection* needs a configuration file to start. In
```
etc/config
```
you can find an example of a configuration file. We can find there the following lines:
```
# Endpoints for implements interfaces
DetectionComponent.Endpoints=tcp -p 10010

# This property is used by the clients to connect to IceStorm.
TopicManager.Proxy=IceStorm/TopicManager:default -p 9999


Ice.Warn.Connections=0
Ice.Trace.Network=0
Ice.Trace.Protocol=0
```

## Starting the component
The component can be started easily using the following command:

```
python detectioncomponent.py
```
It will use the default config file of etc/config. If you want to use a different config file, specify it as a parameter of the program like this:
```
python detectioncomponent.py FILENAME_OF_CONFIG_FILE
```
