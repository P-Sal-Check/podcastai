from dotenv import load_dotenv
from typing import Literal
import os
import requests

load_dotenv()
request_url = "https://api.d-id.com/talks"
avatar_src_url = "https://create-images-results.d-id.com/DefaultPresenters/Fotisa_f_ai/image.jpg"
voice_provider = "microsoft"
voice_id = "ko-KR-SeoHyeonNeural"
did_api_key = os.getenv("DID_API_KEY")


class VideoGenerator:
    # TODO: text, audio 타입에 따라 option이 input, audio_url 로 변경되도록 추상화
    # 근데 왜 파이썬에는 인터페이스가 없지
    __src_type: Literal["text", "audio"] = None
    __option: str = None

    url_param: str = None

    def __init__(self, src_type, option):
        self.__src_type = src_type
        self.__option = option
        pass

    # 비디오를 생성하여 did 서버에 저장
    def postVideo(self):
        headers = {
            "authorization": "Basic {}".format(did_api_key),
            "accept": "application/json",
            "content-type": "application/json"
        }
        payload = {
            "script": {
                "type": self.__src_type,  # "text" | "audio"
                "subtitles": "false",
                "provider": {
                    "type": voice_provider,
                    "voice_id": voice_id
                },
                "ssml": "false",
                "reduce_noise": "false",
                "input": "resolve this url issues ㅠㅠ"  # or "audio_url": "###"
            },
            "config": {
                "fluent": "false",
                "pad_audio": "0.0"
            },
            "source_url": avatar_src_url
        }
        response = requests.post(request_url, json=payload, headers=headers)
        self.url_param = response.text.id
        return response.text.id  # 비디오 저장소 url 요청 param source

    # did 서버에 요청하여 다운로드
    def getVideo(self):
        url = "https://api.d-id.com/talks/{}".format(self.url_param)

        headers = {
            "accept": "application/json",
            "authorization": "Basic {}".format(did_api_key),
        }

        response = requests.get(url, headers=headers)

        print(response.text)
