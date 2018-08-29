from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import re
import time
import threading

threadMain = None
thread_stop_flag = False
thread_running = False

def MainProc():
    global threadMain
    global thread_stop_flag
    global thread_running

    filename = input_file.get()
    print(filename)
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    num_lines = sum(1 for line in open(filename))
    print(num_lines)

    pbStatus["value"] = 0
    pbStatus["maximum"] = num_lines
    lblFile_Text.set("(0/" + str(num_lines) + ")")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("log-level=3")

    print("Initializing ...")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    url = "https://www.amazon.com/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&switch_account="

    file = open("output.txt", "w+")
    success_count = 0
    progress_count = 0
    for iLine in range(num_lines):
        if thread_stop_flag == True:
            break

        progress_count = progress_count + 1
        pbStatus["value"] = progress_count
        lblFile_Text.set("(" + str(progress_count) + "/" + str(num_lines) + ")")

        file = open("output.txt", "a+")
        remaing = num_lines - iLine
        driver.get(url)
        driver.set_window_position(-2000, 0)
        a = driver.find_element_by_id("ap_email")
        email = lines[iLine].strip()
        a.clear()
        a.send_keys(email)
        w = driver.find_element_by_id("continue")
        w.click()
        try:
            driver.find_element_by_xpath("//div[@id='auth-error-message-box']")
            print(email + ": We cannot find an account with that email address")
        except:
            print(email + ": Already exists")
            file.write(email + "\n")
            success_count += 1
            file.write(str(success_count))
    file.close()
    thread_running = False
    btnStart_text.set("Start")

def OnStart():
    global threadMain
    global thread_stop_flag
    global thread_running

    if thread_running == False:
        print("Main thread is running.")
        btnStart_text.set("Stop")
        thread_running = True
        threadMain = threading.Thread(target=MainProc)
        threadMain.start()
    else:
        print("Main thread is stopping.")
        thread_stop_flag = True

def Browser_btn():
    global objConfig
    filename = askopenfilename(initialdir="C:/",
                               filetypes = (("All Files", "*.*"), ("All Files", "")),
                               title = "Choose a file.")
    try:
        file_pathname = filename
        input_file.delete(0, END)
        input_file.insert(0, file_pathname)

    except Exception as inst:
        print(type(inst))

#########################################################
window = Tk()
window.title("Amazon email")
mainframe = Frame(window)
mainframe.grid()

frmMain = LabelFrame(mainframe, text="", padx=5, pady=5)
frmMain.pack(padx=10, pady=10)

lblFile = Label(frmMain, text="File:")
lblFile.grid(column=0, row=0, sticky=W, padx=0, pady=0)

input_file = Entry(frmMain, width=40)
input_file.grid(row=0, column=1)

btnBrowser = Button(frmMain, text='Browse', command=Browser_btn)
btnBrowser.grid(row=0, column=2, sticky=W, pady=4)

lblFile = Label(frmMain, text="Status:")
lblFile.grid(row=1, column=0, sticky=W, padx=0, pady=0)

pbStatus = ttk.Progressbar(frmMain, orient="horizontal", length=245, mode="determinate")
pbStatus.grid(row=1, column=1)

lblFile_Text = StringVar()
lblFile = Label(frmMain, textvariable=lblFile_Text)
lblFile.grid(row=1, column=2, sticky=W, padx=0, pady=0)
lblFile_Text.set("(0/0)")

btnStart_text = StringVar()
btnStart = Button(frmMain, textvariable=btnStart_text, command=OnStart, width=34)
btnStart_text.set("Start")
btnStart.grid(row=2, column=1, sticky='e', padx=10)

window.mainloop( )


