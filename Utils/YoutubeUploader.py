# https://github.com/P-Sal-Check/auto-podcast-ai/blob/master/youtube_module.py
import os
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.service_account import Credentials


class YouTubeUploader:
    def __init__(self):
        # Use the YouTube Data API v3
        self.api_service_name = "youtube"
        self.api_version = "v3"

        self.youtube = None

    def __get_authenticated_service(self):
        # Get credentials and create an API client
        # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        #     self.client_secrets_file, ["https://www.googleapis.com/auth/youtube.upload"])
        # credentials = flow.run_local_server()
        credentials = Credentials.from_service_account_file(
            'client_secrets.json', scopes=[
                "https://www.googleapis.com/auth/youtube.upload"]
        )
        youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, credentials=credentials)
        return youtube

    def upload_video(self, title, description):
        self.youtube = self.__get_authenticated_service()

        request = self.youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "categoryId": '25',
                    "description": description,
                    "title": title
                },
                "status": {
                    "privacyStatus": "private"
                }
            },
            media_body=googleapiclient.http.MediaFileUpload(
                f'videos/{title}.mp4')
        )
        response = request.execute()
        return response
