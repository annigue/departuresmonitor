#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime



#station_numbers =["20018079", "20018234", "20018242", "20018242"]
#line_numbers = ["rbg:71707:%20:R:j20", "rbg:71705:%20:R:j20", "rbg:71708:%20:H:s19", "rbg:71709:%20:H:s19"]

station_numbers =["20018079", "20018234", "20018242"]
line_numbers = ["rbg:71707:%20:R:j20", "rbg:71705:%20:R:j20", "rbg:71709:%20:H:s19"]


abfahrtszeit = []
Line = []
Realtime = []
Direction = []
Platform = []

abfahrtsmonitor = pd.DataFrame({
			"Uhrzeit": abfahrtszeit,
			"Linie": Line,
			"Hinweis": Realtime,
			"Richtung": Direction,
			"Steig": Platform,
})


 # For every page in the interval 1-4
for i, station_number in enumerate(station_numbers):
	line_number = line_numbers[i]
	# Make a get request
	page = requests.get("http://217.70.161.98/nrwAbfahrt/XSLT_DM_REQUEST?language=de&name_dm=" + station_number + "&type_dm=stop&mode=direct&line=" + line_number + "&depType=STOPEVENTS&includeCompleteStopSeq=0&useRealtime=1&limit=3&itdLPxx_hideNavigationBar=false&itdLPxx_transpCompany=Refresh&timeOffset=0")

	all_stations = []

	soup = BeautifulSoup(page.content, 'html.parser')
	station = soup.find_all('tr',class_="heightDirectionMitAbfahrt")
	all_stations.append(station)


#for index, url in enumerate(urls):
#	page = requests.get(url)
#	soup = BeautifulSoup(page.content, 'html.parser')
#	station = soup.find_all('tr',class_="heightDirectionMitAbfahrt")
#	all_stations.append(station)

	resultsset = []

	for station in all_stations:
		abfahrtszeiten_tags = soup.select(".heightDirectionMitAbfahrt .colTime")
		abfahrtszeit = [a1.get_text() for a1 in abfahrtszeiten_tags]


	# Loeschen von \n aus der Liste
		abfahrtszeit = [a11.strip() for a11 in abfahrtszeit if str(a11)]
		abfahrtszeit = [datetime.strptime(x,"%H:%M") for x in abfahrtszeit]

	#
		linien_tags = soup.select(".heightDirectionMitAbfahrt .colLine")
		Line = [lA.get_text() for lA in linien_tags]
	# Loeschen von \n aus der Liste
		Line = [LA1.strip() for LA1 in Line if str(LA1)]
#
		realtime_tags = soup.select(".heightDirectionMitAbfahrt .colRealtime")
		Realtime = [RA.get_text() for RA in realtime_tags]
		if not realtime_tags:
			Realtime = 'N/A'
	
# Loeschen von \n aus der Liste
		Realtime = [RA1.strip() for RA1 in Realtime if str(RA1)]
	

#
		direction_tags = soup.select(".heightDirectionMitAbfahrt .colDirection")
		Direction = [DA.get_text() for DA in direction_tags]
# 	Loeschen von \n aus der Liste
		Direction = [DA1.strip() for DA1 in Direction if str(DA1)]
#
		platform_tags = soup.select(".heightDirectionMitAbfahrt .colPlatform")
		Platform = [PA.get_text() for PA in platform_tags]
# Loeschen von \n aus der Liste
		Platform = [PA1.strip() for PA1 in Platform if str(PA1)]

# Fuer Direction wird statt ein Wert immer zweimal der Wert gezogen, daher loesche ich jedes zweite Argument aus der Liste
		Direction = [item for index, item in enumerate(Direction) if (index + 1) % 2 != 0]
# Auch der STeig wird durch die Websitestruktur zweimal gezogen, also ebenfalls jeden zweiten Wert entfernen
		Platform = [item1 for index, item1 in enumerate(Platform) if (index + 1) % 2 != 0]
		
		monitor_station = pd.DataFrame({
			"Uhrzeit": abfahrtszeit,
			"Linie": Line,
			"Hinweis": Realtime,
			"Richtung": Direction,
			"Steig": Platform,
			})
		monitor_station['Uhrzeit'] = pd.to_datetime(monitor_station.Uhrzeit,format ='%H:%M', errors = 'coerce').dt.time

		
		abfahrtsmonitor = abfahrtsmonitor.append(monitor_station, ignore_index = True)
		abfahrtsmonitor = abfahrtsmonitor.sort_values(by='Uhrzeit', ascending = True)
	
	
print(abfahrtsmonitor)



