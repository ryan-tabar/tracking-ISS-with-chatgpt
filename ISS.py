from flask import Flask, render_template
import folium
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iss_map')
def iss_map():
    # Retrieve the current latitude and longitude of the ISS from the Open Notify API
    response = requests.get("http://api.open-notify.org/iss-now.json")
    data = response.json()
    latitude = data['iss_position']['latitude']
    longitude = data['iss_position']['longitude']

    # Create a map centered on the ISS with zoom level 3
    iss_map = folium.Map(location=[latitude, longitude], zoom_start=3)

    # Add a marker for the ISS to the map using an image and a popup containing the ISS position
    icon = folium.features.CustomIcon('iss.png', icon_size=(50, 50))
    marker = folium.Marker([latitude, longitude], icon=icon, popup=f"Latitude: {latitude}, Longitude: {longitude}", auto_open=True)
    marker.add_to(iss_map)

    # Save the map to an HTML file
    iss_map.save('templates/iss_map.html')

    # Add a meta tag to the HTML file to refresh the page every 5 seconds
    with open('templates/iss_map.html', 'r') as f:
        html = f.read()
    html = html.replace('</head>', '<meta http-equiv="refresh" content="5"></head>')
    with open('templates/iss_map.html', 'w') as f:
        f.write(html)

    return render_template('iss_map.html')

if __name__ == '__main__':
    app.run(debug=True)
