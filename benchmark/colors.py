import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class Colors(Benchmark):
    RESULT_LEN = 'return result.length'
    RESULT = 'return result[1][1]'	
    def __init__(self, driver, logf, appmode=False):
        Benchmark.__init__(self, driver, logf, appmode)

    @property
    def name(self):
        return "Colors%s" % self.name_common_ext()

    @property
    def metric(self):
        return "fps"
        
    def run(self):
        self.open("http://pnp.sh.intel.com/benchmarks/WRTBench-git/css/colors/colors.html")
        time.sleep(5)
        wait.WebDriverWait(self.driver, 3600, 5).until(lambda x: x.execute_script(self.RESULT_LEN) == 2)
        str = self.driver.execute_script(self.RESULT)
        start = str.find(":") + 1	
        end = str.find("fps")	
        str = str[start:end].strip()		
        print str
        fps = float(str)
        return round(fps, 2)	