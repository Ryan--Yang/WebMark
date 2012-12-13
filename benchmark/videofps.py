import time
from selenium.webdriver.support import wait
from benchmark import Benchmark
from common.exceptions import WebMarkException

class VideoFPS(Benchmark):
    ENDED = 'return document.getElementById("video_frame").ended'
    PLAY = 'return document.getElementById("video_frame").play()'

    _SUITES = {
        "fullscreen" : "http://pnp.sh.intel.com/html5_video/",
        "non-fullscreen" : "http://pnp.sh.intel.com/html5_video/"
    }

    def __init__(self, driver, logf, appmode=False, suite = 'fullscreen'):
        if self._SUITES.has_key(suite.lower()):
            self.suite = suite
        else:
            raise WebMarkException("Unsupported suite %s, "
            "should be one of 'fullscreen', 'non-fullscreen'." % suite)
        Benchmark.__init__(self, driver, logf, appmode)

    @property
    def name(self):
        return "VideoFPS %s%s" % (self.suite, self.name_common_ext())

    @property
    def metric(self):
        return "fps"
     
    @property
    def _url(self):
        return self._SUITES[self.suite.lower()]       

    def run(self):
        if self.driver.name.find("internet explorer") !=-1:
            return 0

        self.open(self._url)
        time.sleep(5)

        if self.suite.lower() == "fullscreen":			
            elem = self.driver.find_element_by_id("fullscreen-button")
            elem.click()
            time.sleep(5)

        self.driver.execute_script(self.PLAY)		
		
        wait.WebDriverWait(self.driver, 600, 30).until(lambda x: x.execute_script(self.ENDED))	
        elem = self.driver.find_element_by_id("result")	
        str = elem.text
        print str
        start = str.find(":") + 1
        str = str[start:].strip()	
        return float(str)
