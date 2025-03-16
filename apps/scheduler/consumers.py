import json
from channels.generic.websocket import AsyncWebsocketConsumer

class JobConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("job_updates", self.channel_name) 
        await self.accept()
        await self.send(json.dumps({"message": "WebSocket connected!"}))

    async def disconnect(self, close_code):
        print("WebSocket disconnected")
        #await self.channel_layer.group_discard("job_updates", self.channel_name)  # Leave group


    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.send(json.dumps({"message": f"Received: {data}"}))

    async def send_job_status(self, event):
        """Send job updates to frontend"""
        await self.send(text_data=json.dumps(event["job"]))
