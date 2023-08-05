# hipchat_notif

hipchat_notif is [HipChat](https://www.hipchat.com) client library for sending notification using API v1.


## Python version

3.4

## Dependencies

- requests

## Sample Code

```python
from hipchat_notif import *

TOKEN = "AUTH_TOKEN" # Get token from https://hipchat.com/admin/api
ROOM_ID = 10000
NOTIFICATION_NAME = "NOTIFICATOR" 

# Create a new instance.

notif =  HipchatNotificator(TOKEN)
notif.notification_name = NOTIFICATION_NAME
notif.room = ROOM_ID

# Send Alert notification 
notif.alert("Alert")

# Send Ok message
notif.ok("Not Alert")

# Send message
notif.message("Message")

# Send Notification
notif.notif("Notification")
```

### Correspondence table

Method |  Notify | Color
:----: |  :----: | :----:
alert() |  True | red
ok() |  False | green
message() |  False | yellow
notif() | True | gray