import asyncio

import aiohttp

from decouple import config

HF_TOKEN = config("HF_TOKEN")

API_URL = (
    "https://router.huggingface.co/hf-inference/models/openai/whisper-large-v3-turbo"
)

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "audio/ogg",
}


async def transcribe_bytes(audio_bytes: bytes) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                API_URL,
                headers=HEADERS,
                data=audio_bytes,
                timeout=aiohttp.ClientTimeout(total=120),
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()

        return data.get("text", str(data))

    except asyncio.TimeoutError:
        return "⚠️ The server seems to be down now. Try again in a couple of minutes"

    except Exception as e:
        print(e)
        return "⚠️ Something went wrong. Try again in a couple of minutes"
