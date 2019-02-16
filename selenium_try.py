import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from tkinter import *

#browser = webdriver.Chrome(executable_path='chromedriver.exe')
CHROME_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
CHROMEDRIVER_PATH = 'chromedriver.exe'
#WINDOW_SIZE = "800,600"
chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH

browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)

timeout = 10
iteration_time = 3000
news = []
news_loaded = False
url_open_fail = False
after_id = 0  # ID of iterating process of getting data from opened site
prev_url = ""  # stores successfully opened URL string
actions = ActionChains(browser)
#browser.set_window_position(0,0)

def on_closing():
    browser.quit()
    root.destroy()

def get_start():
    global news_loaded, after_id

    if after_id:
        root.after_cancel(after_id)
    site_name = site_entry.get()
    find_class = find_entry.get()
    print(site_name)
    print(find_class)
    if site_name and find_class:
        start(site_name, find_class)


def start(target_site, target_class):
    global news, url_open_fail, prev_url
    print(target_site)

    if target_site != prev_url:
        try:
            browser.get(target_site)
        except:
            t.insert(END, "Can't open URL\n")
            url_open_fail = True

# Waiting for the page to be loaded

    #try:
        #WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, "tabs__content")))
    #except (TimeoutException, WebDriverException):
        #print("Can't open the page")
        #news.append("Can't open the page")
        #browser.quit()
        #sys.exit()

# Clicking on a tab
    try:
        target_tab = browser.find_element_by_name('clb23640812')
        actions.move_to_element(target_tab)
        actions.click(target_tab)
        actions.perform()
    except:
        pass

    if not url_open_fail:
        prev_url = target_site
        work(target_class)


# Function that will collect needed data every %iteration_time% seconds
def work(target_class):
    global news, news_loaded, iteration_time, after_id
    news.clear()

    try:
        news_element = browser.find_elements_by_class_name(target_class)
        for item in news_element:
            if item.text != "":
                news.append(item.text)
    except:
        pass

    news_loaded = True
    t.delete(1.0, END)
    counter = 0
    for n in news:
        counter += 1
        mystr = "{}. {}\n".format(str(counter), n)
        t.insert(END, mystr)
        
    after_id = root.after(iteration_time, work, target_class)


# Creating a window for our program
root = Tk()
root.title("Новости Mail.ru")
root.config(padx=10, pady=10)
form_frame = LabelFrame(root, text="Данные для загрузки", padx=5, pady=5)
form_frame.grid(row=0, column=0, sticky=W+N)

site_label = Label(form_frame, text="Какой сайт открыть?", padx=5, pady=5)
site_label.grid(row=0, column=0, sticky=W)

site_entry = Entry(form_frame, width=25)
site_entry.grid(row=0, column=1, sticky=W)

find_label = Label(form_frame, text="Имя класса у интересующего объекта: ", padx=5, pady=5)
find_label.grid(row=1, column=0, sticky=W)

find_entry = Entry(form_frame, width=25)
find_entry.grid(row=1, column=1, sticky=W)

text_frame = LabelFrame(root, text="Новости В Мире", padx=5, pady=5)
text_frame.grid(row=1, column=0, sticky=E+W+N+S)

scroll = Scrollbar(text_frame, orient="vertical")
scroll.grid(row=0, column=1, sticky="ns")

t = Text(text_frame, height=20, width=50)
t.grid(row=0, column=0, sticky=E+W+N+S)

btn = Button(text_frame, text="Загрузить новости", font=("Comic Sans", 20), padx=8, pady=8, command=get_start)
btn.grid(row=1, column=0, sticky=E+W)

scroll.config(command=t.yview)
t.config(yscrollcommand=scroll.set)

#root.columnconfigure(0, weight=1)
text_frame.columnconfigure(0, weight=1)

root.protocol("WM_DELETE_WINDOW", on_closing)
mainloop()




