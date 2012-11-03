import time
from selenium.webdriver.support import wait

class SpeedReading(object):
    IS_START = 'return startButtonVisible'
    START_TEST = 'StartButtonClicked()'
    IS_STOP = 'return tryAgainButtonVisible'
    GET_RS = 'return Math.floor(((perf.testDuration - totalCallbackDuration) / 1000)) + " Seconds"'

    def __init__(self, driver, logf):
        self.driver = driver
        self.logf = logf
        
    def run(self):
        print "Run SpeedReading benchmark..."
        self.driver.get("http://ie.microsoft.com/testdrive/Performance/SpeedReading/Default.html")
        time.sleep(10)
        wait.WebDriverWait(self.driver, 3600, 5).until(lambda x: x.execute_script(self.IS_START))
        self.driver.execute_script(self.START_TEST)
        time.sleep(30)
        wait.WebDriverWait(self.driver, 6000, 30).until(lambda x: x.execute_script(self.IS_STOP))
        rs = self.driver.execute_script(self.GET_RS)
        self.logf.write("SpeedReading: " + rs + "\n")