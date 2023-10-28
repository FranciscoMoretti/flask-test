from flask import Flask, request, jsonify
import pypandoc
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"



@app.route('/api/compare-files', methods=['POST'])
def compare_files():
    try:
        file1 = request.files['file1']
        file2 = request.files['file2']

        if file1 and file2:
            file1_content = file1.read().decode('utf-8')
            file2_content = file2.read().decode('utf-8')

            soup = BeautifulSoup(file1_content, "html.parser")

            common_text = pypandoc.convert_text(
                source=soup, format="html", to="gfm"
            )
            

            response = {
                "common_text": common_text
            }

            return jsonify(response)

        return jsonify({"error": "File upload failed."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500