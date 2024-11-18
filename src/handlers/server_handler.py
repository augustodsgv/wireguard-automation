from src.data_models.client import Client
from src.data_models.server import Server
from pydantic import BaseModel

class ServerRequest(BaseModel):
    # TODO: implement an authentication method
    server_name : str
    server_id : str | None

class ServerHandler:
    def __init__(self, server : Server):
        self.server = server

    def create_server(r : server):
    # TODO: create server implementation
    # This should return the server pubkey and it's ID
        return {f'cpu stressed for {r.stress_time} seconds'}

    def enable_server(r : server):
    # TODO: enable a server
    pass

    def disable_server(r : server):
    # TODO: disable a server
    pass

    def get_server_pub_key(r : server):
    # TODO: returns the server public key
    pass
