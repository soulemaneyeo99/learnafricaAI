from typing import List, Dict

class RecommendationEngine:
    def __init__(self):
        # Initialisation (chargement de modèles, connexion DB, etc.)
        pass

    async def get_recommendations_for_user(self, user_id: int, limit: int = 5) -> List[Dict]:
        """
        Génère des recommandations de cours pour un utilisateur spécifique.
        """
        # TODO: Implémenter la logique (Collaborative Filtering / Content-Based)
        # Pour l'instant, retourne des données mockées.
        return [
            {"course_id": 101, "title": "Introduction à l'IA avec Python", "score": 0.98},
            {"course_id": 202, "title": "Développement Mobile avec Flutter", "score": 0.95},
            {"course_id": 303, "title": "Data Science Fundamentals", "score": 0.90},
        ]

recommendation_engine = RecommendationEngine()
