import time
import os
import json
import platform
from common.timer import WinEnumTimer
from suite_runner import SuiteRunner

class WebMarkRunner(object):
    def __init__(self, conf_file = 'config.json'):
        self.conf_file = conf_file
        rs_path = os.path.dirname(os.path.realpath(__file__)) + '/benchmark_test_results/'
        if not os.path.exists(rs_path):
            os.mkdir(rs_path)

        now = time.localtime()
        strTime = time.strftime('%Y-%m-%d_%H_%M_%S', now)
        self.logf = file(rs_path + 'result_' + strTime + '.log', 'w')
        self.driver = None

        self.win_enum_timer = None
        sysstr = platform.system()        
        if(sysstr =="Windows"):        
            self.win_enum_timer = WinEnumTimer()
            self.win_enum_timer.start()

    def __del__(self):
        self.logf.close()
        if self.win_enum_timer is not None:
            self.win_enum_timer.stop()
    
    def _load_config(self):
        f = file(self.conf_file)
        config = json.load(f)    
        f.close()
        return config

    def run(self) :
        config = self._load_config()
        for browser in config :
            suite = config[browser]
            SuiteRunner(self.logf, browser, suite).run()
