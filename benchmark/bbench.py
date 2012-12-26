import time
from benchmark import Benchmark

class BBench(Benchmark):
    Avg_Geo_Mean = 'return bbSiteAvgGeoMean'

    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "BBench"

    @property
    def metric(self):
        return "ms"

    @property
    def default_url(self):
        return "http://pnp.sh.intel.com/benchmarks/WRTBench-git/htmlRendering/bbench/"

    @property
    def default_timeout(self):
        return 1500

    def start(self, driver):
        time.sleep(5)
        driver.find_element_by_tag_name("button").click()

    def chk_finish(self, driver):
        return driver.current_url.lower().find("results.html") != -1

    def get_result(self, driver):
        res = driver.execute_script(self.Avg_Geo_Mean)
        print res
        return round(res, 2)