import numpy as np
from browsermobproxy import Server
from selenium import webdriver
import time
import os


import json

website_links = np.loadtxt('top-1m.csv', delimiter=',', usecols=(1,), dtype=str)

arr_links = np.array(website_links)

server = Server("./browsermob-proxy/bin/browsermob-proxy")
server.start()
i = 0
for site_name in arr_links:
    proxy = server.create_proxy(params=dict(trustAllServers=True))
    # create a new chromedriver instance 
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--proxy-server={}".format(proxy.proxy))
    chrome_options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=chrome_options)

    # do crawling
    proxy.new_har("myhar")
    driver.get(f'http://{site_name}')
    time.sleep(1)
    driver.refresh()

    time.sleep(4)

    output_directory = "./harFiles"
    file_path = os.path.join(output_directory, f'myhar_{site_name}')


    # write har file 
    with open(file_path, 'w') as f:
        f.write(json.dumps(proxy.har))
    
    i += 1

    proxy.close()
    driver.quit()

server.stop()


