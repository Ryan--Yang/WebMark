import time
from selenium.webdriver.support import wait
from selenium.common.exceptions import TimeoutException

class DromaeoAllDOMTests(object):
    def __init__(self, driver, logf):
        self.driver = driver
        self.logf = logf
        
    def run(self):
        print "Run Dromaeo (All DOM Tests)..."
        self.driver.get("http://dromaeo.com/?dom|jslib|cssquery")
        time.sleep(1)
        self.driver.find_element_by_id("pause").click()
        time.sleep(60)
        elem = self.driver.find_element_by_id("timebar")
        try:
            wait.WebDriverWait(self.driver, 1800, 30).until(lambda x: elem.text.find("Total") != -1)
            str = elem.text
            pos1 = str.find(":") + 1
            pos2 = str.find("(Total)")
            str = str[pos1:pos2].strip()
            self.logf.write("Dromaeo (All DOM Tests): " + str + "\n")
        except TimeoutException:
            self.logf.write("Dromaeo (All DOM Tests): NA\n")