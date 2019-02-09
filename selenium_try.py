import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from tkinter import *


browser = webdriver.Chrome(executable_path='chromedriver.exe')
actions = ActionChains(browser)
timeout = 10
iteration_time = 3000
news = []
new_tab_clicked = False

browser.set_window_position(0,0)
browser.get("http://www.mail.ru")

# Waiting for page to be loaded
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, "tabs__content")))
except (TimeoutException, WebDriverException):
    print("Can't open the page")
    news.append("Can't open the page")
    browser.quit()
    sys.exit()

# Clicking on a tab
target_tab = browser.find_element_by_name('clb23640812')
actions.move_to_element(target_tab)
actions.click(target_tab)
actions.perform()

# Creating a window for our program
root = Tk()
S = Scrollbar(root)
T = Text(root, height=4, width=50)
S.pack(side=RIGHT, fill=Y)
T.pack(side=LEFT, fill=Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)

# Function that will collect needed data every %iteration_time% seconds
def work():
    global news, iteration_time
    news.clear()

    try:
        news_element = browser.find_elements_by_class_name('news-item')
        for item in news_element:
            if item.text != "":
                news.append(item.text)
    except:
        pass

    T.delete(1.0, END)
    counter = 0
    for new in news:
        counter += 1
        mystr = "{}. {}\n\n".format(str(counter), new)
        T.insert(END, mystr)
        
    root.after(iteration_time, work)

work()
mainloop()

