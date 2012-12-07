import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class BBench(Benchmark):
    Avg_Geo_Mean = 'return bbSiteAvgGeoMean'

    def __init__(self, driver, logf, appmode=False):
        Benchmark.__init__(self, driver, logf, appmode)

    @property
    def name(self):
        return "BBench%s" % self.name_common_ext()

    @property
    def metric(self):
        return "ms"
        
    def run(self):
        self.open("http://pnp.sh.intel.com/benchmarks/WRTBench-git/htmlRendering/bbench/")
        time.sleep(5)
        elem = self.driver.find_element_by_tag_name("button")
        elem.click()

        wait.WebDriverWait(self.driver, 1200, 10).until(lambda x: x.current_url.lower().find("result") != -1)
        res = self.driver.execute_script(self.Avg_Geo_Mean)
        print res
        return round(res, 2)