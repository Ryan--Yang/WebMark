from selenium.webdriver import Ie as IeDriver

class WebDriver(IeDriver):  
    def stop_service(self):
        self.quit()
