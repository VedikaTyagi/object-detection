# from flask import Flask, request, jsonify
# from main import perform_object_detection  # Import DETR model functions
# from flask import Flask, render_template

# app = Flask(__name__)


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/detect_objects", methods=["POST"])
# def detect_objects():
#     if "file" not in request.files:
#         return jsonify({"error": "No file part"})

#     file = request.files["file"]
#     if file.filename == "":
#         return jsonify({"error": "No selected file"})

#     temp_image_path = "uploaded_image.jpg"
#     file.save(temp_image_path)

#     detection_results = perform_object_detection(temp_image_path)

#     # Remove the temporary image file
#     # (You may want to handle this differently in production)
#     import os

#     os.remove(temp_image_path)

#     return jsonify(detection_results)


# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, jsonify
from main import perform_object_detection
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/detect_objects", methods=["POST"])
def detect_objects():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})

    temp_image_path = "uploaded_image.jpg"
    file.save(temp_image_path)

    # Perform object detection
    detection_results = perform_object_detection(temp_image_path)

    # Remove the temporary image file
    import os

    os.remove(temp_image_path)

    # Structure the detection results in a format expected by JavaScript
    formatted_results = {
        "detected_objects": [
            {
                "label": obj["label"],
                "confidence": obj["confidence"],
                "bounding_box": obj["bounding_box"],
            }
            for obj in detection_results
        ]
    }

    return jsonify(formatted_results)


if __name__ == "__main__":
    app.run(debug=True)
