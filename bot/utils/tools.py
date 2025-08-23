from langchain_core.tools import tool
import requests
import os

@tool
def missing_params(**kwargs):
    """
    Identify missing parameters for the flight search API.
    """
    required_params = ["origin", "destination", "depart_date", "return_date"]
    missing = [param for param in required_params if param not in kwargs]
    return missing

@tool
def get_cheap_flights(origin, destination, depart_date, return_date, token):
    """
    Get cheap flight options from the TravelPayouts API.
    """
    url = "https://api.travelpayouts.com/v1/prices/cheap"
    headers = {
        "Content-Type": "application/json",
        "X-Access-Token": os.getenv("TRAVEL_PAYOUTS_API_KEY")
    }
    params = {
        "origin": origin,
        "destination": destination,
        "depart_date": depart_date,
        "return_date": return_date,
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        if not data.get("success"):
            print("API request failed:", data.get("error", "Unknown error"))
            return None

        flights = data.get("data", {}).get(destination, {})
        if not flights:
            print(f"No flights found from {origin} to {destination} on {depart_date}.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None