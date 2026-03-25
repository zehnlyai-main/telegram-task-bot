import os
import asyncio
import base64
import json

from openai import AsyncOpenAI


LANG_MAP_WHISPER = {"en": "en", "ru": "ru", "uz": "uz"}
LANG_MAP_GOOGLE = {"en": "en-US", "ru": "ru-RU", "uz": "uz-UZ"}


async def transcribe(file_path: str, api_key: str, provider: str, lang: str = "en") -> str:
    if provider == "openai":
        return await _transcribe_openai(file_path, api_key, lang)
    elif provider == "google":
        return await _transcribe_google(file_path, api_key, lang)
    raise ValueError(f"Unknown provider: {provider}")


async def _convert_oga_to_mp3(oga_path: str) -> str:
    mp3_path = oga_path.rsplit(".", 1)[0] + ".mp3"
    proc = await asyncio.create_subprocess_exec(
        "ffmpeg", "-y", "-i", oga_path, "-acodec", "libmp3lame", "-q:a", "2", mp3_path,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
    )
    await proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg conversion failed with code {proc.returncode}")
    return mp3_path


async def _transcribe_openai(file_path: str, api_key: str, lang: str) -> str:
    mp3_path = await _convert_oga_to_mp3(file_path)
    try:
        client = AsyncOpenAI(api_key=api_key)
        with open(mp3_path, "rb") as audio_file:
            response = await client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=LANG_MAP_WHISPER.get(lang, "en"),
            )
        return response.text.strip()
    finally:
        if os.path.exists(mp3_path):
            os.remove(mp3_path)


async def _transcribe_google(file_path: str, api_key: str, lang: str) -> str:
    from google.cloud import speech_v1 as speech
    from google.oauth2 import service_account

    creds_json = json.loads(base64.b64decode(api_key))
    credentials = service_account.Credentials.from_service_account_info(creds_json)
    client = speech.SpeechAsyncClient(credentials=credentials)

    with open(file_path, "rb") as f:
        content = f.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
        sample_rate_hertz=48000,
        language_code=LANG_MAP_GOOGLE.get(lang, "en-US"),
    )

    response = await client.recognize(config=config, audio=audio)
    if response.results:
        return response.results[0].alternatives[0].transcript.strip()
    return ""
