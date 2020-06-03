from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
import PIL
from PIL import Image
import time
import pytesseract
import requests
import math
from .CaptchaSolve import CaptchaSolver

class type_racer:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--log-level=OFF")
        self.driver = webdriver.Chrome(options=chrome_options)
        min_path = 7
        max_path = 12
        self.possible_captcha_paths = range(min_path, max_path + 1, 1)

    def log_in(self):
        """
        Logs in by looking at account.txt for an account
        """
        main_url = "https://play.typeracer.com/"
        self.driver.get(main_url)
        signin_path = "/html/body/div[1]/table/tbody/tr/td[3]/div/table/tbody/tr[2]/td[1]/table/tbody/tr/td[1]/a"
        while True:
            try:
                signin_element = self.driver.find_element_by_xpath(signin_path)
                break
            except NoSuchElementException:
                time.sleep(1)
        signin_element.click()

        as_guest = False
        try:
            with open("account.txt") as account_file:
                userpass = account_file.read().split(":")
                username = userpass[0]
                try:
                    password = userpass[1]
                except IndexError:
                    as_guest = True
        except FileNotFoundError:
            print("Couldn't find an account.txt. Please restart the program with your Username:Password inside."
                  " Alternatively, play as a guest by using Username and no colon")
            with open("account.txt", "w") as account_file:
                account_file.write("SampleUsername:SamplePassword")
                self.driver.quit()
                quit()
        if as_guest:
            print("Found no password in accounts.txt... playing as a guest with name inputted")
            while True:
                try:
                    guest_path = "/html/body/div[5]/div/div/div[3]/div/div[1]/div/table[3]/tbody/tr[1]/td/a/table/tbody/tr/td[2]"
                    guest_elem = self.driver.find_element_by_xpath(guest_path)
                    guest_elem.click()
                    break
                except NoSuchElementException:
                    time.sleep(1)
            nickname_path = "/html/body/div[5]/div/div/div[3]/div/div[1]/div/table[3]/tbody/tr[2]/td/div/table/tbody/tr[1]/td/table/tbody/tr/td[2]/input"
            while True:
                try:
                    nickname_elem = self.driver.find_element_by_xpath(nickname_path)
                    break
                except NoSuchElementException:
                    time.sleep(1)
            if username == "":
                print("No username found in account.txt... playing with name of randomly generated characters")
                time.sleep(1.5)
                username = "IM A BOT LOL"
                print("Name selected: %s" % username)
            nickname_elem.clear()
            nickname_elem.send_keys(username)
            time.sleep(1)
            apply_path = "/html/body/div[5]/div/div/div[3]/div/div[1]/div/table[3]/tbody/tr[2]/td/div/table/tbody/tr[1]/td/table/tbody/tr/td[3]/button"
            apply_elem = self.driver.find_element_by_xpath(apply_path)
            apply_elem.click()
        else:
            user_path = "/html/body/div[5]/div/div/div[3]/div/div[1]/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[2]/input"
            pass_path = "/html/body/div[5]/div/div/div[3]/div/div[1]/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[2]/td[2]/table/tbody/tr[1]/td/input"
            while True:
                try:
                    username_elem = self.driver.find_element_by_xpath(user_path)
                    password_elem = self.driver.find_element_by_xpath(pass_path)
                    break
                except NoSuchElementException:
                    time.sleep(1)
            username_elem.send_keys(username)
            password_elem.send_keys(password)
            enter_path = "/html/body/div[5]/div/div/div[3]/div/div[1]/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[4]/td[2]/table/tbody/tr/td[1]/button"
            enter_elem = self.driver.find_element_by_xpath(enter_path)
            enter_elem.click()

    def enter_race(self):
        """
        Will enter the race assuming that we are at the login page
        """
        while True:
            try:
                racestart_path = "/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/a"
                racestart_elem = self.driver.find_element_by_xpath(racestart_path)
                break
            except ElementNotInteractableException:
                time.sleep(1)
        racestart_elem.click()

    def complete_race(self):
        """
        Completes a race assuming that the player is currently at the race page
        """

        def find_solution():
            # There are two text containers that may or may not appear,
            # So we store their possibilities in these two booleans
            found_third = True
            found_fourth = True
            while True:
                try:
                    # We will try to find the solution to the typeracer by polling these two text elements
                    # If these two elements don't exist, the page hasn't loaded yet, so we sleep and reiterate
                    # The loop
                    firsttext_path = r"/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/span[1]"
                    firsttext_elem = self.driver.find_element_by_xpath(firsttext_path)
                    first_text = firsttext_elem.text
                    secondtext_path = r"/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/span[2]"
                    secondtext_elem = self.driver.find_element_by_xpath(secondtext_path)
                    second_text = secondtext_elem.text
                    try:
                        # There is a possibility of being 3 or 4 text elements storing text,
                        # So we poll these elements to see if they exist
                        thirdtext_path = r"/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/span[3]"
                        thirdtext_elem = self.driver.find_element_by_xpath(thirdtext_path)
                        third_text = thirdtext_elem.text
                        try:
                            fourthtext_path = r"/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/span[4]"
                            fourthtext_elem = self.driver.find_element_by_xpath(fourthtext_path)
                            fourth_text = fourthtext_elem.text
                        except NoSuchElementException:
                            found_fourth = False
                    except NoSuchElementException:
                        found_third = False
                        found_fourth = False
                    except StaleElementReferenceException:
                        # Every time the loop continues, we must reset our variables
                        # Because the page may have moved around the elements and changed
                        found_fourth = True
                        found_third = True
                        continue
                    break
                except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
                    # If the page hasn't loaded yet, we will continue and reset our booleans
                    time.sleep(1)
                    found_fourth = True
                    found_third = True

            if found_fourth:
                solution_text = "%s%s%s%s" % (first_text, second_text, third_text, fourth_text)
                texts = (first_text, second_text, third_text, fourth_text)
            elif found_third:
                if third_text[0] == ',':
                    solution_text = "%s%s%s" % (first_text, second_text, third_text)
                else:
                    solution_text = "%s%s %s" % (first_text, second_text, third_text)
                texts = (first_text, second_text, third_text)
            else:
                solution_text = "%s %s" % (first_text, second_text)
                texts = (first_text, second_text)
            return solution_text, texts

        # We use find solution to find a solution to the race
        solution_text, texts = find_solution()
        text_num = 1
        for text in texts:
            print("Text %i: (%s)" % (text_num, text))
            text_num += 1
        print("Solution: %s" % solution_text)

        while True:
            try:
                raceenter_path = r"/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/input"
                raceenter_elem = self.driver.find_element_by_xpath(raceenter_path)
                num_chars = 5
                num_words = int(math.ceil(len(solution_text) / num_chars))
                words = []
                wait_time = .15
                for word_num in range(num_words):
                    start_ind = word_num * num_chars
                    end_ind = start_ind + num_chars
                    words.append(solution_text[start_ind: end_ind])
                for word in words:
                    start_time = time.time()
                    raceenter_elem.send_keys(word)
                    end_time = time.time()
                    elapsed = end_time - start_time
                    curr_wait = max(wait_time - elapsed, 0)
                    time.sleep(curr_wait)
                try:
                    raceenter_elem.send_keys(" ")
                except ElementNotInteractableException:
                    pass
                break
            except (NoSuchElementException, ElementNotInteractableException):
                time.sleep(1)
            except StaleElementReferenceException:
                continue

    def handle_captcha(self):
        """
        Handles the possibility of a captcha
        assuming that the player is finished with a race
        """
        try:
            for path_num in self.possible_captcha_paths:
                begincaptcha_path = r"/html/body/div[%i]/div/div/div[2]/div/div/table/tbody/tr[4]/td/button" % path_num
                if path_num != self.possible_captcha_paths[len(self.possible_captcha_paths) - 1]:
                    try:
                        begincaptcha_elem = self.driver.find_element_by_xpath(begincaptcha_path)
                        break
                    except NoSuchElementException:
                        pass
                else:
                    begincaptcha_elem = self.driver.find_element_by_xpath(begincaptcha_path)
            begincaptcha_elem.click()
            found_captcha = True
        except NoSuchElementException:
            print("No captcha found")
            found_captcha = False

        if found_captcha:

            def extract_captcha():

                def attempt_find():
                    correct_path = None
                    for path_num in self.possible_captcha_paths:
                        captcha_path = r"/html/body/div[%i]/div/div/div[2]/div/div/table/tbody/tr[3]/td/img" % path_num
                        if path_num != self.possible_captcha_paths[len(self.possible_captcha_paths) - 1]:
                            try:
                                captcha_elem = self.driver.find_element_by_xpath(captcha_path)
                                correct_path = path_num
                                break
                            except NoSuchElementException:
                                pass
                        else:
                            captcha_elem = self.driver.find_element_by_xpath(captcha_path)
                            correct_path = path_num
                    return captcha_elem, correct_path

                while True:
                    try:
                        captcha_elem, path_num = attempt_find()
                        break
                    except NoSuchElementException:
                        time.sleep(1)
                return captcha_elem, path_num

            def solve_captcha():
                captcha_elem, path_num = extract_captcha()
                captcha_url = captcha_elem.get_attribute("src")
                captcha_page = requests.get(captcha_url)
                with open("captcha_image.png", "wb") as captcha_file:
                    captcha_file.write(captcha_page.content)
                solver = CaptchaSolver(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
                solution = solver.resolve("captcha_image.png").replace("\n", "")

                captcha_textbox_path = r"/html/body/div[%i]/div/div/div[2]/div/div/table/tbody/tr[4]/td/textarea" % path_num
                while True:
                    try:
                        captcha_textbox_elem = self.driver.find_element_by_xpath(captcha_textbox_path)
                        captcha_textbox_elem.send_keys(solution)
                        break
                    except (ElementNotInteractableException, NoSuchElementException):
                        time.sleep(1)

                submit_path = r"/html/body/div[%i]/div/div/div[2]/div/div/table/tbody/tr[5]/td/table/tbody/tr/td[2]/button" % path_num
                submit_elem = self.driver.find_element_by_xpath(submit_path)
                submit_elem.click()

            while True:
                solve_captcha()
                time.sleep(1)
                was_closed = False
                for path_num in self.possible_captcha_paths:
                    restart_path = r"/html/body/div[%i]/div/div/div[3]/div/div/table/tbody/tr[3]/td/table/tbody/tr/td[2]/button" % path_num
                    close_path = r"/html/body/div[%i]/div/div/div[1]" % path_num
                    try:
                        restart_elem = self.driver.find_element_by_xpath(restart_path)
                        restart_elem.click()
                        break
                    except NoSuchElementException:
                        try:
                            close_elem = self.driver.find_element_by_xpath(close_path)
                            close_elem.click()
                            was_closed = True
                            break
                        except NoSuchElementException:
                            pass
                if was_closed:
                    break
                time.sleep(1)

    def handle_popup(self):
        possible_paths = range(7, 13, 1)
        for path_num in possible_paths:
            nothanks_path = r"/html/body/div[%i]/div/div/div[3]/div/div[2]/a" % path_num
            try:
                # A no thanks button might appear for joining instead of being a guest
                # If we are running the program as a guest, so we will look for it
                # And click it if it exists
                nothanks_elem = self.driver.find_element_by_xpath(nothanks_path)
                nothanks_elem.click()
            except NoSuchElementException:
                pass

    def initialize_racer(self):
        print("Logging in...")
        self.log_in()
        print("Entering race...")
        self.enter_race()

    def race(self):
        print("Completing race...")
        self.complete_race()
        time.sleep(1)
        print("Handling captcha...")
        self.handle_captcha()
        time.sleep(1)

    def restart_race(self):
        print("Restarting race...")
        while True:
            try:
                raceagain_path = r"/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/a"
                raceagain_elem = self.driver.find_element_by_xpath(raceagain_path)
                # We click the "start a new race" button after the race is over
                raceagain_elem.click()
                # We will try clicking it again in case there was a pop up
                # Asking us to make an account
                time.sleep(1)
                self.handle_popup()
                time.sleep(1)
                try:
                    raceagain_elem.click()
                except StaleElementReferenceException:
                    # This is the exception that will be thrown if we've gone to the next page already
                    # And there is no element to click
                    pass
                break
            except ElementClickInterceptedException:
                time.sleep(1)
        time.sleep(1)

    def quit(self):
        self.driver.quit()

if __name__ == '__main__':

    racer = type_racer()
    racer.initialize_racer()
    racer.race()
    for i in range(5):
        racer.restart_race()
        racer.race()

    input("Exit")
    racer.quit()
