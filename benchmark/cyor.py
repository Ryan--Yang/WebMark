import time
from common.exceptions import WebMarkException
from benchmark import Benchmark

class Cyor(Benchmark):
    tests = ("Triangles", "Pyramids", "Cubes", "Blending", "Spheres", "Lights", "Mass")
    CURRENT = 'return currentTest == 8'
	
    _STYLES = {
        "low" : "styleLow",
        "medium" : "styleMedium",
        "high" : "styleHigh"
    }

    def __init__(self, style = 'medium'):
        if self._STYLES.has_key(style.lower()):
            self.style = style
        else:
            raise WebMarkException("Unsupported style %s, "
            "should be one of 'low', 'medium', 'high'." % style)
        Benchmark.__init__(self)

    @property
    def name(self):
        return "Cyor %s" % self.style

    @property
    def metric(self):
        return "score"      

    @property
    def default_url(self):
        return "http://pnp.sh.intel.com/benchmarks/WRTBench-git/webGL/Cyor/"

    @property
    def _id(self):
        return self._STYLES[self.style.lower()]     
		
    @property
    def default_timeout(self):
        return 1500

    @property
    def expect_time(self):
        return 300

    def start(self, driver):
        if driver.name.find("internet explorer") !=-1:
            raise WebMarkException("internet explorer does not support Cyor")
        driver.find_element_by_id(self._id).click()
        driver.find_element_by_tag_name("button").click()

    def chk_finish(self, driver):
        return driver.execute_script(self.CURRENT)

    def get_result(self, driver):
        fps = 0.0
        for i in range(len(self.tests)):	
            elem = driver.find_element_by_id(self.tests[i])
            str = elem.text
            print str		
            start = str.find("(") + 1
            end = str.find(")")
            str = str[start:end].strip()
            fps = float(str) + fps
        return round(fps, 2)	