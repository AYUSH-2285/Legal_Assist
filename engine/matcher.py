"""
matcher.py - Core matching engine
Maps keywords -> signals -> situations -> laws
"""

import json
from typing import Dict, List, Tuple, Set
from pathlib import Path

class LegalAssistMatcher:
    """
    Main matching engine that:
    1. Normalizes user input
    2. Detects keywords -> semantic signals
    3. Matches signals -> legal situations
    4. Retrieves applicable laws
    5. Ranks by confidence
    """
    
    def __init__(self, keywords: Dict, situations: Dict, laws: Dict):
        self.keywords = keywords
        self.situations = situations
        self.laws = laws
    
    def extract_signals(self, text: str) -> List[str]:
        """
        Extract semantic signals from user text:
        1. Normalize text
        2. Extract words
        3. Match against keyword categories
        4. Return detected signals
        """
        normalized = text.lower()
        words = set(normalized.split())
        
        detected_signals = set()
        
        # Check each keyword category
        for category, keyword_data in self.keywords.items():
            all_keywords = (
                keyword_data.get('keywords', []) +
                keyword_data.get('hinglish', []) +
                keyword_data.get('hindi', [])
            )
            
            # If any keyword from this category is found, add signal
            if any(kw in normalized for kw in all_keywords):
                detected_signals.add(category)
        
        return list(detected_signals)
    
    def match_situations(self, detected_signals: List[str]) -> List[Tuple[str, Dict, float]]:
        """
        Match detected signals to situations and rank by confidence
        Returns: [(situation_id, situation_data, confidence_score), ...]
        """
        results = []
        
        for sit_id, sit_data in self.situations.items():
            required_signals = sit_data.get('required_signals', [])
            optional_signals = sit_data.get('optional_signals', [])
            
            # Check required signals
            required_met = all(sig in detected_signals for sig in required_signals)
            
            if not required_met:
                continue  # Skip if required signals missing
            
            # Base score: all required met = 70%
            score = 70.0
            
            # Add points for optional signals
            optional_present = sum(1 for sig in optional_signals 
                                  if sig in detected_signals)
            optional_bonus = (optional_present / len(optional_signals)) * 30 if optional_signals else 0
            
            score += optional_bonus
            score = min(score, 100.0)  # Cap at 100
            
            results.append((sit_id, sit_data, score))
        
        # Sort by confidence descending
        results.sort(key=lambda x: x[2], reverse=True)
        
        return results
    
    def get_top_matches(self, detected_signals: List[str],
                       threshold: float = 80.0,
                       top_n: int = 3) -> List[Tuple[str, Dict, float]]:
        """
        Get top N matches above threshold
        If confidence >= 80%, return only high confidence matches
        Otherwise return top 3 ranked matches (even if <80%)
        """
        ranked = self.match_situations(detected_signals)
        high_confidence = [r for r in ranked if r[2] >= threshold]
        
        if high_confidence:
            return high_confidence
        else:
            # Return top 3 even if below threshold
            return ranked[:top_n]
    
    def get_laws(self, situation: Dict) -> List[Dict]:
        """Retrieve laws referenced by a situation"""
        law_ids = situation.get('law_ids', [])
        return [self.laws[law_id] for law_id in law_ids if law_id in self.laws]
    
    def process_query(self, user_input: str) -> Dict:
        """
        Complete processing pipeline:
        Input -> Normalized Text
              -> Detected Signals
              -> Matched Situations (ranked)
              -> Associated Laws
              -> Structured Output
        """
        
        normalized_text = user_input.lower()
        signals = self.extract_signals(user_input)
        matches = self.get_top_matches(signals)
        
        results = []
        
        for sit_id, situation, confidence in matches:
            laws = self.get_laws(situation)
            results.append({
                'situation_id': sit_id,
                'situation_name': situation.get('name'),
                'situation_description': situation.get('description'),
                'confidence_score': round(confidence, 1),
                'severity': situation.get('severity'),
                'laws': laws,
                'what_you_can_ask': situation.get('what_you_can_ask', [])
            })
        
        return {
            'user_input': user_input,
            'normalized_text': normalized_text,
            'detected_signals': signals,
            'matches': results
        }
