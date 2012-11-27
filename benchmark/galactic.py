import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class Galactic(Benchmark):
    GET_RS = 'return gFpsData.AvgFps'

    def __init__(self, driver, logf, appmode=False, offline=False):
        Benchmark.__init__(self, driver, logf, appmode, offline)

    @property
    def name(self):
        return "Galactic%s" % self.name_common_ext()

    @property
    def metric(self):
        return "fps"

    @property
    def _url(self):
        if self.offline:
            return self.webbench_path + 'microsoft/testdrive/Performance/Galactic/Default.html'
        return "http://ie.microsoft.com/testdrive/Performance/Galactic/Default.html"
        
    def run(self):
        self.open(self._url)
        time.sleep(300)
        return self.driver.execute_script(self.GET_RS)