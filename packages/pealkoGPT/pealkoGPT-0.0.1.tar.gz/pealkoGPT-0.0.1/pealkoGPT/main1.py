import os
import discord
from dotenv import load_dotenv
from pyChatGPT import ChatGPT
load_dotenv()
token = os.getenv("TOKEN")
gpt = ChatGPT(auth_type='openai', email='perelexa2.0@gmail.com', password='perelexa1998')
bot = discord.Bot(intents=discord.Intents.all())
messages = []

@bot.event
async def on_ready():
    print(f"{bot.user} is ready")

@bot.slash_command(name="chat", description="Start chat")
async def chat(ctx, prompt: str):
    # messages.append({"role": "user", "content": str(prompt)})
    answer = gpt.send_message(prompt)
    await ctx.respond(answer)
    # messages.append({"role": "assistant", "content": answer})

@bot.slash_command(name="ping", description="Ping the bot")
async def ping(ctx):
    await ctx.respond(bot.latency)

bot.run(token)
