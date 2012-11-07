import time
from selenium.webdriver.support import wait
from selenium.common.exceptions import WebDriverException
from benchmark import Benchmark

class V8BenchmarkSuite(Benchmark):
    GET_STATUS_JS = 'return document.getElementById("status").innerHTML'

    def __init__(self, driver, logf):
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "V8 Benchmark Suite"

    @property
    def metric(self):
        return "score"
        
    def run(self):
        self.open("http://v8.googlecode.com/svn/data/benchmarks/v7/run.html")
        time.sleep(60)
        #elem = self.driver.find_element_by_id("status")
        #wait.WebDriverWait(self.driver, 1200, 30).until(lambda x: elem.text.find("Score:") != -1)
        wait.WebDriverWait(self.driver, 1200, 30).until(
            lambda x: x.execute_script(self.GET_STATUS_JS).find("Score:") != -1)
        #str = elem.text
        str = self.driver.execute_script(self.GET_STATUS_JS)
        pos = len("Score:")
        str = str[pos:].strip()
        return int(str)