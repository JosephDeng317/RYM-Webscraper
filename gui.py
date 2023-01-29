import tkinter as tk
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk
from urllib.request import urlopen
import rym


master = tk.Tk()
master.title("Start-Up Screen")
master.geometry("1000x1000")
master.resizable(False, False)
master.withdraw

canvas=Canvas(master)
canvas.pack()

f_name = tk.StringVar()

artist="" 


def display_results(singles, albums):
    new_canvas=Canvas(master)
    new_canvas.pack()
    artist_name=tk.Label(new_canvas,text=artist)
    artist_name.grid(row=0,column=1)

    top_three_album=tk.Label(new_canvas,text="Top Three Albums")
    top_three_album.grid(row=1,column=0)
    top_three_songs=tk.Label(new_canvas,text="Top Three Songs")
    top_three_songs.grid(row=1,column=2)

    if len(albums) > 0:
        imageURL1=albums[0].image
        u1=urlopen(imageURL1)
        raw_data1=u1.read()
        u1.close()
        photo1= ImageTk.PhotoImage(data=raw_data1)
        label1=tk.Label(new_canvas,image=photo1)
        label1.image = photo1
        label1.grid(row=2,column=0)

        album_1_name= "1. " + albums[0].name + ", " + str(albums[0].rating) + " Stars"
        label1_1=tk.Label(new_canvas,text=album_1_name)
        label1_1.grid(row=3,column=0)

    if len(albums) > 1:
        imageURL2=albums[1].image
        u2=urlopen(imageURL2)
        raw_data2=u2.read()
        u2.close()
        photo2= ImageTk.PhotoImage(data=raw_data2)
        label2=tk.Label(new_canvas,image=photo2)
        label2.image = photo2
        label2.grid(row=4,column=0)

        album_2_name="2. " + albums[1].name + ", " + str(albums[1].rating) + " Stars"
        label2_2=tk.Label(new_canvas,text=album_2_name)
        label2_2.grid(row=5,column=0)

    if len(albums) > 2:
        imageURL3=albums[2].image
        u3=urlopen(imageURL3)
        raw_data3=u3.read()
        u3.close()
        photo3= ImageTk.PhotoImage(data=raw_data3)
        label3=tk.Label(new_canvas,image=photo3)
        label3.image = photo3
        label3.grid(row=6,column=0)

        album_3_name="3. " + albums[2].name + ", " + str(albums[2].rating) + " Stars"
        label3_3=tk.Label(new_canvas,text=album_3_name)
        label3_3.grid(row=7,column=0)


    if len(singles) > 0:
        imageURL4=singles[0].image
        u4=urlopen(imageURL4)
        raw_data4=u4.read()
        u4.close()
        photo4= ImageTk.PhotoImage(data=raw_data4)
        label4=tk.Label(new_canvas,image=photo4)
        label4.image = photo4
        label4.grid(row=2,column=2)

        song_1="1. " + singles[0].name + ", " + str(singles[0].rating) + " Stars"
        label4=tk.Label(new_canvas,text=song_1)
        label4.grid(row=3,column=2)

    if len(singles) > 1:
        imageURL5=singles[1].image
        u5=urlopen(imageURL5)
        raw_data5=u5.read()
        u5.close()
        photo5= ImageTk.PhotoImage(data=raw_data5)
        label5=tk.Label(new_canvas,image=photo5)
        label5.image = photo5
        label5.grid(row=4,column=2)

        song_2="2. " + singles[1].name + ", " + str(singles[1].rating) + " Stars"
        label5=tk.Label(new_canvas,text=song_2)
        label5.grid(row=5,column=2)

    if len(singles) > 2:
        imageURL6=singles[2].image
        u6=urlopen(imageURL6)
        raw_data6=u6.read()
        u6.close()
        photo6= ImageTk.PhotoImage(data=raw_data6)
        label6=tk.Label(new_canvas,image=photo6)
        label6.image = photo6
        label6.grid(row=6,column=2)

        song_3="3. " + singles[2].name + ", " + str(singles[2].rating) + " Stars"
        label6=tk.Label(new_canvas,text=song_3)
        label6.grid(row=7,column=2)


def username():
    global artist
    artist = f_name.get()
    if artist != "":
        rym.search_for_artist(str(artist))
        recs = rym.get_recommendations()
        top_picks = rym.get_top_recs(3, recs)
        singles = top_picks['Singles']
        albums = top_picks['Albums']
        canvas.destroy()
        display_results(singles, albums)

        return
    else:
        messagebox.showinfo(
                "Value Error!",
                "You have inputted nothing to be the artist name, please enter an actual name",
            )
  
def get_info(f_name):
    global artist
    f_name_entry = tk.Entry(canvas, textvariable=f_name, font=("calibre", 9, "normal"))
    f_name_entry.grid(row=0, column=1)


    player_name = tk.Button(
            canvas,
            text="Name:   ",
            font=("calibre", 8, "bold"),
            bg="white",
            command=lambda: username(),
        )
    player_name.grid(row=0,column=0)

get_info(f_name)
master.mainloop()

print((artist))


