from src.data_models.server import Server
from src.data_models.client import Client
from src.utils.file_handler import FileHandler
from src.utils.wg_middleware import WgMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI()

class server(BaseModel):
    # TODO: implement an authentication method
    server_name : str
    server_id : str | None

class client(BaseModel):
    client_name : str
    client_id : str | None # Optional on creation
    server_id : str | None
    

@app.post('/server-create')
def create_server(r : server):
    # TODO: create server implementation
    # This should return the server pubkey and it's ID
    return {f'cpu stressed for {r.stress_time} seconds'}

@app.post('/server-enable')
def enable_server(r : server):
    # TODO: enable a server
    pass

@app.post('/server-disable')
def disable_server(r : server):
    # TODO: disable a server
    pass

@app.get('/server-pubkey')
def get_server_pub_key(r : server):
    # TODO: returns the server public key
    pass
 

@app.post('/add-client')
def add_client(r : client):
    # TODO: implement an client add
    # This should return the client private key, it's port, it's id and it's port
    # And the client .conf file
    # Every client should be associated with and server
    pass

@app.delete
def del_client(r : client):
    # TODO: delete an client on an server
    pass

@app.post
def gen_new_client_keys(r : client):
    # TODO: generate new key pairs for a client. It should return the new private keys
    pass

    

if __name__ == '__main__':
    host = os.environ['APP_HOST']
    port = int(os.environ['APP_PORT'])
    uvicorn.run(app, host=host, port=port)