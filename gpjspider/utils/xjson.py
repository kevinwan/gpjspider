import json
from datetime import datetime
from time import mktime
from decimal import Decimal

class MyEncoder(json.JSONEncoder):   
    def default(self, obj):
        if isinstance(obj, datetime):
            return {
                '__type__': '__datetime__', 
                'epoch': int(mktime(obj.timetuple()))
            }
        if isinstance(obj, Decimal):
            return {
                '__type__': '__decimal__',
                'repr': obj.to_eng_string()
            }
        else:
            return json.JSONEncoder.default(self, obj)

def my_decoder(obj):
    if '__type__' in obj:
        if obj['__type__'] == '__datetime__':
            return datetime.fromtimestamp(obj['epoch'])
        elif obj['__type__'] == '__decimal__':
            return Decimal(obj['repr'])
    return obj

# Encoder function      
def my_dumps(obj):
    return json.dumps(obj, cls=MyEncoder)

# Decoder function
def my_loads(obj):
    return json.loads(obj, object_hook=my_decoder)

def init(name='xjson'):
    from kombu.serialization import register
    register(name, my_dumps, my_loads, content_type='application/x-%s' % name.lower(),content_encoding='utf-8')