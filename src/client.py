import textwrap

class Client:
    def __init__(
            self,
            id : str,
            priv_ip : str,
            ips_to_route : str,
            priv_key : str | None = None,
            pub_key : str | None = None):
        self.id = id
        self.priv_ip = priv_ip
        self.ips_to_route = ips_to_route
        self.priv_key = priv_key
        self.pub_key = pub_key

    def interface_str(self)->str:
        server_str = textwrap.dedent(f"""
                [Interface]
                PrivateKey = {self.priv_key}
                AllowedIPs = {self.priv_ip}
                """)
        return server_str

    def peer_str(self)->str:
        server_str = textwrap.dedent(f"""
                [Peer]
                PublicKey = {self.pub_key}
                Address = {self.priv_ip}
                """)
        return server_str