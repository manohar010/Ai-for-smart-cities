import requests
import json
import time
import random

# Backend API URL
API_URL = "http://localhost:5000/api/crowd"

# Locations to simulate
LOCATIONS = ["Main Gate", "Cafeteria", "Library", "CS Block"]

def send_crowd_data():
    """
    Simulates the AI module detecting people and sending the count to the backend.
    """
    print("Starting AI module data simulation...")
    try:
        while True:
            # Generate random simulation data
            location = random.choice(LOCATIONS)
            count = random.randint(5, 100)
            
            # Determine alert level based on count
            if count > 80:
                alert_level = "Critical"
            elif count > 50:
                alert_level = "Warning"
            else:
                alert_level = "Normal"
                
            payload = {
                "location": location,
                "count": count,
                "alertLevel": alert_level
            }
            
            # Send POST request
            print(f"Sending data: {payload}")
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 201:
                print(f"Successfully saved! Server responded: {response.json()}")
            else:
                print(f"Failed to save. Status code: {response.status_code}, Error: {response.text}")
                
            # Wait for next detection (e.g., 5 seconds)
            time.sleep(5)
            
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Connection refused!")
        print("Make sure the Node.js backend server is running on port 5000.")
    except KeyboardInterrupt:
        print("\nStopped simulation.")

if __name__ == "__main__":
    send_crowd_data()
