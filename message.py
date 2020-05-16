import json


class Message:
    
    def __init__(self, type_=None, content=None):
        self.type = type_
        self.content = content

    def __str__(self):
        return f"{self.content} ({self.type})"

    def to_json(self):
        return json.dumps({
            "type": self.type,
            "content": self.content
        }).encode("utf-8")

    def from_json(self, message):
        data = json.loads(message.decode("utf-8"))
        self.type = data["type"]
        self.content = data["content"]

        return self

    def send(self, s, dest):
        s.sendto(self.to_json(), dest)

        return self
