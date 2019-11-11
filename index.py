from flask import Flask, render_template, request
from  selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
import time
import os
import traceback
import logging
import threading

driver_path = os.getcwd() + "/chromedriver.exec"
print(driver_path)

loggedIn = False
exception = False

def tryLogin(username, password, browser):
    
    def navigate():
        inputID = browser.find_element_by_id("UserID")
        inputID.send_keys(username)
        inputPassword = browser.find_element_by_name("PIN")
        inputPassword.send_keys(password)
        submit = browser.find_element_by_css_selector("input[value='Login'][type='submit']")
        submit.click()
        stuButton = browser.find_element_by_link_text("Student")
        stuButton.click()
        regButton = browser.find_element_by_link_text("Registration")
        regButton.click()
        addClassButton = browser.find_element_by_link_text("Look-up Classes to Add")
        addClassButton.click()
   
    try:

        # driver.get() method is waiting untill the requested page is fully loaded
        browser.get("https://bannerweb.sabanciuniv.edu/")
        time.sleep(0.5)
        enterButton = browser.find_element_by_xpath("html/body/h2/a")
        enterButton.click()
        time.sleep(0.5)
        currentUrl = browser.current_url
        #print(currentUrl)

        if currentUrl == "https://suis.sabanciuniv.edu/prod/twbkwbis.P_SabanciLogin" :
            navigate()
            return True, False
        else:
            return False, False

    except : 
        print("An exception occured")
        traceback.print_stack()
        return False, True

def thread_function(username, password, threadId ):

    logging.info("Thread %s: starting", threadId)

    browser = webdriver.Chrome(driver_path)

    def openMultipleTabs(n):
        openTabScript = "window.open()"
        for i in range(n):
            browser.execute_script(openTabScript)

    openMultipleTabs(5)
    Window_List = browser.window_handles
    num_tabs = len(Window_List)    
    
    mutex = threading.Lock()
    global loggedIn
    global exception

    while not loggedIn and not exception:

        for i in range(num_tabs):
            browser.switch_to.window(Window_List[i])
            #mutex HERE
            mutex.acquire()
            loggedIn, exception = tryLogin(username, password, browser)
            #print("Current Page Title is : %s" %browser.title)
            mutex.release()

            if loggedIn or exception:
                break
    return

app = Flask(__name__)

@app.route("/index" )
def index():
    return render_template("index.html")

@app.route("/get_data", methods=['POST', 'GET'])
def get_data():
    username = request.form.get('SUusername')
    password = request.form.get('password')

    crms = []

    for i in range(6):
        newCrm = request.form.get('crm'+str(i+1))
        crms.append(newCrm)

    print(username, password, crms)

    threadList = []

    for idx in range(3):
        newThread = threading.Thread(target=thread_function, args=(username, password,idx))
        threadList.append(newThread)
        newThread.start()
    
    for th in threadList:
        logging.info("Thread %s: finishing", threadList.index(th))
        th.join()
        
    return render_template("result.html")
    


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    app.run()