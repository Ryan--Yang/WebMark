﻿import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class GUIMark3Vector(Benchmark):
    def __init__(self, driver, logf):
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "GUIMark3 vector"

    @property
    def metric(self):
        return "fps"

    def run(self):
        self.open("http://www.craftymind.com/factory/guimark3/vector/GM3_JS_Vector.html")
        elem = self.driver.find_element_by_id("testlabel")
        fps = 0.0
        for i in range(1,16):
            time.sleep(20)
            str = elem.text
            start = str.find(":") + 1
            end = str.find("fps")
            str = str[start:end].strip()
            fps += (float(str) - fps) / i            
        return round(fps, 2)