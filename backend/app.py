# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp_utils import extract_keywords, calculate_match_score, generate_suggestions
from file_utils import save_uploaded_file, read_file, delete_file

app = Flask(__name__)
CORS(app)

@app.route('/match', methods=['POST'])
def match_resume_jd():
    if 'resume' not in request.files or 'jd' not in request.files:
        return jsonify({'error': 'Missing files'}), 400

    resume_file = request.files['resume']
    jd_file = request.files['jd']

    resume_path = save_uploaded_file(resume_file)
    jd_path = save_uploaded_file(jd_file)

    resume_text = read_file(resume_path)
    jd_text = read_file(jd_path)

    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    match_score = calculate_match_score(resume_keywords, jd_keywords)
    suggestions = generate_suggestions(resume_keywords, jd_keywords, resume_text, jd_text)

    delete_file(resume_path)
    delete_file(jd_path)

    return jsonify({'match_score': match_score, 'suggestions': suggestions})

if __name__ == '__main__':
    app.run(debug=True)