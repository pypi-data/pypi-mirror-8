# -*- coding: utf-8 -*-

from collections import namedtuple
import os
import pymysql
import logging
import re

Proxy = namedtuple('Proxy', 'proto, host, port, username, password')
logger = logging.getLogger('GoogleScraper')

def parse_proxy_file(fname):
    """Parses a proxy file

    The format should be like the following:

        socks5 23.212.45.13:1080 username:password
        socks4 23.212.45.13:80 username:password
        http 23.212.45.13:80

        If username and password aren't provided, GoogleScraper assumes
        that the proxy doesn't need auth credentials.

    Args:
        fname: The file name where to look for proxies.

    Returns:
        The parsed proxies.

    Raises:
        ValueError if no file with the path fname could be found.
    """
    proxies = []
    path = os.path.join(os.getcwd(), fname)
    if os.path.exists(path):
        with open(path, 'r') as pf:
            for line in pf.readlines():
                tokens = line.replace('\n', '').split(' ')
                try:
                    proto = tokens[0]
                    host, port = tokens[1].split(':')
                except:
                    raise Exception('Invalid proxy file. Should have the following format: {}'.format(parse_proxy_file.__doc__))
                if len(tokens) == 3:
                    username, password = tokens[2].split(':')
                    proxies.append(Proxy(proto=proto, host=host, port=port, username=username, password=password))
                else:
                    proxies.append(Proxy(proto=proto, host=host, port=port, username='', password=''))
        return proxies
    else:
        raise ValueError('No such file/directory')

def get_proxies(host, user, password, database, port=3306, unix_socket=None):
    """"Connect to a mysql database using pymysql and retrieve proxies for the scraping job.

    Args:
        host: The mysql database host
        user: The mysql user
        password: The database password
        port: The mysql port, by default 3306
        unix_socket: Sometimes you need to specify the mysql socket file when mysql doesn't reside
                     in a standard location.

    Returns;
        A list of proxies obtained from the database

    Raisese:
        An Exception when connecting to the database fails.
    """
    try:
        conn = pymysql.connect(host=host, port=port, user=user, passwd=password, unix_socket=unix_socket)
        conn.select_db(database)
        cur = conn.cursor(pymysql.cursors.DictCursor)
        # Adapt this code for you to make it retrieving the proxies in the right format.
        cur.execute('SELECT host, port, username, password, protocol FROM proxies')
        proxies = [Proxy(proto=s['protocol'], host=s['host'], port=s['port'],
                         username=s['username'], password=s['password']) for s in cur.fetchall()]

        return proxies
    except Exception as e:
        logger.error(e)
        raise

def get_proxies_from_mysql_db(s):
    """Give this function a mysql connection string like this

    mysql://<username>:<password>@<host>/<dbname>

    and it will be happily returning all proxies found in the table 'proxies'
    """
    pattern = re.compile(r'(?P<dbms>\w*?)://(?P<user>\w*?):(?P<pwd>.*?)@(?P<host>\w*?)/(?P<db>\w*)')
    found = pattern.search(s)
    return get_proxies(found.group('host'), found.group('user'),
                                found.group('pwd'), found.group('db'))
