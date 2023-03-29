# Series of functions to be called when an event happens
# Deals with handoffs and threading for async code

import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import *
# from channels.db import database_sync_to_async
# from asgiref.sync import async_to_sync, sync_to_async

class AppConsumer(AsyncJsonWebsocketConsumer):
    """
    This app  consumer handles websocket connections for chat clients.
    It uses AsyncJsonWebsocketConsumer, which means all the handling functions
    must be async functions, and any sync work (like ORM access) has to be
    behind database_sync_to_async or sync_to_async. For more, read
    http://channels.readthedocs.io/en/latest/topics/consumers.html
    """
    # Called on connection
    async def connect(self):
        # To accept the connection call:
        await self.accept()

        self.room_name = self.scope['url_route']['kwargs']['room_id']
        # Add the connection to a named group to enable 
        # sending messages to a group of connections at once.
        await self.channel_layer.group_add(
            self.room_name, # `room_id` is the group name
            self.channel_name
        )

    async def disconnect(self, close_code):
        # Called when WebSocket closes
        print("Disconnected")

        # Remove connection from group
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive_json(self, content):
        # Handles incoming JSON message from client
        print(f"Received JSON message:{content}")
        
        # placeholder: just echo the message back to the client 
        await self.send_json(({
            'echo': content
        }))
