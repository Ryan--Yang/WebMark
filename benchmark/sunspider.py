import time
from selenium.webdriver.support import wait

class SunSpider(object):
    def __init__(self, driver, logf):
        self.driver = driver
        self.logf = logf
        
    def run(self):
        print "Run SunSpider benchmark..."
        self.driver.get("http://www.webkit.org/perf/sunspider-0.9.1/sunspider-0.9.1/driver.html")
        time.sleep(60)
        wait.WebDriverWait(self.driver, 1200, 30).until(lambda x: x.current_url.lower().find("result") != -1)
        elem = self.driver.find_element_by_id("console")
        str = elem.text
        pos = str.find("Total:")+len("Total:")
        str = str[pos:].strip()
        pos = str.find("ms")+2
        self.logf.write("SunSpider: " + str[:pos] + "\n")