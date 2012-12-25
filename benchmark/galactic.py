import time
from benchmark import Benchmark

class Galactic(Benchmark):
    GET_RS = 'return gFpsData.AvgFps'

    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "Galactic"

    @property
    def metric(self):
        return "fps"

    @property
    def default_url(self):
        return "http://ie.microsoft.com/testdrive/Performance/Galactic/Default.html"
        
    def get_result(self, driver):
        time.sleep(300)
        return self.driver.execute_script(self.GET_RS)