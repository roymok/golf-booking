import json
import time

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from seleniumrequests import Chrome

CHROMEDRV_PATH = './chromedriver.exe'


class Browser:
    driver = None

    def __init__(self):
        capabilities = DesiredCapabilities.CHROME
        # capabilities["loggingPrefs"] = {"performance": "ALL"}  # chromedriver < ~75
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+
        self.driver = Chrome(CHROMEDRV_PATH, desired_capabilities=capabilities)

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


def process_browser_logs_for_network_events(logs):
    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if (
                "Network.response" in log["method"]
                or "Network.request" in log["method"]
                or "Network.webSocket" in log["method"]
        ):
            yield log


class FanlingGolf(Browser):

    def __init__(self):
        super().__init__()
        self.goto("https://visitorbookings.hkgolfclub.org/")

    def login(self, u, p):
        self.set_input_value('username', u)
        self.set_input_value('password', p)
        self.click_link('btn')
        time.sleep(0.5)
        have_alert = self.check_elem_exist('Ok')
        if have_alert:
            have_alert.click()
            time.sleep(0.5)
        # logs = self.driver.get_log("performance")
        # events = process_browser_logs_for_network_events(logs)
        # print(list(events))

    def get_time_table(self):
        # webdriver = Chrome()
        response = self.driver.request('POST',
                                       'https://visitorbookings.hkgolfclub.org/Booking/GetTimeTable',
                                       data={'dateParam': '30052021',
                                             "isAdd": False,
                                             "isEdit": False
                                             # 'Referer': 'https://visitorbookings.hkgolfclub.org/',
                                             #   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
                                             #   'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
                                             #   'sec-ch-ua-mobile': '?0'
                                             })
        print(json.loads("".join([s.decode("utf-8") for s in list(response)]))["success"])


if __name__ == '__main__':
    flgb = FanlingGolf()
    flgb.login('sergiopang', 'gmeamctsla@32857')
    flgb.get_time_table()
# 21872.159
