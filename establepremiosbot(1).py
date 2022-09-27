import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
import pymongo
from pymongo import MongoClient
import random
import logging




# ? sdsad
#TODO:
#? ********************************************************************************************************************************************************************

#? ********************************************************************************************************************************************************************
bot = discord.Client()
bot = commands.Bot(command_prefix="a!")
bot.remove_command('help')
#? ********************************************************************************************************************************************************************
@bot.event
async def on_ready():
    cantidadservidores=0
    for serv in bot.guilds:
        cantidadservidores=cantidadservidores+1
        try:
            print(serv)
        except:
            pass
    estado="Support:  https://discord.gg/QcFC7RK"
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(estado))
    print('Conectado como: {0.user}'.format(bot))
    cambiarestatus.start()

#? ********************************************************************************************************************************************************************
@tasks.loop(seconds=30)
async def cambiarestatus():
    statuses=["|| a!help ||","|| Support:  https://discord.gg/QcFC7RK ||",f"|| On {len(bot.guilds)} servers ||","|| a!ayuda ||"]
    status=random.choice(statuses)
    await bot.change_presence(activity=discord.Game(name=status))
#? ********************************************************************************************************************************************************************
@bot.event
async def on_guild_join(guild):
    cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
    db = cluster["awardsbot"]
    collection=db["prefijos"]
    prefijo="a!"
    guildid=guild.id
    usuario=guild.member_count
    dueño=guild.owner_id
    collection.delete_one({"guild_id":guildid})
    post= {"guild_id":guildid,"prefix":prefijo,"usuarios":usuario,"dueño":dueño}
    collection.insert_one(post)
#? ********************************************************************************************************************************************************************
@bot.event
async def on_guild_remove(guild):
    cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
    db = cluster["awardsbot"]
    collection=db["prefijos"]
    guildid=guild.id
    collection.delete_many({"guild_id":guildid})


    cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
    db = cluster["awardsbot"]
    collection=db["entradas"]
    guildid=guild.id
    collection.delete_many({"guild_id":guildid})
#? ********************************************************************************************************************************************************************
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, discord.Forbidden):
        await ctx.send('**Missing Permissions/Sin Permisos**')
    if isinstance(error, commands.BadArgument):
        await ctx.send('**No mention? no text?/No pusiste mencion? no pusiste texto?**')
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('**|Comando no encontrado/Not Found| Try a!help or a!ayuda**')
#! *********************************************************************************************************************************************************************
@bot.command(aliases=['awardsprefix'])
async def premiosprefijo(ctx,prefijo="/"):
    cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
    db = cluster["awardsbot"]
    collection=db["prefijos"]
    guildid=ctx.guild.id
    collection.delete_one({"guild_id":guildid})
    post= {"guild_id":guildid,"prefix":prefijo}
    collection.insert_one(post)
    await ctx.send(f"**NEW Prefijo/Nuevo Prefijo : {prefijo}**")
#! *********************************************************************************************************************************************************************
@bot.command()
async def mensajeatodos(ctx,*,texto='NO DATA ENTERED'):
    # GUARDA CON ESTE COMANDOOOO
    if ctx.author.id==329450671319285763:
        resultados=[]
        cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
        db = cluster["awardsbot"]
        collection=db["prefijos"]
        guildid=ctx.guild.id
        results=collection.find({})
        for result in results:
            resultados.append(result["dueño"])
        repetidos=[]
        for resultado in resultados:
            if resultado in repetidos:
                pass
            else:
                try:
                    user=await bot.fetch_user(resultado)
                    await user.send(texto)
                    repetidos.append(resultado)
                    await ctx.send(f"Mensaje enviado a {user.id}")
                except:
                    pass
    else:
        print("Bad permission")

    
#! *********************************************************************************************************************************************************************
@bot.command(aliases=['aaaaaaaaaaa'])
async def hacerr(ctx,prefijo="/"):
    cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
    db = cluster["awardsbot"]
    collection=db["prefijos"]
    guildid=ctx.guild.id
    collection.delete_one({"guild_id":guildid})
    post= {"guild_id":guildid,"prefix":prefijo}
    collection.insert_one(post)
    await ctx.send(f"**NEW Prefijo/Nuevo Prefijo : {prefijo}**")

#! *********************************************************************************************************************************************************************
@bot.command()
async def ken(ctx):
    if ctx.author.id==329450671319285763:
        await ctx.send(f"**{ctx.author.mention} IS BOT OWNER :3**")
#! *********************************************************************************************************************************************************************
@bot.command()
async def allpremios(ctx):
    cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
    db = cluster["awardsbot"]
    collection=db["entradas"]
    guildid=ctx.guild.id
    results = collection.find({"guild_id":guildid})
    lista=[]
    nombre=ctx.guild.name
    i=0
    for result in results:
        lista.append(result["premio_usuario"])
    #TODO -EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!-
    embed= discord.Embed(
        title='Premios del Servidor',
        colour=discord.Colour.from_rgb(255,0,130)
    )
    if len(lista)==0:
        embed.add_field(name='Premio',value='No hay premios todavia')
        
    else:
        for i in range(len(lista)):
            premio=lista[i]
            embed.add_field(name=' ˞˞',value=premio, inline=False)
    embed.set_author(name="Awardsbot",url="https://top.gg/bot/767061271131455488",icon_url="https://cdn.discordapp.com/attachments/753056988618948748/772542364161409034/trofeo.jpg")
    embed.set_footer(text=nombre, icon_url="https://discordapp.com/channels/@me/753056988618948748/767873755380187177")
    await ctx.send(embed=embed)
#! *********************************************************************************************************************************************************************
@bot.command()
async def allawards(ctx):
    cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
    db = cluster["awardsbot"]
    collection=db["entradas"]
    guildid=ctx.guild.id
    results = collection.find({"guild_id":guildid})
    lista=[]
    nombre=ctx.guild.name
    i=0
    for result in results:
        lista.append(result["premio_usuario"])
    #TODO -EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!-
    embed= discord.Embed(
        title='Server Awards',
        colour=discord.Colour.from_rgb(255,0,130)
    )
    if len(lista)==0:
        embed.add_field(name='Award',value='None yet')
        
    else:
        for i in range(len(lista)):
            premio=lista[i]
            embed.add_field(name=' ˞˞',value=premio, inline=False)
    embed.set_author(name="Awardsbot",url="https://top.gg/bot/767061271131455488",icon_url="https://cdn.discordapp.com/attachments/753056988618948748/772542364161409034/trofeo.jpg")
    embed.set_footer(text=nombre, icon_url="https://discordapp.com/channels/@me/753056988618948748/767873755380187177")
    await ctx.send(embed=embed)
#! *********************************************************************************************************************************************************************
@bot.command()
async def darpremio(ctx,member:discord.Member,*,texto='NO DATA ENTERED'):
    if texto=='NO DATA ENTERED':
        await ctx.send("**Premio??**")
    elif texto!='NO DATA ENTERED':
        if ctx.author.guild_permissions.administrator==True:
            cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
            db = cluster["awardsbot"]
            collection=db["entradas"]
            guildid=ctx.guild.id
            post= {"guild_id":guildid,"id_usuario":member.id,"premio_usuario":texto}
            collection.insert_one(post)
            #TODO -EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!-
            embed= discord.Embed(
                colour=discord.Colour.from_rgb(255,0,130)
                )
            embed.set_author(name="Awardsbot",url="https://top.gg/bot/767061271131455488",icon_url="https://cdn.discordapp.com/attachments/753056988618948748/772542364161409034/trofeo.jpg")
            embed.add_field(name="**Nuevo Premio del Usuario:**",value=member.mention,inline=True)
            embed.add_field(name="**PREMIO:**",value=texto,inline=False)
            await ctx.send(embed=embed)
        else:
            cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
            db = cluster["awardsbot"]
            collection=db["roles"]
            guildid=ctx.guild.id
            result= collection.find_one({"guild_id":guildid})
            rolpremio=result["id_role"]
            for role in ctx.author.roles:
                if role.id==rolpremio:
                    cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
                    db = cluster["awardsbot"]
                    collection=db["entradas"]
                    guildid=ctx.guild.id
                    post= {"guild_id":guildid,"id_usuario":member.id,"premio_usuario":texto}
                    collection.insert_one(post)
                    #TODO -EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!-
                    embed= discord.Embed(
                        colour=discord.Colour.from_rgb(255,0,130)
                    )
                    embed.set_author(name="Awardsbot",url="https://top.gg/bot/767061271131455488",icon_url="https://cdn.discordapp.com/attachments/753056988618948748/772542364161409034/trofeo.jpg")
                    embed.add_field(name="**Nuevo Premio del Usuario:**",value=member.mention,inline=True)
                    embed.add_field(name="**PREMIO:**",value=texto,inline=False)
                    await ctx.send(embed=embed)
    else:
        print("ERROR EN DAR PREMIO")
#! *********************************************************************************************************************************************************************
@bot.command()
async def addaward(ctx,member:discord.Member,*,texto='NO DATA ENTERED'):
    if texto=='NO DATA ENTERED':
        await ctx.send("**Award??**")
    elif texto!='NO DATA ENTERED':
        if ctx.author.guild_permissions.administrator==True:
            cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
            db = cluster["awardsbot"]
            collection=db["entradas"]
            guildid=ctx.guild.id
            post= {"guild_id":guildid,"id_usuario":member.id,"premio_usuario":texto}
            collection.insert_one(post)

            #TODO -EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!-
            embed= discord.Embed(
                colour=discord.Colour.from_rgb(255,0,130)
                )
            embed.set_author(name="Awardsbot",url="https://top.gg/bot/767061271131455488",icon_url="https://cdn.discordapp.com/attachments/753056988618948748/772542364161409034/trofeo.jpg")
            embed.add_field(name="**User New Award:**",value=member.mention,inline=True)
            embed.add_field(name="**AWARD:**",value=texto,inline=False)
            await ctx.send(embed=embed)
        else:
            cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
            db = cluster["awardsbot"]
            collection=db["roles"]
            guildid=ctx.guild.id
            result= collection.find_one({"guild_id":guildid})
            rolpremio=result["id_role"]
            for role in ctx.author.roles:
                if role.id==rolpremio:
                    cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
                    db = cluster["awardsbot"]
                    collection=db["entradas"]
                    guildid=ctx.guild.id
                    post= {"guild_id":guildid,"id_usuario":member.id,"premio_usuario":texto}
                    collection.insert_one(post)
                    #TODO -EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!-
                    embed= discord.Embed(
                        colour=discord.Colour.from_rgb(255,0,130)
                    )
                    embed.set_author(name="Awardsbot",url="https://top.gg/bot/767061271131455488",icon_url="https://cdn.discordapp.com/attachments/753056988618948748/772542364161409034/trofeo.jpg")
                    embed.add_field(name="**User New Award:**",value=member.mention,inline=True)
                    embed.add_field(name="**AWARD:**",value=texto,inline=False)
                    await ctx.send(embed=embed)
    else:
        print("ERROR EN DAR PREMIO")

#! *********************************************************************************************************************************************************************
@bot.command()
async def awards(ctx,member:discord.Member):
    cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
    db = cluster["awardsbot"]
    collection=db["entradas"]
    guildid=ctx.guild.id
    results = collection.find({"guild_id":guildid,"id_usuario":member.id})
    lista=[]
    for result in results:
        lista.append(result["premio_usuario"])
    #TODO -EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!-
    embed= discord.Embed(
        title='User Awards',
        colour=discord.Colour.from_rgb(255,0,130)
    )
    elmiembro=member.name
    embed.set_author(name=elmiembro)
    nombre=ctx.guild.name
    if len(lista)==0:
        embed.add_field(name='Awards',value='None yet')
        
    else:
        for i in range(len(lista)):
            premio=lista[i]
            embed.add_field(name=' ˞˞',value=premio, inline=False)
    embed.set_author(name="Awardsbot",url="https://top.gg/bot/767061271131455488",icon_url="https://cdn.discordapp.com/attachments/753056988618948748/772542364161409034/trofeo.jpg")
    embed.set_footer(text=nombre, icon_url="https://discordapp.com/channels/@me/753056988618948748/767873755380187177")
    await ctx.send(embed=embed)
#! *********************************************************************************************************************************************************************
@bot.command()
async def premios(ctx,member:discord.Member):
    cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
    db = cluster["awardsbot"]
    collection=db["entradas"]
    guildid=ctx.guild.id
    results = collection.find({"guild_id":guildid,"id_usuario":member.id})
    lista=[]
    for result in results:
        lista.append(result["premio_usuario"])
    #TODO -EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!-
    embed= discord.Embed(
        title='Premios del Usuario',
        colour=discord.Colour.from_rgb(255,0,130)
    )
    elmiembro=member.name
    embed.set_author(name=elmiembro)
    nombre=ctx.guild.name
    if len(lista)==0:
        embed.add_field(name='Premios',value='No tiene premios aun')
        
    else:
        for i in range(len(lista)):
            premio=lista[i]
            embed.add_field(name=' ˞˞',value=premio, inline=False)
    embed.set_author(name="Awardsbot",url="https://top.gg/bot/767061271131455488",icon_url="https://cdn.discordapp.com/attachments/753056988618948748/772542364161409034/trofeo.jpg")
    embed.set_footer(text=nombre, icon_url="https://discordapp.com/channels/@me/753056988618948748/767873755380187177")
    await ctx.send(embed=embed)
#! *********************************************************************************************************************************************************************
@bot.command(aliases=['awardsrole'])
@commands.has_permissions(administrator=True)
async def premiosrol(ctx,role:discord.Role):
    if role==None:
        pass
    else:
        cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
        db = cluster["awardsbot"]
        collection=db["roles"]
        guildid=ctx.guild.id
        collection.delete_many({"guild_id":guildid})
        post= {"guild_id":guildid,"id_role":role.id}
        collection.insert_one(post)
        await ctx.send(f"**Role:{role.mention}**")
#! *********************************************************************************************************************************************************************
@bot.command(aliases=['deleteawards'])
@commands.has_permissions(administrator=True)
async def eliminarpremios(ctx,member:discord.Member):
    cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
    db = cluster["awardsbot"]
    collection=db["entradas"]
    guildid=ctx.guild.id
    collection.delete_many({"guild_id":guildid,"id_usuario":member.id})
#! *********************************************************************************************************************************************************************
@bot.command(aliases=['invitar'])
async def invite(ctx):
    embed= discord.Embed(
        colour=discord.Colour.blue(),
        title='Invita al BOT!/Invite The Bot!'
    )
    embed.set_author(name="Awardsbot",url="https://top.gg/bot/767061271131455488",icon_url="https://cdn.discordapp.com/attachments/753056988618948748/772542364161409034/trofeo.jpg")
    embed.add_field(name='LINK:', value='https://discord.com/oauth2/authorize?client_id=767061271131455488&permissions=654336&scope=bot')
    await ctx.send(embed=embed)

#! *********************************************************************************************************************************************************************
@bot.command()
async def help(ctx):
    #TODO -EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!-
    embed= discord.Embed(
        title='BASIC COMMANDS',
        colour=discord.Colour.from_rgb(255,0,130)
    )
    embed.add_field(name='a!addaward @USERMENTION AWARD ',value='Gives a award to a user, YOU CAN USE EMOJIS!',inline=True)
    embed.add_field(name='a!awards @USERMENTION  ',value='Embed to show member awards',inline=False)
    embed.add_field(name='a!allawards',value='Shows server awards',inline=False)
    embed.add_field(name='a!awardsrole @ROLEMENTION',value='Specify a role for giving awards, ONLY ADMIN CMD',inline=False)
    embed.add_field(name='FOR ALL COMMANDS ',value='``` a!help2 ```',inline=False)
    embed.add_field(name='🇪🇸',value='``` a!ayuda ```',inline=False)
    embed.set_author(name="Awardsbot",url="https://discord.gg/QcFC7RK",icon_url="https://cdn.discordapp.com/attachments/753056988618948748/772542364161409034/trofeo.jpg")
    await ctx.send(embed=embed)
#! *********************************************************************************************************************************************************************
@bot.command()
async def help2(ctx):
    #TODO -EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!-
    embed= discord.Embed(
        title='COMMANDS',
        colour=discord.Colour.from_rgb(255,0,130)
    )
    embed.add_field(name='a!addaward @USERMENTION AWARD ',value='Gives a award to a user, YOU CAN USE EMOJIS!',inline=True)
    embed.add_field(name='a!awards @USERMENTION  ',value='Embed to show member awards',inline=False)
    embed.add_field(name='a!allawards',value='Shows server awards',inline=False)
    embed.add_field(name='a!awardsrole @ROLEMENTION',value='Specify a role for giving awards, ONLY ADMIN CMD',inline=False)
    #embed.add_field(name='a!awardsprefix (PREFIXSYMBOL)  ',value='Changes bot prefix, recommended: / . * default ONLY ADMIN CMD',inline=False)
    embed.add_field(name='a!deleteawards @USERMENTION',value='DANGER, DELETES ALL AWARDS FROM A USER ONLY ADMIN CMD',inline=False)
    embed.add_field(name='a!invite',value='Bot invite link',inline=False)
    embed.add_field(name='VOTE THE BOT!',value='https://top.gg/bot/767061271131455488',inline=False)
    embed.set_author(name="Awardsbot",url="https://discord.gg/QcFC7RK",icon_url="https://cdn.discordapp.com/attachments/753056988618948748/772542364161409034/trofeo.jpg")
    await ctx.send(embed=embed)
#! *********************************************************************************************************************************************************************
@bot.command()
async def ayuda(ctx):
    #TODO -EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!-
    embed= discord.Embed(
        title='COMANDOS',
        colour=discord.Colour.from_rgb(255,0,130)
    )
    embed.add_field(name='a!darpremio @MENCIONUSUARIO PREMIO) ',value='Da un premio a un usuario, PODES USAR EMOJIS!',inline=True)
    embed.add_field(name='a!premios @MENCIONUSUARIO  ',value='Tabla que muestra los premios de un usuario',inline=False)
    embed.add_field(name='a!allpremios',value='Muestra los premios del server',inline=False)
    embed.add_field(name='a!premiosrol @ROLMENCION',value='Especifica un rol para dar premios, COMANDO ADM',inline=False)
    embed.add_field(name='PARA TODOS LOS COMANDOS',value='``` a!ayuda2 ```',inline=False)
    embed.add_field(name='🇬🇧',value='``` a!help ```',inline=False)
    embed.set_author(name="Awardsbot",url="https://discord.gg/QcFC7RK",icon_url="https://cdn.discordapp.com/attachments/753056988618948748/772542364161409034/trofeo.jpg")
    await ctx.send(embed=embed)
#! *********************************************************************************************************************************************************************
@bot.command()
async def ayuda2(ctx):
    #TODO -EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!--EMBED!-
    embed= discord.Embed(
        title='COMANDOS',
        colour=discord.Colour.from_rgb(255,0,130)
    )
    embed.add_field(name='a!darpremio @MENCIONUSUARIO PREMIO) ',value='Da un premio a un usuario, PODES USAR EMOJIS!',inline=True)
    embed.add_field(name='a!premios @MENCIONUSUARIO  ',value='Tabla que muestra los premios de un usuario',inline=False)
    embed.add_field(name='a!allpremios',value='Muestra los premios del server',inline=False)
    embed.add_field(name='a!premiosrol @ROLMENCION',value='Especifica un rol para dar premios, COMANDO ADM',inline=False)
    #embed.add_field(name='a!premiosprefijo (SIMBOLODEPREFIJO)  ',value='Cambia el prefijo del bot, recomendados: / . * el normal, COMANDO ADM',inline=False)
    embed.add_field(name='a!eliminarpremios @MENCIONUSUARIO',value='PELIGRO, ELIMINA TODOS LOS PREMIOS DE UN USUARIO, COMANDO ADM',inline=False)
    embed.add_field(name='a!invitar',value='Genera un link para invitar al bot!',inline=False)
    embed.add_field(name='VOTA EL BOT!',value='https://top.gg/bot/767061271131455488',inline=False)
    embed.set_author(name="Awardsbot",url="https://discord.gg/QcFC7RK",icon_url="https://cdn.discordapp.com/attachments/753056988618948748/772542364161409034/trofeo.jpg")
    await ctx.send(embed=embed)
#! *********************************************************************************************************************************************************************
bot.run('NzY3MDYxMjcxMTMxNDU1NDg4.X4sbeg.qYgYAFP5j2hsPdPfv6qxeDoe5L0')
#! *********************************************************************************************************************************************************************