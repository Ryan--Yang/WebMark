import time
from common.exceptions import WebMarkException
from benchmark import Benchmark

class FileOperation(Benchmark):
    WRITEROUND = 'return writeRound'

    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "FileOperation"

    @property
    def metric(self):
        return "read/write MB/s"    

    @property
    def default_url(self):
        return "http://pnp.sh.intel.com/benchmarks/WRTBench-git/fileOperation/fileOperation.html"

    @property
    def default_timeout(self):
        return 1500

    @property
    def expect_time(self):
        return 60

    def start(self, driver):
        if self.driver.name.find("internet explorer") !=-1 or self.driver.name.find("firefox") !=-1:
            raise WebMarkException("internet explorer/firefox does not support FileOperation")

    def chk_finish(self, driver):
        return driver.execute_script(self.WRITEROUND) == 10

    def get_result(self, driver):
        time.sleep(10)	
        res = [0.0, 0.0]
        elems = driver.find_elements_by_tag_name("td")

        str = elems[42].text
        print str
        start = str.find(":") + 1
        end = str.find("(")		
        str = str[start:end].strip()	
        res[0] = float(str)

        str = elems[85].text
        print str
        start = str.find(":") + 1
        end = str.find("(")		
        str = str[start:end].strip()	
        res[1] = float(str)
        return res