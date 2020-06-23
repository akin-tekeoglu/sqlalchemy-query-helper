from sqlalchemy import inspect

"""
{
    "name": {"op": "eq", "value": "joe"},
    "birthdate": {"op": "gte", "value": datetime.datetime.utcnow()},
}
"""

op_mapping = {
    "eq": lambda attr, value: attr == value,
    "neq": lambda attr, value: attr != value,
    "gt": lambda attr, value: attr > value,
    "gte": lambda attr, value: attr >= value,
    "lt": lambda attr, value: attr < value,
    "lte": lambda attr, value: attr <= value,
}


class QueryGenerator:
    def generate(self, session, model, raw_query):
        inst = inspect(model)
        query = session.query(model)
        for c_attr in inst.mapper.column_attrs:
            prop = c_attr.key
            if prop in raw_query:
                simple_query = raw_query[prop]
                operation = op_mapping[simple_query["op"]]
                query = query.filter(operation(getattr(c_attr), simple_query["value"]))
        return query
