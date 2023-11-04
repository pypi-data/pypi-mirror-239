import os.path
import time

from fundrive import GithubDrive
from funtask import Task


class UpdateRssTask(Task):
    def __init__(self):
        self.drive = GithubDrive()
        self.drive.login("farfarfun/funread-cache")
        super(UpdateRssTask, self).__init__()

    def book(self, dir_path="funread/legado/snapshot/lasted/book"):
        files = self.drive.get_file_list(dir_path)
        files = sorted(files, key=lambda x: x["name"])
        return {
            "title": os.path.basename(dir_path),
            #"time": files[0]["time"],
            "pic": "https://gitee.com/alanskycn/yuedu/raw/master/JS/icon.jpg",
            "url": f"https://farfarfun.github.io/funread-cache/{dir_path}/index.html",
            "content": "this is content",
        }

    def run(self, dir_path="funread/legado/snapshot/lasted"):
        data1 = {
            "name": "test",
            "next": "https://json.extendsclass.com/bin/b62da68f7d4d",
            "list": [],
        }
        data1["list"].append(self.book(f"{dir_path}/book"))
        self.drive.upload_file(git_path=f"{dir_path}/source.json", content=data1)

    def update_main(self):
        data2 = [{
            "lastUpdateTime": round(time.time()),
            "sourceName": "funread",
            "sourceIcon": "https://gitee.com/alanskycn/yuedu/raw/master/JS/icon.jpg",
            "sourceUrl": "https://json.extendsclass.com/bin/b62da68f7d4d",
            "loadWithBaseUrl": False,
            "singleUrl": False,
            "sortUrl": "test1::https://json.extendsclass.com/bin/b62da68f7d4d\ntest2::https://json.extendsclass.com/bin/b62da68f7d4d",
            "ruleArticles": "$.list[*]",
            "ruleNextArticles": "$.next",
            "ruleTitle": "$.title",
            "rulePubDate": "$.time",
            "ruleImage": "$.pic",
            "ruleLink": "$.url",

            "ruleDescription": "$.description",
            "sourceGroup": "VIP",
            "customOrder": -9999999,
            "enabled": True,
        }]
        self.drive.upload_file(git_path="funread/legado/rss/rss-main.json", content=data2)
