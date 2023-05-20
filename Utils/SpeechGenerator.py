from google.cloud import texttospeech
from google.oauth2 import service_account


class SpeechGenerator:
    client = None
    credentials = service_account.Credentials.from_service_account_file(
        'gcloud-key.json')

    def __init__(self):
        self.client = texttospeech.TextToSpeechClient(
            credentials=self.credentials)
        pass

    def generate(self, text):
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="ko-KR", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3)
        return self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
