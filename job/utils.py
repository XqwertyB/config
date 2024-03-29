import requests
from rest_framework.exceptions import ValidationError


def send_phone_notification(phone, code):
    abonent_code = phone[3:5]
    if int(abonent_code) in [97, 88]:
        return requests.get(
            f"https://portal.inhub.uz:8443/hunar?sn=6300&msisdn={phone}&message=Tasdiqlash kodi: {code}")
    elif int(abonent_code) in [99, 77, 95, 98, 33]:
        return requests.get(
            f"https://portal.inhub.uz:8443/hunar?sn=6500&msisdn={phone}&message=Tasdiqlash kodi: {code}")

    elif int(abonent_code) in [93, 94, 90, 91]:
        return requests.get(
            f"https://portal.inhub.uz:8443/hunar?sn=8687&msisdn={phone}&message=Tasdiqlash kodi: {code}")
    else:
        data = {
            'succes': False,
            "message": f"Code {abonent_code} is not supported!",
        }
        raise ValidationError(data)
