from datetime import datetime, timedelta
import time

from selenium.webdriver import Chrome

CHROMEDRV_PATH = './chromedriver.exe'


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


class GolfBooking(Browser):
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

    def go_next(self):
        go_next = self.check_elem_exist('Next')
        if go_next:
            go_next.click()


def next_nth_day(n=1):
    day = datetime.today() + timedelta(days=n)
    return day.day


if __name__ == '__main__':
    gb = GolfBooking()
    gb.login('tommy9763@gmail.com', 'shrimpeko')
    resv_day = next_nth_day(7)
    gb.pick_last_day()
    gb.quit()

