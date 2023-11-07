
"""
Mapping engine
Given a record and a json map (dict), evaluates each elements and transform record to map

See template for json map in template_mapping.json

Accepts dot notation. 
To refer to record variable, use dot notation with r as being the record : r.name, r.address

"""



from types import SimpleNamespace

def mapping_engine(record, map):
    """Given a record and a mapping, evaluates the mapping to build output record
    """

    #Initialize r to be accessed with dot notation
    r = _to_dot_notation(record)

    if isinstance(map, dict):
        new_record = {}
        for k, v in map.items():
            new_record[k] = mapping_engine(record, v)
        return new_record

    elif isinstance(map, list):
        new_record = []
        for i in map:
            new_record.append(mapping_engine(record, i))
        return new_record
    else:
        try:
            return eval(map)
        except Exception as e:
            print(e)
            return None



def _to_dot_notation(data):
    """Transform record into dot notation capable
        r = _to_dot_notation(record)
        value = r.a.b[2].c
    """

    if type(data) is list:
        return list(map(_to_dot_notation, data))
    elif type(data) is dict:
        sns = SimpleNamespace()
        for key, value in data.items():
            setattr(sns, key, _to_dot_notation(value))
        return sns
    else:
        return data