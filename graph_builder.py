from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://neo4j:7687', auth=('neo4j','test'))

def build_knowledge_graph(entities, relations):
    """
    Create Entity nodes and REL relationships in Neo4j.
    """
    with driver.session() as session:
        for name, label in entities:
            session.run(
                "MERGE (e:Entity {name: $name, label: $label})",
                {'name': name, 'label': label}
            )
        for subj, pred, obj in relations:
            session.run(
                "MATCH (s:Entity {name: $s}), (o:Entity {name: $o}) "
                "MERGE (s)-[r:REL {type: $pred}]->(o)",
                {'s': subj, 'pred': pred, 'o': obj}
            )