import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class WebTouch(Benchmark):
    TYPE = 'return browserType.ie'
    DETAIL = 'return document.getElementById("bws_panel_control_panel_web_touch__result_summary").innerHTML'

    def __init__(self, driver, logf):
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "WebTouch"

    @property
    def metric(self):
        return "fps"
        
    @property
    def extra_chrome_args(self):
        return ['--enable-touch-events']

			
    def run(self):
        type = self.driver.execute_script(self.TYPE)
        if type:
            return 0

        self.open("http://pnp.sh.intel.com/benchmarks/BWS/workload/webtouch/src/web_touching.html")
        time.sleep(5)
        elem = self.driver.find_elements_by_class_name("bws_c_rpt_item")
        elem[0].click()
        elem = self.driver.find_elements_by_class_name("bwc_c_rpa_button")
        elem[0].click()

        wait.WebDriverWait(self.driver, 300, 30).until(lambda x: x.execute_script(self.DETAIL).find("Primary Metrix") != -1)	
        str = self.driver.execute_script(self.DETAIL)
		
        start = str.find(":") + 1
        end = str.find("(")
        str = str[start:end].strip()
        print str
        fps = float(str)
        return fps