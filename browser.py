import time
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from common.chrome_options import Options
from common import utils
from common.chromedriver import WebDriver as ChromeDriver
from common.iedriver import WebDriver as IeDriver
from common.firefoxdriver import WebDriver as FirefoxDriver

class Browser(object):
    def __init__(self, name='chrome', binary=None, proxy=None):
        self.name = name
        self.binary = binary
        self.proxy = proxy
        self.extra_arguments = None
        self.webdriver = None
        
    def __del__(self):
        self.stop()
        
    def start(self):
        if self.webdriver is not None:
            self._driver_quit()
        if self.name == 'chrome':
            self._chrome_setup()
        elif self.name == 'ie':
            self._ie_setup()
        elif self.name == 'firefox':
            self._firefox_setup()
        else:
            self._chrome_setup()
        self.webdriver.maximize_window()
        return self.webdriver

    def stop(self):
        if self.webdriver is not None:
            self._driver_quit()
    
    def stop_service(self):
        if self.webdriver is not None:
            try:
                self.webdriver.stop_service()
                self.webdriver = None
            except Exception, e:
                print e
                pass
            time.sleep(1)

    @property
    def driver(self):
        return self.webdriver
        
    @property
    def extra_args(self):
        return self.extra_arguments

    @extra_args.setter
    def extra_args(self, args):
        self.extra_arguments = args

    def _chrome_setup(self):
        option = Options()
        if self.binary is not None:
            option.binary_location = self.binary
        if self.proxy is not None:
            utils.add_proxy_to_chrome_options(self.proxy, option)
        if self.extra_arguments is not None:
            option.arguments.extend(self.extra_arguments)
        self.webdriver = ChromeDriver(chrome_options = option)

    def _ie_setup(self):
        if self.proxy is not None:
            utils.set_ie_proxy(self.proxy)
        self.webdriver = IeDriver()

    def _firefox_setup(self) :
        firefox_binary = FirefoxBinary(self.binary)
        firefox_profile = webdriver.FirefoxProfile()
        if self.proxy is not None:
            firefox_profile.set_proxy(utils.proxy_raw_format(self.proxy))
        self.webdriver = FirefoxDriver(firefox_profile=firefox_profile, firefox_binary=firefox_binary)
        
    def _driver_quit(self):
        try:
            self.webdriver.quit()
            self.webdriver = None
        except Exception, e:
            print e
            pass
        time.sleep(1)
