import datetime
import os
from openai import OpenAI
from config.config import config


async def voice_trans(file_name: str):
    client = OpenAI(
        api_key=config.api_key
    )
    try:
        print(f'{datetime.datetime.now()} - [INFO] - send request to OpenAI')
        audio_file = open(file_name, "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        result = transcription.text
    except Exception as ex:
        print(f'{datetime.datetime.now()} - [ERROR] - {ex}')
        return None
    print(f'{datetime.datetime.now()} - [OK] - send successful request. Text: {result}')
    os.remove(file_name)
    return result
