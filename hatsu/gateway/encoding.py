import json
import earl

def compress_json(data):
    return json.dumps(data, separators=(',', ':'))

def decompress_json(data):
    return json.loads(data)

def compress_earl(data):
    sanitized_ = compress_json(data)
    sanitized = decompress_json(sanitized_)
    return earl.pack(sanitized)

def _earl_dict_decompress(data):
    if not isinstance(data, dict):
        return data

    copy = dict(data)

    r = {}

    for key in copy.keys():
        new_key = key.decode()

        r[new_key] = _earl_dict_decompress(data[key])
    
    return r


def decompress_earl(data):
    d = earl.unpack(data)

    if isinstance(d, bytes):
        return d.decode()
    
    if isinstance(d, dict):
        return _earl_dict_decompress(d)
    
    return d
