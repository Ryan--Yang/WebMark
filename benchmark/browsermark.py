from selenium.webdriver.support import wait
from common.exceptions import WebMarkException
from benchmark import Benchmark

class BrowserMark(Benchmark):
    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "BrowserMark"

    @property
    def metric(self):
        return "score"

    @property
    def default_url(self):
        return "http://browsermark.rightware.com/"

    @property
    def default_timeout(self):
        return 1500

    @property
    def expect_time(self):
        return 200

    def start(self, driver):
        driver.find_element_by_xpath("//a[text()='North America']").click()
        driver.find_element_by_class_name("start_test").click()

    def chk_finish(self, driver):
        href = driver.current_url.lower()
        return href.find("result") != -1 or href.find("hash") != -1

    def get_result(self, driver):
        href = driver.current_url.lower()
        if href.find("result") != -1 :
            elem = driver.find_element_by_class_name("score")
            str = elem.text
            return int(str)
        else:
            raise WebMarkException(self.name + " : There was something wrong with your benchmark result")
