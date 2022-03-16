#para rodar o bot localmente, deve ser preciso uma aplicação definida anteriormente e ser gerado um token, alem disso deve-se:
#instalar:  discord.py: para rodar a API
#           python-dotenv: para criar variáveis locais e "esconder" o token
#           requests: somente se quiser realizar acesso da API da binance definida na classe "cryptos.py"
#           nodemon: opicional, mas agiliza bastante no teste do código (compila auto sempre que salva o projeto)


import asyncio
from time import time
from webbrowser import get
import discord
from discord.ext import commands

import os

from dotenv import load_dotenv
load_dotenv()

#import das boas práticas e tratamento de erros
from discord.ext.commands.errors import MissingRequiredArgument, CommandNotFound

#bot token
TOKEN = os.environ["token"]

SERVER_ID = os.environ["server_id"]

ADMIN_ROLE = os.environ["admin_role"]

#bot construction (bot prefix)
intents = discord.Intents.all()

client = commands.Bot(".", intents=intents)

channels = []

Admin = None

@client.event
async def on_ready():
    print(f"{client.user} is online")
    #para saber onde está o canal o bot precisa estar logado antes de rodar "run"

@client.event
async def on_message(message):
        #para não entrar em loop das suas próprias mensagens
        roles = message.author.roles
        if message.author == client.user:
            return
        if not ADMIN_ROLE in [y.name.lower() for y in roles]:
            msg = await message.channel.send(
                f"{message.author.name}, você não tem permissão necessária para fazer isso!"
            )
            await wait_delete(msg)
            await wait_delete(message,3)
            return
        #quando detectar a palavra "palavrão"
        if "palavrão" in message.content:
            msg = await message.channel.send(
                f"Por favor, {message.author.name}, não ofenda os demais usuários!"
            )
            await message.delete()
            await wait_delete(msg)
        #evitar que o bot trave e os outros comandos parem de funcionar
        await client.process_commands(message)

async def wait_delete(msg, seconds=5):
    await asyncio.sleep(seconds)
    await msg.delete()

@client.command(name="channel", help="Makes the channel visible/invisible to the bot. Arguments:\n<option>: on/off")
async def activate_channel(ctx, id, option):
    global channels
    msg = None
    if option in ["on", "off"]:
        if id in channels:
            if option == "on":
                msg = await ctx.send("Channel already online!")
            else:
                index = channels.index(id)
                channels.pop(index)
                msg = await ctx.send("Channel is now offline!")
        else:
            if option == "on":
                channels.append(id)
                msg = await ctx.send("Channel is now online!")
            else:
                msg = await ctx.send("Channel already offline!")
    else:
        msg = await ctx.send("Wrong argument. Possible arguments: on/off")
    await wait_delete(msg)
    await wait_delete(ctx.message,3)


@client.command(name="close-channels", help="Close all channels activated")
async def clear_channels(ctx):
    global channels
    channels.clear()
    await wait_delete(ctx.message,3)


## função que cria o embed
def build_embed():

    embed=discord.Embed(title="Bora pra cima deles (os problemas)!", description="Galera, eu me prontifico de fazer o q estiver no meu alcance/conhecimento para nosso grupo concluir essa fase com sucesso. Vamos todos juntos de mãos dadas arrebentar essa bagaça!", color=0x0ecd1b)
    embed.set_author(name="Thales")
    embed.add_field(name="Qualquer dúvida,", value="Seja sincero, ninguém vai te julgar, todo mundo ta aqui pra aprender :p", inline=False)
    return embed

@client.command(name="embed", help="Cria embed.")
async def create_embed(ctx):
    global channels
    for channel in channels:
        await client.get_channel(int(channel)).send(embed=build_embed())
    await wait_delete(ctx.message,3)

@client.command(name="clear", help="Clear x number of messages in the current channel")
async def clear(ctx, amount=6):
    await ctx.channel.purge(limit=amount)


@client.event
async def on_command_error(ctx, error):
    msg = None
    if isinstance(error, MissingRequiredArgument): #se o erro for falta de argumentos
        msg = await ctx.send("Favor enviar todos os Argumentos.")
    elif isinstance(error, CommandNotFound): #se o erro for comando inexistente
        msg = await ctx.send("O comando não existe.")
    else:
        return
    msg = ctx.send("Digite .help para ver os parâmetros de cada comando.")
    await wait_delete(msg)
    await wait_delete(ctx.message,3)


client.run(TOKEN)