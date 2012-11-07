class Benchmark(object):
    def __init__(self, driver, logf):
        self.driver = driver
        self.logf = logf
    
    @property
    def webdriver(self):
        return self.driver

    @webdriver.setter
    def webdriver(self, driver):
        self.driver = driver

    @property
    def log_file(self):
        return self.logf

    @log_file.setter
    def log_file(self, logf):
        self.logf = logf