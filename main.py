import machine
import network
import socket
import time
import urequests
import dht

# Konfigurasi Wi-Fi
SSID = 'your_wifi_ssid'
PASSWORD = 'your_wifi_password'

# Konfigurasi Webhook Discord
DISCORD_WEBHOOK_URL = 'your_discord_webhook_url'

# Inisialisasi sensor DHT11
dht_pin = machine.Pin(4)  # Ganti dengan pin yang sesuai
sensor = dht.DHT11(dht_pin)

# Fungsi untuk menghubungkan ke Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    while not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        time.sleep(1)
    
    print("Connected to Wi-Fi:", wlan.ifconfig())

# Fungsi untuk mengirim notifikasi ke Discord
def send_discord_notification(message):
    data = {
        "content": message,
        "username": "Webhook Notification"  # Mengatur username
    }
    try:
        response = urequests.post(DISCORD_WEBHOOK_URL, json=data)
        print("Notification sent:", response.text)
    except Exception as e:
        print("Error sending notification:", e)

# Fungsi untuk menangani permintaan HTTP
def web_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Listening on", addr)

    while True:
        cl, addr = s.accept()
        print('Client connected from', addr)
        request = cl.recv(1024)
        request = str(request)
        print("Request:", request)

        # Membaca suhu dan kelembaban
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()

        # Mengirim notifikasi jika suhu di bawah 20°C atau di atas 30°C
        if temperature < 20:
            send_discord_notification(f"Suhu dingin: {temperature}°C, Kelembaban: {humidity}%")
        elif temperature > 30:
            send_discord_notification(f"Suhu panas: {temperature}°C, Kelembaban: {humidity}%")

        # Membuat respons HTML
        response = f"""HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
    <title>Monitor Suhu dan Kelembaban</title>
</head>
<body>
    <h1>Data Sensor DHT11</h1>
    <p>Suhu: {temperature}°C</p>
    <p>Kelembaban: {humidity}%</p>
</body>
</html>
"""
        cl.send(response)
        cl.close()

# Main program
connect_wifi()
web_server()
