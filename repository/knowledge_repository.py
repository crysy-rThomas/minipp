from infrastructure.kg_database import kg


class KnowledgeRepository:
    def do(self, cypher):
        return kg.query(cypher)
