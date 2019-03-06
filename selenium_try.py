import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from tkinter import *
from tkinter import ttk

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
iteration_time = 30000
news = []
news_loaded = False
url_open_fail = False
clicked = False
after_id = 0  # ID of iterating process of getting data from opened site
prev_url = ""  # stores successfully opened URL string
search_modes = ("Search by Class", "Search by Tag", "Search by ID",
                "Search by Name")
search_mode = 0
actions = ActionChains(browser)
#browser.set_window_position(0,0)

def on_closing():
    browser.quit()
    root.destroy()

def change_search_mode(event):
    global search_mode
    search_mode = mode_combobox.current()
    if mode_combobox.current() == 0:
        new_text = "Введите класс интересующего объекта: "
    elif mode_combobox.current() == 1:
        new_text = "Введите тэг интересующего объекта: "
    elif mode_combobox.current() == 2:
        new_text = "Введите ID интересующего объекта: "
    elif mode_combobox.current() == 3:
        new_text = "Введите name интересующего объекта: "
    find_label.configure(text = new_text)
    mode_combobox.selection_clear()

def stop_search():
    global after_id
    mode_combobox.selection_clear()
    if after_id:
        root.after_cancel(after_id)

def get_start():
    global news_loaded, after_id

    if after_id:
        root.after_cancel(after_id)
    site_name = site_entry.get()
    search_text = find_entry.get()
    print(site_name)
    print(search_text)
    if site_name and search_text:
        start(site_name, search_text)


def start(target_site, search_text):
    global news, url_open_fail, prev_url, clicked

    print("Target site: " + target_site + ". Prev_url: " + prev_url)
    if target_site != prev_url:
        clicked = False
        try:
            browser.get(target_site)
            url_open_fail = False
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
    if not clicked:
        try:
            target_tab = browser.find_element_by_name('clb23640812')
            actions.move_to_element(target_tab)
            actions.click(target_tab)
            actions.perform()
            clicked = True
        except:
            pass

    if not url_open_fail:
        prev_url = target_site
        work(search_text)


# Function that will collect needed data every %iteration_time% seconds
def work(search_text):
    global news, news_loaded, iteration_time, search_mode, after_id
    news.clear()

    try:
        if search_mode == 0:
            news_element = browser.find_elements_by_class_name(search_text)
        elif search_mode == 1:
            news_element = browser.find_elements_by_tag_name(search_text)
        elif search_mode == 2:
            news_element = browser.find_elements_by_id(search_text)
        elif search_mode == 3:
            news_element = browser.find_elements_by_name(search_text)
            
        for item in news_element:
            if item.text != "":
                news.append(item.text)
    except:
        news.append("No such object found")
        pass
    print(news)
    news_loaded = True
    t.delete(1.0, END)
    counter = 0
    for n in news:
        counter += 1
        mystr = "{}. {}\n".format(str(counter), n)
        t.insert(END, mystr)
        
    after_id = root.after(iteration_time, work, search_text)


# Creating a window for our program
root = Tk()
root.title("Программа сбора информации с сайтов")
root.config(padx=10, pady=10)
form_frame = LabelFrame(root, text="Данные для загрузки")
form_frame.grid(row=0, column=0, sticky=W+N, padx=5, pady=5)

site_label = Label(form_frame, text="Какой сайт открыть?")
site_label.grid(row=0, column=0, sticky=W, padx=5, pady=5)

site_entry = Entry(form_frame, width=25)
site_entry.grid(row=0, column=1, sticky=W, padx=(0,10))

search_mode_label = Label(form_frame, text="Выберите тип поиска")
search_mode_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)

mode_combobox = ttk.Combobox(form_frame, values=search_modes, state="readonly")
mode_combobox.grid(row=1, column=1, sticky=W)
mode_combobox.current(0)

find_label = Label(form_frame, text="Введите класс интересующего объекта: ",
                   width=35, anchor="w")
find_label.grid(row=2, column=0, sticky="W", padx=5, pady=5)

find_entry = Entry(form_frame, width=25)
find_entry.grid(row=2, column=1, sticky=W)

text_frame = LabelFrame(root, text="Найденные данные", padx=5, pady=5)
text_frame.grid(row=1, column=0, sticky=E+W+N+S)

scroll = Scrollbar(text_frame, orient="vertical")
scroll.grid(row=0, column=1, sticky="ns")

t = Text(text_frame, height=20, width=50)
t.grid(row=0, column=0, columnspan=2, sticky=E+W+N+S)

btn_start = Button(text_frame, text="Загрузить новости", font=16,
                   command=get_start)
btn_start.grid(row=2, column=0, pady=10, sticky=E+W)

btn_stop = Button(text_frame, text="Остановить загрузку", font=16,
                  command=stop_search)
btn_stop.grid(row=2, column=1, pady=10, sticky=E+W)

scroll.config(command=t.yview)
t.config(yscrollcommand=scroll.set)

#root.columnconfigure(0, weight=1)
text_frame.columnconfigure(0, weight=1)

mode_combobox.bind("<<ComboboxSelected>>", change_search_mode)
mode_combobox.selection_clear()
root.protocol("WM_DELETE_WINDOW", on_closing)
mainloop()




