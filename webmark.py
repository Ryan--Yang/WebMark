import logging
import time
import os
import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import wait
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from common.chrome_options import Options
from common.exceptions import WebMarkException
from common import utils
from common.chromedriver import WebDriver as ChromeDriver

class WebMark(object):
    def __init__(self):
        rs_path = 'benchmark_test_results/'
        if not os.path.exists(rs_path):
            os.mkdir(rs_path)

        now = time.localtime()
        strTime = time.strftime('%Y-%m-%d_%H_%M_%S', now)
        self.logf = file(rs_path + 'result_' + strTime + '.log', 'w')
        self.driver = None

    def __del__(self):
        self.logf.close()

    def _suite_setup(self, browser='chrome', binary=None, proxy=None):
        self.browser = browser
        self.binary = binary
        self.proxy = proxy

    def _driver_quit(self):
        try:
            self.driver.quit()
            self.driver = None
        except Exception, e:
            print e
            pass
        time.sleep(1)

    def _suite_teardown(self):
        if self.driver is not None:
            self._driver_quit()
        self.driver = None
        self.browser = None
        self.binary = None
        self.proxy = None

    def _driver_start(self):
        if self.driver is not None:
            self._driver_quit()
        if self.browser == 'chrome':
            self.chrome_setup(binary=self.binary, proxy=self.proxy)
        elif self.browser == 'ie':
            self.ie_setup(proxy=self.proxy)
        elif self.browser == 'firefox':
            self.firefox_setup(binary=self.binary, proxy=self.proxy)
        else:
            self.chrome_setup(binary=self.binary, proxy=self.proxy)

        self.driver.maximize_window()

    def chrome_setup(self, binary=None, proxy=None):
        option = Options()
        if binary is not None:
            option.binary_location = binary
        if proxy is not None:
            utils.add_proxy_to_chrome_options(proxy, option)
    #    self.driver = ChromeDriver(binary=binary, proxy=proxy)
    #    self.driver = webdriver.Chrome(chrome_options = option)
    #    option.add_argument('--app=http://www.webkit.org/perf/sunspider-0.9.1/sunspider-0.9.1/driver.html')
        self.driver = ChromeDriver(chrome_options = option)

    def ie_setup(self, proxy=None):
        #self.driver = IeDriver(proxy=proxy)
        if proxy is not None:
            utils.set_ie_proxy(proxy)
        self.driver = webdriver.Ie()

    def firefox_setup(self, binary=None, proxy=None) :
        firefox_binary = FirefoxBinary(binary)
        firefox_profile = webdriver.FirefoxProfile()
        if proxy is not None:
            firefox_profile.set_proxy(utils.proxy_raw_format(proxy))
        self.driver = webdriver.Firefox(firefox_profile=firefox_profile, firefox_binary=firefox_binary)
        #self.driver = FirefoxDriver(binary=binary, proxy=proxy)

    def _setup_benchmark(self, tc):
        if (not tc.has_key('name')) or tc['name'] is None:
            self._print("Error: Has no name attribute in configure file")
            return None

        name = tc['name']
        try:
            exec 'from benchmark import ' + name
        except ImportError:
            self._print(name + ": Import module error.")
            return None

        args = 'self.driver,self.logf'
        if tc.has_key('args') and tc['args'] is not None:
            args += ', **tc["args"]'

        try:
            benchmark = eval(name + '(' + args + ')')
        except TypeError:
            self._print(name + ": unsupported argument.")
            return None
        except WebMarkException, e:
            self._print(name + ": " + str(e))
            return None

        return benchmark
    
    def _result_str(self, rs):
        if rs == 0.0:
            return 'N/A'
        if isinstance(rs, basestring):
            return rs
        if not isinstance(rs, list):
            return str(round(rs, 2))
        if len(rs) == 0:
            return 'N/A'
        result = str(round(rs[0], 2))
        for k in range(1,len(rs)):
            result += '/' + str(round(rs[k], 2))
        return result

    def test(self, tc):
        benchmark = self._setup_benchmark(tc)
        if benchmark is None:
            return

        print "Run %s ..." % benchmark.name
        times = 1
        if tc.has_key('runTimes') and isinstance(tc['runTimes'], int) and tc['runTimes'] > 1:
            times = tc['runTimes']
        omit_begin_times = 0
        if tc.has_key('omitBegin') and isinstance(tc['omitBegin'], int) and tc['omitBegin'] > 0:
            omit_begin_times = tc['omitBegin']
        omit_end_times = 0
        if tc.has_key('omitEnd') and isinstance(tc['omitEnd'], int) and tc['omitEnd'] > 1:
            omit_end_times = tc['omitEnd']
        if omit_end_times + omit_begin_times >= times:
            self._print(benchmark.name + ": warning, omitBegin or omitEnd too big.")
            return

        rs_avg = 0.0
        valid_times = 0
        for i in range(1,times + 1):
            try:
                self._driver_start()
                benchmark.webdriver = self.driver
                rs = benchmark.run()
                if times > 1:
                    if i > omit_begin_times and i <= times - omit_end_times:
                        valid_times += 1
                        if valid_times == 1:
                            rs_avg = rs
                        elif isinstance(rs, list):
                            for j in range(len(rs)):
                                rs_avg[j] += (rs[j] - float(rs_avg[j])) / valid_times
                        else:
                            rs_avg += (rs - float(rs_avg)) / valid_times
                else:
                    rs_avg = rs
            except Exception, e:
                rs = "N/A"
                print "Exception:", e

            print "Turn %d:rs=%s, avg=%s" % (i, self._result_str(rs), self._result_str(rs_avg))

        self._print("%s: %s %s" % (benchmark.name, self._result_str(rs_avg), benchmark.metric))

    def benchmarks_run(self, conf_file) :
        config = file(conf_file)
        suites = json.load(config)
        for browser in suites :
            suite = suites[browser]

            binary = None
            proxy = None
            if suite.has_key('binary') and suite['binary'] is not None:
                binary = suite['binary']
            if suite.has_key('proxy') and suite['proxy'] is not None:
                proxy = suite['proxy']

            self.logf.write("-------------------- " + browser + " --------------------\n")
            self._suite_setup(browser=browser, binary=binary, proxy=proxy)

            for benchmark in suite['benchmarks']:
                self.test(benchmark)
            self._suite_teardown()
        config.close()

    def _print(self, str):
        print str
        self.logf.write(str + "\n")

def usage():
    print "usage: webmark.py [config]"

#if __name__=="__main__" :

conf_file = 'config.json'
if len(sys.argv) > 1:
    conf_file = sys.argv[1]
if not os.path.isfile(conf_file):
    print conf_file, "is not a file."
    usage()
    sys.exit(1)

#logging.basicConfig(level=logging.DEBUG)
WebMark().benchmarks_run(conf_file)

#print "finished"
