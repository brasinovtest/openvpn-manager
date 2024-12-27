import json

from openvpn_manager import OpenVPNManager


if __name__ == "__main__":

    with OpenVPNManager('ip address', 7505) as openvpn:
        dados = openvpn.status.execute()
        print(json.dumps(dados, indent=4))

# from app import create_app
#
#
#
# app = create_app()