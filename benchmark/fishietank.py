import time
from common.exceptions import WebMarkException
from benchmark import Benchmark
from common.util import LOGGER

class FishIETank(Benchmark):
    CONFIG = {
        'name': 'FishIETank',
        'metric': 'FPS',
        'path': {
            'external': "http://ie.microsoft.com/testdrive/Performance/FishIETank/Default.html",
            'internal': "microsoft/testdrive/Performance/FishIETank/Default.html"
        },
        'fish_number_list': [1, 10, 20, 50, 100, 250, 500, 1000]
    }

    def __init__(self, driver, browser, case):
        self.fish_number = case.fish_number
        super(FishIETank, self).__init__(driver, browser, case)

    def has_started(self, driver):
        if self.driver.find_elements_by_class_name("control"):
            return True
        else:
            return False

    def config(self):
        index = 0
        fish_number_list = self.CONFIG['fish_number_list']
        for i in range(len(fish_number_list)):
            if self.fish_number == fish_number_list[i]:
                index = i * 2 + 2
        if (index == 0):
            LOGGER.error('fish_number in FishIETank is not correct, will use 20 instead')
            index = 6

        fish_elems = self.driver.find_elements_by_class_name("control")
        fish_elems[index].click()

    def get_result(self):
        elem = self.driver.find_element_by_id("fpsCanvas")
        fps = 0.0
        for i in range(1, 3):
            time.sleep(2)
            str = elem.get_attribute("title").lower()
            start = str.find("at") + 2
            end = str.find("fps")
            str = str[start:end].strip()
            fps += (int(str) - fps) / i
        return round(fps, 2)