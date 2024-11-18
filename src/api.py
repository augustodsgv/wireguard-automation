from src.data_models.server import Server
from src.data_models.client import Client
from src.utils.file_handler import FileHandler
from src.utils.wg_middleware import WgMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
import ipaddress
app = FastAPI()

base_server = Server(
    'wg0',
    '10.0.0.1/24',
    '10.0.0.0/24',
    '192.168.0.1',
    51820,
    'eno3'
    )
print(base_server.priv_key)

class ClientRequest(BaseModel):
    client_name : str
    client_id : Optional[str] = None
    ips_to_route : Optional[str] = None


@app.post('/add-client')
def add_client(r : ClientRequest):
    # TODO: implement an client add
    # This should return the client private key, it's port, it's id
    # And the client .conf file
    # Every client should be associated with and server
    
    client_priv_ip = base_server.get_new_ip_in_range()
    ips_to_route = r.ips_to_route

    if ips_to_route is None:        # If user does not provide IPs to route to VPN, route all IPs to VPN
        ips_to_route = '0.0.0.0/0'
    
    new_client = Client(r.client_name, client_priv_ip, ips_to_route)
    base_server.add_client(new_client)
    # FileHandler.write_server_file(base_server)
    # WgMiddleware.refresh_server()
    client_file = FileHandler.gen_client_file(new_client, base_server)
    print(new_client.pub_key)
    
    response = {
        "server_name" : base_server.name,
        "server_public_key" : base_server.pub_key,
        "server_port" : base_server.port,
        "client_name" : new_client.name,
        "client_ip" : new_client.priv_ip,
        "client_private_key" : new_client.priv_key,
        "client_conf_file" : client_file
    }
    return response

@app.delete('/delete-client')
def del_client(r : ClientRequest):
    # TODO: delete an client on an server
    pass

@app.post('/gen-new-keys')
def gen_new_client_keys(r : ClientRequest):
    # TODO: generate new key pairs for a client. It should return the new private keys
    pass  

# if __name__ == '__main__':
    # host = os.environ['APP_HOST']
    # port = int(os.environ['APP_PORT'])
    # uvicorn.run(app, host=host, port=port)
    # uvicorn.run(app, host='0.0.0.0', port=8000)
