"""
LegalAssist - Core Logic Engine
Handles keyword detection, situation matching, and law retrieval
"""

import json
import os
import re

class LegalLogicEngine:
    """Rule-based legal matching engine"""
    
    def __init__(self):
        self.keywords = self.load_json('data/keywords.json')
        self.situations = self.load_json('data/situations.json')
        self.laws = self.load_json('data/laws.json')
        self.law_map = {law['id']: law for law in self.laws}

    def load_json(self, filepath):
        """Load JSON data from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {filepath} not found. Using empty data.")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error parsing {filepath}: {e}")
            return {}

    def normalize_text(self, text):
        """Normalize user input for matching"""
        # Convert to lowercase
        text = text.lower()
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def detect_signals(self, text):
        """Detect semantic signals from user input"""
        signals = set()
        normalized = self.normalize_text(text)
        words = normalized.split()
        
        for category, keyword_list in self.keywords.items():
            for keyword in keyword_list:
                if keyword in words:
                    signals.add(category)
                    break
        
        return list(signals)

    def match_situation(self, signals):
        """Match signals to legal situations"""
        matches = []
        signals_set = set(signals)
        
        for situation in self.situations:
            required = set(situation['required_signals'])
            optional = set(situation['optional_signals'])
            
            # Check if all required signals are present
            if required.issubset(signals_set):
                confidence = len(required)
                # Add bonus for optional signals
                if optional:
                    confidence += len(signals_set.intersection(optional))
                
                matches.append({
                    "situation": situation,
                    "confidence": confidence
                })
        
        # Sort by confidence (highest first)
        matches.sort(key=lambda x: x['confidence'], reverse=True)
        return matches

    def get_laws(self, situation_id):
        """Retrieve laws for a matched situation"""
        return [self.law_map[lid] for lid in situation_id if lid in self.law_map]

    def generate_response(self, user_input, matched_situations):
        """Generate structured legal awareness response"""
        if not matched_situations:
            return {
                "status": "no_match",
                "message": "No specific legal situation detected. Please try describing the situation more clearly with keywords like: police, stop, harassment, parents, etc."
            }
        
        top_match = matched_situations[0]
        situation = top_match['situation']
        laws = self.get_laws(situation['law_ids'])
        
        # Determine confidence level
        confidence = "High" if top_match['confidence'] >= 3 else "Medium"
        
        response = {
            "status": "success",
            "situation": situation['name'],
            "confidence": confidence,
            "laws": laws,
            "guidance": f"Based on the situation '{situation['name']}', here is general legal awareness information.",
            "disclaimer": "⚠️ DISCLAIMER: This is a legal awareness tool, not legal advice. Consult a qualified lawyer for specific cases."
        }
        return response