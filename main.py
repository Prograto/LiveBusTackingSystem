from flask import Flask, request, jsonify, render_template
from datetime import datetime
from geopy.geocoders import Nominatim

app = Flask(__name__)
geolocator = Nominatim(user_agent="bus_tracker")

locations = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_location', methods=['POST'])
def submit_location():
    data = request.json
    lat = data.get('latitude')
    lng = data.get('longitude')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if lat is not None and lng is not None:
        # Reverse geocoding to get area name
        location = geolocator.reverse((lat, lng), exactly_one=True)
        area = location.address if location else "Unknown Area"
        
        locations.append({'lat': lat, 'lng': lng, 'time': timestamp, 'area': area})
        return jsonify({'message': 'Location received', 'area': area}), 200
    else:
        return jsonify({'error': 'Invalid data'}), 400

@app.route('/get_locations', methods=['GET'])
def get_locations():
    return jsonify(locations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
