from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
import PIL
from PIL import Image
import time
import pytesseract
import requests
from CaptchaSolve import CaptchaSolver

if __name__ == '__main__':

    chrome_options = Options()
    chrome_options.add_argument("--log-level=OFF")
    driver = webdriver.Chrome(options = chrome_options)


    def log_in():
        main_url = "https://play.typeracer.com/"
        driver.get(main_url)
        signin_path = "/html/body/div[1]/table/tbody/tr/td[3]/div/table/tbody/tr[2]/td[1]/table/tbody/tr/td[1]/a"
        while True:
            try:
                signin_element = driver.find_element_by_xpath(signin_path)
                break
            except NoSuchElementException:
                time.sleep(1)
        signin_element.click()
        user_path = "/html/body/div[5]/div/div/div[3]/div/div[1]/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[2]/input"
        pass_path = "/html/body/div[5]/div/div/div[3]/div/div[1]/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[2]/td[2]/table/tbody/tr[1]/td/input"
        while True:
            try:
                username_elem = driver.find_element_by_xpath(user_path)
                password_elem = driver.find_element_by_xpath(pass_path)
                break
            except NoSuchElementException:
                time.sleep(1)

        username = "zisop"
        password = "sl4shd0t"
        username_elem.send_keys(username)
        password_elem.send_keys(password)
        enter_path = "/html/body/div[5]/div/div/div[3]/div/div[1]/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[4]/td[2]/table/tbody/tr/td[1]/button"
        enter_elem = driver.find_element_by_xpath(enter_path)
        enter_elem.click()

    def enter_race():
        while True:
            try:
                racestart_path = "/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/a"
                racestart_elem = driver.find_element_by_xpath(racestart_path)
                break
            except ElementNotInteractableException:
                time.sleep(1)
        racestart_elem.click()


    def complete_race():

        found_third = True
        found_fourth = True
        while True:
            try:
                firsttext_path = r"/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/span[1]"
                firsttext_elem = driver.find_element_by_xpath(firsttext_path)
                first_text = firsttext_elem.text
                secondtext_path = r"/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/span[2]"
                secondtext_elem = driver.find_element_by_xpath(secondtext_path)
                second_text = secondtext_elem.text
                try:
                    thirdtext_path = r"/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/span[3]"
                    thirdtext_elem = driver.find_element_by_xpath(thirdtext_path)
                    third_text = thirdtext_elem.text
                    try:
                        fourthtext_path = r"/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/span[4]"
                        fourthtext_elem = driver.find_element_by_xpath(fourthtext_path)
                        fourth_text = fourthtext_elem.text
                    except NoSuchElementException:
                        found_fourth = False
                except NoSuchElementException:
                    found_third = False
                except StaleElementReferenceException:
                    continue
                break
            except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
                time.sleep(1)
        if found_fourth:
            solution_text = "%s%s%s%s" % (first_text, second_text, third_text, fourth_text)
        elif found_third:
            try:
                solution_text = "%s%s %s" % (first_text, second_text, third_text)
            except UnboundLocalError:
                solution_text = "%s %s" % (first_text, second_text)
        else:
            solution_text = "%s %s" % (first_text, second_text)

        while True:
            try:
                raceenter_path = r"/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/input"
                raceenter_elem = driver.find_element_by_xpath(raceenter_path)
                for char in solution_text:
                    raceenter_elem.send_keys(char)
                    time.sleep(.00001)
                try:
                    raceenter_elem.send_keys(" ")
                except ElementNotInteractableException:
                    pass
                break
            except (NoSuchElementException, ElementNotInteractableException):
                time.sleep(1)

    def handle_captcha():
        try:
            begincaptcha_path = r"/html/body/div[7]/div/div/div[2]/div/div/table/tbody/tr[4]/td/button"
            other_begincaptcha = r"/html/body/div[8]/div/div/div[2]/div/div/table/tbody/tr[4]/td/button"
            last_begincaptcha = r"/html/body/div[9]/div/div/div[2]/div/div/table/tbody/tr[4]/td/button"
            try:
                begincaptcha_elem = driver.find_element_by_xpath(begincaptcha_path)
            except NoSuchElementException:
                begincaptcha_elem = driver.find_element_by_xpath(other_begincaptcha)
            except NoSuchElementException:
                begincaptcha_elem = driver.find_element_by_xpath(last_begincaptcha)
            begincaptcha_elem.click()
            found_captcha = True
        except NoSuchElementException:
            found_captcha = False

        if found_captcha:

            def extract_captcha():
                captcha_path = r"/html/body/div[9]/div/div/div[2]/div/div/table/tbody/tr[3]/td/img"
                other_path = r"/html/body/div[8]/div/div/div[2]/div/div/table/tbody/tr[3]/td/img"
                while True:
                    try:
                        captcha_elem = driver.find_element_by_xpath(captcha_path)
                        return captcha_elem
                    except NoSuchElementException:
                        try:
                            captcha_elem = driver.find_element_by_xpath(other_path)
                            return captcha_elem
                        except NoSuchElementException:
                            time.sleep(1)
            def solve_captcha():
                captcha_elem = extract_captcha()
                captcha_url = captcha_elem.get_attribute("src")
                captcha_page = requests.get(captcha_url)
                with open("captcha_image.png", "wb") as captcha_file:
                    captcha_file.write(captcha_page.content)
                solver = CaptchaSolver(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
                solution = solver.resolve("captcha_image.png").replace("\n", "")

                while True:
                    try:
                        captcha_textbox_path = r"/html/body/div[8]/div/div/div[2]/div/div/table/tbody/tr[4]/td/textarea"
                        other_captchabox = r"/html/body/div[9]/div/div/div[2]/div/div/table/tbody/tr[4]/td/textarea"
                        try:
                            captcha_textbox_elem = driver.find_element_by_xpath(captcha_textbox_path)
                        except NoSuchElementException:
                            captcha_textbox_elem = driver.find_element_by_xpath(other_captchabox)
                        captcha_textbox_elem.send_keys(solution)
                        break

                    except (ElementNotInteractableException, NoSuchElementException):
                        time.sleep(1)

                submit_path = r"/html/body/div[8]/div/div/div[2]/div/div/table/tbody/tr[5]/td/table/tbody/tr/td[2]/button"
                other_submit = r"/html/body/div[9]/div/div/div[2]/div/div/table/tbody/tr[5]/td/table/tbody/tr/td[2]/button"
                try:
                    submit_elem = driver.find_element_by_xpath(submit_path)
                except NoSuchElementException:
                    submit_elem = driver.find_element_by_xpath(other_submit)
                submit_elem.click()

            while True:
                solve_captcha()
                time.sleep(2)
                try:
                    restart_path = r"/html/body/div[9]/div/div/div[3]/div/div/table/tbody/tr[3]/td/table/tbody/tr/td[2]/button"
                    other_restart = r"/html/body/div[8]/div/div/div[3]/div/div/table/tbody/tr[3]/td/table/tbody/tr/td[2]/button"
                    try:
                        restart_elem = driver.find_element_by_xpath(restart_path)
                    except NoSuchElementException:
                        restart_elem = driver.find_element_by_xpath(other_restart)
                    restart_elem.click()
                    time.sleep(2)
                except NoSuchElementException:
                    break
            close_path = r"/html/body/div[8]/div/div/div[1]"
            other_close = r"/html/body/div[9]/div/div/div[1]"
            try:
                close_elem = driver.find_element_by_xpath(close_path)
            except NoSuchElementException:
                close_elem = driver.find_element_by_xpath(other_close)
            except NoSuchElementException:
                return
            close_elem.click()


    log_in()
    enter_race()
    complete_race()
    time.sleep(2)
    handle_captcha()
    time.sleep(2)
    for i in range(5):
        raceagain_path = r"/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/a"
        raceagain_elem = driver.find_element_by_xpath(raceagain_path)
        raceagain_elem.click()
        time.sleep(2)
        print("Completing race...")
        complete_race()
        time.sleep(2)
        print("Handling captcha...")
        handle_captcha()
        time.sleep(2)





    input("Exit")
    driver.quit()