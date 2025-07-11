from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from database import fs, db
import io
from bson import ObjectId
import os
from geopy.geocoders import Nominatim

app = Flask(__name__)
CORS(app, origins=["https://vrgallery.netlify.app"])

def get_location_details(latitude, longitude):
    try:
        geolocator = Nominatim(user_agent="image_upload_app")
        location = geolocator.reverse(f"{latitude}, {longitude}")
        if location:
            address = location.raw.get('address', {})
            return {
                "district": address.get('county', 'Unknown'),
                "state": address.get('state', 'Unknown'),
                "country": address.get('country', 'Unknown'),
                "city": address.get('city', address.get('town', address.get('village', 'Unknown'))),
                "postcode": address.get('postcode', 'Unknown')
            }
        return None
    except Exception as e:
        print(f"Location lookup error: {e}")
        return None

@app.route('/images', methods=['GET'])
def get_all_images():
    files = db.fs.files.find({}, {"_id": 1, "username": 1, "email": 1, "likes": 1, "location": 1})
    return jsonify([
        {
            "_id": str(file["_id"]),
            "username": file.get("username", ""),
            "email": file.get("email", ""),
            "likes": len(file.get("likes", [])),
            "location": file.get("location")
        } for file in files
    ])

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file found"}), 400

        image_file = request.files['image']
        if not image_file.filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
            return jsonify({"error": "Invalid image format. Only JPG, PNG, GIF allowed."}), 400

        username = request.form.get('username')
        email = request.form.get('email')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        if not username or not email:
            return jsonify({"error": "Username and email are required"}), 400

        location_data = None
        location_details = None
        if latitude and longitude:
            location_data = {
                "type": "Point",
                "coordinates": [float(longitude), float(latitude)]
            }
            location_details = get_location_details(latitude, longitude)

        file_id = fs.put(
            image_file,
            filename=image_file.filename,
            username=username,
            email=email,
            likes=[],
            location=location_data,
            location_details=location_details
        )

        return jsonify({
            "message": "Image uploaded successfully",
            "file_id": str(file_id),
            "username": username,
            "email": email,
            "location": location_data,
            "location_details": location_details
        }), 201

    except Exception as e:
        print("Upload error:", e)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/image/<file_id>', methods=['GET'])
def get_image(file_id):
    try:
        image_data = fs.get(ObjectId(file_id))
        return send_file(io.BytesIO(image_data.read()), mimetype="image/jpeg")
    except Exception as e:
        print("Image retrieval error:", e)
        return jsonify({"error": "Image not found"}), 404

@app.route('/image/<file_id>/like', methods=['POST'])
def like_image(file_id):
    try:
        user_ip = request.remote_addr
        image_data = db.fs.files.find_one({"_id": ObjectId(file_id)})

        if not image_data:
            return jsonify({"error": "Image not found"}), 404

        if user_ip in image_data.get("likes", []):
            return jsonify({"message": "You have already liked this image"}), 400

        db.fs.files.update_one({"_id": ObjectId(file_id)}, {"$push": {"likes": user_ip}})
        return jsonify({"message": "Image liked successfully"}), 200

    except Exception as e:
        print("Like error:", e)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/images/with-location', methods=['GET'])
def get_images_with_location():
    try:
        files = db.fs.files.find({
            "location": {"$exists": True, "$ne": None}
        }, {
            "_id": 1,
            "username": 1,
            "email": 1,
            "likes": 1,
            "location": 1,
            "location_details": 1
        })
        return jsonify([
            {
                "_id": str(file["_id"]),
                "username": file.get("username", ""),
                "email": file.get("email", ""),
                "likes": len(file.get("likes", [])),
                "location": file.get("location"),
                "location_details": file.get("location_details", {})
            } for file in files
        ])
    except Exception as e:
        print("Geolocation retrieval error:", e)
        return jsonify({"error": "Could not retrieve geotagged images"}), 500

@app.route('/get-location-details', methods=['GET'])
def get_location_details_route():
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        if not lat or not lon:
            return jsonify({"error": "Latitude and longitude are required"}), 400
        details = get_location_details(lat, lon)
        return jsonify(details) if details else jsonify({"error": "Not found"}), 404
    except Exception as e:
        print("Location route error:", e)
        return jsonify({"error": "Internal server error"}), 500