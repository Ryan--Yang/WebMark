import shutil
from selenium.webdriver import Firefox as FirefoxDriver

class WebDriver(FirefoxDriver):
    def stop_service(self):
        self.binary.kill()
        try:
            shutil.rmtree(self.profile.path)
        except Exception, e:
            print str(e)
