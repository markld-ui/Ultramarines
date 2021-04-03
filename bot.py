import discord
import config
import json
import os
import youtube_dl

from discord.ext import commands
from discord.utils import get
from discord import utils
from discord import FFmpegPCMAudio
from os import system


intents = discord.Intents.all()
intents.members = True


bot = commands.Bot(command_prefix = config.PREFIX, intents=intents)
bot.remove_command('help')


#Bot status
@bot.event
async def on_ready():
    print('Bot is ready!')

    await bot.change_presence( status = discord.Status.online )


@bot.event
async def on_message( message ):
    try:
        with open('E:\\Discord bot\\lvl.json', 'r') as file:
            users = json.load(file)
    except Exception:
        users = {}

    async def update_data(users, user):
        if not user in users:
            users[user] = {}
            users[user]['exp'] = 0
            users[user]['lvl'] = 1

        if users[user] == "792492149547466752":
            users[user]['exp'] = 0
            users[user]['lvl'] = 1

    async def add_exp(users, user, exp):
        users[user]['exp'] += exp


    async def add_lvl(users, user):
        exp = users[user]['exp']
        lvl = users[user]['lvl']
        if exp > lvl:
            await message.channel.send(f'{message.author.mention} повысил свой уровень до {lvl + 1}!')
            users[user]['exp'] = 0
            users[user]['lvl'] = lvl + 1


    await update_data(users, str(message.author.id))
    await add_exp(users, str(message.author.id), 0.1)
    await add_lvl(users, str(message.author.id))

    with open('E:\\Discord bot\\lvl.json', 'w') as file:
        users = json.dump( users, file, sort_keys=True, ensure_ascii=False, indent=4)

    await bot.process_commands ( message )


@bot.event
async def on_member_join(member):
    await member.send(f"Добро пожаловать {member.mention} в наш Discord канал, \n "
                      f"чтоб просмотреть доступные комманды напишите $help")


@bot.event
async def on_command_error(ctx, error):
    pass


'''Ассинхронная функция для выдачи роли или ролей пользователю по его ID и ID реакции'''
@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 793493541216190476:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == 'CS_GO':
            role = discord.utils.get(guild.roles, name='Штурмовик')
        elif payload.emoji.name == 'block':
            role = discord.utils.get(guild.roles, name='Шахтёр')
        elif payload.emoji.name == 'Among_Us':
            role = discord.utils.get(guild.roles, name='Космонавт')
        elif payload.emoji.name == 'Diablo':
            role = discord.utils.get(guild.roles, name='Демон')
        elif payload.emoji.name == 'GTA':
            role = discord.utils.get(guild.roles, name='Нига')
        elif payload.emoji.name == 'Fortnite':
            role = discord.utils.get(guild.roles, name='Павлин')
        elif payload.emoji.name == 'PUBG':
            role = discord.utils.get(guild.roles, name='Куриное крылышко')
        else:
            role = discord.utils.get(guild.roles, name= payload.emoji.name)

        if role is not None:
            member = payload.member
            if member is not None:
                await member.add_roles(role)
                print("done! Roles is added")
            else:
                print("Member not found")
        else:
            print("Role not found")

'''Ассинхронная функция для удаления role у member по их ID'''
@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 793493541216190476:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == 'CS_GO':
            role = discord.utils.get(guild.roles, name='Штурмовик')
        elif payload.emoji.name == 'block':
            role = discord.utils.get(guild.roles, name='Шахтёр')
        elif payload.emoji.name == 'Among_Us':
            role = discord.utils.get(guild.roles, name='Космонавт')
        elif payload.emoji.name == 'Diablo':
            role = discord.utils.get(guild.roles, name='Демон')
        elif payload.emoji.name == 'GTA':
            role = discord.utils.get(guild.roles, name='Нига')
        elif payload.emoji.name == 'Fortnite':
            role = discord.utils.get(guild.roles, name='Павлин')
        elif payload.emoji.name == 'PUBG':
            role = discord.utils.get(guild.roles, name='Куриное крылышко')
        else:
            role = discord.utils.get(guild.roles, name= payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print("done! Role is removed")
            else:
                print("Member not found")
        else:
            print("Role not found")


#help command
@bot.command(pass_context = True)
async def help(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)

    emb = discord.Embed( title = ' Доступные комманды для участников: ', colour = discord.Color.blue() )

    emb.add_field( name = '{}help'.format(config.PREFIX), value = ' Доступные  комманды участников. ' )
    emb.add_field( name = '{}echo'.format(config.PREFIX), value = ' Повторение сообщения за пользователем. ')
    emb.add_field( name = '{}_myroles'.format(config.PREFIX), value = ' Узнать список своих ролей ' )
    emb.add_field( name = '{}get_info'.format(config.PREFIX), value = ' Узнать информацию о себе на этом сервере '  )
    emb.add_field( name = '{}join'.format(config.PREFIX), value = ' Присоеденить бота к голосовому каналу ' )
    emb.add_field( name = '{}leave'.format(config.PREFIX), value = ' Убрать бота из голосового канала. ' )
    emb.add_field( name = '{}play'.format(config.PREFIX), value = ' Проигрывание музыки. Формат: $play url-видео с ютуб. ' )

    emb.add_field( name = '{}adminCommands'.format(config.PREFIX), value = ' Доступные комманды администраторов. ' )

    emb.set_author(name = bot.user.name, icon_url = bot.user.avatar_url)
    emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
    emb.set_thumbnail(url = 'https://pngimg.com/uploads/question_mark/question_mark_PNG54.png')

    await ctx.send(embed = emb)


#echo command
@bot.command(pass_context = True)
async def echo(ctx, arg):
    await ctx.send(arg)



@bot.command(aliases=['myroles'])
async def _myroles(ctx):
      member = ctx.message.author
      member_roles = member.roles
      await ctx.send(f"{member.mention} список твоих ролей:\n{member_roles}")



@bot.command(pass_context = True)
async def get_info(ctx,member:discord.Member = None, guild: discord.Guild = None):
    await ctx.message.delete()
    if member == None:
        emb = discord.Embed(title="Информация о пользователе", color=ctx.message.author.color)
        emb.add_field(name="Имя:", value=ctx.message.author.display_name,inline=False)
        emb.add_field(name="Айди пользователя:", value=ctx.message.author.id,inline=False)
        t = ctx.message.author.status
        if t == discord.Status.online:
            d = " В сети"

        t = ctx.message.author.status
        if t == discord.Status.offline:
            d = "⚪ Не в сети"

        t = ctx.message.author.status
        if t == discord.Status.idle:
            d = " Не активен"

        t = ctx.message.author.status
        if t == discord.Status.dnd:
            d = " Не беспокоить"

        emb.add_field(name="Активность:", value=d,inline=False)
        emb.add_field(name="Статус:", value=ctx.message.author.activity,inline=False)
        emb.add_field(name="Роль на сервере:", value=f"{ctx.message.author.top_role.mention}",inline=False)
        emb.add_field(name="Акаунт был создан:", value=ctx.message.author.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
        emb.set_thumbnail(url=ctx.message.author.avatar_url)
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(title="Информация о пользователе", color=member.color)
        emb.add_field(name="Имя:", value=member.display_name,inline=False)
        emb.add_field(name="Айди пользователя:", value=member.id,inline=False)
        t = member.status
        if t == discord.Status.online:
            d = " В сети"

        t = member.status
        if t == discord.Status.offline:
            d = "⚪ Не в сети"

        t = member.status
        if t == discord.Status.idle:
            d = " Не активен"

        t = member.status
        if t == discord.Status.dnd:
            d = " Не беспокоить"
        emb.add_field(name="Активность:", value=d,inline=False)
        emb.add_field(name="Статус:", value=member.activity,inline=False)
        emb.add_field(name="Роль на сервере:", value=f"{member.top_role.mention}",inline=False)
        emb.add_field(name="Акаунт был создан:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
        await ctx.send(embed = emb)


@bot.command(pass_context=True, brief="Makes the bot join your channel", aliases=['j', 'jo'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await voice.disconnect()
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send(f"Joined {channel}")


@bot.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl'])
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music end or use the 'stop' command")
        return
    await ctx.send("Getting everything ready, playing audio soon")
    print("Someone wants to play music let me get that ready for them...")
    voice = get(bot.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, 'song.mp3')
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    voice.volume = 100
    voice.is_playing()


@bot.command(pass_context=True, brief="Makes the bot leave your channel", aliases=['l', 'le', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Left {channel}")
    else:
        await ctx.send("Don't think I am in a voice channel")


#adminCommands
@bot.command(pass_context = True)
async def adminCommands(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)

    emb = discord.Embed( title = ' Комманды администрации: ', colour = discord.Color.red() )

    emb.add_field( name = '{}clear'.format(config.PREFIX), value = ' Очистка сообщений в чате' )
    emb.add_field( name = '{}mute'.format(config.PREFIX), value = ' Мут пользователя' )
    emb.add_field( name = '{}unmute'.format(config.PREFIX), value = ' Размут пользователя' )
    emb.add_field( name = '{}ban'.format(config.PREFIX), value = ' Бан пользователя' )

    emb.set_author(name = bot.user.name, icon_url = bot.user.avatar_url)
    emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
    emb.set_thumbnail(url = 'https://img1.freepng.ru/20180712/cir/kisspng-computer-icons-icon-design-business-administration-admin-icon-5b46fc466e6446.7801239015313787584522.jpg')

    await ctx.send(embed = emb)


# Ban
@bot.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def ban (ctx, member: discord.Member, *, reason = None, amount = 1):
    emb = discord.Embed (title = 'Ban :lock:', colour = discord.Color.dark_red())

    await ctx.channel.purge(limit = amount)

    await member.ban(reason = reason)

    emb.set_author (name = member.name, icon_url = member.avatar_url)
    emb.add_field (name = 'Ban user', value = 'Baned user : {}'.format(member.mention))
    emb.set_footer (text = 'Был заблокирован администратором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)

    await ctx.send (embed = emb)


#mute command
@bot.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def mute(ctx, member : discord.Member, amount = 1):
    await ctx.channel.purge(limit =  amount)

    emb = discord.Embed (title = 'Mute :mute:', colour = discord.Color.gold())
    mute_role = discord.utils.get(ctx.message.guild.roles, name = 'mute')
    await member.add_roles (mute_role)

    emb.set_author (name = member.name, icon_url = member.avatar_url)
    emb.add_field (name = 'mute', value = 'Muted user : {}'.format(member.mention))
    emb.set_footer (text = 'Был помещён в мут администратором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)
    await ctx.send (embed = emb)


@bot.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def unmute(ctx, member : discord.Member, amount = 1):
    await ctx.channel.purge(limit = amount)

    emb = discord.Embed (title = 'Unmute :loud_sound: ', colour = discord.Color.green())
    mute_role = discord.utils.get(ctx.message.guild.roles, name = 'mute')
    await member.remove_roles (mute_role)

    emb.set_author (name = member.name, icon_url = member.avatar_url)
    emb.add_field (name = 'unmute', value = 'Unmuted user : {}'.format(member.mention))
    emb.set_footer (text = 'Был размутчен администратором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)
    await ctx.send (embed = emb)


#message clearing
@bot.command (pass_context = True)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit = amount)

#work with error in function
@ban.error
async def ban_error ( ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send( f'{ctx.author.name}, укажите аргумент!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.name}, у вас недостаточно прав для испльзования этой команды!')


#work with error in function
@clear.error
async def clear_error ( ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send( f'{ctx.author.name}, укажите аргумент!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.name}, у вас недостаточно прав для испльзования этой команды!')


#work with error in function
@echo.error
async def echo_error ( ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send( f'{ctx.author.name}, укажите аргумент!')


bot.run(config.TOKEN)