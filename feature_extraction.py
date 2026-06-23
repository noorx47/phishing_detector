import re

# List of common suspicious words often found in phishing emails
SUSPICIOUS_WORDS = [
    "urgent", "suspended", "verify", "congratulations", "billing", 
    "invoice", "action", "security", "warning", "login", "password",
    "immediate", "alert", "expire", "winner", "prize", "account"
]

def count_urls(text):
    """
    Counts the number of HTTP/HTTPS URLs in the raw email text.
    """
    urls = re.findall(r'https?://', text, re.IGNORECASE)
    return len(urls)

def count_ip_links(text):
    """
    Counts how many links contain an IP address instead of a domain name.
    Example: http://192.168.5.23/login.php
    """
    ip_links = re.findall(r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text, re.IGNORECASE)
    return len(ip_links)

def count_suspicious_words(text):
    """
    Counts the occurrences of predefined suspicious words.
    Uses regex boundary checks (\b) to count whole words only.
    """
    text_lower = text.lower()
    count = 0
    for word in SUSPICIOUS_WORDS:
        # Match whole words only to avoid false positives (e.g., 'action' inside 'transactional')
        pattern = r'\b' + re.escape(word) + r'\b'
        count += len(re.findall(pattern, text_lower))
    return count

def count_exclamations(text):
    """
    Counts the number of exclamation marks in the email.
    """
    return text.count('!')

def count_all_caps_words(text):
    """
    Counts words containing only uppercase letters that are longer than 1 character.
    Example: URGENT, ATTENTION (ignores 'I' or 'A').
    """
    # Matches words with 2 or more consecutive capital letters
    words = re.findall(r'\b[A-Z]{2,}\b', text)
    return len(words)

def get_handcrafted_features(text):
    """
    Extracts all handcrafted features from the raw email text and
    returns them as a dictionary for easy database insertion and reporting.
    """
    return {
        "num_urls": count_urls(text),
        "num_ip_links": count_ip_links(text),
        "num_suspicious_words": count_suspicious_words(text),
        "num_exclamations": count_exclamations(text),
        "num_all_caps": count_all_caps_words(text),
        "email_length": len(text)
    }

def get_feature_vector(text):
    """
    Converts the features dictionary into a flat list of numerical values
    ready to be combined with text features for machine learning.
    """
    features = get_handcrafted_features(text)
    return [
        features["num_urls"],
        features["num_ip_links"],
        features["num_suspicious_words"],
        features["num_exclamations"],
        features["num_all_caps"],
        features["email_length"]
    ]

if __name__ == "__main__":
    # Test our features on a mock phishing email
    sample_email = "URGENT: Verify your account immediately! Click here: http://192.168.5.23/login.php. This is your final warning!"
    
    print("Sample Email text:")
    print(sample_email)
    print("\nExtracted features dict:")
    features_dict = get_handcrafted_features(sample_email)
    for key, val in features_dict.items():
        print(f"  {key}: {val}")
        
    print("\nExtracted feature vector:")
    print(f"  {get_feature_vector(sample_email)}")
