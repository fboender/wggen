#!/bin/env python3

import ast
import os
import subprocess
import morestd.template


def read_config(path):
    with open(path, 'r') as fh:
        try:
            conf = ast.literal_eval(fh.read())
            return conf
        except Exception as err:
            raise err

def get_pub_key(priv_key):
    res = subprocess.run(
        ["wg", "pubkey"],
        input=priv_key,
        text=True,
        capture_output=True,
        check=True,
    )
    return res.stdout.strip()


if __name__ == "__main__":
    config = read_config("wggen.conf")

    # Create out/ dir
    if not os.path.exists("out"):
        os.mkdir("out")
        os.chmod("out", 0o700)

    # Read template
    with open("wg.conf.tpl", "r") as fh:
        tpl_server = fh.read()

    # Generate public keys from private keys and set for each device
    for name, info in config["devices"].items():
        info["pub_key"] = get_pub_key(info["priv_key"])

    # Generate wireguard configs for each device
    for device_name, device_config in config["devices"].items():
        with open(os.path.join("out", f"{device_name}.{config['interface']}.conf"), "w") as fh:
            fh.write(
                morestd.template.render(
                    tpl_server,
                    {
                        "device_name": device_name,
                        "device_config": device_config,
                        "config": config,
                    }
                )
            )
