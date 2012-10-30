import logging
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import wait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from benchmark import *
        
class WebMark(object):
    def setup(self, browser='chrome'):
        rs_path = 'benchmark_test_results/'
        if not os.path.exists(rs_path):
            os.mkdir(rs_path)
            
        now = time.localtime()
        strTime = time.strftime('%Y-%m-%d_%H_%M_%S', now)
        self.logf = file(rs_path + browser + '_result_' + strTime + '.log', 'w')
        
        if browser == 'chrome':
            self.chrome_setup()
        elif browser == 'ie':
            self.ie_setup()
        elif browser == 'firefox':
            self.firefox_setup()
        else:
            self.chrome_setup()
        return self.driver
    
    def teardown(self):
        self.logf.close()
        

    def chrome_setup(self):
        option = Options()
    #   path = '/home/pinger/chromium/src/out/Release/chrome'
        path = 'chrome'
    #   option.binary_location = path
        option.add_argument("--proxy-server=http://proxy.pd.intel.com:911")
        self.driver = webdriver.Chrome(chrome_options=option)
        
    def ie_setup(self):
        self.driver = webdriver.Ie()
        
    def firefox_setup(self):
        PROXY_HOST = "proxy.pd.intel.com"
        PROXY_PORT = 911
        fp = webdriver.FirefoxProfile()
        fp.set_preference("network.proxy.type", 1)
        fp.set_preference("network.proxy.http", PROXY_HOST)
        fp.set_preference("network.proxy.http_port", PROXY_PORT)
        fp.set_preference("network.proxy.ftp", PROXY_HOST)
        fp.set_preference("network.proxy.ftp_port", PROXY_PORT)
        fp.set_preference("network.proxy.ssl", PROXY_HOST)
        fp.set_preference("network.proxy.ssl_port", PROXY_PORT)
        fp.set_preference("network.proxy.no_proxies_on", "localhost,127.0.0.1") 
        self.driver = webdriver.Firefox(fp)    
        
    def test(self, tc):
        benchmark = eval(tc + '(self.driver,self.logf)')
        benchmark.run()
        
    def test_suite_run(self):
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



def usage():
    print "usage:"
    print "   webmark.py [browser]"
    print "   [browser] in ('chrome', 'ie', 'firefox')"
    
#if __name__=="__main__" :
browser = 'chrome'
if len(sys.argv) > 1 :
    if not sys.argv[1] in ('chrome', 'ie', 'firefox') :
        usage()
        sys.exit(1)
    else :
        browser = sys.argv[1]

logging.basicConfig(level=logging.DEBUG)
webmark =  WebMark()
driver = webmark.setup(browser)
webmark.test_suite_run() 
driver.quit() 
webmark.teardown() 
#print "finished"    
