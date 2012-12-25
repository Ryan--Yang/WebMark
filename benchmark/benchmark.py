import os
import time
from selenium.webdriver.support import wait
from common.exceptions import WebMarkException

class Benchmark(object):
    def __init__(self):
        self.driver = None
        self.logf = None
        self.__appmode = False
        self.__offline = False
        self.__url = None
        self.__wait_time = None
        self.__timeout = None
    
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

    @property
    def appmode(self):
        return self.__appmode

    @appmode.setter
    def appmode(self, mode):
        self.__appmode = mode

    @property
    def offline(self):
        return self.__offline

    @appmode.setter
    def offline(self, mode):
        self.__offline = mode

    @property
    def default_url(self):
        """
        Return the default url of the benchmark, must be overridden by specify benchmark.
        """
        return None;

    @property
    def url(self):
        if self.__url is not None:
            return self.__url
        return self.default_url

    @url.setter
    def url(self, url):
        self.__url = url
        
    @property
    def expect_time(self):
        """
        Return the expect time the benchmark run, 
        Used to wait related time after benchmark start running.
        Should be overridden by specify benchmark if need.
        """
        return 0;

    @property
    def default_timeout(self):
        """
        Return the benchmark default timeout value, 
        Should be overridden by specify benchmark if need.
        """
        return 3600;

    @property
    def wait_time(self):
        """
        Return the expect time the benchmark run, 
        Used to wait related time after benchmark start running.
        Should be overridden by specify benchmark if need.
        """
        if self.__wait_time is not None:
            return self.__wait_time
        return self.expect_time

    @wait_time.setter
    def wait_time(self, t):
        self.__wait_time = t

    @property
    def timeout(self):
        if self.__timeout is not None:
            return self.__timeout
        return self.default_timeout

    @timeout.setter
    def timeout(self, t):
        self.__timeout = t
        
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
        if self.__appmode:
            if with_comma:
                return 'appmode,'
            return 'appmode'
        return ''

    def _offline_str(self, with_comma=False):
        if self.__offline:
            if with_comma:
                return 'offline,'
            return 'offline'
        return ''

    @property        
    def _name_common_ext(self):
        if (not self.__appmode) and (not self.__offline):
            return ''
        if self.__offline:
            return '(%s%s)' % (self._appmode_str(True), self._offline_str())
        return '(%s)' % self._appmode_str()

    @property
    def name(self):
        """
        Return the name of the benchmark, must be overridden by specify benchmark.
        """
        return '';
        
    @property
    def identifier(self):
        """
        Return the identifier of the benchmark.
        """
        _id = self.name
        if self.__appmode:
            _id += '_appmode'
        if self.__offline:
            _id += '_offline'
        return _id

    @property
    def metric(self):
        """
        Return the metric of the benchmark, must be overridden by specify benchmark.
        """
        return None;

    def _app_mode_setup(self):
        app_path = self.path + 'webapp/'
        self.driver.install_extension(app_path)
        self.driver.get('chrome:newtab')
        handles = self.driver.window_handles
        self.driver.find_element_by_xpath("//div[@title='Run Benchmark']").click()
        self.driver.switch_to_new_window(handles)
        self.driver.maximize_window()
        
    def open(self):
        if self.url is None:
            raise WebMarkException("Url is not configured and"
            " no default url of the benchmark.")
        if self.__appmode:
            self._app_mode_setup()
        self.driver.get(self.url)
        
    def start(self, driver):
        """
        Make sure the benchmark start to run, if the benchmark does not run automatically.        
        Should be overridden by specify benchmark if need.

        :Args:
        - driver - The webdriver.       
        """
        pass
        
    def chk_finish(self, driver):
        """
        Check the benchmark finish or not.        
        Must be overridden by specify benchmark if need.
        
        :Args:
        - driver - The webdriver.
        
        :Returns:
        - True - If the benchmark finish running.
        - False - If the benchmark does not finish running.
        """
        return True
        
    def get_result(self, driver):
        """
        Get the benchmark result after finish.        
        Must be overridden by specify benchmark if need.

        :Args:
        - driver - The webdriver.
        
        :Returns:
            The result of the benchmark, should be number or list.
        """
        return 0.0
    
    def run(self):
        if self.driver is None:
            raise WebMarkException("The webdriver does not run.")
        #print "Wait_time:%d" % self.wait_time
        #print "timeout:%d" % self.timeout
        #print "url:%s" % self.url
        self.open()
        self.start(self.driver)
        time.sleep(self.wait_time)
        __driver_timeout = self.timeout - self.wait_time
        wait.WebDriverWait(self.driver, __driver_timeout, 90).until(self.chk_finish)
        return self.get_result(self.driver)
        