from flask import Flask, flash, redirect, render_template, request, session, abort
from  selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
import time
import os 

driver_path = os.getcwd() + "/chromedriver"
print(driver_path)

def loginBannerWeb(username, password):

    browser = webdriver.Chrome(executable_path=driver_path)
    browser.get("https://bannerweb.sabanciuniv.edu/")

    enterButton = browser.find_element_by_xpath("html/body/h2/a")

    currentUrl = browser.current_url

    print(currentUrl)

    while currentUrl != "https://suis.sabanciuniv.edu/prod/twbkwbis.P_SabanciLogin":
        browser.get("https://bannerweb.sabanciuniv.edu/")
        enterButton = browser.find_element_by_xpath("html/body/h2/a")
        enterButton.click()
        
        currentUrl = browser.current_url


    browser.get("https://suis.sabanciuniv.edu/prod/twbkwbis.P_SabanciLogin")

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

    print(username, password)
    print(crms)

    loginBannerWeb(username, password)

    return render_template("result.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)