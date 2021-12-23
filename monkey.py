from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import ElementNotInteractableException, NoSuchWindowException
import time

TIME_LENGTHS = [10, 25, 50, 100]
WORD_LENGTHS = [15, 30, 60, 120]
MONKEY_TYPE_SITE = "https://monkeytype.com"
lengths = []
modes = []


class Monkey:
    def __init__(self, path):
        self.service = Service(executable_path=path)
        self.d = webdriver.Chrome(service=self.service)
        self.score = 0
        self.mode = 0
        self.length = 0
        self.choice_picked = 0
        self.fetch_site()
        self.set_options()

    def fetch_site(self):
        self.d.get(MONKEY_TYPE_SITE)

    def set_options(self):
        global modes, lengths
        try:
            modes = self.d.find_elements("css selector", ".mode .buttons .text-button")
            modes[self.mode].click()
        except NoSuchWindowException:
            print("Error: Window Closed. You need to restart the program!")
        else:
            if self.mode == 0:
                lengths = self.d.find_elements("css selector", ".time .buttons .text-button")
            elif self.mode == 1:
                lengths = self.d.find_elements("css selector", ".wordCount .buttons .text-button")
            elif self.mode == 2:
                lengths = self.d.find_elements("css selector", ".quoteLength .buttons .text-button")

            lengths[self.length].click()

    def type_n_words(self):
        try:
            test = self.d.find_element("id", "typingTest")
            test.click()
            WebDriverWait(self.d, 10).until(ec.presence_of_element_located(("css selector", "#words div.active")))
            input_word = self.d.find_element("id", "wordsInput")
            for i in range(WORD_LENGTHS[self.length]):
                active_word = self.d.find_element("css selector", "#words div.active")
                input_word.send_keys(active_word.text + " ")
        except ElementNotInteractableException:
            print("Race Over. Try 'Do Another Race'.")
            return
        except NoSuchWindowException:
            print("Error: Window Closed. You need to restart the program!")

    def type_quote(self):
        try:
            test = self.d.find_element("id", "typingTest")
            test.click()
            WebDriverWait(self.d, 10).until(ec.presence_of_element_located(("css selector", "#words div.active")))
            active_word = self.d.find_element("css selector", "#words div.active")
            input_word = self.d.find_element("id", "wordsInput")
            input_word.send_keys(active_word.text + " ")
            WebDriverWait(self.d, 10).until(ec.presence_of_element_located(("css selector",
                                                                            "#miniTimerAndLiveWpm .time")))
            timer = self.d.find_element("css selector", "#miniTimerAndLiveWpm .time")
            words_amount = int(timer.text.split("/")[1])
            for _ in range(words_amount - 1):
                active_word = self.d.find_element("css selector", "#words div.active")
                input_word = self.d.find_element("id", "wordsInput")
                input_word.send_keys(active_word.text + " ")
        except ElementNotInteractableException:
            print("Race Over. Try 'Do Another Race'.")
            return
        except NoSuchWindowException:
            print("Error: Window Closed. You need to restart the program!")

    def type_for_time(self):
        try:
            test = self.d.find_element("id", "typingTest")
            test.click()
            WebDriverWait(self.d, 10).until(ec.presence_of_element_located(("css selector", "#words div.active")))
            input_word = self.d.find_element("id", "wordsInput")
            while time.time() < time.time() + TIME_LENGTHS[self.length]:
                active_word = self.d.find_element("css selector", "#words div.active")
                input_word.send_keys(active_word.text + " ")
        except ElementNotInteractableException:
            print("Race Over. Try 'Do Another Race'.")
            return
        except NoSuchWindowException:
            print("Error: Window Closed. You need to restart the program!")

    def bye(self):
        self.d.quit()

    def menu_choice(self):
        try:
            choice = int(input("What do you want the Monkey to do?\n\n1: Set Options\n2: Start Typing\n3: Do Another "
                               "Race\n4: Quit\n\n>>>>"))
            if choice > 4 or choice < 1:
                raise ValueError
        except ValueError:
            print("Not an option. Try again.")
            self.menu_choice()
        else:
            self.choice_picked = choice

    def set_mode(self):
        try:
            mode = int(input("Enter mode (0 = time, 1 = words, 2 = quote): "))
            if mode > 2 or mode < 0:
                raise ValueError
        except ValueError:
            print("Looks like that's not right. Try again.")
            self.set_mode()
        else:
            self.mode = mode

    def set_length(self):
        try:
            length = int(input("Enter length(could be a number from 0 to 4 => increasing in length): "))
            if (((self.mode == 1 or self.mode == 0) and length > 3) or length < 0) or (self.mode == 2 and length > 4):
                raise ValueError
        except ValueError:
            print("Looks like that's not right. Try again.")
            self.set_length()
        else:
            self.length = length

    def do_another_test(self):
        try:
            WebDriverWait(self.d, 30).until(ec.presence_of_element_located(("id", "nextTestButton")))
            do_next = self.d.find_element("id", "nextTestButton")
            do_next.click()
        except ElementNotInteractableException:
            WebDriverWait(self.d, 30).until(ec.presence_of_element_located(("id", "restartTestButton")))
            restart = self.d.find_element("id", "restartTestButton")
            restart.click()
        except NoSuchWindowException:
            print("Error: Window Closed. You need to restart the program!")
