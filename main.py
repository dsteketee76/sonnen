import requests
import network
import secrets
import time
import schedule

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PASSWORD)
print("WLAN Connected:" + str(wlan.isconnected()))
hasAlert = False
lat = [LAT]
lon = [LONG]

def get_weather_alerts():
    global hasAlert
    global lat
    global lon
    print("Calling NWS")
    # Construct the URL for the NWS API
    url = f"https://api.weather.gov/alerts/active?point={lat},{lon}"

    headers = {
        "User-Agent": "WeatherApp/1.0 ([IDENTIFIER])",  # Replace with your email or app info
        "Accept": "application/geo+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("NWS Response Received")
        data = response.json()
        alerts = data.get('features', [])

        if not alerts:
            print("No severe weather alerts for the given location.")
            if hasAlert != False:
                updateBatteryStatus(40)
                hasAlert = False
        else:
            for alert in alerts:
                if (alert['properties']['category'] == 'Met'
                and (alert['properties']['urgency'] == 'Future'
                     or alert['properties']['urgency'] == 'Expected'
                     or alert['properties']['urgency'] == 'Immediate')
                and (alert['properties']['severity'] == 'Moderate'
                     or alert['properties']['severity'] == 'Severe'
                     or alert['properties']['severity'] == 'Extreme')
                and value_in_list(['properties']['event'], eventTypes)):
                    print('Alerts Found')
                    if hasAlert != True:
                        updateBatteryStatus(100)
                        hasAlert = True
    else:
        print(f"Error {response.status_code}: Unable to fetch data from NWS.")

def value_in_list(value, lst):
    return value in lst

def updateBatteryStatus(val):
    #call battery
    print('Updating battery status')
    url = f"http://[SONNEN IP ADDRESS]/api/v2/configurations?EM_USOC=" + str(val)

    headers = {
        "Auth-Token": "[AUTH TOKEN]",
        "Accept": "application/json",
        "Content-Length": "0"
    }
    response = requests.put(url, headers=headers)
    print(response.content)

if __name__ == "__main__":
    # Madison NJ
    schedule.every(10).minutes.do(get_weather_alerts)
    print("Get Weather Alerts Scheduled")

while True:
    schedule.run_pending()
    time.sleep(1)
    
eventTypes = [
        #"911 Telephone Outage Emergency",
        #"Administrative Message",
        #"Air Quality Alert",
        #"Air Stagnation Advisory",
        #"Arroyo And Small Stream Flood Advisory",
        #"Ashfall Advisory",
        #"Ashfall Warning",
        #"Avalanche Advisory",
        #"Avalanche Warning",
        #"Avalanche Watch",
        #"Beach Hazards Statement",
        "Blizzard Warning",
        "Blizzard Watch",
        #"Blowing Dust Advisory",
        #"Blowing Dust Warning",
        "Brisk Wind Advisory",
        #"Child Abduction Emergency",
        "Civil Danger Warning",
        "Civil Emergency Message",
        #"Coastal Flood Advisory",
        #"Coastal Flood Statement",
        #"Coastal Flood Warning",
        #"Coastal Flood Watch",
        #"Dense Fog Advisory",
        #"Dense Smoke Advisory",
        #"Dust Advisory",
        #"Dust Storm Warning",
        #"Earthquake Warning",
        #"Evacuation - Immediate",
        "Excessive Heat Warning",
        "Excessive Heat Watch",
        "Extreme Cold Warning",
        "Extreme Cold Watch",
        #"Extreme Fire Danger",
        "Extreme Wind Warning",
        #"Fire Warning",
        #"Fire Weather Watch",
        #"Flash Flood Statement",
        #"Flash Flood Warning",
        #"Flash Flood Watch",
        #"Flood Advisory",
        #"Flood Statement",
        #"Flood Warning",
        #"Flood Watch",
        "Freeze Warning",
        "Freeze Watch",
        "Freezing Fog Advisory",
        "Freezing Rain Advisory",
        "Freezing Spray Advisory",
        #"Frost Advisory",
        "Gale Warning",
        "Gale Watch",
        "Hard Freeze Warning",
        "Hard Freeze Watch",
        #"Hazardous Materials Warning",
        #"Hazardous Seas Warning",
        #"Hazardous Seas Watch",
        #"Hazardous Weather Outlook",
        #"Heat Advisory",
        #"Heavy Freezing Spray Warning",
        #"Heavy Freezing Spray Watch",
        #"High Surf Advisory",
        #"High Surf Warning",
        "High Wind Warning",
        "High Wind Watch",
        "Hurricane Force Wind Warning",
        "Hurricane Force Wind Watch",
        "Hurricane Local Statement",
        "Hurricane Warning",
        "Hurricane Watch",
        #"Hydrologic Advisory",
        #"Hydrologic Outlook",
        "Ice Storm Warning",
        #"Lake Effect Snow Advisory",
        #"Lake Effect Snow Warning",
        #"Lake Effect Snow Watch",
        #"Lake Wind Advisory",
        #"Lakeshore Flood Advisory",
        #"Lakeshore Flood Statement",
        #"Lakeshore Flood Warning",
        #"Lakeshore Flood Watch",
        #"Law Enforcement Warning",
        #"Local Area Emergency",
        #"Low Water Advisory",
        #"Marine Weather Statement",
        #"Nuclear Power Plant Warning",
        #"Radiological Hazard Warning",
        #"Red Flag Warning",
        #"Rip Current Statement",
        "Severe Thunderstorm Warning",
        "Severe Thunderstorm Watch",
        "Severe Weather Statement",
        "Shelter In Place Warning",
        #"Short Term Forecast",
        #"Small Craft Advisory",
        #"Small Craft Advisory For Hazardous Seas",
        #"Small Craft Advisory For Rough Bar",
        #"Small Craft Advisory For Winds",
        #"Small Stream Flood Advisory",
        "Snow Squall Warning",
        #"Special Marine Warning",
        #"Special Weather Statement",
        #"Storm Surge Warning",
        #"Storm Surge Watch",
        "Storm Warning",
        "Storm Watch",
        #"Test",
        "Tornado Warning",
        "Tornado Watch",
        "Tropical Depression Local Statement",
        "Tropical Storm Local Statement",
        "Tropical Storm Warning",
        "Tropical Storm Watch",
        #"Tsunami Advisory",
        #"Tsunami Warning",
        #"Tsunami Watch",
        #"Typhoon Local Statement",
        #"Typhoon Warning",
        #"Typhoon Watch",
        #"Urban And Small Stream Flood Advisory",
        #"Volcano Warning",
        "Wind Advisory",
        #"Wind Chill Advisory",
        #"Wind Chill Warning",
        #"Wind Chill Watch",
        "Winter Storm Warning",
        "Winter Storm Watch",
        "Winter Weather Advisory"
    ]
