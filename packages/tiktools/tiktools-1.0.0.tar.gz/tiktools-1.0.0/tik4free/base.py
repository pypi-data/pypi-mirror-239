import requests
from re import findall
from requests   import get

class Tik4free():
    @staticmethod
    def short2long(url: str) -> str:
        try:
            url = "https://api2.musical.ly/tiktok/linker/target/get/v1/?url={}".format(url)
            response = requests.request("GET", url).json()
            if not response['landing_url'] or response['status_code'] != 0:
                return False
            else:
                return response['landing_url']
        except Exception as e:
            return print(str(e))
    
    @staticmethod
    def aweme(video_link):
        try:
            return findall(r"(\d{18,19})", video_link)[0] if len(findall(r"(\d{18,19})", video_link)) != 0 else findall(r"(\d{18,19})", get(video_link, allow_redirects=False, timeout=2).headers['Location'])[0]
        except:
            return False

    @staticmethod
    def checkExist(username):
        try:
            username = requests.get(f'https://www.tiktok.com/oembed?url=https://www.tiktok.com/@{username}').json()['author_name']
            return True
        except:
            return False

    @staticmethod
    def long2short(url: str) -> str:
        try:
            url = "https://www.tiktok.com/shorten/?target={}&belong=tiktok_tv_short_url".format(url)
            response = requests.request("POST", url).json()
            if response['message'] != "success" or response['code'] != 0:
                return False
            else:
                return response['data']
        except Exception as e:
            return print(str(e))
    
    @staticmethod
    def removeWm(awemeid: int):
        try:
            url = "https://api16-normal-useast5.us.tiktokv.com/tiktok/v1/videos/detail/?aweme_ids=%5B{}%5D".format(awemeid)
            headers = {"User-Agent": "com.zhiliaoapp.musically/2023102040 (Linux; U; Android 9; de_DE; SM-N975F; Build/PI;tt-ok/3.12.13.4-tiktok)"}
            response = requests.request("GET", url, headers=headers).json()
            if not response['aweme_details'][0]['aweme_id']:
                return None
            else:
                return response['aweme_details'][0]['video']['bit_rate'][0]['play_addr']['url_list'][0]
        except Exception as e:
            return print(str(e))
    
    @staticmethod
    def getSound(awemeid: int):
        try:
            url = "https://api16-normal-useast5.us.tiktokv.com/tiktok/v1/videos/detail/?aweme_ids=%5B{}%5D".format(awemeid)
            headers = {"User-Agent": "com.zhiliaoapp.musically/2023102040 (Linux; U; Android 9; de_DE; SM-N975F; Build/PI;tt-ok/3.12.13.4-tiktok)"}
            response = requests.request("GET", url, headers=headers).json()
            if not response['aweme_details'][0]['aweme_id']:
                return False
            else:
                return response['aweme_details'][0]['music']['play_url']['uri']
        except Exception as e:
            return print(str(e))
    
    @staticmethod
    def getUserid(username: str or int = str) -> str:
        try:
            url = "https://tiktok.livecounts.io/user/search/{}".format(username)
            headers = {
                "Accept"        : "*/*",
                "Connection"    : "keep-alive",
                "Host"          : "tiktok.livecounts.io",
                "Origin"        : "https://livecounts.io",
                "Referer"       : "https://livecounts.io/",
                "User-Agent"    : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            }

            response = requests.request("GET", url, headers=headers).json()
            if not response['userData'][0]['userId']:
                return False
            else:
                return response['userData'][0]['userId']
        except Exception as e:
            return print(str(e))