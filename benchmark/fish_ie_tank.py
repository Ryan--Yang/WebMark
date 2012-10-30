import time
from selenium.webdriver.support import wait

class FishIETank(object):
    def __init__(self, driver, logf):
        self.driver = driver
        self.logf = logf

    def run(self):
        print "Run FishIE Tank benchmark..."
        self.driver.get("http://ie.microsoft.com/testdrive/Performance/FishIETank/Default.html")
        elem = self.driver.find_element_by_id("fpsCanvas")
        fps = 0.0
        time.sleep(20)
        for i in range(1,16):
            str = elem.get_attribute("title").lower()
            start = str.find("at") + 2
            end = str.find("fps")
            str = str[start:end].strip()
            fps += (int(str) - fps) / i
            time.sleep(20)
        self.logf.write("FishIE Tank (20 fish): %.2f%s\n" % (fps, "FPS"))