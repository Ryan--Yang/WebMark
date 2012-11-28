import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class LSZone(Benchmark):
    TASKID = 'return taskID'
	
    def __init__(self, driver, logf):
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "LSZone"

    @property
    def metric(self):
        return "write/read/rewrite KB/s"

    def run(self):
        self.open("http://pnp.sh.intel.com/benchmarks/WRTBench-git/localStorage/localStorage_Test2.1.html")
        time.sleep(10)
		
        res = [0.0, 0.0, 0.0]		

        wait.WebDriverWait(self.driver, 600, 30).until(lambda x: x.execute_script(self.TASKID) == 57)		
        elems = self.driver.find_elements_by_tag_name("td")
		
        str = elems[9].text
        str = str.strip()
        print str	
        res[0] = float(str)	
	
        str = elems[29].text
        str = str.strip()
        print str	
        res[1] = float(str)	

        str = elems[49].text
        str = str.strip()
        print str	
        res[2] = float(str)	

        return res
