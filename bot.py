#para rodar o bot localmente, deve ser preciso uma aplicação definida anteriormente e ser gerado um token, alem disso deve-se:
#instalar:  discord.py: para rodar a API
#           python-dotenv: para criar variáveis locais e "esconder" o token
#           requests: somente se quiser realizar acesso da API da binance definida na classe "cryptos.py"
#           nodemon: opicional, mas agiliza bastante no teste do código (compila auto sempre que salva o projeto)


import discord
from discord.ext import commands

import os

from dotenv import load_dotenv
load_dotenv()

#import das boas práticas e tratamento de erros
from discord.ext.commands.errors import MissingRequiredArgument, CommandNotFound

#bot token
TOKEN = os.environ["token"]

#bot construction (bot prefix)
intents = discord.Intents.all()

client = commands.Bot(".", intents=intents)

channels = []

@client.event
async def on_ready():
    print(f"{client.user} is online")
    #para saber onde está o canal o bot precisa estar logado antes de rodar "run"


@client.event
async def on_message(message):
        #para não entrar em loop das suas próprias mensagens
        if message.content.startswith('!admin'):
            if (message.author == message.server.owner):
            # do stuff
                await client.process_commands(message)
            else:
                msg = "This command can only be executed by the owner."
        await client.send_message(message.channel, msg)
        if message.author == client.user:
            return
        #quando detectar a palavra "palavrão"
        if "palavrão" in message.content:
            await message.channel.send(
                f"Por favor, {message.author.name}, não ofenda os demais usuários!"
            )
            await message.delete()
        #evitar que o bot trave e os outros comandos parem de funcionar


@client.command(name="channel", help="Makes the channel visible/invisible to the bot. Arguments:\n<option>: on/off")
async def activate_channel(ctx, id, option):
    global channels
    if option in ["on", "off"]:
        if id in channels:
            if option == "on":
                await ctx.send("Channel already online!")
            else:
                index = channels.index(id)
                channels.pop(index)
                await ctx.send("Channel is now offline!")
        else:
            if option == "on":
                channels.append(id)
                await ctx.send("Channel is now online!")
            else:
                await ctx.send("Channel already offline!")
    else:
        await ctx.send("Wrong argument. Possible arguments: on/off")


@client.command(name="close-channels", help="Close all channels activated")
async def clear_channels():
    global channels
    channels.clear()


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

@client.command(name="clear", help="Clear x number of messages in the current channel")
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingRequiredArgument): #se o erro for falta de argumentos
        await ctx.send("Favor enviar todos os Argumentos.")
    elif isinstance(error, CommandNotFound): #se o erro for comando inexistente
        await ctx.send("O comando não existe.")
    else:
        return
    ctx.send("Digite .help para ver os parâmetros de cada comando.")


client.run(TOKEN)