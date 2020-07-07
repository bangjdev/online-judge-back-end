from channels.consumer import AsyncConsumer


class SubmissionConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept",
        })
        await self.channel_layer.group_add("submissions-client", self.channel_name)

    async def websocket_receive(self, event):
        print("received", event)

    async def websocket_disconnect(self, event):
        print("disconnect", event)
        await self.channel_layer.group_discard("submissions-client", self.channel_name)

    async def database_change(self, event):
        print("From Consumer", event)
        await self.send({
            "type": "websocket.send",
            "text": "NEW_SUBMISSION_CHANGE"
        })
