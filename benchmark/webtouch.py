import time
from benchmark import Benchmark

class WebTouch(Benchmark):
    DETAIL = 'return document.getElementById("bws_panel_control_panel_web_touch__result_summary").innerHTML'

    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "WebTouch"

    @property
    def metric(self):
        return "fps"

    @property
    def default_url(self):
        return "http://pnp.sh.intel.com/benchmarks/BWS/workload/webtouch/src/web_touching.html"

    @property
    def extra_chrome_args(self):
        return ['--enable-touch-events']

    @property
    def default_timeout(self):
        return 300

    @property
    def expect_time(self):
        return 0

    def start(self, driver):
        if self.driver.name.find("internet explorer") !=-1 or self.driver.name.find("firefox") !=-1:
            raise WebMarkException("internet explorer/firefox does not support WebGLModel")

        time.sleep(5)
        self.driver.find_elements_by_class_name("bws_c_rpt_item")[0].click()
        self.driver.find_elements_by_class_name("bwc_c_rpa_button")[0].click()


    def chk_finish(self, driver):
        return driver.execute_script(self.DETAIL).find("Primary Metrix") != -1

    def get_result(self, driver):
        str = driver.execute_script(self.DETAIL)
        start = str.find(":") + 1
        end = str.find("(")
        str = str[start:end].strip()
        print str
        fps = float(str)
        return fps
