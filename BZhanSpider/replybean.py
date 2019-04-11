import collections

from hamcrest.library import collection


class replybean(object):
    # 视频id
    oid = ''
    # reply id
    rpid_str = ''
    # reply 时间
    date = ''
    # reply 楼层，第几楼
    floor = ''
    # reply 用户id，mid
    mid = ''
    # reply 用户的用户名
    uname = ''
    # 用户评论内容
    content = ''
    # 根评论的reply id，对应rpid_str
    root_str = ''
    # 上一级评论(可能是回复的回复多层嵌套)
    parent_str = ''

    def __init__(self, oid, rpid_str, date, floor, mid, uname, content, root_str, parent_str):
        self.oid = oid
        self.rpid_str = rpid_str
        self.date = date
        self.floor = floor
        self.mid = mid
        self.uname = uname
        self.content = content
        self.root_str = root_str
        self.parent_str = parent_str

    def get_oid(self):
        return self.oid

    def get_rpid_str(self):
        return self.rpid_str

    def get_date(self):
        return self.date

    def get_floor(self):
        return self.floor

    def get_mid(self):
        return self.mid

    def get_uname(self):
        return self.uname

    def get_content(self):
        return self.content

    def get_root_str(self):
        return self.root_str

    def get_parent_str(self):
        return self.parent_str

    def to_string(self):
        print('oid: ' + self.oid
              + ', rpid_str: ' + self.rpid_str
              + ', date: ' + self.date
              + ', floor: ' + self.floor
              + ', mid: ' + self.mid
              + ', uname: ' + self.uname
              + ', content: ' + self.content
              + ', root_str: ' + self.root_str
              + ', parent_str: ' + self.parent_str)
