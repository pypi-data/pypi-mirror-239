from engine import engine

def transform(records, map):

    if not records:
        return []
        
    results = engine.mapping_engine(records, map)
    return results