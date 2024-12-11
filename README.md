
# DHT11 Temperature and Humidity Monitor with Discord Notifications

Proyek ini adalah aplikasi berbasis MicroPython yang menggunakan sensor DHT11 untuk memantau suhu dan kelembaban. Aplikasi ini juga memiliki web server untuk menampilkan data secara real-time dan mengirim notifikasi ke Discord melalui webhook ketika suhu berada di bawah 20°C (dingin) atau di atas 30°C (panas).

## Fitur

- Memantau suhu dan kelembaban menggunakan sensor DHT11.
- Menampilkan data suhu dan kelembaban melalui web server.
- Mengirim notifikasi ke Discord ketika suhu mencapai ambang batas tertentu.
- Mudah diatur dan digunakan dengan ESP8266 atau ESP32.

## Persyaratan

- **Hardware**:
  - ESP8266 atau ESP32
  - Sensor DHT11
  - Koneksi Wi-Fi

- **Software**:
  - MicroPython
  - Library `dht` dan `network` (sudah termasuk dalam firmware MicroPython)

## Instalasi

1. **Persiapkan Hardware**:
   - Hubungkan sensor DHT11 ke board ESP8266/ESP32 Anda. Pastikan untuk mencatat pin yang digunakan.

2. **Instal MicroPython**:
   - Pastikan Anda telah menginstal MicroPython pada board Anda. Anda dapat mengikuti petunjuk di [situs resmi MicroPython](https://micropython.org/download/).

3. **Unggah Kode**:
   - Salin kode program yang disediakan di bawah ini ke dalam file Python (misalnya `main.py`).
   - Ganti `your_wifi_ssid`, `your_wifi_password`, dan `your_discord_webhook_url` dengan informasi yang sesuai.

```python
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
```

4. **Jalankan Program**:
   - Setelah mengunggah kode, jalankan program di board Anda. Anda dapat mengakses web server dengan membuka alamat IP board di browser.

## Penggunaan

- Setelah program berjalan, Anda dapat mengakses data suhu dan kelembaban melalui web browser dengan mengunjungi alamat IP board Anda.
- Notifikasi akan dikirim ke Discord setiap kali suhu berada di bawah 20°C atau di atas 30°C.

## Kontribusi

Jika Anda ingin berkontribusi pada proyek ini, silakan buat fork dari repositori ini dan kirim pull request dengan perubahan Anda.

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

## Kontak

Jika Anda memiliki pertanyaan atau saran, silakan hubungi saya di [admin@unreliablecode.net](mailto:admin@unreliablecode.net).
