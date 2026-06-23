import re

def clean_text(text):
    """
    Cleans the input email text by lowercasing it and removing punctuation 
    and special characters, leaving only words and numbers.
    """
    if not isinstance(text, str):
        return ""
    
    # Convert text to lowercase
    text = text.lower()
    
    # Remove punctuation and special characters (keep letters, numbers, and spaces)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    
    # Collapse multiple spaces into a single space and remove leading/trailing spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

if __name__ == "__main__":
    # Test the clean_text function
    sample_text = "Dear Customer, your Chase Bank account has been suspended! Click here: http://192.168.5.23/login.php."
    print("Original text:")
    print(sample_text)
    print("\nCleaned text:")
    print(clean_text(sample_text))
