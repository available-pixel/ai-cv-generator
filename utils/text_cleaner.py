# utils/text_cleaner.py

def clean_text(text: str) -> str:
    """
    Clean a string by:
    - stripping leading/trailing spaces
    - replacing multiple spaces with a single space
    - ensuring proper capitalization for sentences
    """
    if not text:
        return ""
    
    # Strip spaces
    text = text.strip()
    
    # Replace multiple spaces with single space
    import re
    text = re.sub(r'\s+', ' ', text)
    
    # Capitalize first letter
    text = text[0].upper() + text[1:] if len(text) > 0 else text
    
    return text