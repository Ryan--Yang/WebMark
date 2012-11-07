import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class SpeedReading(Benchmark):
    IS_START = 'return startButtonVisible'
    START_TEST = 'StartButtonClicked()'
    IS_STOP = 'return tryAgainButtonVisible'
    GET_RS = 'return Math.floor(((perf.testDuration - totalCallbackDuration) / 1000))'

    def __init__(self, driver, logf):
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "SpeedReading"

    @property
    def metric(self):
        return "second"
        
    def run(self):
        self.open("http://ie.microsoft.com/testdrive/Performance/SpeedReading/Default.html")
        time.sleep(10)
        wait.WebDriverWait(self.driver, 3600, 5).until(lambda x: x.execute_script(self.IS_START))
        self.driver.execute_script(self.START_TEST)
        time.sleep(60)
        wait.WebDriverWait(self.driver, 6000, 90).until(lambda x: x.execute_script(self.IS_STOP))
        return self.driver.execute_script(self.GET_RS)