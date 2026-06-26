import numpy as np
import joblib

from preprocess import clean_text
from feature_extraction import get_feature_vector

# Paths to the saved model and vectorizer
MODEL_PATH = "saved_model/phishing_model.joblib"
VECTORIZER_PATH = "saved_model/tfidf_vectorizer.joblib"

def load_model():
    """
    Loads the trained model and TF-IDF vectorizer from disk.
    Returns both as a tuple (model, vectorizer).
    """
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer

def analyze_email(email_text, model, vectorizer):
    """
    Takes a raw email string and returns the prediction result.
    Returns a dictionary with the verdict, confidence, and extracted features.
    """
    # Step 1: Extract handcrafted features from the raw text
    handcrafted = get_feature_vector(email_text)
    
    # Step 2: Clean the text and transform it using the saved vectorizer
    cleaned = clean_text(email_text)
    tfidf_features = vectorizer.transform([cleaned]).toarray()
    
    # Step 3: Combine TF-IDF and handcrafted features into one row
    combined = np.hstack((tfidf_features, [handcrafted]))
    
    # Step 4: Make the prediction
    prediction = model.predict(combined)[0]
    confidence = model.predict_proba(combined)[0]
    
    # Build a readable result dictionary
    verdict = "phishing" if prediction == 1 else "legitimate"
    confidence_score = confidence[prediction]
    
    result = {
        "verdict": verdict,
        "confidence": round(confidence_score * 100, 2),
        "handcrafted_features": {
            "num_urls": handcrafted[0],
            "num_ip_links": handcrafted[1],
            "num_suspicious_words": handcrafted[2],
            "num_exclamations": handcrafted[3],
            "num_all_caps": handcrafted[4],
            "email_length": handcrafted[5]
        }
    }
    return result

if __name__ == "__main__":
    # Quick test with a phishing-style email
    test_phishing = "URGENT: Your PayPal account has been suspended! Verify your identity now at http://192.168.5.23/login.php or your account will be permanently closed!"
    
    # Quick test with a legitimate-style email
    test_legit = "Hi Sarah, just checking in to see if you had a chance to review the project document I sent yesterday. Let me know if you have any questions."
    
    model, vectorizer = load_model()
    
    print("--- Test 1: Phishing Email ---")
    print(f"Text: {test_phishing}\n")
    result1 = analyze_email(test_phishing, model, vectorizer)
    print(f"Verdict: {result1['verdict'].upper()}")
    print(f"Confidence: {result1['confidence']}%")
    print(f"Features: {result1['handcrafted_features']}")
    
    print("\n--- Test 2: Legitimate Email ---")
    print(f"Text: {test_legit}\n")
    result2 = analyze_email(test_legit, model, vectorizer)
    print(f"Verdict: {result2['verdict'].upper()}")
    print(f"Confidence: {result2['confidence']}%")
    print(f"Features: {result2['handcrafted_features']}")
