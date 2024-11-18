import subprocess
from src.data_models.server import Server

class WgMiddleware:
    @classmethod
    def enable_server(cls, server : Server):
        """"Enables the server on the wireguard"""
        subprocess.call(f'wg-quick up {server.name}', shell=True)

    @classmethod
    def disable_server(cls, server : Server):
        subprocess.call(f'wg-quick down {server.name}', shell=True)

    @classmethod
    def refresh_server(cls, server : Server, file_name : str):
        """"Hot reloads a server to add or remove peers or change configurations"""
        subprocess.call(f'wg syccconf {server.name} {file_name}', shell=True)
        