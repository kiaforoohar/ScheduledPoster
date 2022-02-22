import praw
import prawcore.exceptions as pe
from datetime import date
import time
import os.path
import sys
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkm

import schedule


# calculates the number of seconds the application has to wait until the targeted time


def quitIt(m):
        m.destroy()
        sys.exit(0)

# creates the input window for getting the reddit account information
def init_input():

    # gets the information from the entries and writes them in info.txt
    def get_info():

        #checks if the entries are not empty
        if e1.get() == "":
            tkm.showinfo("Warning", "Please write your Client ID")
            return
        if e2.get() == "":
            tkm.showinfo("Warning", "Please write your Client Secret")
            return
        if e3.get() == "":
            tkm.showinfo("Warning", "Please write your Username")
            return
        if e4.get() == "":
            tkm.showinfo("Warning", "Please write your Password")
            return
        if e5.get() == "":
            tkm.showinfo("Warning", "Please write your User Agent")
            return

        # writes the information into info.txt
        info = open('info.txt', 'w')
        info.write(e1.get() + "\n")
        info.write(e2.get() + "\n")
        info.write(e3.get() + "\n")
        info.write(e4.get() + "\n")
        info.write(e5.get() + "\n")
        info.close()

        # closes the window
        master.destroy()

    # creates the user interface for the window
    master = tk.Tk()
    master.title("Please enter your Reddit Information")
    master.geometry("300x135")
    master.resizable(False, False)
    tk.Label(master, text="Client ID:").grid(row=1)
    tk.Label(master, text="Client Secret:").grid(row=3)
    tk.Label(master, text="Username:").grid(row=5)
    tk.Label(master, text="Password:").grid(row=7)
    tk.Label(master, text="User Agent:").grid(row=9)
    e1 = tk.Entry(master, width = 36)
    e2 = tk.Entry(master, width = 36)
    e3 = tk.Entry(master, width = 36)
    e4 = tk.Entry(master, width = 36)
    e5 = tk.Entry(master, width = 36)
    b1 = tk.Button(master, text = "Enter", command = get_info)
    b2 = tk.Button(master, text = "Quit", command = lambda: quitIt(master))
    e1.grid(row=1, column=1)
    e2.grid(row=3, column=1)
    e3.grid(row=5, column=1)
    e4.grid(row=7, column=1)
    e5.grid(row=9, column=1)
    b1.grid(row=11, column=1)
    b2.grid(row=11, column=0)
    b1.focus_set()
    master.mainloop()

# creates the input window for getting the targeted subreddit 
def subreddit_input():

    # gets the targeted subreddit, checks if the input is correct, and proceeds to post input window
    def get_subreddit():

        # checks if the entry is not empty
        if e1.get() == "":
            tkm.showinfo("Warning", "Please write a subreddit name")
            return

        # brings up the user reddit account information
        info = open('info.txt', 'r')
        reddit = praw.Reddit(
                client_id=info.readline().strip(),
                client_secret=info.readline().strip(),
                username=info.readline().strip(),
                password=info.readline().strip(),
                user_agent =info.readline().strip())
        reddit.validate_on_submit = True
        info.close()

        # gets the subreddit from the entry
        sr = e1.get()
        url = '/r/'+sr+'/api/link_flair_v2'

        # gets the flairs for the subreddit
        flairs = []
        try:
            for flair in reddit.get(url):
                flairs.append(flair.get('text'))

        # Warns the user if they entered the wrong subreddit
        except pe.Redirect:
            tkm.showinfo("Warning", "The subreddit name was invalid. Please try again")
            return

        # In case there is no flair for the subreddit
        except pe.Forbidden:
            flairs = []

        
        subreddit = reddit.subreddit(sr)
        master.destroy()

        # Opens the post input window
        post_input(reddit, subreddit, flairs)

    # creates the user interface
    master = tk.Tk()
    master.title("Enter Subrredit name:")
    master.geometry("430x50")
    master.resizable(False, False)
    tk.Label(master, text="Enter Subreddit name:").grid(row=1)
    e1 = tk.Entry(master, width = 30)
    b1 = tk.Button(master, text = "Enter", command = get_subreddit)
    b2 = tk.Button(master, text = "Quit", command = lambda: quitIt(master))
    b3 = tk.Button(master, text = "Change Reddit Info", command = init_input)
    e1.grid(row=1, column=1)
    b2.grid(row=5, column=0)
    b1.grid(row=5, column=1)
    b3.grid(row=5, column=2)
    b1.focus_set()
    master.mainloop()

# Creates the window for inputting post information
def post_input(reddit, subreddit, flairs):

    # Gets the flair id based on the selected flair text
    def get_flair():

        # returns none if the subreddit has no flair
        if select.get() == "":
            return None

        # Loops through all the flairs to find the one that matches the selected flair in the option window
        else:
            for flair in reddit.get('/r/silenthill/api/link_flair_v2'):

                # when the matching flair is found, the flair id is returned
                if flair.get('text').lower() == select.get():
                    return flair['id']

    
    def get_post():

        #checks if the entries are not empty
        if e1.get() == "":
            tkm.showinfo("Warning", "Please write your Title")
            return
        if e2.get() == "":
            tkm.showinfo("Warning", "Please write your Link")
            return

        # gets the time from spinbox 
        time = s1.get()+':'+s2.get()

        # causes the application to wait until the selected time arrives
        schedule.timer(time)

        # creates or appends to results.txt for writing the result of the operation
        results = open('results.txt', 'a')
        try:

            # posts the link to subreddit
            subreddit.submit(e1.get(),
                     selftext = None,
                     url = e2.get(),
                     flair_id = get_flair(),
                     flair_text = None,
                     resubmit = True,
                     send_replies = True,
                     nsfw = False,
                     spoiler = False,
                     collection_id = None,
                     discussion_type = None,
                     inline_media = None)

        # in case an error occurs, writes the outcome in results.txt with time, date, and the exception
        except Exception as inst:
            results.write("{} {} Faliure {}\n".format(date.today(), time.strftime("%H-%M-%S", time.localtime()), inst))

        # in case of success, writes the outcome in results.txt with time, date, and the title of the post
        else:
            results.write("{} {} Success!!! {}\n".format(date.today(), time.strftime("%H-%M-%S", time.localtime()), e1.get()))
        finally:
            # closes the result.txt
            results.close()
        # end of this window
        quitIt(master)

    # creates the user interface for the window 
    master = tk.Tk()
    master.title("Please enter your Post Information")
    master.geometry("490x125")
    master.resizable(False, False)
    tk.Label(master, text="Title:").grid(row=1)
    tk.Label(master, text="Link:").grid(row=3)
    tk.Label(master, text="Time:").grid(row=5)
    tk.Label(master, text="Flaire ID:").grid(row=7)
    
    e1 = tk.Entry(master, width = 50)
    e2 = tk.Entry(master, width = 50)
    ct = time.localtime()

    # displays the current time on the spinboxes
    ct_hour = int(time.strftime("%H", ct))
    ct_minute = int(time.strftime("%M", ct))
    current_value = tk.StringVar(value=ct_hour)
    s1 = ttk.Spinbox(
        master,
        from_=0,
        to=23,
        textvariable=current_value,
        width = 5,
        wrap=True)
    current_value1 = tk.StringVar(value=ct_minute)
    s2 = ttk.Spinbox(
        master,
        from_=0,
        to=59,
        textvariable=current_value1,
        width = 5,
        wrap=True)

    # in case there are no flairs for the targeted subreddit, displays empty on the option menu
    if len(flairs) == 0:
        flairs = [""]
    select = tk.StringVar()

    # selcts the first item in the list of flairs
    select.set(flairs[0])
    
    drop = tk.OptionMenu( master , select , *flairs )
    
        
    b1 = tk.Button(master, text = "Enter", command = get_post)
    b2 = tk.Button(master, text = "Quit", command = lambda: quitIt(master))
    b3 = tk.Button(master, text = "Change Previous Info", command = subreddit_input)
    
    e1.grid(row=1, column=1)
    e2.grid(row=3, column=1)
    s1.grid(row=5, column=1)
    s2.grid(row=5, column=2)
    drop.grid(row=7, column = 1)
    
    b1.grid(row=11, column=1)
    b2.grid(row=11, column=0)
    b3.grid(row=11, column=2)
    b1.focus_set()
    master.mainloop()
