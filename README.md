# Sentiment Analysis using Machine Learning & NLP

## 📌 Project Overview
This project performs sentiment analysis on text data using Machine Learning and Natural Language Processing techniques. It classifies user input into positive, negative, or neutral sentiments through a Django-based web interface.

## 🎯 Objectives
- Analyze textual data sentiment
- Apply NLP preprocessing techniques
- Train ML models for sentiment classification
- Build a simple web interface for predictions

## 🧠 Techniques Used
- Text preprocessing (tokenization, stopword removal)
- Feature extraction (TF-IDF / Bag of Words)
- Machine Learning models (Naive Bayes / Logistic Regression)
- NLP concepts

## 🛠️ Tech Stack
- Python
- Django
- Scikit-learn
- NLTK / SpaCy
- HTML, CSS

## 📂 Project Structure
- `sentanapp/` – Django app for sentiment analysis
- `templates/` – UI templates
- `models.py` – ML model integration
- `views.py` – request handling logic

## 🚀 How to Run
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
