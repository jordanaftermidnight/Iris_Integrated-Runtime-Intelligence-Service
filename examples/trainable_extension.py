#!/usr/bin/env python3
"""
Trainable Extension Example for Multi-AI MCP Integration
Shows how to add learning capabilities to the system
"""

import json
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import pickle

@dataclass
class QueryFeedback:
    query: str
    provider_used: str
    response: str
    user_rating: float  # 1-5 scale
    response_time: float
    timestamp: datetime

class ResponseQualityPredictor:
    """ML model to predict response quality and optimize provider selection"""
    
    def __init__(self):
        self.training_data: List[QueryFeedback] = []
        self.model = None  # Would use scikit-learn, tensorflow, etc.
        
    def add_feedback(self, feedback: QueryFeedback):
        """Add user feedback for learning"""
        self.training_data.append(feedback)
        
        # Auto-retrain after collecting enough data
        if len(self.training_data) % 100 == 0:
            self.retrain_model()
    
    def extract_features(self, query: str, provider: str) -> List[float]:
        """Extract features from query for ML model"""
        features = []
        
        # Query length
        features.append(len(query))
        
        # Query complexity (number of technical terms)
        technical_terms = ['api', 'database', 'algorithm', 'security', 'performance']
        complexity = sum(1 for term in technical_terms if term.lower() in query.lower())
        features.append(complexity)
        
        # Provider encoding
        features.append(1.0 if provider == 'gemini' else 0.0)
        features.append(1.0 if provider == 'llama2' else 0.0)
        
        # Query type indicators
        features.append(1.0 if any(word in query.lower() for word in ['how', 'what', 'why']) else 0.0)
        features.append(1.0 if any(word in query.lower() for word in ['compare', 'vs', 'versus']) else 0.0)
        
        return features
    
    def predict_quality(self, query: str, provider: str) -> float:
        """Predict response quality for query-provider combination"""
        if not self.model or len(self.training_data) < 10:
            return 3.0  # Default neutral rating
        
        features = self.extract_features(query, provider)
        # In real implementation, use trained ML model
        # return self.model.predict([features])[0]
        
        # Simplified heuristic for demo
        if 'gemini' in provider and any(word in query.lower() for word in ['complex', 'detailed']):
            return 4.2
        elif 'llama2' in provider and any(word in query.lower() for word in ['quick', 'simple']):
            return 4.0
        return 3.5
    
    def retrain_model(self):
        """Retrain the quality prediction model"""
        if len(self.training_data) < 10:
            return
            
        # Prepare training data
        X = []
        y = []
        
        for feedback in self.training_data:
            features = self.extract_features(feedback.query, feedback.provider_used)
            X.append(features)
            y.append(feedback.user_rating)
        
        # In real implementation, train ML model here
        # from sklearn.ensemble import RandomForestRegressor
        # self.model = RandomForestRegressor()
        # self.model.fit(X, y)
        
        print(f"Model retrained with {len(self.training_data)} samples")

class QueryTypeClassifier:
    """Classify queries to route to best provider"""
    
    def __init__(self):
        self.query_patterns = {
            'technical': ['api', 'code', 'programming', 'debug', 'error'],
            'creative': ['design', 'idea', 'brainstorm', 'creative', 'innovative'],
            'analytical': ['analyze', 'compare', 'evaluate', 'pros', 'cons'],
            'factual': ['what is', 'define', 'explain', 'how does'],
            'privacy': ['private', 'confidential', 'secure', 'gdpr', 'sensitive']
        }
        
        self.provider_preferences = {
            'technical': {'gemini': 0.7, 'llama2': 0.3},
            'creative': {'gemini': 0.8, 'llama2': 0.2}, 
            'analytical': {'gemini': 0.6, 'llama2': 0.4},
            'factual': {'gemini': 0.5, 'llama2': 0.5},
            'privacy': {'gemini': 0.1, 'llama2': 0.9}  # Privacy-focused queries go to local
        }
    
    def classify_query(self, query: str) -> Dict[str, float]:
        """Classify query and return type probabilities"""
        query_lower = query.lower()
        scores = {}
        
        for query_type, patterns in self.query_patterns.items():
            score = sum(1 for pattern in patterns if pattern in query_lower)
            scores[query_type] = score / len(patterns)
        
        # Normalize scores
        total_score = sum(scores.values()) or 1.0
        return {k: v / total_score for k, v in scores.items()}
    
    def recommend_provider(self, query: str) -> Dict[str, float]:
        """Recommend provider based on query classification"""
        query_types = self.classify_query(query)
        
        provider_scores = {'gemini': 0.0, 'llama2': 0.0}
        
        for query_type, type_score in query_types.items():
            if query_type in self.provider_preferences:
                for provider, pref_score in self.provider_preferences[query_type].items():
                    provider_scores[provider] += type_score * pref_score
        
        return provider_scores

class TrainableMultiAI:
    """Extended Multi-AI system with learning capabilities"""
    
    def __init__(self):
        self.quality_predictor = ResponseQualityPredictor()
        self.query_classifier = QueryTypeClassifier()
        self.adaptation_history = []
    
    async def smart_provider_selection(self, query: str, available_providers: List[str]) -> str:
        """Select provider using learned preferences"""
        
        # Get ML-based recommendations
        provider_scores = self.query_classifier.recommend_provider(query)
        
        # Add quality predictions
        quality_scores = {}
        for provider in available_providers:
            quality_scores[provider] = self.quality_predictor.predict_quality(query, provider)
        
        # Combine scores (70% type-based, 30% quality-based)
        final_scores = {}
        for provider in available_providers:
            type_score = provider_scores.get(provider, 0.5)
            quality_score = quality_scores.get(provider, 3.0) / 5.0  # Normalize to 0-1
            final_scores[provider] = 0.7 * type_score + 0.3 * quality_score
        
        # Select best provider
        best_provider = max(final_scores.keys(), key=lambda p: final_scores[p])
        
        # Log adaptation decision
        self.adaptation_history.append({
            'query': query,
            'selected_provider': best_provider,
            'scores': final_scores,
            'timestamp': datetime.now()
        })
        
        return best_provider
    
    def learn_from_feedback(self, query: str, provider: str, response: str, 
                          user_rating: float, response_time: float):
        """Learn from user feedback"""
        feedback = QueryFeedback(
            query=query,
            provider_used=provider,
            response=response,
            user_rating=user_rating,
            response_time=response_time,
            timestamp=datetime.now()
        )
        
        self.quality_predictor.add_feedback(feedback)
        print(f"Learning from feedback: {user_rating}/5 for {provider}")
    
    def export_learning_data(self, filename: str):
        """Export learned patterns for analysis"""
        data = {
            'training_data': [
                {
                    'query': f.query,
                    'provider': f.provider_used,
                    'rating': f.user_rating,
                    'response_time': f.response_time,
                    'timestamp': f.timestamp.isoformat()
                }
                for f in self.quality_predictor.training_data
            ],
            'adaptation_history': self.adaptation_history
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"Learning data exported to {filename}")

# Example usage
async def demo_trainable_system():
    """Demonstrate trainable multi-AI system"""
    print("🧠 Trainable Multi-AI System Demo")
    print("=" * 50)
    
    trainable_ai = TrainableMultiAI()
    
    # Simulate some queries and learning
    test_scenarios = [
        {
            'query': 'How do I implement secure API authentication?',
            'available_providers': ['gemini', 'llama2'],
            'simulated_rating': 4.5
        },
        {
            'query': 'What are my private data storage options?',
            'available_providers': ['gemini', 'llama2'], 
            'simulated_rating': 4.8
        },
        {
            'query': 'Quick help with Python syntax',
            'available_providers': ['gemini', 'llama2'],
            'simulated_rating': 4.2
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{i}. Processing: '{scenario['query'][:50]}...'")
        
        # Smart provider selection
        selected_provider = await trainable_ai.smart_provider_selection(
            scenario['query'], 
            scenario['available_providers']
        )
        
        print(f"   🎯 Selected provider: {selected_provider}")
        
        # Simulate response and feedback
        trainable_ai.learn_from_feedback(
            query=scenario['query'],
            provider=selected_provider,
            response=f"Simulated response from {selected_provider}",
            user_rating=scenario['simulated_rating'],
            response_time=2.1
        )
    
    # Export learning data
    trainable_ai.export_learning_data('learning_data.json')
    
    print(f"\n📊 System has learned from {len(trainable_ai.quality_predictor.training_data)} interactions")
    print("✅ Ready for continuous improvement!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(demo_trainable_system())