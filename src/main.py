from src.server import Server
from src.client import Client
from src.file_handler import FileHandler
s = Server(address='10.0.0.1/24',
           endpoint='201.23.7.247',
           port=51820,
           nic='eno3',
           priv_key='priv',
           pub_key='pub')

c = Client('1',
           '10.0.0.14/32',
           '0.0.0.0/0',
           'priv',
           'pub')

s.add_client(c)
FileHandler.write_server_file(s, './wg1.conf')
FileHandler.write_client_file(c, s, 'client0.conf')