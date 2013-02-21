import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class Dromaeocoredom(Benchmark):
    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "Dromaeo core dom"

    @property
    def metric(self):
        return "runs/second"

    @property
    def default_url(self):
        return "http://dromaeo.com/"      

    @property
    def expect_time(self):
        return 300

    @property
    def default_timeout(self):
        return 1800

    def start(self, driver):
        time.sleep(5)       
        self.driver.find_element_by_xpath("//a[@href='?dom']").click()
        time.sleep(5)        
        pause = driver.find_element_by_id("pause")
        wait.WebDriverWait(driver, 120, 10).until(lambda x: pause.get_attribute("value") == "Run")
        pause.click()
        self.timebar = self.driver.find_element_by_id("timebar")

    def chk_finish(self, driver):
        return self.timebar.text.find("Total") != -1

    def get_result(self, driver):
        str = self.timebar.text
        pos1 = str.find("runs/s")
        str = str[:pos1].strip()
        return float(str)
