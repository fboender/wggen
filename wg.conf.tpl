{%
    server_device_name = config["server"]["device_name"]
    server_config = config["devices"][server_device_name]
    is_server = device_name == config["server"]["device_name"]
%}
[Interface]
Address = {{ device_config["ip"] }}/24
{%
    if is_server:
        print("ListenPort = 51820")
%}
PrivateKey = {{ device_config["priv_key"] }}

{%
    if is_server:
        # Server
        for peer_name, peer_info in config["devices"].items():
            if peer_name == device_name:
                continue

            print(f"# {peer_name}")
            print(f"[Peer]")
            print(f"PublicKey = {peer_info["pub_key"]}")
            print(f"AllowedIPs = {peer_info["ip"]}/32")
            print()
    else:
        # Client
        print(f"[Peer]")
        print(f"PublicKey = {server_config["pub_key"]}")
        print(f"Endpoint = {config["server"]["domain_name"]}:51820")
        print(f"AllowedIPs = {config["server"]["network"]}/24")
        if config["keepalive"] is not False:
            print(f"PersistentKeepAlive = {config["keepalive"]}")
%}
