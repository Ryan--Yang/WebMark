import time
from common.exceptions import WebMarkException
from benchmark import Benchmark

class HTML5MyAlbum(Benchmark):
    _SUITES = {
        "slideshow" : "cb_slide_show",
        "zoom" : "cb_zoom",
        "grayscale" : "cb_gray_scale",
	"fancyshow" : "cb_fancy_show"
    }

    def __init__(self, suite = 'slideshow'):
        if self._SUITES.has_key(suite.lower()):
            self.suite = suite
        else:
            raise WebMarkException("Unsupported suite %s, "
            "should be one of 'slideshow', 'zoom', 'grayscale', 'fancyshow'." % suite)
        Benchmark.__init__(self)

    @property
    def name(self):
        return "HTML5MyAlbum %s" % self.suite

    @property
    def metric(self):
        return "ms"    

    @property
    def default_url(self):
        return "http://pnp.sh.intel.com/benchmarks/WRTBench-git/canvas2D/myalbum/"

    @property
    def _id(self):
        return self._SUITES[self.suite.lower()]        
		
    @property
    def default_timeout(self):
        return 600

    @property
    def expect_time(self):
        return 0

    def start(self, driver):
        time.sleep(5)	
        driver.find_element_by_id("cb_all").click()
        driver.find_element_by_id(self._id).click()		
        driver.find_element_by_tag_name("button").click()

    def chk_finish(self, driver):
        return driver.current_url.lower().find("result.html") != -1

    def get_result(self, driver):
        elem = driver.find_element_by_class_name("cont_primary_metric")
        str = elem.text
        print str
        start = str.find("=") + 1
        end = str.find("ms")
        str = str[start:end].strip()
        print str
        fps = float(str)
        return round(fps, 2)	