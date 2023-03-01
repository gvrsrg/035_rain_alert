#Note! For the code to work you need to replace all the placeholders with
#Your own details. e.g. account_sid, lat/lon, from/to phone numbers.

import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import credentials

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = credentials.api_key #os.environ.get("OWM_API_KEY")
account_sid = credentials.account_sid #"YOUR ACCOUNT SID"
auth_token = credentials.auth_token #os.environ.get("AUTH_TOKEN")

weather_params = {
    "lat": 31.893730,
    "lon": 34.811067,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["list"][:4]

will_rain = False
need_water = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
    temperature = int(hour_data["main"]["temp"])-273.15
    if temperature > 20:
        need_water = True

if will_rain or need_water:
    proxy_client = TwilioHttpClient()
#    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    umbrella_text = ("", "It's going to rain today. Remember to bring an ☔️")[will_rain]
    water_text = ("", "It's going to be hot today.  Dont forget to take your water!️")[need_water]
    divider = ("","\n")[will_rain and need_water]
    message_body = f"{umbrella_text}{divider}{water_text}"

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        body=message_body,
        from_=credentials.MY_PHONE_NUMBER_FROM,
        to=credentials.MY_PHONE_NUMBER_TO
    )
    print(message.status)
