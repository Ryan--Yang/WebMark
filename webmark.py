import logging
import time
import os
import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import wait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from common import utils
from benchmark.test import Test1,Test2,Test3
from benchmark import *

        
class WebMark(object) :
    def __init__(self):
        rs_path = 'benchmark_test_results/'
        if not os.path.exists(rs_path):
            os.mkdir(rs_path)
            
        now = time.localtime()
        strTime = time.strftime('%Y-%m-%d_%H_%M_%S', now)
        self.logf = file(rs_path + 'result_' + strTime + '.log', 'w')

    def __del__(self) :
        self.logf.close()

    def _suite_setup(self, browser='chrome', binary=None, proxy=None) :
        self.logf.write("-------------------- " + browser + " --------------------\n")
        if browser == 'chrome':
            self.chrome_setup(binary=binary, proxy=proxy)
        elif browser == 'ie':
            self.ie_setup()
        elif browser == 'firefox':
            self.firefox_setup(binary=binary, proxy=proxy)
        else:
            self.chrome_setup(binary=binary, proxy=proxy)
            
        self.driver.maximize_window()
    
    def _suite_teardown(self) :
        try:
            self.driver.quit()
        except:
            pass
        

    def chrome_setup(self, binary=None, proxy=None) :
        option = Options()
        if binary is not None:
            option.binary_location = binary
        if proxy is not None:
            utils.add_proxy_to_chrome_options(proxy, option)
    #    self.driver = ChromeDriver(binary=binary, proxy=proxy)
        self.driver = webdriver.Chrome(chrome_options = option)
        
    def ie_setup(self) :
        #self.driver = IeDriver(proxy=proxy)
        self.driver = webdriver.Ie()
        
    def firefox_setup(self, binary=None, proxy=None) :
        firefox_binary = FirefoxBinary(binary)
        firefox_profile = webdriver.FirefoxProfile()
        if proxy is not None:
            firefox_profile.set_proxy(utils.proxy_raw_format(proxy))
        self.driver = webdriver.Firefox(firefox_profile=firefox_profile, firefox_binary=firefox_binary)
        #self.driver = FirefoxDriver(binary=binary, proxy=proxy)    
        
    def test(self, tc) :
        benchmark = eval(tc + '(self.driver,self.logf)')
        benchmark.run()
        
    def test_suite_run(self) :
        self.test('SunSpider')
        self.test('V8BenchmarkSuite')
        self.test('FishIETank')
        self.test('Octane')
        self.test('GUIMark3Bitmap')
        self.test('GUIMark3BitmapCache')
        self.test('GUIMark3Vector')
        self.test('DromaeoAllJavascriptTests')
        self.test('DromaeoAllDOMTests')
        self.test('BrowserMark')
        self.test('Peacekeeper')
        self.test('SpeedReading')
        self.test('Kraken')
        self.test('Galactic')
        
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

            self._suite_setup(browser=browser, binary=binary, proxy=proxy)
 
            for benchmark in suite['benchmarks'] :
                self.test(benchmark['name'])
            self._suite_teardown()
        config.close()

def usage() :
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