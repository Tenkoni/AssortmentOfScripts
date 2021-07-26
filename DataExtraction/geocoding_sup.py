from geopy.geocoders.googlev3 import GoogleV3
from geopy.extra.rate_limiter import RateLimiter
import csv

geolocator = GoogleV3(api_key = '', domain = 'maps.google.cl')
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.03)
geocodeReverse = RateLimiter(geolocator.reverse, min_delay_seconds=0.03)


with open('superior_edu_raw.csv', mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)
    data = list(csv_reader)

with open("education/superior_edu_coordinates.csv", "w", newline="", encoding='utf-8') as f:
	writer = csv.writer(f)
	writer.writerow(header)
	for facility in data:
		if True: # I just don't want to reformat this ughhhh this doesn't affects the efficiency as the optimizer takes care of it
			 #replace the list value to the ones corresponding to your data (your address)
			if facility[6]:
				address= " ".join((facility[6], "Chile"))
			else:
				address= " ".join((facility[2], "Chile"))
				print("USING NAME!!!!")
			print(address)
			try: 
				location = geocode(address)
				coordinates = (location.latitude, location.longitude)
				facility.append(location.longitude)
				facility.append(location.latitude)
				writer.writerow(facility)
				print("^__ Found ", coordinates)
			except Exception as e:
				print(e)
				facility.append("")
				facility.append("")
				writer.writerow(facility)
				print(" ^__ Not Found")
		else:
			writer.writerow(facility)




