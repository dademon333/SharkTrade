from datetime import date, datetime


def json_serializer(obj):
    """Hook for json.dumps to serialize datetime in iso format.

    Usage example:
    data = json.dumps(data, default=json_serializer)

    """
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()


def json_deserializer(pairs):
    """Hook for json.loads to deserialize iso format values in datetime.

    Usage example:
    data = json.loads(data, object_pairs_hook=json_deserializer)

    """
    result = {}
    for key, value in pairs:
        if isinstance(value, str):
            try:
                result[key] = datetime.fromisoformat(value)
            except ValueError:
                result[key] = value
        else:
            result[key] = value
    return result
