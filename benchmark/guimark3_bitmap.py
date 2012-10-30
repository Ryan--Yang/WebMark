import time
from selenium.webdriver.support import wait

class GUIMark3Bitmap(object):
    def __init__(self, driver, logf):
        self.driver = driver
        self.logf = logf

    def run(self):
        print "Run GUIMark3 bitmap benchmark..."
        self.driver.get("http://www.craftymind.com/factory/guimark3/bitmap/GM3_JS_Bitmap.html")
        elem = self.driver.find_element_by_id("testlabel")
        fps = 0.0
        time.sleep(20)
        for i in range(1,16):
            str = elem.text
            start = str.find(":") + 1
            end = str.find("fps")
            str = str[start:end].strip()
            print str
            fps += (float(str) - fps) / i
            time.sleep(20)
        self.logf.write("GUIMark3 bitmap: %.2f%s\n" % (fps, "FPS"))