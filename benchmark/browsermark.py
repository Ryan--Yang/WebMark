import time
from selenium.webdriver.support import wait

class BrowserMark(object):
    def __init__(self, driver, logf):
        self.driver = driver
        self.logf = logf
    
    def _chk_finished(self, driver):
        href = driver.current_url.lower()
        if href.find("result") != -1 or href.find("hash") != -1 :
            return href
        return None

    def run(self):
        print "Run BrowserMark benchmark..."
        self.driver.get("http://browsermark.rightware.com/browsermark/run.action")
        time.sleep(360)
        href = wait.WebDriverWait(self.driver, 1200, 30).until(self._chk_finished)
        if href.find("result") != -1 :
            elem = self.driver.find_element_by_id("score")
            str = elem.text
            self.logf.write("BrowserMark: " + str + "\n")
        else :
            self.logf.write("BrowserMark: Network Error\n")