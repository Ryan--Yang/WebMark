import logging
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import wait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class SunSpider(object):
    def __init__(self, driver, logf):
        self.driver = driver
        self.logf = logf
        
    def run(self):
        print "Run SunSpider benchmark..."
        self.driver.get("http://www.webkit.org/perf/sunspider-0.9.1/sunspider-0.9.1/driver.html")
        wait.WebDriverWait(self.driver, 120).until(lambda x: x.current_url.lower().find("result") != -1)
        elem = self.driver.find_element_by_id("console")
        str = elem.text
        pos = str.find("Total:")+len("Total:")
        str = str[pos:].strip()
        pos = str.find("ms")+2
        self.logf.write("SunSpider: " + str[:pos] + "\n")
        
class V8BenchmarkSuite(object):
    def __init__(self, driver, logf):
        self.driver = driver
        self.logf = logf
        
    def run(self):
        print "Run V8 Benchmark Suite..."
        self.driver.get("http://octane-benchmark.googlecode.com/svn/latest/index.html")
        self.driver.find_element_by_id("run-octane").click()
        elem = self.driver.find_element_by_id("main-banner")
        wait.WebDriverWait(self.driver, 1200).until(lambda x: elem.text.find("Score:") != -1)
        str = elem.text
        pos = str.find(":") + 1
        str = str[pos:].strip()
        self.logf.write("V8 Benchmark Suite: " + str[:pos] + "\n")
        
class FishIETank(object):
    def __init__(self, driver, logf):
        self.driver = driver
        self.logf = logf

    def run(self):
        print "Run FishIE Tank benchmark..."
        self.driver.get("http://ie.microsoft.com/testdrive/Performance/FishIETank/Default.html")
        elem = self.driver.find_element_by_id("fpsCanvas")
        fps = 0.0
        time.sleep(10)
        for i in range(1,11):
            str = elem.get_attribute("title").lower()
            start = str.find("at") + 2
            end = str.find("fps")
            str = str[start:end].strip()
            print str
            fps += (int(str) - fps) / i
            time.sleep(6)
        self.logf.write("FishIE Tank (20 fish): %.2f%s\n" % (fps, "FPS"))
        
class BentchmarkAuto(object):
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



def usage():
    print "usage:"
    print "   benchmark_auto.py [browser]"
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
bentchmark_auto =  BentchmarkAuto()
driver = bentchmark_auto.setup(browser)
bentchmark_auto.test_suite_run() 
driver.quit() 
bentchmark_auto.teardown() 
#print "finished"    