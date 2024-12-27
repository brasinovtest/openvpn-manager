from fastapi import APIRouter

from openvpn_manager import OpenVPNManager

status = APIRouter(
    prefix="/status",
)

@status.get("/status")
def get_status():
    openvpn = OpenVPNManager()
    openvpn.connect('ip address', 7505)
    dados = openvpn.status.execute()
    openvpn.close()
    return dados
