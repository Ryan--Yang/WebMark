import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class FileOperation(Benchmark):
    WRITEROUND = 'return writeRound'
	
    def __init__(self, driver, logf, appmode=False):
        Benchmark.__init__(self, driver, logf, appmode)

    @property
    def name(self):
        return "FileOperation%s" % self.name_common_ext()

    @property
    def metric(self):
        return "read/write MB/s"    
		
    def run(self):
        if self.driver.name.find("internet explorer") !=-1 or self.driver.name.find("firefox") !=-1:
            return 0

        self.open("http://pnp.sh.intel.com/benchmarks/WRTBench-git/fileOperation/fileOperation.html")
        time.sleep(10)
		
        res = [0.0, 0.0]
		
        wait.WebDriverWait(self.driver, 600, 30).until(lambda x: x.execute_script(self.WRITEROUND) == 10)
        time.sleep(10)		
        print "finish"			
        elems = self.driver.find_elements_by_tag_name("td")

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