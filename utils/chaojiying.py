#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5


class VerifyHandler(object):

    def __init__(self):
        self.username = '账号'
        password = '密码'.encode('utf-8')
        self.password = md5(password).hexdigest()
        self.soft_id = ''
        self.vid = 1902  # 4-6位字母数字验证id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def verify_pic(self, im, code_type):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': code_type,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()

    def report_error(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

    def main(self, img_path, code_type):
        with open(img_path, 'rb') as f:
            img = f.read()
            return self.verify_pic(img, code_type)


if __name__ == '__main__':
    img_path = '../pic/17tarck_1626244539.jpg'
    code_type = 1902
    v_result = VerifyHandler().main(img_path=img_path, code_type=code_type)
    print(v_result, type(v_result))
