"""
resolver.py - Confidence scoring and situation ranking
Calculates how well user input matches each situation
"""

from typing import Dict, List, Tuple

class Resolver:
    """
    Calculates confidence score for each situation based on:
    - How many required signals are present (mandatory)
    - How many optional signals are present (bonus)
    - Weight of each signal
    """
    
    def __init__(self, situations: Dict, laws: Dict):
        self.situations = situations
        self.laws = laws
    
    def calculate_confidence(self, detected_signals: List[str], 
                            situation: Dict) -> float:
        """
        Calculate match confidence (0-100):
        - All required signals present = base score
        - Each optional signal adds points
        - Signal weights affect the score
        """
        
        required_signals = situation.get('required_signals', [])
        optional_signals = situation.get('optional_signals', [])
        
        # Check required signals
        required_met = all(sig in detected_signals for sig in required_signals)
        
        if not required_met:
            return 0.0  # If required signals missing, confidence is 0
        
        # Base score: all required met = 70%
        score = 70.0
        
        # Add points for optional signals
        optional_present = sum(1 for sig in optional_signals 
                              if sig in detected_signals)
        optional_bonus = (optional_present / len(optional_signals)) * 30 if optional_signals else 0
        
        score += optional_bonus
        
        return min(score, 100.0)  # Cap at 100
    
    def rank_situations(self, detected_signals: List[str],
                       situations: Dict) -> List[Tuple[str, Dict, float]]:
        """
        Rank all situations by confidence score
        Returns: [(situation_id, situation_data, confidence_score), ...]
        """
        
        results = []
        
        for sit_id, sit_data in situations.items():
            confidence = self.calculate_confidence(detected_signals, sit_data)
            if confidence > 0:  # Only include matches
                results.append((sit_id, sit_data, confidence))
        
        # Sort by confidence descending
        results.sort(key=lambda x: x[2], reverse=True)
        
        return results
    
    def get_top_matches(self, detected_signals: List[str],
                       situations: Dict,
                       threshold: float = 80.0,
                       top_n: int = 3) -> List[Tuple[str, Dict, float]]:
        """
        Get top N matches above threshold
        If confidence >= 80%, return only high confidence matches
        Otherwise return top 3 ranked matches (even if <80%)
        """
        
        ranked = self.rank_situations(detected_signals, situations)
        high_confidence = [r for r in ranked if r[2] >= threshold]
        
        if high_confidence:
            return high_confidence
        else:
            # Return top 3 even if below threshold
            return ranked[:top_n]
