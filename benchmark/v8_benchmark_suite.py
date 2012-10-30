import time
from selenium.webdriver.support import wait

class V8BenchmarkSuite(object):
    def __init__(self, driver, logf):
        self.driver = driver
        self.logf = logf
        
    def run(self):
        print "Run V8 Benchmark Suite..."
        self.driver.get("http://v8.googlecode.com/svn/data/benchmarks/v7/run.html")
        time.sleep(30)
        elem = self.driver.find_element_by_id("status")
        wait.WebDriverWait(self.driver, 1200, 15).until(lambda x: elem.text.find("Score:") != -1)
        str = elem.text
        pos = len("Score:")
        str = str[pos:].strip()
        self.logf.write("V8 Benchmark Suite: " + str + "\n")