# -*- coding: utf-8 -*-
import yaml
import os

DOC_DIR = "docs"
KEY = "key"
KeywordsToDocMapping = {}


class Doc:
    def __init__(self, file, desc, key):
        self.file = file
        self.desc = desc
        self.key = key

    def __str__(self):
        return self.file + ":" + self.desc + ":" + self.key


# 扫描docs文件夹下的所有文件，返回关键字和文件的映射
# YAML front matter 是 Markdown 文件的一种特殊格式，
# 它可以在 Markdown 文件的开头添加一些额外的元数据，例如文章的标题、作者、日期等。
def index_keywords():
    global KeywordsToDocMapping
    files = os.listdir(DOC_DIR)
    for f in files:
        if f.endswith(".md"):
            with open(os.path.join(DOC_DIR, f), "r") as file:
                try:
                    data = yaml.load_all(file, Loader=yaml.Loader)
                    # get the first section in the stream
                    d = next(data)
                    for k, v in d.items():
                        # print(k, "->", v)
                        if k == KEY:
                            f = os.path.join(DOC_DIR, f)
                            KeywordsToDocMapping[v] = Doc(f, d["desc"], v)
                except:
                    # get filename without ext
                    f = os.path.join(DOC_DIR, f)
                    filename = os.path.splitext(f)[0]
                    KeywordsToDocMapping[filename] = Doc(f, "", filename)
                    pass
