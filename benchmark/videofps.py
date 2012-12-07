import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class VideoFPS(Benchmark):
    ENDED = 'return document.getElementById("video_frame").ended'
    PLAY = 'return document.getElementById("video_frame").play()'

    def __init__(self, driver, logf, appmode=False):
        Benchmark.__init__(self, driver, logf, appmode)

    @property
    def name(self):
        return "VideoFPS%s" % self.name_common_ext()

    @property
    def metric(self):
        return "fps"
        
    def run(self):
        if self.driver.name.find("internet explorer") !=-1:
            return 0

        self.open("http://pnp.sh.intel.com/html5_video/")
        time.sleep(10)
			
        self.driver.execute_script(self.PLAY)		
		
        wait.WebDriverWait(self.driver, 600, 30).until(lambda x: x.execute_script(self.ENDED))	
        elem = self.driver.find_element_by_id("result")	
        str = elem.text
        print str
        start = str.find(":") + 1
        str = str[start:].strip()	
        return float(str)		