import json
from channels import Channel, Group
from channels.auth import channel_session_user_from_http, channel_session_user

from .settings import MSG_TYPE_LEAVE, MSG_TYPE_ENTER, NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS
from .models import Room
from .utils import get_room_or_error, catch_client_error
from .exceptions import ClientError
from django.conf import settings
from event.utils import active_questions_json



@channel_session_user_from_http
def ws_connect(message):
    # print(message.user.is_authenticated)
    message.reply_channel.send({'accept': True})
    message.channel_session['rooms'] = []


@channel_session_user
def ws_receive(message):
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel("chat.receive").send(payload)


@channel_session_user
def ws_disconnect(message):
    for room_id in message.channel_session.get("rooms", set()):
        try:
            room = Room.objects.get(title=room_id)
            room.websocket_group.discard(message.reply_channel)
        except Room.DoesNotExist:
            pass


# @channel_session_user
@catch_client_error
@channel_session_user
def chat_join(message):
    room = get_room_or_error(message["room"], message.user)

    if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        room.send_message(None, message.user, MSG_TYPE_ENTER)

    room.websocket_group.add(message.reply_channel)
    message.channel_session['rooms'] = list(
        set(message.channel_session['rooms']).union([room.title]))
    message.reply_channel.send({
        "text": json.dumps({
            "join": str(room.title),
            "title": room.title,
        }),
    })

    room.send_message(active_questions_json(room.title), message.user, 0)



@channel_session_user
@catch_client_error
def chat_leave(message):
    room = get_room_or_error(message["room"], message.user)

    if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        room.send_message(None, message.user, MSG_TYPE_LEAVE)

    room.websocket_group.discard(message.reply_channel)
    message.channel_session['rooms'] = list(
        set(message.channel_session['rooms']).difference([room.title]))
    message.reply_channel.send({
        "text": json.dumps({
            "leave": str(room.title),
        }),
    })


@catch_client_error
@channel_session_user
def chat_send(message):
    print(message.user)
    room = get_room_or_error(message["room"], message.user)
    room.send_message(message["message"], message.user)
