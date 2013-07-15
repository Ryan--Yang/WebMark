import shutil
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver

class FirefoxDriver(WebDriver):
    def __init__(self, browser):
        binary = FirefoxBinary(browser.path)
        self.profile = webdriver.FirefoxProfile()

        proxy = browser.proxy
        if proxy.type == 'direct':
            self.profile.set_preference('network.proxy.type', 1)
        elif proxy.type == 'manual':
            self.profile.set_preference('network.proxy.type', 1)
            self.profile.set_preference('network.proxy.http', 'proxy-shz.intel.com')
            self.profile.set_preference('network.proxy.http_port', 911)
            if hasattr(proxy, 'noproxy'):
                self.profile.set_preference("network.proxy.no_proxies_on", proxy.noproxy)

        self.driver = super(FirefoxDriver, self).__init__(firefox_profile=self.profile, firefox_binary=binary)
    def __del__(self):
        self.driver.quit()
        shutil.rmtree(self.profile.path)