# backend/nlp_utils.py
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim.models import KeyedVectors
import numpy as np
import re

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

stop_words = set(stopwords.words('english'))
additional_stops = {"eg", "etc", "experience", "used", "familiarity", "problem", "ability", "detail", "way", "making", "process", "role", "organization", "provide", "used", "challenging", "join", "strong", "result", "understanding"}
stop_words.update(additional_stops)

lemmatizer = WordNetLemmatizer()

# Load Word2Vec model
word2vec_model = KeyedVectors.load_word2vec_format(
    '/Users/meeralizjoy/Desktop/ResumeMatchingSystem/backend/GoogleNews-vectors-negative300.bin',
    binary=True
)

def preprocess_text(text):
    """Preprocesses text for NLP tasks."""
    text = re.sub(r'[^\w\s]', '', text).lower()
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return tokens

def extract_keywords(text):
    """Extracts relevant keywords from preprocessed text."""
    tokens = preprocess_text(text)
    tagged_tokens = nltk.pos_tag(tokens)
    relevant_tokens = [
        token for token, pos in tagged_tokens
        if pos.startswith(('NN', 'VB', 'JJ', 'RB'))
    ]
    return relevant_tokens

def calculate_semantic_similarity(resume_keywords, jd_keywords):
    """Calculates semantic similarity using Word2Vec."""
    resume_vectors = [word2vec_model[word] for word in resume_keywords if word in word2vec_model]
    jd_vectors = [word2vec_model[word] for word in jd_keywords if word in word2vec_model]

    if not resume_vectors or not jd_vectors:
        return 0.0

    resume_vector = np.mean(resume_vectors, axis=0)
    jd_vector = np.mean(jd_vectors, axis=0)

    similarity = np.dot(resume_vector, jd_vector) / (np.linalg.norm(resume_vector) * np.linalg.norm(jd_vector))
    return similarity

def calculate_match_score(resume_keywords, jd_keywords):
    """Calculates the match score (combined lexical and semantic)."""
    lexical_score = calculate_lexical_match_score(resume_keywords, jd_keywords)
    semantic_score = calculate_semantic_similarity(resume_keywords, jd_keywords)

    return 0.6 * lexical_score + 0.4 * semantic_score

def calculate_lexical_match_score(resume_keywords, jd_keywords):
    """Calculates lexical match score."""
    if not jd_keywords:
        return 0.0

    jd_counter = Counter(jd_keywords)
    resume_counter = Counter(resume_keywords)

    common_keywords = sum((resume_counter & jd_counter).values())
    total_jd_keywords = sum(jd_counter.values())

    return common_keywords / total_jd_keywords if total_jd_keywords > 0 else 0.0

def find_requirements_sections(jd_text):
    """Finds requirement sections in the JD."""
    section_patterns = [
        r"(Requirements|Qualifications|Job Requirements|Skill Requirements|Candidate Requirements|Is This Role For You?|What You'll Need|Desired Skills):([\s\S]*?)(?=\n\n|\Z)",
    ]
    requirements_text = ""
    for pattern in section_patterns:
        match = re.search(pattern, jd_text, re.IGNORECASE)
        if match:
            requirements_text += match.group(2).strip() + " "
    return requirements_text.strip()

def generate_suggestions(resume_keywords, jd_keywords, resume_text, jd_text):
    """Generates categorized and contextual suggestions for resume improvement."""
    requirements_text = find_requirements_sections(jd_text)
    requirements_keywords = extract_keywords(requirements_text)
    jd_counter = Counter(requirements_keywords)

    missing_keywords = set(requirements_keywords) - set(resume_keywords)

    keyword_frequencies = {keyword: jd_counter[keyword] for keyword in missing_keywords if keyword in jd_counter} #Added check.

    sorted_keywords = sorted(keyword_frequencies.items(), key=lambda item: item[1], reverse=True)
    top_n_keywords = sorted_keywords[:5]  # Limit to top 5

    suggestions = {
        "Skills": [],
        "Experience": [],
        "General Improvements": []
    }

    for item in top_n_keywords:
        if isinstance(item, tuple) and len(item) == 2: #Added check.
            keyword, frequency = item
            if nltk.pos_tag([keyword])[0][1].startswith(('NN', 'VB', 'JJ')):
                if keyword in ["team","collaboration","leadership"]:
                    suggestions["Experience"].append(f"Highlight your experience with '{keyword}' in your experience section, as it's mentioned in the job description ({frequency} times).")
                else:
                    suggestions["Skills"].append(f"Add '{keyword}' to your skills section, as it's mentioned in the job description ({frequency} times).")
            else:
                suggestions["General Improvements"].append(f"Consider using '{keyword}' in your resume, as it's mentioned in the job description ({frequency} times).")

    jd_bigrams = [' '.join(jd_keywords[i:i + 2]) for i in range(len(jd_keywords) - 1)]
    resume_bigrams = [' '.join(resume_keywords[i:i + 2]) for i in range(len(resume_keywords) - 1)]

    for bigram in jd_bigrams:
        if bigram not in resume_bigrams and bigram.split()[0] in resume_keywords and bigram.split()[1] in resume_keywords:
            suggestions["Experience"].append(f"Consider using '{bigram}' as in the JD, if it matches your experience.")

    return suggestions