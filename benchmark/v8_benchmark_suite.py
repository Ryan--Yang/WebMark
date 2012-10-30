import time
from selenium.webdriver.support import wait
from selenium.common.exceptions import WebDriverException

class V8BenchmarkSuite(object):
    GET_STATUS_JS = 'return document.getElementById("status").innerText'

    def __init__(self, driver, logf):
        self.driver = driver
        self.logf = logf
        
    def run(self):
        print "Run V8 Benchmark Suite..."
        self.driver.get("http://v8.googlecode.com/svn/data/benchmarks/v7/run.html")
        time.sleep(100)
        try:
            #elem = self.driver.find_element_by_id("status")
            #wait.WebDriverWait(self.driver, 1200, 30).until(lambda x: elem.text.find("Score:") != -1)
            wait.WebDriverWait(self.driver, 1200, 30).until(
                lambda x: x.execute_script(self.GET_STATUS_JS).find("Score:") != -1)
            #str = elem.text
            str = self.driver.execute_script(self.GET_STATUS_JS)
            pos = len("Score:")
            str = str[pos:].strip()
            self.logf.write("V8 Benchmark Suite: " + str + "\n")
        except WebDriverException as e:
            print e
            self.logf.write("V8 Benchmark Suite: NA\n")