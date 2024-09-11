from repository.knowledge_repository import KnowledgeRepository
from services.fireworks_service import FireworksService


class KnowledgeService:
    def __init__(self):
        self.knwoledge_repository = KnowledgeRepository()
        self.fireworks_service = FireworksService()
    
    def request(self, data):
        query = self.fireworks_service.generate_query(data)
        return self.knwoledge_repository.do(query)
        
    
    