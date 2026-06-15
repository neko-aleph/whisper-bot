from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message

from .whisper import transcribe_bytes

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Hi, {message.from_user.first_name}! Just send me a voice message and I'll turn it into text"
    )


@router.message(F.voice | F.audio | F.video_note)
async def handle_media(message: Message, bot: Bot):
    media = message.voice or message.audio or message.video_note

    file = await bot.get_file(media.file_id)
    data = await bot.download_file(file.file_path)

    audio_bytes = data.read()

    text = await transcribe_bytes(audio_bytes)

    await message.answer(text)
