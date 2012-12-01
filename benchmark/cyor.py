import time
from selenium.webdriver.support import wait
from benchmark import Benchmark
from common.exceptions import WebMarkException

class Cyor(Benchmark):
    tests = ("Triangles", "Pyramids", "Cubes", "Blending", "Spheres", "Lights", "Mass")
	
    TYPE = 'return browserType.ie'
    CURRENT = 'return currentTest == 8'
	
    _STYLES = {
        "low" : "styleLow",
        "medium" : "styleMedium",
        "high" : "styleHigh"
    }

    def __init__(self, driver, logf, style = 'medium'):
        if self._STYLES.has_key(style.lower()):
            self.style = style
        else:
            raise WebMarkException("Unsupported style %s, "
            "should be one of 'low', 'medium', 'high'." % style)
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "Cyor %s style" % self.style

    @property
    def metric(self):
        return "score"    

    @property
    def _id(self):
        return self._STYLES[self.style.lower()]        
		
    def run(self):
        self.open("http://pnp.sh.intel.com/benchmarks/WRTBench-git/webGL/Cyor/")

        type = self.driver.execute_script(self.TYPE)
        if type:
            return 0

        time.sleep(5)	

        ratio = self.driver.find_element_by_id(self._id)
        ratio.click()	
		
        elem = self.driver.find_element_by_tag_name("button")
        elem.click()
		
        time.sleep(300)

        wait.WebDriverWait(self.driver, 1200, 30).until(lambda x: x.execute_script(self.CURRENT))
        fps = 0.0
        for i in range(len(self.tests)):	
            elem = self.driver.find_element_by_id(self.tests[i])
            str = elem.text
            print str		
            start = str.find("(") + 1
            end = str.find(")")
            str = str[start:end].strip()
            fps = float(str) + fps
        return round(fps, 2)	