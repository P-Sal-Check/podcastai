from moviepy import editor
from io import BytesIO
from PIL import Image
import requests


class ThumbVideoGenerator:
    def __init__(self):
        pass

    def generate(self, thumb_source, audio_source, file_name):
        response = requests.get(thumb_source)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img.save(f'images/{file_name}.jpg')

        audio = editor.AudioFileClip(audio_source)
        image = editor.ImageClip(
            f'images/{file_name}.jpg', duration=audio.duration)

        videoclip = image.set_audio(audio)

        videoclip.write_videofile(
            f"videos/{file_name}.mp4", codec='libx264', fps=24)

        print('ThumbVideoGeneratorpy - Generate Video.')
        return videoclip
