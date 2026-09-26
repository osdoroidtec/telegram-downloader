import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

app = Client(
    "telegram_downloader_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply_text(
        "🤖 Telegram Downloader Bot\n\n"
        "Send me a Telegram media message that this bot "
        "is allowed to access."
    )


@app.on_message(filters.media & ~filters.command("start"))
async def receive_media(client: Client, message: Message):
    status = await message.reply_text("⏳ Processing...")

    try:
        file_path = await message.download()

        await status.edit_text("📤 Uploading...")

        await message.reply_document(
            document=file_path,
            caption="✅ Download completed."
        )

        try:
            os.remove(file_path)
        except OSError:
            pass

        await status.delete()

    except Exception as e:
        await status.edit_text(
            f"❌ Error:\n{str(e)[:1000]}"
        )


async def main():
    await app.start()
    print("Telegram Bot is ONLINE")
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
