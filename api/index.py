from flask import Flask, request, jsonify
import pypandoc
from bs4 import BeautifulSoup
import tempfile
import os

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
            # file1_content = file1.read().decode('utf-8')
            # file2_content = file2.read().decode('utf-8')

            with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as temp_file1:
                file1.save(temp_file1.name)
                article_epub_file_path = temp_file1.name

                output = pypandoc.convert_file(
                    source_file=article_epub_file_path,
                    format="epub",
                    to="html",
                )

                soup = BeautifulSoup(output, "html.parser")

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
    finally:
        # Clean up temporary files
        os.unlink(article_epub_file_path)