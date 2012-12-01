import time
from selenium.webdriver.support import wait
from benchmark import Benchmark
from common.exceptions import WebMarkException

class HTML5MyAlbum(Benchmark):
    _SUITES = {
        "slideshow" : "cb_slide_show",
        "zoom" : "cb_zoom",
        "grayscale" : "cb_gray_scale",
		"fancyshow" : "cb_fancy_show"
    }

    def __init__(self, driver, logf, suite = 'slideshow'):
        if self._SUITES.has_key(suite.lower()):
            self.suite = suite
        else:
            raise WebMarkException("Unsupported suite %s, "
            "should be one of 'slideshow', 'zoom', 'grayscale', 'fancyshow'." % suite)
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "HTML5MyAlbum %s" % self.suite

    @property
    def metric(self):
        return "ms"    

    @property
    def _id(self):
        return self._SUITES[self.suite.lower()]        
		
    def run(self):
        self.open("http://pnp.sh.intel.com/benchmarks/WRTBench-git/canvas2D/myalbum/")
        time.sleep(5)	

        ratio = self.driver.find_element_by_id("cb_all")
        ratio.click()
        ratio = self.driver.find_element_by_id(self._id)
        ratio.click()	
				
        elem = self.driver.find_element_by_tag_name("button")
        elem.click()

        wait.WebDriverWait(self.driver, 1200, 30).until(lambda x: x.current_url.lower().find("result.html") != -1)
        elem = self.driver.find_element_by_class_name("cont_primary_metric")
        str = elem.text
        print str
        start = str.find("=") + 1
        end = str.find("ms")
        str = str[start:end].strip()
        print str
        fps = float(str)
        return round(fps, 2)	