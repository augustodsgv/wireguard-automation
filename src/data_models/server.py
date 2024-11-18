from src.data_models.client import Client
from src.data_models.key import Key
import ipaddress
import textwrap
class Server:
    def __init__(
            self,
            name : str,
            address : str,
            subnet : str,
            endpoint : str,
            port : int,
            nic : str,
            priv_key : str | None = None,
            id : str | None = None,
            ):
        
        self.name = name
        self.id = id
        self.address = address
        self.subnet = subnet
        self.endpoint = endpoint
        self.port = port
        self.nic = nic
        if priv_key is None:
            self.priv_key = Key.gen_private_key()
        else:
            self.priv_key = priv_key
        self.pub_key = Key.gen_public_key(self.priv_key)
        self.client_list = {}
        self.used_ips = []

    def add_client(self, client : Client):
        """"Add a client peer to the server"""
        if client.id in self.client_list.keys():
            raise KeyError(f"The client \"{client.id}\" already exists")
        
        if not ipaddress.ip_address(client.priv_ip) in ipaddress.ip_network(self.subnet):    # Checks if client ip in within the server subnet
            raise ValueError(f"The client ip \"{client.priv_ip}\" does not belong to the server subnet {self.subnet}")
        
        self.client_list[client.name] = client
        self.used_ips.append(client.priv_ip)

    def interface_str(self)->str:
        """Gets the server interface string"""
        server_str = textwrap.dedent(f"""
                [Interface]
                PrivateKey = {self.priv_key}
                ListenPort = {self.port}
                """)

        return server_str
    
    def peer_str(self)->str:
        """Gets the server peer string"""
        server_str = textwrap.dedent(f"""
                [Peer]
                PublicKey = {self.pub_key}
                Endpoint = {self.endpoint}:{self.port}
                """)
        return server_str
    
    def get_new_ip_in_range(self)->str:
        """"Returns an unused IP in the server range"""
        network = ipaddress.ip_network(self.subnet, strict=False)
        
        # Convert used IPs to ipaddress objects
        used_ip_objects = {ipaddress.ip_address(ip) for ip in self.used_ips}
        
        # Find the first unused IP
        for ip in network.hosts():  # Excludes network and broadcast addresses
            if ip not in used_ip_objects:
                return str(ip)