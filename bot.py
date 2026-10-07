import os
import discord
from openai import OpenAI

# إعدادات الاتصال بـ OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True

client_discord = discord.Client(intents=intents)

@client_discord.event
async def on_ready():
    print(f'Logged in as {client_discord.user} (Sera is online!)')

@client_discord.event
async def on_message(message):
    if message.author == client_discord.user:
        return

    # لو البوت اتبعتله رسالة أو تم الإشارة ليه (Mention)
    if client_discord.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        prompt = message.content.replace(f'<@{client_discord.user.id}>', '').strip()
        
        if not prompt:
            return

        async with message.channel.typing():
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "أنت مساعد ذكي ولطيف اسمك سيرا (Sera) وتتحدث باللغة العربية."},
                        {"role": "user", "content": prompt}
                    ]
                }
                reply = response.choices[0].message.content
                await message.reply(reply)
            except Exception as e:
                await message.reply(f"حصلت مشكلة بسيطة: {e}")

# تشغيل البوت باستخدام التوكن من إعدادات الاستضافة
TOKEN = os.environ.get("TOKEN")
client_discord.run(TOKEN)