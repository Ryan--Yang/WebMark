import time
from selenium.webdriver.support import wait
from selenium.common.exceptions import TimeoutException
from benchmark import Benchmark

class DromaeoAllDOMTests(Benchmark):
    def __init__(self, driver, logf):
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "Dromaeo (All DOM Tests)"

    @property
    def metric(self):
        return "runs/second"
        
    def run(self):
        self.driver.get("http://dromaeo.com/?dom|jslib|cssquery")
        time.sleep(1)
        pause = self.driver.find_element_by_id("pause")
        wait.WebDriverWait(self.driver, 60, 3).until(lambda x: pause.get_attribute("value") == "Run")
        pause.click()
        time.sleep(200)
        elem = self.driver.find_element_by_id("timebar")
        wait.WebDriverWait(self.driver, 1500, 120).until(lambda x: elem.text.find("Total") != -1)
        str = elem.text
        pos1 = str.find(":") + 1
        pos2 = str.find("runs/s")
        str = str[pos1:pos2].strip()
        return float(str)