import time
import threading
import win32gui
import win32con

def winEnumHandler(hwnd, ctx):
    title = win32gui.GetWindowText(hwnd)
    if title=='Warning: Unresponsive script' or title=='Windows Internet Explorer' or title.find("Command line server") != -1:
        print title
        win32gui.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)

class WinEnumTimer(threading.Thread):  
	def __init__(self):  
		threading.Thread.__init__(self) 
		threading.Thread.setDaemon(self,True)
		self.isPlay = True

	def do(self):  	
		win32gui.EnumWindows(winEnumHandler, None)
		
	def run(self): 
		while self.isPlay :  
			time.sleep(300)  
			self.do()  

	def stop(self):  
		self.isPlay = False