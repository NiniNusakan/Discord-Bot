import discord
import random
import os
import requests
import asyncio
import typing

from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

def gen_img():
    lista = os.listdir('images')
    img_escolhida = random.choice(lista)
    return img_escolhida

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

def get_cat():
    url = "https://api.thecatapi.com/v1/images/search"
    response = requests.get(url)
    data = response.json()
    return data[0]["url"]

dicionário = {
    "caixa de sapato" : 'https://www.youtube.com/watch?v=O4_-Edd8EGY',
    "garrafa pet" : "https://www.youtube.com/watch?v=xCaI-5WVRlY",
    "rolinho de papel" : "https://www.youtube.com/watch?v=XpJ5c_WJ0BI",
    "meias" : "https://www.youtube.com/watch?v=0nB69-RfKsY",
    "cano pvc" : "https://www.youtube.com/watch?v=9dgTXcd_ub8"

}


@bot.event
async def on_ready():
    print(f'Estamos logados como {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Olá! eu sou um bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def meme(ctx):
    with open(f'images/{gen_img()}', 'rb') as f:
        #Vamos armazenar o arquivo convertido da biblioteca do Discord nesta variável!
        picture = discord.File(f)
    # Podemos então enviar esse arquivo como um parâmetro
    await ctx.send(file=picture)

@bot.command('duck')
async def duck(ctx):
    '''Uma vez que chamamos o comando duck, o programa chama a função get_duck_image_url '''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command()
async def cat(ctx):
    import requests
    url = "https://api.thecatapi.com/v1/images/search"
    res = requests.get(url).json()
    await ctx.send(res[0]["url"])

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('$guess'):
            await message.channel.send('Guess a number between 1 and 10.')

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()

            answer = random.randint(1, 10)

            try:
                guess = await self.wait_for('message', check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry, you took too long it was {answer}.')

            if int(guess.content) == answer:
                await message.channel.send('You are right!')
            else:
                await message.channel.send(f'Oops. It is actually {answer}.')

@bot.command()
async def reciclagem_incomum(ctx):
    await ctx.send(dicionário.values())

@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    await channel.send(f'Bem-vindo ao servidor, {member.mention}!')

bot.run("token")
