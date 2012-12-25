import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class SpeedReading(Benchmark):
    IS_START = 'return startButtonVisible'
    START_TEST = 'StartButtonClicked()'
    IS_STOP = 'return tryAgainButtonVisible'
    GET_RS = 'return Math.floor(((perf.testDuration - totalCallbackDuration) / 1000))'

    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "SpeedReading"

    @property
    def metric(self):
        return "second"

    @property
    def default_url(self):
        return "http://ie.microsoft.com/testdrive/Performance/SpeedReading/Default.html"

    def start(self, driver):
        time.sleep(10)
        wait.WebDriverWait(driver, 3600, 5).until(lambda x: x.execute_script(self.IS_START))
        driver.execute_script(self.START_TEST)
    
    def chk_finish(self, driver):
        return driver.execute_script(self.IS_STOP)

    def get_result(self, driver):
        return driver.execute_script(self.GET_RS)
