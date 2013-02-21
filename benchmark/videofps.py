import time
from common.exceptions import WebMarkException
from benchmark import Benchmark

class VideoFPS(Benchmark):
    ENDED = 'return document.getElementById("video_frame").ended'
    PLAY = 'return document.getElementById("video_frame").play()'
    _SUITES = ("fullscreen", "non-fullscreen")

    def __init__(self, suite = 'fullscreen'):
        if suite in self._SUITES:
            self.suite = suite
        else:
            raise WebMarkException("Unsupported suite %s, "
            "should be one of 'fullscreen', 'non-fullscreen'." % suite)
  
        Benchmark.__init__(self)

    @property
    def name(self):
        return "VideoFPS %s" % self.suite

    @property
    def metric(self):
        return "fps"

    @property
    def default_url(self):
        return "http://pnp.sh.intel.com/html5_video/"
      
    @property
    def default_timeout(self):
        return 1800

    @property
    def expect_time(self):
        return 0
  
    def start(self, driver):
        if driver.name.find("internet explorer") !=-1:
            raise WebMarkException("internet explorer does not support VideoFPS")

        time.sleep(1)

        for i in range(1,8):
            driver.find_element_by_id("right_click").click()
            time.sleep(1)

        driver.find_element_by_id("thumb_2").click()
        time.sleep(1)

        if self.suite.lower() == "fullscreen":			
            driver.find_element_by_id("fullscreen-button").click()
            time.sleep(1)
        driver.execute_script(self.PLAY)	

    def chk_finish(self, driver):
        return driver.execute_script(self.ENDED)

    def get_result(self, driver):
        str = driver.find_element_by_id("result").text	
        print str
        start = str.find(":") + 1
        str = str[start:].strip()	
        return float(str)
