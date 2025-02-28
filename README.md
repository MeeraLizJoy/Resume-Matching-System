# Resume Matching System

A web application that matches resumes to job descriptions using advanced Natural Language Processing (NLP) techniques. It provides a match score and actionable suggestions for resume improvement.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [NLP Techniques](#nlp-techniques)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)


## Features

- **Resume and Job Description Upload:** Users can upload resumes (PDF, DOCX, TXT) and job descriptions (PDF, DOCX, TXT).
- **Advanced NLP Processing:** Uses Word2Vec, Sentence-BERT, and other NLP techniques for accurate matching.
- **Match Score:** Provides a numerical match score indicating the compatibility between the resume and job description.
- **Actionable Suggestions:** Generates categorized suggestions for resume improvement, including skills, experience, and general enhancements.
- **User-Friendly Interface:** A clean and intuitive React frontend for easy interaction.

## Technologies Used

- **Backend:**
    - Python
    - Flask (API framework)
    - spaCy (NLP library)
    - scikit-learn (machine learning)
    - Gensim (Word2Vec)
    - Sentence Transformers (Sentence-BERT)
    - PyPDF2 (PDF handling)
    - python-docx (DOCX handling)
- **Frontend:**
    - React
    - Material UI (UI component library)
    - Axios (HTTP client)
- **Other:**
    - Node.js (for frontend)
    - npm (package manager)


    ## Installation

1.  **Clone the Repository:**
    ```bash
    git clone [your-repository-url]
    cd ResumeMatchingSystem
    ```
2.  **Backend Setup:**
    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    pip install -r requirements.txt
    #Download GoogleNews-vectors-negative300.bin and place it in the backend folder.
    python app.py
    ```
3.  **Frontend Setup:**
    ```bash
    cd ../frontend
    npm install
    npm start
    ```
4.  **Access the Application:**
    * Open your browser and go to `http://localhost:3000`.


## Usage

1.  Upload your resume and the job description using the file upload inputs.
2.  Click the "Match" button.
3.  View the match score and suggestions for resume improvement.


## Architecture

The application follows a client-server architecture:

-   **Frontend (React):** Handles user interactions and displays the results.
-   **Backend (Flask):** Processes file uploads, performs NLP tasks, and returns the match score and suggestions.
-   **NLP Modules:** The NLP logic is organized into separate modules for better maintainability.


## NLP Techniques

-   **Text Preprocessing:** Cleaning and normalizing text data.
-   **Keyword Extraction:** Identifying relevant keywords using POS tagging and lemmatization.
-   **Word Embeddings (Word2Vec):** Calculating word-level semantic similarity.
-   **Sentence Embeddings (Sentence-BERT):** Capturing contextual similarity between resume and job description sections.
-   **Lexical Matching:** Comparing the frequency of keywords.
-   **Combined Match Score:** Combining lexical and semantic similarity scores.
-   **Suggestion Generation:** Providing contextual and actionable suggestions for resume improvement.

## Future Enhancements

-   Implement Named Entity Recognition (NER) for more accurate skill extraction.
-   Enhance resume structure analysis to identify and extract information from different sections.
-   Add fuzzy matching to handle variations in skill names.
-   Implement a ranking system to prioritize suggestions.
-   Improve error handling and input validation.
-   Add user authentication and authorization.
-   Deploy the application to a cloud platform.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

[MIT License]

## Author

Meera Liz Joy
# Resume-Matching-System
