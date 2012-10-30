import time
from selenium.webdriver.support import wait

class DromaeoAllJavascriptTests(object):
    def __init__(self, driver, logf):
        self.driver = driver
        self.logf = logf
        
    def run(self):
        print "Run Dromaeo (All JavaScript Tests)..."
        self.driver.get("http://dromaeo.com/?dromaeo|sunspider|v8")
        time.sleep(1)
        self.driver.find_element_by_id("pause").click()
        time.sleep(600)
        elem = self.driver.find_element_by_id("timebar")
        wait.WebDriverWait(self.driver, 6000, 30).until(lambda x: elem.text.find("Total") != -1)
        str = elem.text
        pos1 = str.find(":") + 1
        pos2 = str.find("(Total)")
        str = str[pos1:pos2].strip()
        self.logf.write("Dromaeo (All JavaScript Tests): " + str + "\n")