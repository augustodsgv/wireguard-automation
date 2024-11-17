from src.data_models.server import Server
from src.data_models.client import Client

class FileHandler:
    # Writes a server .conf file
    @classmethod
    def write_server_file(cls, server : Server, file_name : str | None = None)->None:
        if file_name is None:
            file_name = f'/etc/wireguard/{server.name}.conf'
        with open(file_name, 'w+') as f:
            f.write(server.interface_str())
            for id, client in server.client_list.items():
                f.write(f"\n# Client {id}")
                f.write(client.peer_str())

    # Writes a client .conf file
    @classmethod
    def write_client_file(cls, client : Client, server : Server, file_name : str | None = None):
        if file_name is None:
            file_name = f'client{client.id}.conf'
        with open(file_name, 'w+') as f:
            f.write(client.interface_str())
            f.write(server.peer_str())
            f.write(f'AllowedIPs = {client.ips_to_route}')