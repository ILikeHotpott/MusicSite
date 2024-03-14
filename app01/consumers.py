from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        sender = self.scope['url_route']['kwargs']['sender']
        receiver = self.scope['url_route']['kwargs']['receiver']

        # 按字典序排序用户名，确保房间名称的唯一性和一致性
        self.room_name = "_".join(sorted([sender, receiver]))
        self.room_group_name = f'chat_{self.room_name}'

        # 加入房间
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 离开房间
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 处理接收到的消息
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json.get('sender')

        # 发送消息到房间组，同时包含发送者信息
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

    # 收到房间组内的消息
    async def chat_message(self, event):
        message = event['message']
        sender = event.get('sender')  # 获取发送者信息

        # 发送消息到WebSocket，包括发送者信息
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
