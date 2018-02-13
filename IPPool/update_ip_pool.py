import sys
sys.path.append('/home/user/crawl')
from spider_tool import *
from ip_source import *
import requests
import time
from db_tool import *


TEST_URL = '://ip.cip.cc'
IPPool_DB = 'IPPool'

def test_proxies_efficience(proxy, method='http'):
    # if the proxy is un usable or time out > 5 seconds, will return a negative value to mark it as faile
    if method not in ['http', 'https']:
        g_log.error("method %s in correct." % method)
        return -1
    g_log.debug('Now test the efficiency of %s, with method %s' % (proxy, method))
    proxies = {method: proxy}
    start_time = time.time()
    try:
        response = requests.get(method+TEST_URL, proxies=proxies, timeout=5)
        cost = time.time() - start_time
        g_log.debug(response.text)
        g_log.debug('proxy %s costs %s' % (proxy, str(cost)))
        if cost < 5:
            return cost
        return -1
    except Exception as e:
        g_log.info('proxy unusable')
        return -1

def update_up_pool(cur):
    g_log.debug('first check the avaliable proxies')
    cur.execute('select ip_addr, port, method, id from tb_ip_pool where is_active=True')
    count = cur.fetchall()
    g_log.debug('Now have active proxies %d' % len(count))
    update_proxies(cur, count)
    if count == None or len(count) < 30:
        get_new_proxies(cur)

def update_proxies(cur, proxies):
    g_log.debug('Now check avaliability of current proxies')
    for items in proxies:
        proxy = items[0]+':'+items[1]
        method = items[2]
        ret = test_proxies_efficience(proxy, method)
        if ret<0:
            g_log.warn(proxy+' is not working, deactivate it!')
            cur.execute('update tb_ip_pool set is_active=False where id=%d' % items[3])
            cur.connection.commit()
    return

def get_new_proxies(cur):
    html = open_url(IP_Source['66ip'])
    if html == None:
        return
    bsObj = BeautifulSoup(html, 'html.parser')
    ip_ports = bsObj.findAll('br')

    ip_info = []
    for item in ip_ports:
        temp_info = item.next_sibling.strip()
        if len(temp_info)> 10 and temp_info not in ip_info:
            ip_info.append(temp_info)
    g_log.debug(len(ip_info))
    # get the existed ip/port to reduce the connection number
    cur.execute('select ip_addr, port from tb_ip_pool')
    existed = cur.fetchall()
    for proxy in ip_info:
        temp = proxy.split(':')
        if (temp[0], temp[1]) in existed:
            continue
        ret_http = test_proxies_efficience(proxy)
        if ret_http < 0:
            ret_https = test_proxies_efficience(proxy, 'https')
            if ret_https < 0:
                continue
            else:
                cur.execute('replace into tb_ip_pool (ip_addr, port, method, is_active, latency) values (\"%s\", \"%s\", \"%s\", True, \"%f\")' % (temp[0], temp[1], 'https', ret_https))
                cur.connection.commit() 
        else:
            cur.execute('replace into tb_ip_pool (ip_addr, port, method, is_active, latency) values (\"%s\", \"%s\", \"%s\", True, \"%f\")' % (temp[0], temp[1], 'http', ret_http))
            cur.connection.commit() 



def main():
    try:
        conn = create_new_connect(db = IPPool_DB)
        if conn == None:
            return
        cur = create_new_cursor(conn)
        if cur == None:
            return
        update_up_pool(cur)
    except Exception as e:
        g_log.error(e)
    finally:
        close_cursor(cur)
        close_conn(conn)


if __name__ == "__main__":
    main()
