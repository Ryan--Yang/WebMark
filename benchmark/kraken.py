import time
from selenium.webdriver.support import wait

class Kraken(object):
    def __init__(self, driver, logf):
        self.driver = driver
        self.logf = logf
        
    def run(self):
        print "Run Kraken benchmark..."
        self.driver.get("http://krakenbenchmark.mozilla.org/kraken-1.1/driver.html")
        time.sleep(180)
        wait.WebDriverWait(self.driver, 6000, 30).until(lambda x: x.current_url.lower().find("results") != -1)
        elem = self.driver.find_element_by_id("console")
        str = elem.text
        pos = str.find("Total:")+len("Total:")
        str = str[pos:].strip()
        pos = str.find("ms")+2
        self.logf.write("Kraken: " + str[:pos] + "\n")