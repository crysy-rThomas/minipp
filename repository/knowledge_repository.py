from infrastructure.database import get_kg


class KnowledgeRepository:
    
    def do(self, query):
        with get_kg() as session:
            return session.run(query)