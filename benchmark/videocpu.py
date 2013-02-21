import platform
import time
from common.exceptions import WebMarkException
from benchmark import Benchmark

class VideoCPU(Benchmark):
    ENDED = 'return document.getElementById("video_frame").ended'
    PLAY = 'return document.getElementById("video_frame").play()'
    _SUITES = ("fullscreen", "non-fullscreen")

    def __init__(self, suite = 'fullscreen'):
        if suite in self._SUITES:
            self.suite = suite
        else:
            raise WebMarkException("Unsupported suite %s, "
            "should be one of 'fullscreen', 'non-fullscreen'." % suite)
  
        Benchmark.__init__(self)

    @property
    def name(self):
        return "VideoCPU %s" % self.suite

    @property
    def metric(self):
        return "%"

    @property
    def default_url(self):
        return "http://pnp.sh.intel.com/html5_video/"
      
    @property
    def default_timeout(self):
        return 1800

    @property
    def expect_time(self):
        return 0
 
    def _read_cpu_usage(self): 
        try:
            fd = open("/proc/stat", 'r')
            lines = fd.readlines()
        finally:
            if fd:
                fd.close()
        for line in lines:
            l = line.split()
            if l[0].startswith('cpu'):
                return l
        return []

    def get_cpu_usage(self):
        cpustr=self._read_cpu_usage()
        if not cpustr:
            return 0
        usni1 = long(cpustr[1])+long(cpustr[2])+long(cpustr[3])+long(cpustr[5])+long(cpustr[6])+long(cpustr[7])+long(cpustr[8])+long(cpustr[9])+long(cpustr[10])+long(cpustr[4]) 
        usn1 = long(cpustr[1])+long(cpustr[2])+long(cpustr[3])+long(cpustr[5])+long(cpustr[6])+long(cpustr[7])+long(cpustr[8])+long(cpustr[9])+long(cpustr[10])
        time.sleep(1)
        cpustr=self._read_cpu_usage()
        if not cpustr:
            return 0
        usni2 = long(cpustr[1])+long(cpustr[2])+long(cpustr[3])+long(cpustr[5])+long(cpustr[6])+long(cpustr[7])+long(cpustr[8])+long(cpustr[9])+long(cpustr[10])+long(cpustr[4])  
        usn2 = long(cpustr[1])+long(cpustr[2])+long(cpustr[3])+long(cpustr[5])+long(cpustr[6])+long(cpustr[7])+long(cpustr[8])+long(cpustr[9])+long(cpustr[10])
        cpuper=float(usn2-usn1)/float(usni2-usni1)
        return round(100*cpuper, 2)
		
    def start(self, driver):
        time.sleep(5)

        sysstr = platform.system()		
        if(sysstr =="Windows"):	
            import pythoncom	
            import wmi
            self.utilization = []
            pythoncom.CoInitialize()	
            c = wmi.WMI()
            for cpu in c.Win32_Processor():
                self.utilization.append(0.0)
        else:
            self.utilization = 0.0

        for i in range(1,8):
            driver.find_element_by_id("right_click").click()
            time.sleep(1)

        driver.find_element_by_id("thumb_2").click()
        time.sleep(1)

        if self.suite.lower() == "fullscreen":			
            driver.find_element_by_id("fullscreen-button").click()
            time.sleep(5)
        driver.execute_script(self.PLAY)	
        time.sleep(3)
			
        i = 0			
        while not driver.execute_script(self.ENDED):
            i += 1			
            if(sysstr =="Windows"):			
                j = 0				
                for cpu in c.Win32_Processor():
                    print '%s Utilization: %d%%' % (cpu.DeviceID, cpu.LoadPercentage)
                    self.utilization[j] += (cpu.LoadPercentage - self.utilization[j])/i
                    j += 1	
            else:			
                self.utilization += (self.get_cpu_usage() - self.utilization)/i
                print 'CPU Utilization: %.2f%%' % (self.utilization)				
            time.sleep(20)	

        if(sysstr =="Windows"):	
            pythoncom.CoUninitialize()

    def get_result(self, driver):
        return self.utilization
