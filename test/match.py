import time
import platform
import argparse
from selenium import webdriver

system = platform.system()

def test():
    if args.browser == 'chrome':
        binary_path = ''
        driver_path = ''

        if system == 'Linux':
            binary_path = '/usr/bin/google-chrome'
            driver_path = '/workspace/project/gyagp/WebMark/third_party/webdriver/chromedriver/chromedriver'
        elif system == 'windows':
            binary_path = ''
            driver_path = ''

        exec 'import selenium.webdriver.chrome.service as service'
        exec 'from selenium import webdriver'
        service = service.Service(driver_path)
        service.start()
        capabilities = {'chrome.binary': binary_path}
        driver = webdriver.Remote(service.service_url, capabilities)
    elif args.browser == 'firefox':
        binary_path = '/usr/bin/firefox'
        exec 'from selenium.webdriver.firefox.webdriver import WebDriver'
        exec 'from selenium.webdriver.firefox.firefox_binary import FirefoxBinary'
        exec 'from selenium.webdriver.firefox.firefox_profile import FirefoxProfile'
        firefox_binary = FirefoxBinary(binary_path)
        firefox_profile = FirefoxProfile('./')
        driver = WebDriver(firefox_profile=firefox_profile, firefox_binary=firefox_binary)
    elif args.browser == 'ie':
        pass

    driver.get('http://localhost');
    time.sleep(2)
    driver.close()

if __name__== '__main__':
    # Handle options
    parser = argparse.ArgumentParser(description = 'Test to see if browser binary and driver match with each other',
                                     formatter_class = argparse.RawTextHelpFormatter,
                                     epilog = '''
examples:
  python %(prog)s config.json

''')

    parser.add_argument('-b', '--browser', dest='browser', help='browser to test', choices=['chrome', 'firefox', 'ie'], default='chrome')

    args = parser.parse_args()

    test()