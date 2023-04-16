# Series of functions to be called when an event happens
# Deals with handoffs and threading for async code

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *
from .serializers import *
from asgiref.sync import sync_to_async
import random


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

        await self.send_json(({
            'type': 'connection_established',
            "message": "You are now connected!",
        }))

        # self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_name = "placeholder"
        # Add the connection to a named group to enable
        # sending messages to a group of connections at once.
        await self.channel_layer.group_add(
            self.room_name,  # `room_id` is the group name
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "send_json_message",
                "message": "You are now connected to the group!",
            }
        )

    async def send_json_message(self, event):
        message = event["message"]
        await self.send_json(message)

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

        # 'register' => user registers, return a random new user id in uuid4
        # 'create_room' => user creates a room, needs user id as own, return a random room id in uuid4 if success otherwise indicate fail
        # 'join_room' => user joins a room, needs user id and room id, return a success or fail message
        # 'start_game' => user starts a game, needs user id and room id, return a success or fail message
        # 'game_move' =>
        # 'game_end' =>
        # 'game_reset' =>
        # 'game_pause' =>
        # 'discard_tile' => user discards a tile, needs user id + room id + tile suite and number, return none (proceed w game logic)
        # 'draw_tile' (i.e. 'your_turn') => return random tile (suite + number)

        event_type = content.get('type')
        if event_type == 'echo':
            await self.send_json(content)
        elif event_type == 'create_room':
            print(f"Creating room")
            await self.create_room()
        elif event_type == 'join_room':
            room_id = content.get('room_id')
            await self.join_room(room_id, content)
        elif event_type == 'leave_room':
            room_id = content.get('room_id')
            await self.leave_room(room_id)
        elif event_type == 'start_game':
            await self.start_game()
        else:
            await self.send_json({
                'message': 'not an event type'
            })

        # try:
        #     response = handler(data)
        # except Exception as e:
        #     response = {
        #         'type': 'error',
        #         'data':
        #             'message': str(e)
        #         }
        #     }

        # """
        # # Example code of how to update models
        # pid = content['player_id']
        # try:
        #     player = await self.get_model(pid)
        #     # Stuff
        # except Player.DoesNotExist:
        #     return
        # """

    # Add client to a group with specified room_id

    async def create_room(self):
        # make sure player isn't already in room

        """ # test create_room function from front end
        random_room_id = random.randint(10000000, 99999999)
        await self.send_json({
            'message': 'Successfully created room!',
            'room_id': random_room_id,
            'result': 'room_id',
            'status': '202'
        })
        return """

        # create player ID
        client_key = self.scope["session"].session_key
        try:
            player = await self.get_player_model(client_key)
        except Player.DoesNotExist:
            player = await self.create_player_model(client_key)

        # creates random room id and makes sure it's not already in use
        random_room_id = random.randint(10000000, 99999999)
        while await self.filter_room_models(random_room_id).count() != 0:
            random_room_id = random.randint(10000000, 99999999)

        # creates a room
        if player.room is None:
            room = await self.create_room_model(random_room_id)
            await self.send_json({
                'message': 'Successfully created room!',
                'room_id': random_room_id,
                'result': 'roomNum',
                'status': '202'
            })
            await self.join_room(room)
        else:
            await self.send_json({
                'message': 'Player already in a room.'
            })

    async def join_room(self, room_id, content):
        client_key = self.scope["session"].session_key
        # try:
        #     player = self.get_player_model(client_key)
        # except Player.DoesNotExist:
        #     player = self.create_player_model(client_key)
        room_result = await self.filter_room_models(room_id)
        if await sync_to_async(Player.objects.filter(room__room_id=room_id)).count() == 4:
            await self.send_json({
                'Bad Request': 'Room is full'
            })
        elif await sync_to_async(Player.objects.filter)(player_id=client_key).count() == 0:
            player = await self.create_player_model(client_key)
            player.room = room_result[0]
            await sync_to_async(player.save)()

            await self.serialize_player_data(player, content)
        else:
            player = await self.filter_player_models(client_key)[0]
            player.room = room_result[0]
            await sync_to_async(player.save)()

            await self.serialize_player_data(player, content)

    # mimic serializer function in views
    # need to make sure the content has all of the necessary fields for Room model from the frontend
    # and omit the `type` key when assigning to fields
    # serializer = PlayerSerializer(player, context={'request': request})
    # just sending a json for now
    async def serialize_player_data(self, player, content):
        serializer = await sync_to_async(PlayerSerializer)(player, context={'content':content})
        is_valid = await sync_to_async(serializer.is_valid)()
        if is_valid:
            # Update object using serializer data asynchronously
            await sync_to_async(serializer.save)()
            await self.send_json({
                'data': serializer.data,
                'status': '202'
            })
        else:
            # serializer data is invalid asynchronously 
            errors = await sync_to_async(serializer.error)()
            await self.send_json({
                'errors': errors,
                'status': '400'
            })

    async def leave_room(self, room_id):
        client_key = self.scope["session"].session_key
        if await self.filter_player_models(client_key).count() != 0:
            if Player.objects.filter(player_id=self.request.session.session_key)[0].room == None:
                await self.send_json({
                    'message': 'You are not in a room',
                    'status': 400
                })
            
            player = await self.filter_player_models(client_key)[0]
            curr_room = player.room.room_id
            player.room = None
            await sync_to_async(player.save)()
            
            if sync_to_async(Player.objects.filter)(room__room_id=curr_room).count() == 0:
                await self.filter_room_models(curr_room).delete()

    async def start_game(self):
        return

    async def add_to_group(self):
        await self.channel_layer.group_add(
            self.room_name,  # `room_id` is the group name
            self.channel_name
        )


    # methods to access player and room model databases
    @database_sync_to_async
    def get_room_model(self, room_id):
        return Room.objects.get(room_id=room_id)

    @database_sync_to_async
    def create_room_model(self, room_id):
        return Room.objects.create(room_id=room_id)
    
    @database_sync_to_async
    def filter_room_models(self, room_id):
        return Room.objects.filter(room_id=room_id)

    @database_sync_to_async
    def get_player_model(self, player_id):
        return Player.objects.get(player_id=player_id)

    @database_sync_to_async
    def create_player_model(self, player_id):
        return Player.objects.create(player_id=player_id)
    
    @database_sync_to_async
    def filter_player_models(self, player_id):
        return Player.objects.filter(player_id=player_id)
