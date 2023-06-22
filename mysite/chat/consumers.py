import json
import base64
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import User, Thread, ChatMessage, Channel, ChannelMessage
from django.core.files.base import ContentFile
from multidict import MultiDict


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        # print('connected', event)
        session = self.scope["session"]
        user_id = session.get('user_id')
        workspace_id = session.get('workspaceID')
        chat_room = f'user_chatroom_{workspace_id}'
        self.chat_room = chat_room

        # Join room group
        await self.channel_layer.group_add(self.chat_room, self.channel_name)

        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        # print('Recieve', event)
        recieved_data = json.loads(event['text'])
        message = recieved_data.get('message')
        sent_by_id = recieved_data.get('sent_by')
        thread_id = recieved_data.get('thread_id')
        is_channel = recieved_data.get('is_channel')
        has_file = recieved_data.get('has_file')
        file = recieved_data.get('file')
        file_type = recieved_data.get('file_type')

        sender_name = await self.get_sender_name(sent_by_id)

        if not message:
            print('Error: Empty Message')
            return False

        if is_channel == '1':
            sent_by_user = await self.get_user_object(sent_by_id)
            channel_obj = await self.get_channel_object(thread_id)
            if not sent_by_user:
                print('Error:: sent by user is incorrect')
            if not channel_obj:
                print('Error:: Channel id is incorrect')

            await self.create_channel_message(sent_by_user, channel_obj, message, has_file, file_type, file)

            response = {
                'message': message,
                'sent_by': sent_by_id,
                'thread_id': thread_id,
                'is_channel': is_channel,
                'sender_name': sender_name,
                'file': file,
                'file_type': file_type
            }

            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'chat_message',
                    'text': json.dumps(response)
                }
            )
        else:
            sent_by_user = await self.get_user_object(sent_by_id)
            thread_obj = await self.get_thread_object(thread_id)
            if not sent_by_user:
                print('Error:: sent by user is incorrect')
            if not thread_obj:
                print('Error:: Thread id is incorrect')

            await self.create_chat_message(sent_by_user, thread_obj, message, has_file, file_type, file)

            response = {
                'message': message,
                'sent_by': sent_by_id,
                'thread_id': thread_id,
                'is_channel': is_channel,
                'sender_name': sender_name,
                'file': file,
                'file_type': file_type
            }

            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'chat_message',
                    'text': json.dumps(response)
                }
            )

    async def websocket_disconnect(self, event):
        print("Disconnet: ", event)

    async def chat_message(self, event):
        # print('chat_message: ', event)

        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    @database_sync_to_async
    def get_user_object(self, user_id):
        qs = User.objects.filter(id=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def get_channel_object(self, channel_id):
        qs = Channel.objects.filter(id=channel_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def get_sender_name(self, user_id):
        user = User.objects.get(id=user_id)
        name = user.name
        return name

    @database_sync_to_async
    def get_thread_object(self, thread_id):
        qs = Thread.objects.filter(id=thread_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def create_channel_message(self, user, channel, message, has_file, file_type, file):
        ChannelMessage.objects.create(
            send_by=user, channel=channel, message=message, has_file=has_file, file_type=file_type, file=file)

    @database_sync_to_async
    def create_chat_message(self, user, thread, message, has_file, file_type, file):
        ChatMessage.objects.create(
            send_by=user, thread=thread, message=message, has_file=has_file, file_type=file_type, file=file)
