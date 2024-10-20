import json

class Message:
    def __init__(self, type, content):
        self.type = type
        self.content = content

    # 序列化
    def serialize(self):
        # 利用jasn以及__dict__将对象序列化为json字符串
        # __dict__是一个包含对象属性的字典
        return json.dumps(self.__dict__)
    
    
    # 反序列化
    @classmethod
    def deserialize(cls, byte_stream):
        try:
            json_data = byte_stream.decode('utf-8')
            data = json.loads(json_data)
            return cls(data['type'], data['content'])
        except (ValueError, KeyError, TypeError) as e:
            # 捕获 JSON 解析错误或数据不全的情况
            print(f"Failed to deserialize message: {e}")
            return None

    

