import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class CanvasPerf(Benchmark):
    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "CanvasPerf(Canvas 2D)"

    @property
    def metric(self):
        return "score"

    @property
    def default_url(self):
        return "http://flashcanvas.net/examples/dl.dropbox.com/u/1865210/mindcat/canvas_perf.html"      
        #return "file:///C:/Users/perf/Desktop/canvasperf/canvas_perf.html"    

    @property
    def expect_time(self):
        return 120

    @property
    def default_timeout(self):
        return 600

    def start(self, driver):    
        self.driver.find_element_by_xpath("//button[@onclick='demo.stop();perf.start()']").click()
        self.output = driver.find_element_by_id("output")        

    def chk_finish(self, driver):
        print self.output.text  
        return self.output.text.find("Total Score:") != -1
        
    def get_result(self, driver):
        str = self.output.text 
        pos1 = str.find("Total Score:") + len("Total Score:")
        str = str[pos1:].strip()   
        return float(str)
