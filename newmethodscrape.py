import requests
import json
import mysql.connector
import re


url = "https://www.soulorigin.com.au/wp-admin/admin-ajax.php"

payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"action\"\r\n\r\nget_store_location\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"search\"\r\n\r\n,AU\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"region_dr\"\r\n\r\nall\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'cache-control': "no-cache",
    'postman-token': "e5ee3a70-eb44-055b-3c3d-02865d7c53ee"
    }

response = requests.request("POST", url, data=payload, headers=headers)
latitude=[]
longitude=[]
title=[]
store_details_urls = []
store_suburb = []
store_city = []
store_country=[]
store_postal = []
store_info = []
try:
	if (response.status_code == 200):
		jsonfile = response.json()
		length_json = len(jsonfile['location_markers'])
		print(length_json)
		for i in range(length_json-1):
			latitude.append(jsonfile['location_markers'][i]['lat'])
			longitude.append(jsonfile['location_markers'][i]['lng'])
			title.append(jsonfile['location_markers'][i]['title'])
			store_details_urls.append("https://www.soulorigin.com.au/store/{}/".format((jsonfile['location_markers'][i]['title'])).replace(" ","-").lower())
			store_det = jsonfile['location_markers'][i]['info']
			result_n = re.search('<div class=\"map-tooltip\"><address>(.*)</address></div>',store_det)
			result = result_n.group(1)
			store_info.append(result)
	connection = mysql.connector.connect(host="localhost",database="store_info",user="root",password="saimohan1")
	cursor = connection.cursor()
	for tit,lat,log,store_det,store_ad in zip(title,latitude,longitude,store_details_urls,store_info):
		cursor.execute("INSERT INTO store_info (Store_name,Latitude,Longitude,Store_Details_URL,Store_Address) VALUES (%s,%s,%s,%s,%s)",(tit,lat,log,store_det,store_ad))
	connection.commit()
	print("Inserted rows are:",cursor.rowcount)
	cursor.close()	
		
except IndexError:
	print("No value at this key")






