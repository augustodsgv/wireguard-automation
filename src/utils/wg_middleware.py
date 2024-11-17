import subprocess
from src.data_models.server import Server

class WgMiddleware:
    @classmethod
    def enable_server(cls, server : Server):
        subprocess.call(f'wg-quick up {server.name}', shell=True)

    @classmethod
    def disable_server(cls, server : Server):
        subprocess.call(f'wg-quick down {server.name}', shell=True)

    @classmethod
    def refresh_server(cls, server : Server):
        subprocess.call(f'wg-quick up {server.name}', shell=True)
        subprocess.call(f'wg-quick down {server.name}', shell=True)
        