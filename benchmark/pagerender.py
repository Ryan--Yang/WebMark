import time
from benchmark import Benchmark

class PageRender(Benchmark):
    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "PageRender"

    @property
    def metric(self):
        return "s"

    @property
    def default_url(self):
        return "http://pnp.sh.intel.com/benchmarks/WRTBench-git/htmlRendering/PageRender/iterations_rev11_new.html"

    @property
    def default_timeout(self):
        return 1500

    def chk_finish(self, driver):
        elem = driver.find_elements_by_tag_name("p")
        return len(elem)

    def get_result(self, driver):
        elem = self.driver.find_element_by_xpath("//div/p")
        str = elem.text
        pos = str.find("The Final Result is") + len("The Final Result is")
        str = str[pos:].strip()
        print str
        res = float(str)
        return round(res, 2)