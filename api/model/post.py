class Post():
    def __init__(self, id = "0", process_id = "", status = "", file = "", tag = ""):
        self.result = {}
        self.result["id"] = id
        self.result["process_id"] = id
        self.result["status"] = status
        self.result["file"] = file
        self.result["tag"] = tag

    def set_id(self, value: str):
        self.result["id"] = value

    def set_status(self, value: str):
        self.result["status"] = value

    def set_file(self, value: str):
        self.result["file"] = value

    def set_tag(self, value: str):
        self.result["tag"] = value

    def set_process_id(self, value: str):
        self.result["process_id"] = value

    def get_id(self):
        return self.result["id"]

    def get_status(self):
        return self.result["status"]

    def get_file(self):
        return self.result["file"]

    def get_data(self):
        return self.result

    def get_tag(self):
        return self.result["tag"]

    def get_process_id(self):
        return self.result["process_id"]
