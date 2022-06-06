from django.shortcuts import render
from django.http import HttpResponse
from twocaptcha import solver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json


def get_url():
    url = "https://www.turkcell.com.tr/yukle/hazir-kart-paket-yukle?place=qa"
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(4)
    return driver

def get_inputs(driver):
    phone_no = driver.find_element_by_xpath("/html/body/div[2]/section[1]/div/div/div/div/div[2]/ul/li/form/article/ul/li/input")
    captcha_field = driver.find_element_by_id("captcha")
    sub_btn = driver.find_element_by_xpath("/html/body/div[2]/section[1]/div/div/div/div/div[2]/ul/li/form/button")
    return phone_no,captcha_field,sub_btn

def solve_captcha(phone,captcha,btn,driver,number):
    s = solver.TwoCaptcha("30401c3991a0613d228dcf56698d0d12")
    phone.send_keys(number)

    captcha_img = driver.find_element_by_xpath("/html/body/div[2]/section[1]/div/div/div/div/div[2]/ul/li/form/article/div/div/div/div/div[1]/div/div/img").get_attribute("src")
    resault = s.normal(captcha_img)
    captcha.send_keys(resault['code'])
    btn.send_keys(Keys.ENTER)


def write_json(driver):
    time.sleep(4)
    packges = driver.find_elements_by_class_name("card_info")
    data = {"data":{
        0:{
            "p_name":"",
            "p_price":""
        },
    }}
    i = 0
    for package in packges:
        p = package.find_element_by_css_selector("input:first-child")
        p_name = p.get_attribute("data-package_name")
        p_price = p.get_attribute("data-package_price")
        data["data"][i] = {
            "p_name":p_name,
            "p_price":p_price,
        }
        i = i+1

    j_data = json.dumps(data)
    jsonFile = open("template/data.json", "w")
    jsonFile.write(j_data)
    jsonFile.close()
    driver.close()

def index(request):
    if request.GET:
        gsm = request.GET.get("gsm")
        print(gsm)
        driver = get_url()
        phone,captcha,btn = get_inputs(driver)
        solve_captcha(phone,captcha,btn,driver,gsm)
        write_json(driver)
    return render(request,"data.json")