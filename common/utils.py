import _winreg
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.proxy import Proxy

def print_results(logf, str):
    print str
    logf.write(str)

def _proxy_type_format(proxy_type):
    if proxy_type == 'direct':
        return ProxyType.DIRECT
    if proxy_type == 'manual':
        return ProxyType.MANUAL
    if proxy_type == 'pac':
        return ProxyType.PAC
    if proxy_type == 'reserved1':
        return ProxyType.RESERVED_1
    if proxy_type == 'autodetect':
        return ProxyType.AUTODETECT
    if proxy_type == 'system':
        return ProxyType.SYSTEM
    
    return ProxyType.UNSPECIFIED

def proxy_raw_format(proxy_raw):
    if proxy_raw is not None and proxy_raw.has_key('proxyType') and proxy_raw['proxyType'] is not None:
        proxy_raw['proxyType'] = _proxy_type_format(proxy_raw['proxyType'])
    return Proxy(proxy_raw)

def add_proxy_to_chrome_options(proxy_raw, options):
    if proxy_raw is None:
        raise ValueError("proxy can not be None")

    if options is None:
        raise ValueError("options can not be None")
        
    proxy = proxy_raw_format(proxy_raw)

    if proxy.proxy_type is ProxyType.UNSPECIFIED:
        return

    if proxy.proxy_type is ProxyType.MANUAL:
        proxy_server = ''
        if proxy.ftp_proxy:
            proxy_server = proxy_server + proxy.ftp_proxy + ';'
        if proxy.http_proxy:
            proxy_server = proxy_server + proxy.http_proxy + ';'
        if proxy.ssl_proxy:
            proxy_server = proxy_server + proxy.ssl_proxy + ';'
        if proxy_server:
            options.add_argument("--proxy-server=" + proxy_server)
        if proxy.no_proxy:
            options.add_argument("--proxy-bypass-list=" + proxy.no_proxy)
    elif proxy.proxy_type is ProxyType.PAC:
        options.add_argument("--proxy-pac-url=" + proxy.proxy_autoconfig_url)
    elif proxy.proxy_type is ProxyType.AUTODETECT:
        options.add_argument("--proxy-auto-detect")
    elif  proxy.proxy_type is ProxyType.DIRECT:
        options.add_argument("--no-proxy-server")


def set_ie_proxy_old(proxy_raw):
    if proxy_raw is None:
        return
    
    key = _winreg.OpenKey(
        _winreg.HKEY_CURRENT_USER,
        "Software\Microsoft\Windows\CurrentVersion\Internet Settings",
        0, 
        _winreg.KEY_WRITE | _winreg.KEY_READ
        )
    
    proxy_server = ''
    if proxy_raw.has_key('ftpProxy') and proxy_raw['ftpProxy'] is not None:
        proxy_server = proxy_server + "ftp=" + proxy_raw['ftpProxy'] + ';'
    if proxy_raw.has_key('httpProxy') and proxy_raw['httpProxy'] is not None:
        proxy_server = proxy_server + "http=" + proxy_raw['httpProxy'] + ';'
    if proxy_raw.has_key('sslProxy') and proxy_raw['sslProxy'] is not None:
        proxy_server = proxy_server + "https=" + proxy_raw['sslProxy'] + ';'
    
    print proxy_server
    if proxy_server:
        _winreg.SetValueEx(key,"ProxyEnable",0, _winreg.REG_DWORD, 1)
        _winreg.SetValueEx(key,"ProxyServer",0, _winreg.REG_SZ, proxy_server)
    
    no_proxy = '<local>;'
    if proxy_raw.has_key('noProxy') and proxy_raw['noProxy']:
        no_proxy = no_proxy + proxy_raw['noProxy']
    _winreg.SetValueEx(key,"ProxyOverride",0, _winreg.REG_SZ, no_proxy)

    if proxy_raw.has_key('proxyAutoconfigUrl') and proxy_raw['proxyAutoconfigUrl']:
        _winreg.SetValueEx(key,"AutoConfigURL",0, _winreg.REG_SZ, proxy_raw['proxyAutoconfigUrl'])
        
    _winreg.FlushKey(key)
    _winreg.CloseKey(key)

def set_ie_proxy(proxy_raw):
    if proxy_raw is None:
        return
    
    proxy = proxy_raw_format(proxy_raw)
    key = _winreg.OpenKey(
        _winreg.HKEY_CURRENT_USER,
        "Software\Microsoft\Windows\CurrentVersion\Internet Settings",
        0, 
        _winreg.KEY_WRITE | _winreg.KEY_READ
        )
    
    if proxy.proxy_type is ProxyType.MANUAL:
        proxy_server = ''
        if proxy.ftp_proxy:
            proxy_server = proxy_server + "ftp=" + proxy.ftp_proxy + ';'
        if proxy.http_proxy:
            proxy_server = proxy_server + "http=" + proxy.http_proxy + ';'
        if proxy.ssl_proxy:
            proxy_server = proxy_server + "https=" + proxy.ssl_proxy + ';'
        if proxy_server:
            _winreg.SetValueEx(key,"ProxyEnable",0, _winreg.REG_DWORD, 1)
            _winreg.SetValueEx(key,"ProxyServer",0, _winreg.REG_SZ, proxy_server)

        no_proxy = '<local>;'
        if proxy.no_proxy:
            no_proxy = no_proxy + proxy.no_proxy
        _winreg.SetValueEx(key,"ProxyOverride",0, _winreg.REG_SZ, no_proxy)
    else:
        _winreg.SetValueEx(key,"ProxyEnable",0, _winreg.REG_DWORD, 0)
        if proxy.proxy_type is ProxyType.PAC:
            _winreg.SetValueEx(key,"AutoConfigURL",0, _winreg.REG_SZ, proxy.proxy_autoconfig_url)
        elif proxy.proxy_type is ProxyType.AUTODETECT:
        #TODO: Set the fifth bit of ninth byte of HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\
        #      Internet Settings\Connections\DefaultConnectionSettings to be 1
            pass
      
    _winreg.FlushKey(key)
    _winreg.CloseKey(key)