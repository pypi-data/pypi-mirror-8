FAQ
****

What is this?
-------------
An interface to make calls to the pingme server.  This allows you to send arbitrary notifications to your android phone, provided you have the android application installed.

How does this work?
-------------------

It is just sending post calls to the server with the correct arguments.  If you want to make your own calls to the server you can do so with this structure.
::

    POST
    Header
    Content-Type: application/json
    Body
    {
    "device_id":["device_ids"],
    "message":"message"
    }

An example curl request would look like this ::

    curl -X POST -H "Content-Type: application/json" -d '{"device_id":["PUTIDHERE"],"message":"TEST MESSAGE"}' https://ping.blu3f1re.com/ping/

To get a device id you must download the Android app from the app store.
