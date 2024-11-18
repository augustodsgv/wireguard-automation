import textwrap
from src.data_models.key import Key

class Client:
    def __init__(
            self,
            name : str,
            priv_ip : str,
            ips_to_route : str,
            priv_key : str | None = None,
            id : str | None = None,
            ):
        self.name = name
        self.priv_ip = priv_ip
        self.ips_to_route = ips_to_route
        self.id = id

        if priv_key is None:
            self.priv_key = Key.gen_private_key()
        else:
            self.priv_key = priv_key
        self.pub_key = Key.gen_public_key(self.priv_key)

    def interface_str(self)->str:
        server_str = textwrap.dedent(f"""
                [Interface]
                PrivateKey = {self.priv_key}
                Address = {self.priv_ip}
                """)
        return server_str

    def peer_str(self)->str:
        server_str = textwrap.dedent(f"""
                [Peer]
                PublicKey = {self.pub_key}
                AllowedIPs = {self.priv_ip}/32
                """)
        return server_str