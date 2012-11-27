import os

class Benchmark(object):
    def __init__(self, driver, logf, appmode=False, offline=False):
        self.driver = driver
        self.logf = logf
        self.appmode = appmode
        self.offline = offline
    
    @property
    def webdriver(self):
        return self.driver

    @webdriver.setter
    def webdriver(self, driver):
        self.driver = driver

    @property
    def log_file(self):
        return self.logf
        
    @property
    def path(self):
        return os.path.dirname(os.path.realpath(__file__)) + '/'

    @property
    def webbench_path(self):
        return 'file:///' + self.path + 'WebBench/'
		
    @property
    def extra_chrome_args(self):
        return None


    def _appmode_str(self, with_comma=False):
        if self.appmode:
            if with_comma:
                return 'appmode,'
            return 'appmode'
        return ''

    def _offline_str(self, with_comma=False):
        if self.offline:
            if with_comma:
                return 'offline,'
            return 'offline'
        return ''
        
    def name_common_ext(self, with_comma=False):
        if (not self.appmode) and (not self.offline):
            return ''
        if with_comma:
            return self._appmode_str(True) + self._offline_str(True)
        if self.offline:
            return '(%s%s)' % (self._appmode_str(True), self._offline_str())
        return '(%s)' % self._appmode_str()

    @log_file.setter
    def log_file(self, logf):
        self.logf = logf
        
    def _app_mode_setup(self):
        app_path = self.path + 'webapp/'
        self.driver.install_extension(app_path)
        self.driver.get('chrome:newtab')
        handles = self.driver.window_handles
        self.driver.find_element_by_xpath("//div[@title='Run Benchmark']").click()
        self.driver.switch_to_new_window(handles)
        self.driver.maximize_window()
        
    def open(self, url):
        if self.appmode:
            self._app_mode_setup()
        self.driver.get(url)
        #self.driver.implicitly_wait(300)
