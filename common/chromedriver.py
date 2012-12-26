from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Chrome as ChromeDriver
from selenium.webdriver.support.wait import WebDriverWait


class _ViewType(object):

  TAB = 1
  EXTENSION_POPUP = 2
  EXTENSION_BG_PAGE = 3
  EXTENSION_INFOBAR = 4
  APP_SHELL = 6


class WebDriver(ChromeDriver):

  _CHROME_GET_EXTENSIONS = "chrome.getExtensions"
  _CHROME_INSTALL_EXTENSION = "chrome.installExtension"
  _CHROME_GET_EXTENSION_INFO = "chrome.getExtensionInfo"
  _CHROME_MODIFY_EXTENSION = "chrome.setExtensionState"
  _CHROME_UNINSTALL_EXTENSION = "chrome.uninstallExtension"
  _CHROME_GET_VIEW_HANDLES = "chrome.getViewHandles"
  _CHROME_DUMP_HEAP_PROFILE = "chrome.dumpHeapProfile"

  def __init__(self, executable_path="chromedriver", port=0,
                 chrome_options=None):
    ChromeDriver.__init__(self,
        executable_path, port, chrome_options)

    custom_commands = {
    WebDriver._CHROME_GET_EXTENSIONS:
        ('GET', '/session/$sessionId/chrome/extensions'),
    WebDriver._CHROME_INSTALL_EXTENSION:
        ('POST', '/session/$sessionId/chrome/extensions'),
    WebDriver._CHROME_GET_EXTENSION_INFO:
        ('GET', '/session/$sessionId/chrome/extension/$id'),
    WebDriver._CHROME_MODIFY_EXTENSION:
        ('POST', '/session/$sessionId/chrome/extension/$id'),
    WebDriver._CHROME_UNINSTALL_EXTENSION:
        ('DELETE', '/session/$sessionId/chrome/extension/$id'),
    WebDriver._CHROME_GET_VIEW_HANDLES:
        ('GET', '/session/$sessionId/chrome/views'),
    WebDriver._CHROME_DUMP_HEAP_PROFILE:
        ('POST', '/session/$sessionId/chrome/heapprofilerdump')
    }
    self.command_executor._commands.update(custom_commands)
	
  def stop_service(self):
    self.service.stop()

  def get_installed_extensions(self):
    ids = ChromeDriver.execute(
        self, WebDriver._CHROME_GET_EXTENSIONS)['value']
    return map(lambda id: Extension(self, id), ids)

  def install_extension(self, path):
    params = {'path': path}
    id = ChromeDriver.execute(
        self, WebDriver._CHROME_INSTALL_EXTENSION, params)['value']
    return Extension(self, id)

  def dump_heap_profile(self, reason):
    if self.IsLinux():
      params = {'reason': reason}
      ChromeDriver.execute(self, WebDriver._CHROME_DUMP_HEAP_PROFILE, params)
    else:
      raise WebDriverException('Heap-profiling is not supported in this OS.')
      
  def get_new_window_handle(self, old_handles):
    if old_handles is None:
      raise ValueError("old_handles can not be None")
    handles = self.window_handles
    if len(handles) > 0:
      new_handles = filter(lambda handle: handle not in old_handles, handles)
      if len(new_handles) == 1:
        return new_handles[0]
      raise WebDriverException('More than one new windows')
    return None
    
  def switch_to_new_window(self, old_handles):
    if old_handles is None:
      raise ValueError("old_handles can not be None")
    def new_window(driver):
      return driver.get_new_window_handle(old_handles)
    new_handle = WebDriverWait(self, 10).until(new_window)
    self.switch_to_window(new_handle)


class Extension(object):

  def __init__(self, parent, id):
    self._parent = parent
    self._id = id

  @property
  def id(self):
    return self._id

  def get_name(self):
    return self._get_info()['name']

  def get_version(self):
    return self._get_info()['version']

  def is_enabled(self):
    return self._get_info()['is_enabled']

  def set_enabled(self, value):
    self._execute(WebDriver._CHROME_MODIFY_EXTENSION, {'enable': value})

  def is_page_action_visible(self):
    return self._get_info()['is_page_action_visible']

  def uninstall(self):
    self._execute(WebDriver._CHROME_UNINSTALL_EXTENSION)

  def click_browser_action(self):
    self._execute(WebDriver._CHROME_MODIFY_EXTENSION,
                  {'click_button': 'browser_action'})

  def click_page_action(self):
    self._execute(WebDriver._CHROME_MODIFY_EXTENSION,
                  {'click_button': 'page_action'})

  def get_app_shell_handle(self):
    return self._get_handle(_ViewType.APP_SHELL)

  def get_bg_page_handle(self):
    return self._get_handle(_ViewType.EXTENSION_BG_PAGE)

  def get_popup_handle(self):
    return self._get_handle(_ViewType.EXTENSION_POPUP)

  def get_infobar_handles(self):
    infobars = filter(lambda view: view['type'] == _ViewType.EXTENSION_INFOBAR,
                      self._get_views())
    return map(lambda view: view['handle'], infobars)

  def _get_handle(self, type):
    pages = filter(lambda view: view['type'] == type, self._get_views())
    if len(pages) > 0:
      return pages[0]['handle']
    return None

  @property    
  def handle(self):
    pages = filter(lambda view: view.has_key('extension_id') and view['extension_id'] == self.id, self._get_views())
    if len(pages) > 0:
      return pages[0]['handle']
    return None    

  def _get_info(self):
    return self._execute(WebDriver._CHROME_GET_EXTENSION_INFO)['value']

  def _get_views(self):
    print "id: ", self._id
    views = self._parent.execute(WebDriver._CHROME_GET_VIEW_HANDLES)['value']
    print views
    ext_views = []
    for view in views:
      if 'extension_id' in view and view['extension_id'] == self._id:
        ext_views += [view]
    print ext_views
    return ext_views

  def _execute(self, command, params=None):
    if not params:
        params = {}
    params['id'] = self._id
    return self._parent.execute(command, params)
