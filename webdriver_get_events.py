#!/usr/local/bin/python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

driver = webdriver.Firefox()
driver.maximize_window()
driver.get("https://erp.iitkgp.ernet.in/SSOAdministration/login.htm?sessionToken=4BD68AB998A06C5181566BB9BF079295.worker2&requestedUrl=https://erp.iitkgp.ernet.in/IIT_ERP3/")


roll_no = driver.find_element_by_id("user_id")
password = driver.find_element_by_id("password")

#Insert the answers in the quotes left empty
roll_no.send_keys("")

time.sleep(1)
driver.find_element_by_class_name("row").click()
time.sleep(2)
password.send_keys("")

time.sleep(3)

question = driver.find_element_by_id("answer_div").text 
ans = ""

if(question == ""):
	ans = ""
elif(question == ""):
	ans = ""
else:
	ans = ""

answer = driver.find_element_by_id("answer")
answer.send_keys(ans)

#Submit the form
driver.find_element_by_class_name("btn.btn-primary").click()
time.sleep(7)

try:
	driver.find_element_by_id("skiplink").click()#Coz I don't yet have a voter card and some stuff they ask for
	time.sleep(2)
except NoSuchElementException:
	pass

driver.find_element_by_xpath("//a[@href='menulist.htm?module_id=16']").click()
time.sleep(2)

driver.find_element_by_link_text("Time Table").click()
time.sleep(1)

driver.find_element_by_link_text("My Time Table(Student)").click()
time.sleep(3)
print("Hopefully Loaded")

driver.save_screenshot('MyTimeTable.png')
time.sleep(1)

driver.get("https://erp.iitkgp.ernet.in/Acad/student/view_stud_time_table.jsp")

from bs4 import BeautifulSoup as bs 
soup = bs(driver.page_source,'html.parser')

print(soup.prettify())
driver.quit()


