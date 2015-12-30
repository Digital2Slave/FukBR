"""
Name    : config
Author  : JohnTian
Date    : 12/18/2015
Version : 0.01
CopyLeft: OpenSource
"""
import os

#User-Agent maybe a json file or list of user_agent_string
USER_AGENT = './file/UserAgentString.json'

#Proxy
USER_KEY = os.environ.get('CRAWLERA_USER')
PROXY_HOST = "proxy.crawlera.com"

#MongoDB
MONGODB_SERVER = os.environ.get('FUKKEY')
#MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = '17Mbook'
MONGODB_COLLECTION = 'book'
