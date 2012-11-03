import time
from selenium.webdriver.support import wait

class Galactic(object):
    GET_RS = 'return gFpsData.AvgFps + " FPS"'

    def __init__(self, driver, logf):
        self.driver = driver
        self.logf = logf
        
    def run(self):
        print "Run Galactic benchmark..."
        self.driver.get("http://ie.microsoft.com/testdrive/Performance/Galactic/Default.html")
        time.sleep(60)
        rs = self.driver.execute_script(self.GET_RS)
        self.logf.write("Galactic: " + rs + "\n")