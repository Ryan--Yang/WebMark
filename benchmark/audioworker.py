import platform
import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class AudioWorker(Benchmark):	
    def __init__(self, driver, logf):
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "AudioWorker"

    @property
    def metric(self):
        return "%"
        
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
		
    def run(self):
        self.open("http://pnp.sh.intel.com/benchmarks/WRTBench-git/audio/AudioWorker/audio_transform.html")
        time.sleep(5)
		
        elem = self.driver.find_element_by_id("audioProcess")
        elem.click()
        time.sleep(10)	
		
        sysstr = platform.system()		
        if(sysstr =="Windows"):		
            import wmi
            utilization = []	
            c = wmi.WMI()
            for cpu in c.Win32_Processor():
                utilization.append(0.0)
        else:
            utilization = 0.0
			
        i = 0			
        while i < 12:
            i += 1			
            if(sysstr =="Windows"):			
                j = 0				
                for cpu in c.Win32_Processor():
                    print '%s Utilization: %d%%' % (cpu.DeviceID, cpu.LoadPercentage)
                    utilization[j] += (cpu.LoadPercentage - utilization[j])/i
                    j += 1	
            else:			
                utilization += (self.get_cpu_usage() - utilization)/i
                print 'CPU Utilization: %.2f%%' % (utilization)				
            time.sleep(5)			
			
        return utilization		
		
