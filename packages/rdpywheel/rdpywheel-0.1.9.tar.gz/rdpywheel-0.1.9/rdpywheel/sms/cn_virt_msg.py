import os
from urllib.parse import urljoin, urlencode
import requests

sms_token = os.environ.get("CN_VIRTUAL_TOKEN")
sms_base_url = os.environ.get("CN_VIRTUAL_BASE_URL")


class CnVirtMsg:
    def get_sms_phone_number(token: str):
        try:
            params = {
                "code": "getPhone",
                "token": token,
                "cardType": "实卡"
            }
            url = urljoin(sms_base_url, "?" + urlencode(params))
            response = requests.get(url=url, timeout=10)
            data = response.content
            string_data = data.decode('utf-8')
            return string_data
        except Exception as e:
            print(e)

    def get_sms_msg(token: str, phone_no: str, key_word: str):
        try:
            params = {
                "code": "getMsg",
                "token": token,
                "phone": phone_no,
                "keyWord": key_word
            }
            url = urljoin(sms_base_url, "?" + urlencode(params))
            response = requests.get(url=url, timeout=10)
            data = response.content
            string_data = data.decode('utf-8')
            return string_data
        except Exception as e:
            print(e)

    def block_phone(token: str, phone_no: str):
        try:
            params = {
                "code": "block",
                "token": token,
                "phone": phone_no,
            }
            url = urljoin(sms_base_url, "?" + urlencode(params))
            response = requests.get(url=url, timeout=10)
            data = response.content
            string_data = data.decode('utf-8')
            return string_data
        except Exception as e:
            print(e)

    def get_msg_text(token: str, phone_no: str, key_word: str):
        try:
            params = {
                "code": "block",
                "token": token,
                "phone": phone_no,
                "keyWord": key_word
            }
            url = urljoin(sms_base_url, "?" + urlencode(params))
            response = requests.get(url=url, timeout=10)
            data = response.content
            string_data = data.decode('utf-8')
            return string_data
        except Exception as e:
            print(e)
