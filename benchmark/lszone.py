import time
from benchmark import Benchmark

class LSZone(Benchmark):
    TASKID = 'return taskID'

    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "LSZone"

    @property
    def metric(self):
        return "write/read/rewrite KB/s"

    @property
    def default_url(self):
        return "http://pnp.sh.intel.com/benchmarks/WRTBench-git/localStorage/localStorage_Test2.1.html"

    @property
    def default_timeout(self):
        return 1500

    @property
    def expect_time(self):
        return 60

    def chk_finish(self, driver):
        return driver.execute_script(self.TASKID) == 57

    def get_result(self, driver):
        res = [0.0, 0.0, 0.0]
        time.sleep(30)	
        elems = driver.find_elements_by_tag_name("td")	
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