from __future__ import division

import pandas as pd
import os
import sys

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

from bs4 import BeautifulSoup
import urllib2


path = os.path.dirname(__file__)
delimiter="##--##--##"
dataSetLoader=0
out=""
str_buffer=""
readAirportInfo=1
readPriceInfo=1
readPriceInfo=1
dictAirports={'ATL' ,'BOS', 'CLT', 'DEN', 'DFW', 'DTW', 'EWR', 'IAH', 'JFK', 'LAS', 'LAX', 'LGA','MCO', 'MIA', 'MSP', 'ORD', 'PHL', 'PHX', 'SEA' ,'SFO'}

dictRoutes={'ATL_BOS', 'ATL_CLT', 'ATL_DEN', 'ATL_DFW', 'ATL_DTW', 'ATL_EWR', 'ATL_LAX',
 'ATL_LGA', 'ATL_MCO', 'ATL_MIA', 'ATL_MSP', 'ATL_ORD', 'ATL_PHL', 'ATL_SFO',
 'BOS_ATL', 'BOS_DFW', 'BOS_EWR', 'BOS_LAX', 'BOS_LGA', 'BOS_ORD', 'BOS_PHL',
 'BOS_SFO', 'CLT_ATL', 'CLT_LGA', 'DEN_ATL', 'DEN_DFW', 'DEN_LAS', 'DEN_LAX',
 'DEN_MSP', 'DEN_ORD', 'DEN_PHX', 'DEN_SEA', 'DEN_SFO', 'DFW_ATL', 'DFW_DEN',
 'DFW_LAS', 'DFW_LAX', 'DFW_LGA', 'DFW_ORD', 'DFW_PHL', 'DFW_SFO', 'DTW_ATL',
 'DTW_LGA', 'DTW_ORD', 'EWR_ATL', 'EWR_BOS', 'EWR_LAX', 'EWR_MCO', 'EWR_ORD',
 'EWR_SFO', 'IAH_LAX', 'IAH_ORD', 'JFK_LAS', 'JFK_LAX', 'JFK_MIA', 'JFK_SFO',
 'LAS_DEN', 'LAS_DFW', 'LAS_JFK', 'LAS_LAX', 'LAS_ORD', 'LAS_SFO', 'LAX_ATL',
 'LAX_BOS', 'LAX_DEN', 'LAX_DFW', 'LAX_EWR', 'LAX_IAH', 'LAX_JFK', 'LAX_LAS',
 'LAX_ORD', 'LAX_SEA', 'LAX_SFO', 'LGA_ATL', 'LGA_BOS', 'LGA_CLT', 'LGA_DFW',
 'LGA_DTW', 'LGA_MIA', 'LGA_ORD', 'MCO_ATL', 'MCO_EWR', 'MCO_JFK', 'MCO_PHL',
 'MIA_ATL', 'MIA_JFK', 'MIA_LGA', 'MSP_ATL', 'MSP_DEN', 'MSP_ORD', 'ORD_ATL',
 'ORD_BOS', 'ORD_DEN', 'ORD_DFW', 'ORD_DTW', 'ORD_EWR', 'ORD_IAH', 'ORD_LAS',
 'ORD_LAX', 'ORD_LGA', 'ORD_MSP', 'ORD_PHL', 'ORD_PHX', 'ORD_SEA', 'ORD_SFO',
 'PHL_ATL', 'PHL_BOS', 'PHL_DFW', 'PHL_MCO', 'PHL_ORD', 'PHX_DEN', 'PHX_ORD',
 'SEA_DEN', 'SEA_LAX', 'SEA_ORD', 'SEA_SFO', 'SFO_ATL', 'SFO_BOS', 'SFO_DEN',
 'SFO_DFW', 'SFO_EWR', 'SFO_JFK', 'SFO_LAS', 'SFO_LAX', 'SFO_ORD', 'SFO_SEA'}

def createRoute(row):
     airport1=str(row["ORIGIN"])
     airport2=str(row["DEST"])
     route=airport1+"_"+airport2
     if route in dictRoutes:
        return route
     else:
        return "NaN"

if readAirportInfo==1:
                    header_row=['Airport_ID','Name','City','Country', 'IATA_FAA', 'ICAO','Latitude','Longitude','Altitude','Timezone','DST','Tz']
                    airports_info = pd.read_csv(os.path.join(path, "../airports.dat"),names=header_row, parse_dates=False,header=None)
                    airports_info = airports_info.drop('Airport_ID', axis=1)
                    airports_info = airports_info.drop('Name', axis=1)
                    airports_info = airports_info.drop('ICAO', axis=1)
                    airports_info = airports_info.drop('Altitude', axis=1)
                    airports_info = airports_info.drop('Timezone', axis=1)
                    airports_info = airports_info.drop('DST', axis=1)
                    airports_info = airports_info.drop('Tz', axis=1)
                    rows2delete=[]
                    for i, row in airports_info.iterrows():
                        country = row["Country"]
                        faa=str(row["IATA_FAA"])
                        if not country=="United States" or (not len(faa)==3):
                            rows2delete.append(i)
                    airports_info=airports_info.drop(airports_info.index[rows2delete])
                    header_row=['City','FAA','IATA','ICAO','Airport','Role','Enplanements']
                    airports_info_category = pd.read_csv(os.path.join(path, "../airportCategories.csv"),delimiter=";",names=header_row, parse_dates=False,header=None)
                    airports_info_category=airports_info_category.rename(columns={'FAA': 'IATA_FAA'})
                    airports_info_category['Role'] = airports_info_category['Role'].apply(lambda row: str(row).split(" ")[0])
                    airports_info_category=airports_info_category.drop('City', axis=1)
                    airports_info_category=airports_info_category.drop('IATA', axis=1)
                    airports_info_category=airports_info_category.drop('ICAO', axis=1)
                    airports_info_category=airports_info_category.drop('Airport', axis=1)
                    rows2delete=[]
                    for i, row in airports_info_category.iterrows():
                        faa = str(row["IATA_FAA"])
                        if  faa=="nan" or  faa=="NaN":
                            rows2delete.append(i)
                    airports_info_category=airports_info_category.drop(airports_info_category.index[rows2delete])
                    airports_info=pd.merge(airports_info, airports_info_category, how='inner', on=['IATA_FAA'])
                    #print airports_info.tail(25)
                    str_buffer=airports_info.to_csv()+delimiter+"\n"
s1 = StringIO()
if readPriceInfo==1:
                    header_row=["ITIN_ID","ORIGIN","DEST","PASSENGERS"]
                    price_source_port_info = pd.read_csv(os.path.join(path, "../271165565_T_DB1B_MARKET.csv"))
                    price_source_port_info=price_source_port_info.drop("Unnamed: 4",axis=1)
                    price_source_port_info=price_source_port_info[price_source_port_info['PASSENGERS'].notnull()]
                    price_source_port_info=price_source_port_info[price_source_port_info['PASSENGERS']>5]
                    price_source_port_info=price_source_port_info[price_source_port_info['PASSENGERS']<400]
                    price_source_port_info["Route"]=price_source_port_info.apply(createRoute, axis=1)
                    price_source_port_info=price_source_port_info[price_source_port_info['Route'].notnull()]
                    price_source_port_info=price_source_port_info.groupby(['Route'])['PASSENGERS'].mean()
                    print price_source_port_info.tail(50)
                    price_source_port_info.to_csv(s1)
                    str_buffer=str_buffer+s1.getvalue()+delimiter

f = open("dataExtOut.csv", "w")
f.write(str_buffer)      # str() converts to string
f.close()
    #print len(original_ext_data)




