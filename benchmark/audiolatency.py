import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class AudioLatency(Benchmark):
    TABLE = 'return document.getElementById("table").innerHTML'
	
    def __init__(self, driver, logf, appmode=False):
        Benchmark.__init__(self, driver, logf, appmode)

    @property
    def name(self):
        return "AudioLatency%s" % self.name_common_ext()

    @property
    def metric(self):
        return "ms"
        
    def run(self):
        if self.driver.name.find("internet explorer") !=-1 or self.driver.name.find("firefox") !=-1:
            return 0

        self.open("http://pnp.sh.intel.com/benchmarks/WRTBench-git/audio/AudioLatency/")
        time.sleep(60)

        wait.WebDriverWait(self.driver, 600, 30).until(lambda x: x.execute_script(self.TABLE).find("Total Latency") != -1)
		
        elems = self.driver.find_elements_by_tag_name("td")

        str = elems[27].text
        str = str.strip()
        print str		
        return float(str)	