from src.data_models.server import Server
from src.data_models.client import Client
from src.utils.file_handler import FileHandler
from src.utils.wg_middleware import WgMiddleware
s = Server(name='wg0',
           address='10.0.0.1/24',
           endpoint='192.168.0.2',
           port=51820,
           nic='wlp0s20f3',
           priv_key='SOb6VottRkts/TgQyeCuaITRej6aduCtXiSVu3WRTnY=',
           pub_key='+wnONXyF8um2P6VQLx2mFEeuLvecQhgH30y7q6Eao1g=')

c = Client('1',
           '10.0.0.14/32',
           '0.0.0.0/0',
           'UAcdEHKH2a8vXVKAxKGP/nNtPmQtOLmRDbGYCL7hf3s=',
           '+FlWfDYLCI4i7PZXBx/uXRMpbGaooWuNxjTbr8ahY0k=')

s.add_client(c)
FileHandler.write_server_file(s)
FileHandler.write_client_file(c, s, 'client0.conf')
WgMiddleware.enable_server(s)
