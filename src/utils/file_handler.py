from src.data_models.server import Server
from src.data_models.client import Client

class FileHandler:
    # Writes a server .conf file
    @classmethod
    def write_server_file(cls, server : Server, file_name : str | None = None)->str:
        """"Writes the server file and returns it's path"""
        if file_name is None:
            file_name = f'/etc/wireguard/{server.name}.conf'
        server_file_str = cls.gen_server_file(server, file_name)
        with open(file_name, 'w+') as f:
            f.write(server_file_str)
        return file_name

    @classmethod
    def gen_server_file(cls, server : Server)->str:
        server_file = ''
        server_file += server.interface_str()
        for id, client in server.client_list.items():
            server_file += f"\n# Client {id}"
            server_file += client.peer_str()
        return server_file
    
    # Writes a client .conf file
    @classmethod
    def write_client_file(cls, client : Client, server : Server, file_name : str | None = None)->str:
        """"Writes the client file and returns it's path"""
        if file_name is None:
            file_name = f'{client.name}.conf'

        client_file = cls.gen_client_file(client, server, file_name)
        with open(file_name, 'w+') as f:
            f.write(client_file)
        return file_name
    
    @classmethod
    def gen_client_file(cls, client : Client, server : Server)->str:
        client_file = ''
        client_file += client.interface_str()
        client_file += server.peer_str()
        client_file += f'AllowedIPs = {client.ips_to_route}'

        return client_file