from datetime import datetime, timedelta
import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

CHROMEDRV_PATH = './chromedriver.exe'
course_sequence = "East,South,North"

class Browser:
    driver = None

    def __init__(self):
        self.driver = Chrome(CHROMEDRV_PATH)

    def goto(self, url):
        self.driver.get(url)

    def set_input_value(self, name, value):
        self.driver.find_element_by_id(name).send_keys(value)

    def click_link(self, class_name):
        self.driver.find_element_by_class_name(class_name).click()

    def check_elem_exist(self, name):
        elem = None
        try:
            elem = self.driver.find_element_by_xpath(f"//*[text()='{name}']")
        finally:
            return elem

    def quit(self):
        self.driver.quit()


class KscGolfBooking(Browser):
    def __init__(self):
        super().__init__()
        self.goto("https://booking.kscgolf.org.hk/login")

    def login(self, u, p):
        self.set_input_value('username', u)
        self.set_input_value('password', p)
        self.click_link('login-btn')
        time.sleep(0.5)
        have_alert = self.check_elem_exist('Ok')
        if have_alert:
            have_alert.click()
            time.sleep(0.5)
            time.sleep(0.5)

        self.goto('https://booking.kscgolf.org.hk/newBooking')
        time.sleep(0.5)

    def pick_last_day(self):
        options = self.driver.find_elements_by_class_name('filterOptsBtn')
        options[6].click() if len(options) > 0 else None
        time.sleep(0.3)
        self.go_next()

    def pick_course(self, sequence):
        [self.find_course_btn(seq) for seq in ",".split(sequence)]
        time.sleep(0.3)

    def find_course_btn(self, direction):
        label = self.check_elem_exist(f'{direction} Course')
        if label:
            btn = label.find_element_by_xpath('../..')
            if not btn.is_enabled():
                btn.click()

    def pick_course_type(self, course_type):
        [self.find_course_type_btn(typ) for typ in ",".split(course_type)]
        time.sleep(0.3)
        self.go_next()

    def find_course_type_btn(self, course_type):
        label = self.check_elem_exist(f'{course_type}')
        if label:
            btn = label.find_element_by_xpath('../..')
            if not btn.is_enabled():
                btn.click()

    def check_full_or_available(self,):
        full = "Sorry, the selected course is full on that day."
        WebDriverWait(self.driver, 15).until(
            lambda driver: driver.find_elements(By.XPATH, full) or driver.find_elements(By.ID, "bking-time-picker"))
        isfull = self.check_elem_exist(full)
        if isfull:
            # skip 1 or 2 element in pick_course
        else:
            # pick_time


    def go_next(self):
        go_next = self.check_elem_exist('Next')
        if go_next:
            go_next.click()

def next_nth_day(n=1):
    day = datetime.today() + timedelta(days=n)
    return day.day


if __name__ == '__main__':
    gb = KscGolfBooking()
    gb.login('tommy9763@gmail.com', 'shrimpeko')
    resv_day = next_nth_day(7)
    gb.pick_last_day()
    gb.pick_course(course_sequence)
    gb.pick_course_type("Twilight,9-hole,18-hole")
    # gb.quit()

