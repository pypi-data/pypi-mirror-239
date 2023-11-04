import dolphindb as ddb


class ddb_process:

    def __init__(self, url, port):
        self.url = url
        self.port = port

    def connect(self):
        s = ddb.session()
        s.connect(self.url, self.port, userid="admin", password="123456")
        return s

    def close_ddb(self, s):
        s.close()

    def execute(self, package, process, param):
        # 根据param是一个list 的个数 写出一个 %s的字符串
        x = ['%s'] * len(param)
        s = self.connect()
        s.run(f"{package}::{process}")
        result = s.run(((f"{process}::exec({','.join(x)})") % (",".join(param))))
        self.close_ddb(s)
        return result
