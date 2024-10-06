import requests
from datetime import date, timedelta
import json

def get_nasa_power_data(lat, lon, start_date, end_date):
    base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "start": start_date,
        "end": end_date,
        "latitude": lat,
        "longitude": lon,
        "community": "ag",
        "parameters": "T2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN",
        "format": "JSON"
    }
    response = requests.get(base_url, params=params)
    print(response)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch NASA data: {response.status_code} {response.text}")


def test_nasa_power_api():
    # Sample parameters
    lat = 19.7515
    lon = 75.7139
    start_date = date(2024, 6, 21)  # June 21st, 2024
    end_date = start_date + timedelta(days=7)  # 7 days from start date

    # Convert dates to string format required by the API
    start_date_str = start_date.strftime("%Y%m%d")
    end_date_str = end_date.strftime("%Y%m%d")

    try:
        data = get_nasa_power_data(lat, lon, start_date_str, end_date_str)
        print("API request successful!")
        print("Sample of the data received:")
        print(json.dumps(data, indent=2)[:1000])  # Print first 1000 characters of the formatted JSON
    except Exception as e:
        print(f"API request failed: {str(e)}")

if __name__ == "__main__":
    test_nasa_power_api()