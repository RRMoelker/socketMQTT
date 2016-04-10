Adapter between one or multipe socket client and a MQTT broker.
It is meant as a proxy for very basic devices that do not have a MQTT client.
Devices such as the Wipy.

Forwards topic messages send over socket connection to MQTT broker.
Currently only forwarding of messages is supported (publishing).

![Socket MQTT proxy demo](https://cloud.githubusercontent.com/assets/205326/14408839/f8c5883c-ff04-11e5-8773-0e1f2611d478.gif)

## Install

Run `pip install -r requirements.txt`. Advanced users don't forget to use a virtualenv.

## Configure

Configure both the socket server and the MQTT broker in the file `config.py`:

```
SOCKET_HOST = '<HOST>'
SOCKET_PORT = <PORT>

MQTT_HOST = "<HOST_NAME>"
MQTT_PORT = <BASIC_PORT>
```

If authentication to the MQTT broker is required add a file `credentials.py` next to the `socketServer.py` with the contents:

```
username="<username>"
password="<password>"
```

## Run

Start the socket to MQTT server with:

```
python socketServer.py
```

## Test

```
telnet localhost 12345
```

Send a message with:

```
someTopic::someMessage
```
