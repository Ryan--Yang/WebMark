from common.exceptions import WebMarkException

class BenchmarkRunner(object):
    def __init__(self, logf, configure, browser=None):
        self.logf = logf
        self.browser = browser
        self.driver = None
        self._parse_configure(configure)
    
    def __del__(self):
        if self.browser is not None:
            self.browser.stop()
            
    def run(self):
        if self.benchmark is None or self.browser is None:
            return
        print "Run %s ..." % self.benchmark.name
        self.browser.extra_args = self.benchmark.extra_chrome_args
        self._run_benchmark()
        self.browser.extra_args = None
    
    def _run_benchmark(self):
        rs_avg = 0.0
        valid_times = 0
        for i in range(1,self.run_times + 1):
            try:               
                self.benchmark.webdriver = self.browser.start()
                rs = self.benchmark.run()
                if self.run_times > 1:
                    if i > self.omit_begin_times and i <= self.run_times - self.omit_end_times:
                        valid_times += 1
                        if valid_times == 1:
                            rs_avg = rs
                        elif isinstance(rs, list):
                            for j in range(len(rs)):
                                rs_avg[j] += (rs[j] - float(rs_avg[j])) / valid_times
                        else:
                            rs_avg += (rs - float(rs_avg)) / valid_times
                else:
                    rs_avg = rs
            except Exception, e:
                rs = "N/A"
                print "Exception:", e
            finally:
                self.browser.stop()
            print "Turn %d:rs=%s, avg=%s" % (i, self._result_str(rs), self._result_str(rs_avg))
        self._print("%s: %s %s" % (self.benchmark.name, self._result_str(rs_avg), self.benchmark.metric))
        
    def _parse_configure(self, conf):
        self.benchmark = None
        self.run_times = 1
        self.omit_begin_times = 0
        self.omit_end_times = 0
        self.benchmark = self._setup_benchmark(conf)
        if conf.has_key('runTimes') and isinstance(conf['runTimes'], int) and conf['runTimes'] > 1:
            self.run_times = conf['runTimes']
        if conf.has_key('omitBegin') and isinstance(conf['omitBegin'], int) and conf['omitBegin'] > 0:
            self.omit_begin_times = conf['omitBegin']        
        if conf.has_key('omitEnd') and isinstance(conf['omitEnd'], int) and conf['omitEnd'] > 1:
            self.omit_end_times = conf['omitEnd']
        if self.omit_end_times + self.omit_begin_times >= self.run_times:
            self._print(self.benchmark.name + ": warning, omitBegin or omitEnd too big.")
            return
    
    def _setup_benchmark(self, conf):
        if (not conf.has_key('name')) or conf['name'] is None:
            self._print("Error: Has no name attribute in configure file")
            return None
        name = conf['name']
        try:
            exec 'from benchmark import ' + name
        except ImportError:
            self._print(name + ": Import module error.")
            return None
        args = 'self.driver,self.logf'
        if conf.has_key('args') and conf['args'] is not None:
            args += ', **conf["args"]'
        try:
            benchmark = eval(name + '(' + args + ')')
        except TypeError:
            self._print(name + ": unsupported argument.")
            return None
        except WebMarkException, e:
            self._print(name + ": " + str(e))
            return None
        return benchmark

    def _result_str(self, rs):
        if rs == 0.0:
            return 'N/A'
        if isinstance(rs, basestring):
            return rs
        if not isinstance(rs, list):
            return str(round(rs, 2))
        if len(rs) == 0:
            return 'N/A'
        result = str(round(rs[0], 2))
        for k in range(1,len(rs)):
            result += '/' + str(round(rs[k], 2))
        return result
            
    def _print(self, str):
        print str
        self.logf.write(str + "\n")
        self.logf.flush()
    