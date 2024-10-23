import json

'''
服务端发送给客户端的消息类型以及内容需要按下面的格式打包
1."id"              content为int        客户端的id(int)
2."rename"          content无意义       用-1代替
3."wait"            content无意义       用-1代替
4."new_player"      content为lst        [id(int)以及名字(str)]
5."start"           content无意义       用-1代替
6."play"

客户端发送给服务端的消息需要按下面的格式打包



'''

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

    

