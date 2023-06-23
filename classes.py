import sys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import os
import json

class RoyalMailTrackingImporter:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        self.tracking_dict = dict()

    def GetTrackingIDs(self):

        MYEMAIL = os.environ["MYEMAIL"]
        MYPASS = os.environ["MYPASS"]
        postcode_list = []

        self.driver.get("https://www.postoffice.co.uk/auth-service/#/login")
        #orders_num = int(input("How many orders did we post today?\n"))
        orders_num = 50
        time.sleep(2)
        email_field = self.driver.find_element(By.CSS_SELECTOR, "#email")
        email_field.send_keys(MYEMAIL)
        password_field = self.driver.find_element(By.CSS_SELECTOR, "#password")
        password_field.send_keys(MYPASS)
        time.sleep(2)
        # Login
        while True:
            try:
                login_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/button')
                login_button.click()
                time.sleep(3)
                break
            except:
                continue
        time.sleep(1.5)
        self.driver.get("https://www.postoffice.co.uk/dng/purchase-history?page=1&size=50")


        # tracking_numbers = self.driver.find_elements(By.CLASS_NAME, "spanTrackingCopy")
        # Wait for them to appear, not sure why this doesnt select them correctly but it works time-wise so whatever.
        tracking_numbers = WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
            self.driver.find_element(By.CLASS_NAME, "spanTrackingCopy")))
        tracking_numbers = self.driver.find_elements(By.CLASS_NAME, "spanTrackingCopy")
        postcodes = self.driver.find_elements(By.CSS_SELECTOR, 'tbody tr td span')

        # I think this loop is for filtering out rare elements that would cause it to error
        # something other than a postcode
        for i in range(0, len(postcodes)):
            if 8 > len(postcodes[i].text) > 4:
                if postcodes[i].text[0] == "£":
                    pass
                else:
                    postcode_list.append(postcodes[i].text)
        rm_post_dict = {}
        for i in range(0, orders_num):
            try:
                tnum = tracking_numbers[i].text
            except:
                tnum = "None Found"
            try:
                postcode = postcode_list[i]
            except:
                postcode = "None Found"
            print(f"{tnum} - {postcode}")
            rm_post_dict[postcode] = tnum
        f = open("rm_post_dict.json", "w")
        f.truncate()
        f.close()
        with open('rm_post_dict.json', 'w') as fd:
            json.dump(rm_post_dict, fd)
            print("json dumped")
        time.sleep(1)

    def InputTrackingIDs(self):
        print("Starting input...")
        with open('rm_post_dict.json') as json_file:
            data = json.load(json_file)
            self.tracking_dict = data
        my_website = os.environ["MY_WEBSITE"]
        self.driver.get(f"{my_website}/wp-admin/edit.php?post_status=wc-packed&post_type=shop_order")

        USERNAME = os.environ["USERNAME"]
        FFPASS = os.environ["FFPASS"]
        time.sleep(0.5)
        email_field = self.driver.find_element(By.CSS_SELECTOR, "#user_login")
        email_field.send_keys(USERNAME)
        password_field = self.driver.find_element(By.CSS_SELECTOR, "#user_pass")
        password_field.send_keys(FFPASS)
        time.sleep(0.5)
        login_button = self.driver.find_element(By.CSS_SELECTOR, '#wp-submit')
        login_button.click()
        #time.sleep(40)

        #orders = self.driver.find_elements(By.CLASS_NAME, "type-shop_order")
        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
            self.driver.find_element(By.CLASS_NAME, "type-shop_order")))

        for i in range(0, len(self.tracking_dict)):

            order = self.driver.find_elements(By.CLASS_NAME, "type-shop_order")
            # status = order[0].find_element(By.CSS_SELECTOR, ".column-order_status mark span").text
            # print(status)
            try:
                print("-------------------------")
                print(f' Importing tracking for {order[0].get_attribute("id")}')
                shipping_address = order[0].find_element(By.CLASS_NAME, "shipping_address")
                shipping_postcode = shipping_address.text.split(", ")[-1]
                shipping_postcode = shipping_postcode.replace(" ", "").split("\n")[0]
                #print(shipping_postcode)
                #print(self.tracking_dict[shipping_postcode])
                tracking_number = self.tracking_dict[shipping_postcode]
                #Insert tracking to popup
                add_tracking = order[0].find_element(By.CSS_SELECTOR, ".add_inline_tracking")
                add_tracking.click()

                # WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located(self.driver.find_element(By.NAME, "Submit")))

                element_present = expected_conditions.presence_of_element_located((By.NAME, "Submit"))
                WebDriverWait(self.driver, 5).until(element_present)

                tracking_number_field = self.driver.find_element(By.CSS_SELECTOR, "#tracking_number")
                tracking_number_field.send_keys(tracking_number)
                time.sleep(0.5)
                self.driver.find_element(By.NAME, "Submit").click()
                print(f'Tracking added for #{order[0].get_attribute("id").split("-")[1]}')

                time.sleep(4)
            except IndexError:
                sys.exit("No further orders marked as packed.")
            except KeyError:
                print(f'>>> Postcode issue for #{order[0].get_attribute("id").split("-")[1]}')

                continue

        else:
            print("No further orders marked as packed.")


        time.sleep(100)