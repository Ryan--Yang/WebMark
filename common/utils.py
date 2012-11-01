from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.proxy import Proxy

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

def proxy_raw_format(raw):
    if raw is not None and raw.has_key('proxyType') and raw['proxyType'] is not None:
        raw['proxyType'] = _proxy_type_format(raw['proxyType'])
    return Proxy(raw)

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

        
