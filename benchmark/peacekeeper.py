import time
from selenium.webdriver.support import wait

class Peacekeeper(object):
    def __init__(self, driver, logf):
        self.driver = driver
        self.logf = logf

    def _chk_finished(self, driver):
        href = driver.current_url.lower()
        if href.find("results") != -1 or href.find("error") != -1 :
            return href
        return None      

    def run(self):
        print "Run Peacekeeper benchmark..."
        self.driver.get("http://peacekeeper.futuremark.com/run.action")
        time.sleep(420)
        href = wait.WebDriverWait(self.driver, 1200, 30).until(self._chk_finished)
        if href.find("results") != -1 :
            elem = self.driver.find_element_by_class_name("your-score")
            str = elem.text
            self.logf.write("Peacekeeper: " + str + "\n")
        else :
            self.logf.write("Peacekeeper: Network Error\n")