import time
from selenium.webdriver.support import wait
from common.exceptions import WebMarkException
from benchmark import Benchmark

class BrowserMark(Benchmark):
    def __init__(self, driver, logf, appmode=False):
        Benchmark.__init__(self, driver, logf, appmode)

    @property
    def name(self):
        return "BrowserMark%s" % self.name_common_ext()

    @property
    def metric(self):
        return "score"
    
    def _chk_finished(self, driver):
        href = driver.current_url.lower()
        if href.find("result") != -1 or href.find("hash") != -1 :
            return href
        return None

    def run(self):
        self.open("http://browsermark.rightware.com/")
        self.driver.find_element_by_xpath("//a[text()='North America']").click()
        self.driver.find_element_by_class_name("start_test").click()
        time.sleep(200)
        href = wait.WebDriverWait(self.driver, 1200, 60).until(self._chk_finished)
        if href.find("result") != -1 :
            elem = self.driver.find_element_by_class_name("score")
            str = elem.text
            return int(str)
        else:
            raise WebMarkException(self.name + " : There was something wrong with your benchmark result")