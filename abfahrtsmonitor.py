#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

page = requests.get(
    "http://openservice-test.vrr.de/vrr/XSLT_DM_REQUEST?language=de&name_dm=20018234&type_dm=stop&mode=direct&line=rbg:71705:%20:R:s19&depType=STOPEVENTS&includeCompleteStopSeq=1&useRealtime=1&limit=3&itdLPxx_hideNavigationBar=false&itdLPxx_transpCompany=Refresh&timeOffset=0")

# print the html document but nicer
soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())

# using the children property to first select the elements at the top level
list(soup.children)

p = list(body.children)[1]
p.get_text()

# find_all returns a list, so we have to loop through this list
soup = BeautifulSoup(page.content, 'html.parser')
# soup.find_all('p', class_='outer-text')
# soup.find_all(id="first")
soup.select("td")
