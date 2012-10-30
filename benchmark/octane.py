import time
from selenium.webdriver.support import wait

class Octane(object):
    def __init__(self, driver, logf):
        self.driver = driver
        self.logf = logf
        
    def run(self):
        print "Run Octane benchmark..."
        self.driver.get("http://octane-benchmark.googlecode.com/svn/latest/index.html")
        self.driver.find_element_by_id("run-octane").click()
        elem = self.driver.find_element_by_id("main-banner")
        time.sleep(60)
        wait.WebDriverWait(self.driver, 1200, 30).until(lambda x: elem.text.find("Score:") != -1)
        str = elem.text
        pos = str.find(":") + 1
        str = str[pos:].strip()
        print "Octane: " + str
        self.logf.write("Octane: " + str + "\n")