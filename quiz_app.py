from tkinter import *
import time
from tkinter import messagebox


def startCountdown():
    time_settings_button['state'] = 'disabled'
    word_settings_button['state'] = 'disabled'
    global counting
    counting = True
    remaining_time = 3600 * int(hours.get()) + 60 * int(minutes.get()) + int(seconds.get())
    while remaining_time >= 0 and counting:
        remaining_hours, remaining_minutes = divmod(remaining_time, 3600)
        remaining_minutes, remaining_seconds = divmod(remaining_minutes, 60)
        hours.set("{:0>2d}".format(remaining_hours))
        minutes.set("{:0>2d}".format(remaining_minutes))
        seconds.set("{:0>2d}".format(remaining_seconds))
        master.update()
        time.sleep(1)
        if remaining_time == 0:
            messagebox.showinfo("Time Countdown", "Time's up ")
        remaining_time -= 1
    return


def stopCountdown():
    global counting
    counting = False
    time_settings_button['state'] = 'active'
    word_settings_button['state'] = 'active'


def readSettingsFromFile():
    with open("settings.txt", "r") as file:
        data = file.readlines()
    i = 0
    for line in data:
        value = line.split(' ')[-1].split('\n')[0]
        settings[i].set(value)
        i += 1
    formatTime()
    file.close()
    return


def SaveTime():
    with open("settings.txt", "r") as file:
        data = file.readlines()
    data[0] = 'hours = '
    if len(new_hours.get()) == 0:
        data[0] += '0\n'
    else:
        data[0] += f'{new_hours.get()}\n'
    data[1] = 'minutes = '
    if len(new_minutes.get()) == 0:
        data[1] += '0\n'
    else:
        data[1] += f'{new_minutes.get()}\n'
    data[2] = 'seconds = '
    if len(new_seconds.get()) == 0:
        data[2] += '0\n'
    else:
        data[2] += f'{new_seconds.get()}\n'
    with open('settings.txt', 'w') as file:
        file.writelines(data)
    readSettingsFromFile()


def formatTime():
    hours.set("{:0>2d}".format(int(hours.get())))
    minutes.set("{:0>2d}".format(int(minutes.get())))
    seconds.set("{:0>2d}".format(int(seconds.get())))


def resetCountdown():
    stopCountdown()
    readSettingsFromFile()


def openTimeSettings():
    start_time_button['state'] = 'disabled'
    stop_time_button['state'] = 'disabled'
    reset_time_button['state'] = 'disabled'
    time_settings_button['state'] = 'disabled'
    word_settings_button['state'] = 'disabled'
    top = Toplevel(master)
    top.geometry("350x150")
    top.title("Time settings")
    Label(top, text='Set time between quizzes', font=("Arial", 18)).pack()
    Label(top, text=f'hours', width=6, anchor="w").place(x=99, y=time_label_y)
    Label(top, text=f'minutes', width=6, anchor="w").place(x=167, y=time_label_y)
    Label(top, text=f'seconds', width=6, anchor="w").place(x=250, y=time_label_y)
    new_hours.set("{:0>0d}".format(int(hours.get())))
    new_minutes.set("{:0>0d}".format(int(minutes.get())))
    new_seconds.set("{:0>0d}".format(int(seconds.get())))
    Entry(top, textvariable=new_hours, width=2, font=("Arial", 18)).place(x=67, y=time_label_y - 5)
    Entry(top, textvariable=new_minutes, width=2, font=("Arial", 18)).place(x=134, y=time_label_y - 5)
    Entry(top, textvariable=new_seconds, width=2, font=("Arial", 18)).place(x=217, y=time_label_y - 5)
    Button(top, text="Save new time", command=SaveTime).place(x=130, y=time_label_y + 45)

    def on_closing():
        start_time_button['state'] = 'active'
        stop_time_button['state'] = 'active'
        reset_time_button['state'] = 'active'
        time_settings_button['state'] = 'active'
        word_settings_button['state'] = 'active'
        top.destroy()

    top.protocol("WM_DELETE_WINDOW", on_closing)


def saveWordsSettings():
    with open("settings.txt", "r") as file:
        data = file.readlines()
    data[3] = f'category = {new_category.get()}\n'
    data[4] = f'difficulty = {new_difficulty.get()}\n'
    data[5] = f'tag1 = {new_tag1.get()}\n'
    data[6] = f'tag2 = {new_tag2.get()}\n'
    data[7] = f'tag3 = {new_tag3.get()}'
    with open('settings.txt', 'w') as file:
        file.writelines(data)
    readSettingsFromFile()


def prepareNewSettingsVariables():
    new_category.set(category.get())
    new_difficulty.set(difficulty.get())
    new_tag1.set(tag1.get())
    new_tag2.set(tag2.get())
    new_tag3.set(tag3.get())


def resetNewSettingsVariables():
    new_category.set('all')
    new_difficulty.set('-')
    new_tag1.set('')
    new_tag2.set('')
    new_tag3.set('')


def openWordsSettings():
    start_time_button['state'] = 'disabled'
    stop_time_button['state'] = 'disabled'
    reset_time_button['state'] = 'disabled'
    time_settings_button['state'] = 'disabled'
    word_settings_button['state'] = 'disabled'
    prepareNewSettingsVariables()
    zero_x = 10
    top = Toplevel(master)
    top.geometry("470x150")
    top.title("Words settings")
    Label(top, text='Set available word constraints', font=("Arial", 18)).pack()
    Label(top, text="Word category").place(x=zero_x, y=55)
    Label(top, text="Tags:").place(x=zero_x, y=85)
    Label(top, text="Word difficulty").place(x=zero_x + 225, y=55)
    OptionMenu(top, new_category, *categoryList).place(x=125, y=50)
    Entry(top, width=18, textvariable=new_tag1).place(x=50, y=85)
    Entry(top, width=18, textvariable=new_tag2).place(x=175, y=85)
    Entry(top, width=18, textvariable=new_tag3).place(x=300, y=85)
    OptionMenu(top, new_difficulty, *difficulties).place(x=125 + 200, y=50)
    Button(top, text="Reset settings", command=resetNewSettingsVariables, width=10).place(x=350, y=time_label_y + 60)
    Button(top, text="Save new settings", command=saveWordsSettings, width=14).place(x=140, y=time_label_y + 60)

    def on_closing():
        start_time_button['state'] = 'active'
        stop_time_button['state'] = 'active'
        reset_time_button['state'] = 'active'
        time_settings_button['state'] = 'active'
        word_settings_button['state'] = 'active'
        top.destroy()

    top.protocol("WM_DELETE_WINDOW", on_closing)


def showMainMenu():
    # labels
    main_menu_time_label.pack()
    hours_label.place(x=99, y=time_label_y)
    minutes_label.place(x=167, y=time_label_y)
    seconds_label.place(x=250, y=time_label_y)
    hours_value_label.place(x=67, y=time_label_y - 5)
    minutes_value_label.place(x=134, y=time_label_y - 5)
    seconds_value_label.place(x=217, y=time_label_y - 5)
    # buttons
    start_time_button.place(x=30, y=time_buttons_y)
    stop_time_button.place(x=140, y=time_buttons_y)
    reset_time_button.place(x=250, y=time_buttons_y)
    time_settings_button.place(x=70, y=settings_buttons_y)
    word_settings_button.place(x=200, y=settings_buttons_y)


def hideMainMenu():
    global counting
    counting = False
    # labels
    main_menu_time_label.pack_forget()
    hours_label.place_forget()
    minutes_label.place_forget()
    seconds_label.place_forget()
    hours_value_label.place_forget()
    minutes_value_label.place_forget()
    seconds_value_label.place_forget()
    # buttons
    start_time_button.place_forget()
    stop_time_button.place_forget()
    reset_time_button.place_forget()
    time_settings_button.place_forget()
    word_settings_button.place_forget()


def on_closing():
    global counting
    counting = False
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        master.destroy()


master = Tk()
photo = PhotoImage(file='french_flag.png')
master.iconphoto(True, photo)
master.title("Pop-up quiz")
master.geometry("350x200")

# Time things
hours = StringVar()
minutes = StringVar()
seconds = StringVar()
new_hours = StringVar()
new_minutes = StringVar()
new_seconds = StringVar()
counting = False

# Words things
category = StringVar()
new_category = StringVar()
categoryList = ["all", "basic", "noun", "verb", "adjective"]
difficulty = StringVar()
new_difficulty = StringVar()
difficulties = ["-", "easy", "normal", "hard"]
tag1 = StringVar()
tag2 = StringVar()
tag3 = StringVar()
new_tag1 = StringVar()
new_tag2 = StringVar()
new_tag3 = StringVar()

# All things
settings = [hours, minutes, seconds, category, difficulty, tag1, tag2, tag3]

# Set default values for variables
readSettingsFromFile()
prepareNewSettingsVariables()

# Master label setting
main_menu_time_label = Label(master, text='Time until quiz', font=("Arial", 20))
time_label_y = 55
hours_label = Label(master, text=f'hours', width=6, anchor="w")
minutes_label = Label(master, text=f'minutes', width=6, anchor="w")
seconds_label = Label(master, text=f'seconds', width=6, anchor="w")
hours_value_label = Label(master, textvariable=hours, width=2, font=("Arial", 18), anchor="e")
minutes_value_label = Label(master, textvariable=minutes, width=2, font=("Arial", 18), anchor="e")
seconds_value_label = Label(master, textvariable=seconds, width=2, font=("Arial", 18), anchor="e")

# Master button setting
button_width = 10
time_buttons_y = time_label_y + 40
start_time_button = Button(master, text="START", width=button_width, pady=2, command=startCountdown)
stop_time_button = Button(master, text="STOP", width=button_width, pady=2, command=stopCountdown)
reset_time_button = Button(master, text="RESET", width=button_width, pady=2, command=resetCountdown)
settings_buttons_y = time_buttons_y + 50
time_settings_button = Button(master, text="Time settings", width=button_width, pady=2, command=openTimeSettings)
word_settings_button = Button(master, text="Word settings", width=button_width, pady=2, command=openWordsSettings)

master.protocol("WM_DELETE_WINDOW", on_closing)
showMainMenu()
master.mainloop()
