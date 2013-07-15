from google.chromedriver import WebDriver as GoogleWebDriver
from google.chromedriver_launcher import ChromeDriverLauncher as GoogleChromeDriverLauncher
from selenium.webdriver.support.wait import WebDriverWait

class ChromeDriver(GoogleWebDriver):
    def __init__(self, browser):
        driver_path = browser.driver
        binary = browser.path
        self.server = GoogleChromeDriverLauncher(driver_path).Launch()
        capabilities = {}
        capabilities['chrome.binary'] = binary

        switches = []
        proxy = browser.proxy
        if proxy.type == 'direct':
            switches.append("--no-proxy-server")
        elif proxy.type == 'manual':
            s = ''
            if hasattr(proxy, 'ftp'):
                s += proxy.ftp + ';'
            if hasattr(proxy, 'http'):
                s = proxy.http + ';'
            if hasattr(proxy, 'ssl'):
                s = proxy.ssl + ';'
            if s:
                switches.append('--proxy-server=' + s)
            if hasattr(proxy, 'noproxy'):
                switches.append(' --proxy-bypass-list=' + proxy.noproxy)
        elif proxy.type == 'pac':
            switches.append('--proxy-pac-url=' + proxy.proxy_autoconfig_url)
        elif proxy.type == 'autodetect':
            switches.append('--proxy-auto-detect')
        #elif proxy.type == 'system':

        if hasattr(browser, 'switches'):
            switches.append(browser.switches)

        capabilities['chrome.switches'] = switches
        super(ChromeDriver, self).__init__(self.server.GetUrl(), capabilities)

    def get_new_window_handle(self, old_handles):
        handles = self.window_handles
        if len(handles) > 0:
            new_handles = filter(lambda handle: handle not in old_handles, handles)
            if len(new_handles) == 1:
                return new_handles[0]
            raise WebDriverException('More than one new windows')
        return None

    def switch_to_new_window(self, old_handles):
        def new_window(driver):
            return driver.get_new_window_handle(old_handles)
        new_handle = WebDriverWait(self, 10).until(new_window)
        self.switch_to_window(new_handle)

    def quit(self):
        super(ChromeDriver, self).quit()
        self.server.Kill()