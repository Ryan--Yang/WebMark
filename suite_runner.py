from benchmark_runner import BenchmarkRunner
from browser import Browser
from common.exceptions import WebMarkException

class SuiteRunner(object):
    def __init__(self, logf, browser_name, configure):
        self.logf = logf
        self.browser_name = browser_name
        self._parse_configure(configure)

    def _parse_configure(self, conf):
        if not conf.has_key('benchmarks'):
            raise WebMarkException("Configure error: "
                "No benchmarks in suite %s" % self.browser_name)        
        self.binary = None
        self.proxy = None
        self.benchmarks = conf['benchmarks']
        if conf.has_key('binary') and conf['binary'] is not None:
            self.binary = conf['binary']
        if conf.has_key('proxy') and conf['proxy'] is not None:
            self.proxy = conf['proxy']
            
    def run(self):
        self.logf.write("-------------------- " + self.browser_name + " --------------------\n")
        browser = Browser(name = self.browser_name, binary = self.binary, 
                            proxy = self.proxy)
        for benchmark in self.benchmarks:
            BenchmarkRunner(self.logf, benchmark, browser).run()
