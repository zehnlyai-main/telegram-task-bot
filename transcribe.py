from openai import AsyncOpenAI


async def transcribe(file_path: str, api_key: str) -> str:
    """Transcribe a voice file using OpenAI Whisper. Auto-detects language."""
    client = AsyncOpenAI(api_key=api_key)
    with open(file_path, "rb") as audio:
        response = await client.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
        )
    return response.text.strip()
