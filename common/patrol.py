import time
import threading
import win32gui
import win32con
import logging

class Patrol(threading.Thread):
	def __init__(self):  
		threading.Thread.__init__(self) 
		threading.Thread.setDaemon(self,True)
		while True:  
			time.sleep(300)  
			win32gui.EnumWindows(self.winEnumHandler, None)

    def winEnumHandler(hwnd, ctx):
        title = win32gui.GetWindowText(hwnd)
        if title=='Warning: Unresponsive script' or title=='Windows Internet Explorer' or title.find("Command line server") != -1 or title.find("chromedriver.exe") != -1:
            win32gui.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)
