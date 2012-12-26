import time
from benchmark import Benchmark

class AudioLatency(Benchmark):
    TABLE = 'return document.getElementById("table").innerHTML'

    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "AudioLatency"

    @property
    def metric(self):
        return "ms"

    @property
    def default_url(self):
        return "http://pnp.sh.intel.com/benchmarks/WRTBench-git/audio/AudioLatency/"

    @property
    def default_timeout(self):
        return 300

    @property
    def expect_time(self):
        return 60

    def start(self, driver):
        if self.driver.name.find("internet explorer") !=-1 or self.driver.name.find("firefox") !=-1:
            raise WebMarkException("internet explorer/firefox does not support AudioWorker")

    def chk_finish(self, driver):
        return driver.execute_script(self.TABLE).find("Total Latency") != -1

    def get_result(self, driver):
        str = self.driver.find_elements_by_tag_name("td")[27].text
        str = str.strip()
        print str		
        return float(str)