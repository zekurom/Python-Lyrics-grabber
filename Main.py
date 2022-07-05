
# import modules
import os as os
os.system('pip install lyrics_extractor')
os.system('pip install pytube')
os.system('pip install YT-DLP')
os.system('pip3 install youtube-search-python')
from tkinter import *
from lyrics_extractor import SongLyrics
from pytube import YouTube
from youtubesearchpython import VideosSearch

def get_song():

	extract_lyrics = SongLyrics(
		"AIzaSyA_QxVG1pBOe1207n-0iRltY8p3LLUy6Pc", "2749d8edd42850fb4")
	
	temp = extract_lyrics.get_lyrics(str(e.get()))
	res = temp['lyrics']
	#result.set(res)
	lb.config(state=NORMAL)
	lb.delete(1.0,"end")
	lb.insert(1.0,res)
	lb.tag_add("tag_lol", "1.0", "end")
	lb.config(state=DISABLED)


def get_video():
	VideosSearch = VideosSearch(str(e.get()), limit = 1)

master = Tk()
master.configure(bg='light grey')
master.geometry("1250x750")


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

b.grid(row=0, column=2, columnspan=2,
	rowspan=2, padx=5, pady=5,)
lb.grid(row=3, column=1, sticky=W)
lb.tag_configure("tag_lol", justify='center')
lb.config(state=DISABLED)

mainloop()
