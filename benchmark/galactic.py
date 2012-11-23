import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class Galactic(Benchmark):
    GET_RS = 'return gFpsData.AvgFps'

    def __init__(self, driver, logf, appmode=False):
        Benchmark.__init__(self, driver, logf, appmode)

    @property
    def name(self):
        return "Galactic"

    @property
    def metric(self):
        return "fps"
        
    def run(self):
        self.open("http://ie.microsoft.com/testdrive/Performance/Galactic/Default.html")
        time.sleep(300)
        return self.driver.execute_script(self.GET_RS)