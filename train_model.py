import csv
import os
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Import preprocess and feature extraction functions we wrote earlier
from preprocess import clean_text
from feature_extraction import get_feature_vector

def train_phishing_detector():
    print("Loading dataset from data/emails.csv...")
    
    # Lists to store raw text and corresponding binary labels
    emails_text = []
    labels = []
    
    # Load emails using Python's built-in CSV reader (no pandas needed)
    with open("data/emails.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            emails_text.append(row["email_text"])
            # Label conversion: 1 for phishing, 0 for legitimate
            labels.append(1 if row["label"] == "phishing" else 0)
            
    print(f"Loaded {len(emails_text)} emails.")
    
    print("Extracting handcrafted features from raw email text...")
    # Extract handcrafted features for all emails
    X_handcrafted = []
    for text in emails_text:
        X_handcrafted.append(get_feature_vector(text))
    X_handcrafted = np.array(X_handcrafted)
    
    print("Cleaning text and fitting TF-IDF Vectorizer...")
    # Clean text using preprocess.py
    cleaned_texts = [clean_text(text) for text in emails_text]
    
    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()
    X_tfidf_sparse = vectorizer.fit_transform(cleaned_texts)
    # Convert sparse TF-IDF matrix to dense array to easily stack features
    X_tfidf = X_tfidf_sparse.toarray()
    
    # Combine TF-IDF features and handcrafted features side-by-side
    X_combined = np.hstack((X_tfidf, X_handcrafted))
    y = np.array(labels)
    
    # Split the dataset into 80% train and 20% test (using stratify to balance labels)
    X_train, X_test, y_train, y_test = train_test_split(
        X_combined, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("Training Random Forest Classifier...")
    # Initialize and fit the classifier
    model = RandomForestClassifier(random_state=42, n_estimators=50)
    model.fit(X_train, y_train)
    
    print("\nEvaluating model performance on the test set:")
    # Make predictions on test set
    y_pred = model.predict(X_test)
    
    # Calculate and show accuracy and detailed metrics
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Legitimate", "Phishing"]))
    
    # Ensure saved_model directory exists and save the trained artifacts
    os.makedirs("saved_model", exist_ok=True)
    joblib.dump(model, "saved_model/phishing_model.joblib")
    joblib.dump(vectorizer, "saved_model/tfidf_vectorizer.joblib")
    print("Model and vectorizer saved successfully to 'saved_model/' folder.")

if __name__ == "__main__":
    train_phishing_detector()
