from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket]= {}

    async def connect(self, user_id:int, websocket: WebSocket):
        await websocket.accept()

        existing_connection = self.active_connections.get(user_id)

        if existing_connection and existing_connection is not websocket:
            try:
                await existing_connection.close()
            except Exception:
                pass

        self.active_connections[user_id] = websocket

    def disconnect(self, user_id:int, websocket: WebSocket):
        current_connection = self.active_connections.get(user_id)

        if current_connection is websocket:
            self.active_connections.pop(user_id, None)

    async def send_to_user(self, user_id:int, data:dict)->bool:
        websocket = self.active_connections.get(user_id)

        if websocket is None:
            return False

        try:
            await websocket.send_json(data)
            return True
        except Exception:
            self.disconnect(user_id, websocket)
            return False

manager = ConnectionManager()