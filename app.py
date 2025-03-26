from flask import Flask, request, jsonify, render_template
from geopy.geocoders import Nominatim

app = Flask(__name__)
geolocator = Nominatim(user_agent="bus_tracker")

# Store bus locations {bus_no: [{'lat': xx, 'lng': yy, 'area': 'xyz'}]}
bus_locations = {}

@app.route('/update_location', methods=['POST'])
def update_location():
    try:
        data = request.get_json()
        print("Received Data:", data)  # Debugging

        if not data or 'bus_no' not in data or 'latitude' not in data or 'longitude' not in data:
            return jsonify({"error": "Missing required fields"}), 400  

        lat, lng = data['latitude'], data['longitude']
        bus_no = data['bus_no']

        # Get Area using Geopy
        location = geolocator.reverse((lat, lng), language="en")
        area = location.address if location else "Unknown"

        # Save data
        if bus_no not in bus_locations:
            bus_locations[bus_no] = []
        bus_locations[bus_no].append({"lat": lat, "lng": lng, "area": area})

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Invalid request"}), 400

@app.route('/get_locations/<bus_no>')
def get_locations(bus_no):
    return jsonify(bus_locations.get(bus_no, []))

if __name__ == '__main__':
    app.run(debug=True)
