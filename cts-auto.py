import pyautogui
import time
import threading
import pygetwindow as gw
import configparser
import tkinter as tk

from tkinter import scrolledtext

ini = configparser.ConfigParser()

process = ""
delay = ""

clicker = False
stop_msg = False


def read_ini():
    global process, delay
    ini.read("data/info.ini")
    process = ini['basic_info']['process']
    delay = int(ini['basic_info']['delay'])


def write_ini(secs, name):
    ini.read("data/info.ini")

    ini.set("basic_info", "delay", str(secs))
    ini.set("basic_info", "process", str(name))

    with open("data/info.ini", 'w') as configfile:
        ini.write(configfile)


def message_box(msg):
    msg_box.config(state="normal")
    msg_box.insert(tk.END, msg)
    msg_box.config(state="disabled")
    msg_box.see("end")


def start_clicker():
    global clicker, stop_msg
    clicker = True

    message_box(f"\nSTARTING CLICKER THREADS\n=========================\nDelay in seconds: {delay}\n=========================\n")

    def keys(teclas, opt):
        global clicker, stop_msg

        time.sleep(delay)

        message_box(f"{opt} - THREAD STARTED\n")
        # print(f"{opt} - THREAD STARTED")

        while clicker:
            try:
                ventana = gw.getWindowsWithTitle(process)
                if ventana:
                    ventana = ventana[0]
                    ventana.activate()
                    for key in teclas:
                        pyautogui.press(key)
                else:
                    message_box(f"=========================\nPROCESS NOT FOUND: {process}\n=========================\n")
                    break
            except pyautogui.FailSafeException:
                clicker = False
                message_box(f"\n=========================\nTHREADS STOPPED\n=========================\n")
                break

    t1 = threading.Thread(target=keys, args=(['z', 'x', 'c'], 1))
    t2 = threading.Thread(target=keys, args=(['v', 'b', 'n'], 2))
    t3 = threading.Thread(target=keys, args=(['m', 'z', 'v'], 3))
    t4 = threading.Thread(target=keys, args=(['m', 'z', 'v'], 4))
    t5 = threading.Thread(target=keys, args=(['m', 'z', 'v'], 5))
    t6 = threading.Thread(target=keys, args=(['v', 'b', 'n'], 6))

    threads = [t1, t2, t3, t4, t5, t6]

    for thread in threads:
        thread.start()


def settings():

    def save_changes():
        message_box(f"\n=========================\nINFO CHANGES SAVED\n=========================\nDelay: {delay_int.get()}\nProcess: {process_str.get()}\n=========================")
        write_ini(delay_int.get(), process_str.get())
        read_ini()
        config_button.configure(state="normal")
        settings_window.destroy()

    def on_closing():
        message_box(f"\n=========================\nNO CHANGES WERE MADE\n=========================\n")
        config_button.configure(state="normal")
        settings_window.destroy()

    global delay, process

    config_button.configure(state="disabled")

    settings_window = tk.Toplevel(root)
    settings_window.title("SETTINGS")
    settings_window.config(bg="black")
    settings_window.resizable(0, 0)

    root_x, root_y = root.winfo_x(), root.winfo_y()

    new_x = root_x + root.winfo_width() + 10
    new_y = root_y

    settings_window.geometry(f"300x150+{new_x}+{new_y}")

    settings_window.protocol("WM_DELETE_WINDOW", on_closing)

    frame = tk.Frame(settings_window, bg="black")

    delay_label = tk.Label(frame, text="DELAY", bg="black", fg="#33ff33")
    delay_label.pack()
    delay_int = tk.IntVar()
    delay_entry = tk.Entry(frame, textvariable=delay_int)
    delay_int.set(delay)
    delay_entry.pack()

    process_label = tk.Label(frame, text="PROCESS", bg="black", fg="#33ff33")
    process_label.pack()
    process_str = tk.StringVar()
    process_entry = tk.Entry(frame, textvariable=process_str)
    process_str.set(process)
    process_entry.pack()

    save_button = tk.Button(settings_window, text="SAVE CHANGES", command=save_changes, bg="black", fg="#33ff33", width=13, height=2)
    save_button.place(x=100, y=105)

    frame.place(x=90, y=15)


def help_func():
    help_window = tk.Toplevel()
    help_window.title(f"HELP - README")
    help_window.resizable(0, 0)

    root_x, root_y = root.winfo_x(), root.winfo_y()

    new_x = root_x + root.winfo_width() + 10
    new_y = root_y

    help_window.geometry(f"500x500+{new_x}+{new_y}")

    text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, width=40, height=15, bg="black", fg="#33ff33")
    text_widget.pack(fill=tk.BOTH, expand=True)

    with open(f"readme.txt", "r", encoding="UTF-8") as f:
        msg = f.read()

    text_widget.insert(tk.INSERT, msg)

    text_widget.configure(state="disabled")

    help_window.transient(root)
    help_window.grab_set()
    root.wait_window(help_window)


read_ini()

root = tk.Tk()

root.title("Automatic Clicker")
root.geometry("300x300")
root.configure(bg="black")
root.resizable(0, 0)

start_button = tk.Button(root, text="START", command=start_clicker, bg="black", fg="#33ff33", width=10, height=2)
config_button = tk.Button(root, text="SETTINGS", command=settings, bg="black", fg="#33ff33", width=10, height=2)
help_button = tk.Button(root, text="?", command=help_func, bg="black", fg="#33ff33", width=3, height=1)
msg_box = tk.Text(root, bg="black", fg="#33ff33", height=10, width=35)


start_button.place(x=60, y=50)
config_button.place(x=160, y=50)
help_button.place(x=10, y=10)
msg_box.place(x=10, y=110)


root.mainloop()
