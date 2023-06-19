from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
from twilio.rest import Client

client = Client('AC895d3596813e53902e948ec2a240bb24', 'e8d7abf8285b0d9425e5b8c1068c6586')

driver = webdriver.Firefox()
driver.get('https://secureapps.wsdot.wa.gov/ferries/reservations/vehicle/SailingSchedule.aspx')

fromStation = driver.find_element(By.XPATH, "//select[@tabindex = '1']")
dropFromStation=Select(fromStation)
dropFromStation.select_by_visible_text("Anacortes")

driver.implicitly_wait(time_to_wait=.2)
toStation = driver.find_element(By.XPATH, "//select[@tabindex = '2']")
dropToStation=Select(toStation)
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "option[value='10']"))
    )
except:
    print("Time exceeded!")

driver.implicitly_wait(time_to_wait=.2)
dropToStation.select_by_visible_text("Friday Harbor")


vehicleLength = driver.find_element(By.XPATH, "//select[@tabindex = '4']")
dropVehicleLength=Select(vehicleLength)
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "option[value='3']"))
    )
except:
    print("Time exceeded!")
dropVehicleLength.select_by_visible_text("Vehicle under 22 feet")

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[@id = 'MainContent_ddlCarTruck14To22']"))
    )
except:
    print("Time exceeded!")
vehicleHeight = driver.find_element(By.XPATH, "//select[@id = 'MainContent_ddlCarTruck14To22']")
dropVehicleHeight=Select(vehicleHeight)
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "option[value='1000']"))
    )
except:
    print("Time exceeded!")
dropVehicleHeight.select_by_visible_text("Up to 7'2'' tall")

#06/30/2023
date = driver.find_element(By.XPATH, "//input[@tabindex = '3']")
driver.execute_script("arguments[0].setAttribute('value',arguments[1])",date, '06/30/2023')

driver.implicitly_wait(time_to_wait=.2)
showAvailability=driver.find_element(By.XPATH, "//div[@id = 'MainContent_btnContinue']")
showAvailability.click()

driver.implicitly_wait(time_to_wait=5)

timeList = driver.find_element(By.XPATH, "//table[@id = 'MainContent_gvschedule']")
timeListString = driver.execute_script("return arguments[0].innerHTML;",timeList)

timeListString = timeListString[timeListString.index("</tr>")+5:]

#print(timeListString)

goodTimes = ["9:05 AM", "12:00 PM", "2:00 PM", "4:45 PM"]

while "<tr>" in timeListString:
    timeListString = timeListString[timeListString.index("<tr>")+4:]
    div = timeListString[timeListString.index('<td style="width:60px;"')+4:]
    time = div[div.index(">")+1:div.index("<")]

    if time in goodTimes:
        client.messages.create(from_='+18886128944',
                        to='+13103399837',
                        body=f'{time} IS AVAILABLE. GO GET IT')

driver.close()