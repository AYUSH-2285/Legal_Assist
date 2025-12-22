"""
normalizer.py - Text normalization and language detection
Converts user input to lowercase, removes punctuation, detects language mix
"""

import re
import json
from typing import Dict, List, Tuple

# Hindi to English transliteration mapping (common Hinglish words)
HINGLISH_MAP = {
    # Police/Authority
    'police': 'police', 'cop': 'cop', 'thana': 'police', 'thanedar': 'police',
    'sipahi': 'police', 'uniform': 'police', 'khaki': 'police',
    
    # Actions
    'roka': 'stopped', 'rukne': 'stopped', 'rukwaya': 'stopped',
    'jane nahi diya': 'prevented from leaving',
    'gaali': 'abuse', 'badmashi': 'insult', 'badhejabi': 'disrespect',
    'dhamki': 'threat', 'dar': 'fear', 'maarunga': 'will beat',
    
    # Relationships
    'bhai': 'brother', 'bahan': 'sister', 'rishta': 'relationship',
    'saath': 'together', 'couple': 'couple',
    
    # Age
    '18 saal': '18 years', 'balig': 'adult', 'badi umar': 'grown up',
    
    # Negation
    'kuch nahi kiya': 'did nothing', 'innocent': 'innocent',
    'apradh nahi': 'no crime',
}

class Normalizer:
    def __init__(self):
        self.hinglish_map = HINGLISH_MAP
    
    def normalize(self, text: str) -> str:
        """
        Normalize user input:
        1. Convert to lowercase
        2. Remove extra whitespace
        3. Apply Hinglish translation
        4. Remove punctuation (keeping some for context)
        """
        # Lowercase
        text = text.lower()
        
        # Hinglish translation
        for hinglish, english in self.hinglish_map.items():
            text = re.sub(r'\b' + hinglish + r'\b', english, text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove punctuation except spaces
        text = re.sub(r'[!?@#$%^&*()[\]{}+=<>|\\:;"\'`~.,]', ' ', text)
        
        # Clean up again
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_words(self, text: str) -> List[str]:
        """Extract individual words from normalized text"""
        normalized = self.normalize(text)
        return normalized.split()
    
    def detect_languages(self, text: str) -> Dict[str, bool]:
        """Detect if text contains English, Hindi, Hinglish"""
        has_english = bool(re.search(r'[a-z]', text))
        has_hindi = bool(re.search(r'[\u0900-\u097F]', text))  # Devanagari script
        has_hinglish = bool(re.search(r'[a-z].*[\u0900-\u097F]|[\u0900-\u097F].*[a-z]', text))
        
        return {
            'english': has_english,
            'hindi': has_hindi,
            'hinglish': has_hinglish
        }

# Test
if __name__ == "__main__":
    n = Normalizer()
    test_inputs = [
        "police ne roka aur parents ko call karne ko bola",
        "They stopped me without reason!!!",
        "मुझे गाली दी पुलिस ने"
    ]
    
    for text in test_inputs:
        print(f"Original: {text}")
        print(f"Normalized: {n.normalize(text)}")
        print(f"Languages: {n.detect_languages(text)}")
        print()
