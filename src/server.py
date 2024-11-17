from src.client import Client
import textwrap
class Server:
    def __init__(
            self,
            name : str,
            address : str,
            endpoint : str,
            port : int,
            nic : str,
            priv_key : str,
            pub_key : str | None = None,
            ):
        
        self.name = name
        self.address = address
        self.endpoint = endpoint
        self.port = port
        self.nic = nic
        self.priv_key = priv_key
        self.pub_key = pub_key
        self.client_list = {}

        # TODO: generating new priv_keys and pub keys from it
    
    # TODO
    # @property
    # def pub_key(self)->str:
    #     pass

    # Adds a client to the list
    def add_client(self, client : Client):
        if not client.id in self.client_list.keys():
            self.client_list[client.id] = client
        else:
            raise KeyError(f"The client \"{client.id}\" already exists")
            # TODO: Check if client ip is not already used

    # Gets the server interface string
    def interface_str(self)->str:
        server_str = textwrap.dedent(f"""
                PostUp = ufw route allow in on wg0 out on {self.nic}
                PostUp = iptables -t nat -I POSTROUTING -o {self.nic} -j MASQUERADE
                PostUp = ip6tables -t nat -I POSTROUTING -o {self.nic} -j MASQUERADE
                PreDown = ufw route delete allow in on wg0 out on {self.nic}
                PreDown = iptables -t nat -D POSTROUTING -o {self.nic} -j MASQUERADE
                PreDown = ip6tables -t nat -D POSTROUTING -o {self.nic} -j MASQUERADE
                                     
                [Interface]
                SaveConfig = true
                Address = {self.address}
                PrivateKey = {self.priv_key}
                ListenPort = {self.port}
                """)
            
        return server_str
    
    # Gets the server peer string
    def peer_str(self)->str:
        server_str = textwrap.dedent(f"""
                [Peer]
                PublicKey = {self.pub_key}
                Endpoint = {self.endpoint}:{self.port}
                """)
        return server_str