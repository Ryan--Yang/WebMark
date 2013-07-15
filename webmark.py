import json
import argparse
import time
import platform
import logging
import os
from common.util import LOGGER
from common.util import SYSTEM
from common.util import PROJECT_PATH

class Format:
    NAME = 0
    REQUIRED = 1 # (O)ptional or (M)andatory
    TYPE = 2 # A for Array, O for Object, P for Property

    @staticmethod
    def format_has_member(format, member):
        for f in format:
            if f[Format.NAME] == member or f[Format.NAME] == '*':
                return f
        return None

    @staticmethod
    def format(instance):
        # Check if all mandatory members in FORMAT are satisfied
        for format in instance.FORMAT:
            if format[Format.REQUIRED] == 'M' and not format[Format.NAME] in instance.data:
                LOGGER.error(format[Format.NAME]+ ' is not defined in ' + instance.__class__.__name__)
                quit()

        for member in instance.data:
            # Check all members in instance are recognized
            format = Format.format_has_member(instance.FORMAT, member)
            if not format:
                LOGGER.warning('Can not recognize ' + ' in ' + instance.__class__.__name__)
                continue

            if format[Format.NAME] == '*':
                format_name = member
            else:
                format_name = format[Format.NAME]
            format_type = format[Format.TYPE]
            instance_data = instance.data[format_name]
            if format_type == 'P':
                instance.__dict__[format_name] = instance_data
            elif format_type == 'O':
                instance.__dict__[format_name] = eval(format_name.capitalize())(instance_data)
            elif format_type == 'A':
                for element in instance_data:
                    instance.__dict__[format_name].append(eval(format_name.capitalize()[:-1])(element))

class Case:
    FORMAT = [
        ['name', 'M', 'P'],
        ['path', 'O', 'P'],
        ['timeout', 'O', 'P'],
        ['run_times', 'O', 'P'],
        ['skip_times', 'O', 'P'],
        ['*', 'O', 'P'] # Configuration for specific case
    ]
    def __init__(self, data):
        self.path = 'external'
        self.timeout = 60
        self.run_times = 1
        self.skip_times = 0
        self.data = data
        self.result = []
        self.metric = ''
        self.average = 0
        Format.format(self)

    def add_result(self, result):
        self.result.append(result)

    def log_result(self):
        total = 0
        for i in range(self.skip_times, self.run_times):
            total += self.result[i]

        if self.run_times > self.skip_times:
            self.average = round(total / (self.run_times - self.skip_times), 2)
        LOGGER.info(vars(self))

class Proxy:
    FORMAT = [
        ['type', 'O', 'P'],
        ['http', 'O', 'P'],
        ['noproxy', 'O', 'P']
    ]

    def __init__(self, data):
        self.data = data
        Format.format(self)

class Browser:
    FORMAT = [
        ['name', 'M', 'P'],
        ['path', 'M', 'P'],
        ['mode', 'O', 'P'],
        ['proxy', 'O', 'O'],
        ['switches', 'O', 'P'],
        ['driver', 'O', 'P']
    ]

    def __init__(self, data):
        self.mode = 'browser'
        self.data = data
        Format.format(self)

class Suite:
    FORMAT = [
        ['browser', 'M', 'O'],
        ['cases', 'M', 'A'],
        ['name', 'O', 'P'],
        ['description', 'O', 'P']
    ]
    def __init__(self, data):
        self.cases = []
        self.data = data
        Format.format(self)

    def run(self):
        driver_name = self.browser.name.capitalize() + 'Driver'
        exec 'from common.' + driver_name.lower() + ' import ' + driver_name
        self.driver = eval(driver_name)(self.browser)

        # Handle app mode
        if self.browser.mode == 'app':
            app_path = PROJECT_PATH + 'hosted_app'
            self.extension = self.driver.install_extension(app_path)
            self.driver.get('chrome:newtab')
            handles = self.driver.window_handles
            self.driver.find_element_by_xpath("//div[@title='Hosted App Benchmark']").click()
            self.driver.switch_to_new_window(handles)

        for i in range(len(self.cases)):
            case_name = self.cases[i].name
            exec 'from benchmark.' + case_name.lower() + ' import ' + case_name
            eval(case_name)(self.driver, self.browser, self.cases[i])

        self.extension.uninstall()
        self.driver.quit()

class WebMark:
    FORMAT = [
        ['suites', 'M', 'A']
    ]
    def __init__(self, config_file):
        # Init LOGGER
        LOGGER.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s - %(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S")

        result_path = PROJECT_PATH + 'test_results/'
        if not os.path.exists(result_path):
            os.mkdir(result_path)
        log_file = logging.FileHandler(result_path + time.strftime('%Y-%m-%d-%X', time.localtime()) + '.log')
        log_file.setFormatter(formatter)
        LOGGER.addHandler(log_file)

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        LOGGER.addHandler(console)

        # Log start
        self.start_time = time.time()
        LOGGER.info('Start of ' + self.__class__.__name__ + '.')

        # Parse
        if not os.path.isfile(config_file):
            LOGGER.error(config_file + ' is not a valid file.')
            quit()
        f = file(config_file)
        self.data = json.load(f)
        f.close()

        self.suites = []
        Format.format(self)

        # Start patrol
        if SYSTEM == 'windows':
            exec 'from common.patrol import Patrol'
            self.patrol = Patrol()


        # Run
        for i in range(len(self.suites)):
            self.suites[i].run()

    def __del__(self):
        self.stop_time = time.time()
        LOGGER.info('End of ' + self.__class__.__name__ + '. Total elapsed time: ' + str(int(self.stop_time - self.start_time)) + ' seconds')


if __name__== '__main__':
    # Handle options
    parser = argparse.ArgumentParser(description = 'Test Automation tool to measure the performance of browser and web runtime',
                                     formatter_class = argparse.RawTextHelpFormatter,
                                     epilog = '''
examples:
  python %(prog)s config.json

''')

    parser.add_argument('config', help='designate the config file for test')
    args = parser.parse_args()
    if not args.config:
        parser.print_help()
        quit()

    WebMark(args.config)
