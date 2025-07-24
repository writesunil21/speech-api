from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import tempfile
import os

app = Flask(__name__)
CORS(app)

model = whisper.load_model("tiny")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    try:
        if "audio" not in request.files:
            return jsonify({"error": "No audio file uploaded"}), 400

        audio = request.files["audio"]

        # 🔥 Use original file extension (e.g., .mp3)
        suffix = os.path.splitext(audio.filename)[1] or ".webm"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            temp_path = tmp.name
            audio.save(temp_path)

        # 🧠 Transcribe using Whisper
        result = model.transcribe(temp_path)

        # 🧹 Delete temp file
        try:
            os.remove(temp_path)
        except Exception as e:
            print(f"Warning: Could not delete temp file: {e}")

        return jsonify({"text": result["text"]})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
