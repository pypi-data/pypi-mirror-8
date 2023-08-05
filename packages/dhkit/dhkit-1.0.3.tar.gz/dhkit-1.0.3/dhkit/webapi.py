# coding:utf8

"""
Created on 2014-09-10

@author: tufei
@description:
         
Copyright (c) 2014 infohold inc. All rights reserved.
"""
import json
import mimetypes
import itertools
from dhkit import log
from tornado.httpclient import HTTPClient, HTTPError, HTTPRequest
from dhkit.error import Error
from mimetools import choose_boundary
from dhkit.util import gzip_compress, urlconcat, urlencode


class ApiError(Error):
    """
    """

    cls_code = -9000

    def __init__(self, msg=None, code=-1000, httpcode=None, httpmsg=None):
        super(ApiError, self).__init__(msg, code)
        self.httpcode = httpcode
        self.httpmsg = httpmsg


class ShouYiApiError(ApiError):
    """爱手艺API接口错误
    """

    cls_code = -9000


class SendCloudApiError(ApiError):
    """SendCloud邮件WEB API接口错误
    """
    cls_code = -9100


class Api(object):

    def fetch(self, request):
        try:
            http_client = HTTPClient()
            log.debug("[REQ] url:[%s] body:[%s]" % (request.url, request.body))
            print "[REQ] url:[%s] body:[%s]" % (request.url, request.body)
            response = http_client.fetch(request)
            log.debug("[RES] body:[%s]" % response.body)
            return response.body
        except HTTPError, e:
            log.exception("[ERR] fetch from server error: %s" % e.message)
            raise e


class ShouYiApi(Api):

    API_URL = "http://api.ishouyi.com"

    def __init__(self, api_url=None, timeout=30, use_gzip=True):
        self.api_url = api_url or self.API_URL
        self.timeout = timeout
        self.use_gzip = use_gzip

    def get(self, api_path, **kwargs):
        headers = {
            'Accept': "application/json",
            'Connection': 'Keep-Alive',
        }

        if kwargs:
            url = urlconcat(self.part_url(api_path), kwargs)
        else:
            url = self.part_url(api_path)
        request = HTTPRequest(url, method="GET", headers=headers, connect_timeout=self.timeout,
                              request_timeout=self.timeout, use_gzip=self.use_gzip, validate_cert=False)
        return self.fetch(request)

    def post(self, api_path, **kwargs):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': "application/json",
            'Connection': 'Keep-Alive',
        }
        url = self.part_url(api_path)
        body = kwargs and urlencode(kwargs) or None
        request = HTTPRequest(url, method="POST", headers=headers, body=body, connect_timeout=self.timeout,
                              request_timeout=self.timeout, use_gzip=self.use_gzip, validate_cert=False)
        return self.fetch(request)

    def fetch(self, request):
        try:
            resp_body = super(ShouYiApi, self).fetch(request)
            json_body = json.loads(resp_body)
            return json_body
        except HTTPError, e:
            if e.code == 599:
                raise ShouYiApiError(msg=e.message)

            try:
                log.debug("http code: [%s] response body: [%s]" % (e.code, e.response.body))
                json_body = json.loads(e.response.body)
                if not isinstance(json_body, dict):
                    json_body = dict()
            except Exception:
                json_body = dict()
            if json_body.has_key('return_message') and json_body.has_key('return_code'):
                raise ShouYiApiError(msg=json_body.get('return_message'), code=json_body.get('return_code'),
                                     httpcode=e.code, httpmsg=e.response.body)
            else:
                raise ShouYiApiError(msg="Unkown message description", httpcode=e.code, httpmsg=e.response.body)
        except Exception, e:
            raise ShouYiApiError(msg=e.message)

    def part_url(self, api_path):
        api_url = self.api_url[:-1] if self.api_url.endswith("/") else self.api_url
        return "%s%s" % (api_url, api_path)


class MultiPartForm(object):

    CONTENT_TYPE = ""

    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = choose_boundary()
        self.content_type = 'multipart/form-data; boundary=%s' % self.boundary

    def add_filed(self, name, value):
        self.form_fields.append((str(name), str(value)))

    def add_file(self, field_name, file_name, fp, mime_type=None):
        body = fp.read()
        if mime_type is None:
            mime_type = mimetypes.guess_type(file_name)[0] or 'applicatioin/octet-stream'
        self.files.append((field_name, file_name, mime_type, body))

    def __str__(self):
        parts = []
        part_boundary = '--' + self.boundary

        for name, value in self.form_fields:
            parts.append((part_boundary,
                          'Content-Disposition: form-data; name="%s"' % name,
                          '', value))

        for field_name, filename, content_type, body in self.files:
            parts.append((part_boundary,
                          'Content-Disposition: form-data; name="%s"; filename="%s"' % (field_name, filename),
                          "Content-Type: %s" % content_type,
                          '', body))

        flattened = list(itertools.chain(*parts))
        flattened.append('--' + self.boundary + '--')
        flattened.append('')
        return '\r\n'.join(flattened)


class SendCloudApi(Api):

    API_URL = "https://sendcloud.sohu.com"
    API_USER = "username"
    API_KEY = "password"

    def __init__(self, api_url=None, api_user=None, api_key=None):
        self.api_url = api_url or self.API_URL
        self.api_user = api_user or self.API_USER
        self.api_key = api_key or self.API_KEY

    def send_mail(self, to_users, subject, content, from_user, use_maillist=False, from_name=None,
                  cc_users=None,bcc_users=None, replyto=None, mail_headers=None, attachments=None,
                  x_smtpapi=None, resp_email_id=False, gzip_content=False):
        """
        利用SendCloud发送邮件

        :param to_users: list或者tuple类型 接收邮箱列表
        :param subject: str类型 邮件主题
        :param content: str类型 邮件正文内容，文本格式或者html格式
        :param use_maillist boolean类型 to_users中是否含有邮件列表地址
        :param from_user: str类型 发件人邮箱
        :param from_name: str类型 发件人名称
        :param cc_users: list或者tuple类型 抄送邮箱列表
        :param bcc_users: list或者tuple类型 密送邮箱列表
        :param replyto: str类型 回复邮箱，如果没有设置，默认为from_user
        :param mail_headers: dict类型 邮件头部信息
        :param attachments: list或者tuple类型 附件文件名列表，使用文件的绝对路径
        :param x_smtpapi: dict类型 扩展SMTP字段
        :param resp_email_id boolean类型 是否返回emailId
        :param gzip_content boolean类型 邮件正文是否启用gzip压缩
        :return: dict 接口响应包体
        """
        if not isinstance(to_users, (list, tuple)):
            raise TypeError("param: to_users expect type list or tuple")

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        params = {
            'api_user': self.api_user,
            'api_key': self.api_key,
            'to': ';'.join(to_users),
            'subject': subject,
            'html': content,
            'from': from_user
        }
        if use_maillist:
            params['use_maillist'] = 'true'
        if from_name is not None:
            params['fromname'] = from_name
        if cc_users is not None:
            if not isinstance(cc_users, (list, tuple)):
                raise TypeError("param: cc_users expect type list or tuple")
            params['cc'] = ';'.join(cc_users)
        if bcc_users is not None:
            if not isinstance(bcc_users, (list, tuple)):
                raise TypeError("param: bcc_users expect type list or tuple")
            params['bcc'] = ';'.join(bcc_users)
        if replyto is not None:
            params['replyto'] = replyto
        if mail_headers is not None:
            if not isinstance(mail_headers, dict):
                raise TypeError("param: mail_headers expect type dict")
            params['headers'] = json.dumps(mail_headers)
        if x_smtpapi is not None:
            if not isinstance(x_smtpapi, dict):
                raise TypeError("param: x_smtpapi expect type dict")
            params['x_smtpapi'] = json.dumps(x_smtpapi)
        params['resp_email_id'] = str(resp_email_id).lower()
        params['gzip_compress'] = str(gzip_content).lower()

        # 如果gzip压缩开启，启用对邮件正文压缩
        if gzip_content:
            params['html'] = gzip_compress(content)

        body = urlencode(params)
        # 处理附件
        if attachments is not None:
            if not isinstance(attachments, (list, tuple)):
                raise TypeError("param: attachments expect type list or tuple")
            if attachments:
                form = MultiPartForm()
                headers['Content-Type'] = form.content_type
                for attachment in attachments:
                    last_name = attachment.split("/")[-1]
                    form.add_file("files", last_name, open(attachment, "rb"))
                for name, value in params.iteritems():
                    form.add_filed(name, value)
                body = str(form)

        url = self.part_url("/webapi/mail.send.json")
        request = HTTPRequest(url, method="POST", headers=headers, body=body, validate_cert=False)
        return self.fetch(request)

    def create_maillist(self, address, name=None, description=None):
        """ 创建邮件列表
        :param address: 邮件列表地址
        :param name: 邮件列表名称
        :param description: 邮件列表描述
        :return: dict 接口响应包体
        """
        kwargs = dict(address=address, name=name, description=description)
        return self.post("/webapi/list.create.json", **kwargs)

    def query_mailiist(self, address=None, start=0, limit=100):
        """查询邮件列表
        :param address: 邮件列表地址，不填则查询所有的
        :param start: 查询起始位置，默认为0
        :param limit: 限制返回的邮件列表的个数。如果不设置，默认为100个
        :return: dict 接口响应包体
        """
        kwargs = dict(address=address, start=start, limit=limit)
        return self.get("/webapi/list.get.json", **kwargs)

    def delete_maillist(self, address):
        """删除邮件列表
        :param address: 邮件列表地址
        :return: dict 接口响应包体
        """
        return self.get("/webapi/list.delete.json", address=address)

    def update_maillist(self, address, to_address, name=None, description=None):
        """更新邮件列表
        :param address: 邮件列表地址
        :param to_address: 要更新的邮件列表地址
        :param name: 邮件列表名称
        :param description: 邮件列表描述
        :return: dict 接口响应包体
        """
        kwargs = dict(address=address, to_address=to_address, name=name, description=description)
        return self.post("/webapi/list.update.json", **kwargs)

    def add_maillist_member(self, mail_list_addr, member_addr, name=None,
                            vars_dct=None, subscribed=True, upsert=True):
        """添加邮件列表成员
        :param mail_list_addr: 邮件列表地址
        :param member_addr: str类型或者list(tuple)类型 邮件成员或者邮件成员列表
        :param name: 邮件成员列表名称
        :param vars_dct: dict类型，用于模板替换的变量
        :param subscribed: boolean类型 如果为true，进行邮件列表发送邮件时，可以接受到邮件，如果为false，将收不到邮件
        :param upsert: boolean类型 当为true时，如果该成员存在，则更新；为false时，如果成员地址存在，将报重复地址错误
        :return: dict 接口响应包体
        """
        kwargs = dict(mail_list_addr=mail_list_addr)
        if isinstance(member_addr, (str, unicode)):
            kwargs['member_addr'] = member_addr
        elif isinstance(member_addr, (list, tuple)):
            kwargs['member_addr'] = ";".join(member_addr)
        else:
            raise TypeError("param: member_addr expect type str or type list or type tuple")

        kwargs['name'] = name
        if vars_dct is not None and not isinstance(vars_dct, dict):
            raise TypeError("param: vars_dct expect type dict")
        kwargs['vars'] = json.dumps(vars_dct) and vars_dct or None
        kwargs['subscribed'] = str(subscribed).lower()
        kwargs['upsert'] = str(upsert).lower()
        return self.post("/webapi/list_member.add.json", **kwargs)

    def delete_maillist_member(self, mail_list_addr, member_addr="", name=None):
        """删除邮件列表成员
        :param mail_list_addr: 邮件列表地址
        :param member_addr: 邮件列表成员地址。如果为空删除全部邮件列表成员地址
        :param name: 邮件列表成员名称
        :return: dict 接口响应包体
        """
        kwargs = dict(mail_list_addr=mail_list_addr, member_addr=member_addr, name=name)
        return self.post("/webapi/list_member.delete.json", **kwargs)

    def query_maillist_member(self, mail_list_addr, member_addr="", start=0, limit=100):
        """查询邮件列表成员
        :param mail_list_addr: 邮件列表地址
        :param member_addr: 邮件列表成员地址。如果为空查询全部邮件列表成员地址
        :param start: 查询索引位置
        :param limit: 限制返回的结果数
        :return: dict 接口响应包体
        """
        kwargs = dict(mail_list_addr=mail_list_addr, member_addr=member_addr, start=start, limit=limit)
        return self.get("/webapi/list_member.get.json", **kwargs)

    def update_maillist_member(self, mail_list_addr, member_addr="", name=None, vars_dct=None):
        """更新邮件列表成员
        :param mail_list_addr: 邮件列表地址
        :param member_addr: 邮件列表成员地址
        :param name: 邮件列表成员名称，不能大于48个字符。
        :param vars_dct: dict类型 模板替换的变量
        :return: dict 接口响应包体
        """
        kwargs = dict(mail_list_addr=mail_list_addr, member_addr=member_addr, name=name)
        if vars_dct is not None and not isinstance(vars_dct, dict):
            raise TypeError("param: vars_dct expect type dict")
        kwargs['vars'] = json.dumps(vars_dct) and vars_dct or None
        return self.post("/webapi/list_member.get.json", **kwargs)

    def get(self, api_path, **kwargs):
        if kwargs:
            url = urlconcat(self.part_url(api_path), kwargs)
        else:
            url = self.part_url(api_path)
        request = HTTPRequest(url, method="GET", validate_cert=False)
        return self.fetch(request)

    def post(self, api_path, **kwargs):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        url = self.part_url(api_path)
        body = kwargs and urlencode(kwargs) or None
        request = HTTPRequest(url, method="POST", headers=headers, body=body, validate_cert=False)
        return self.fetch(request)

    def fetch(self, request):
        try:
            resp_body = super(SendCloudApi, self).fetch(request)
            json_body = json.loads(resp_body)
            if json_body.get('message') == 'error':
                errors = str(json_body.get("errors"))
                raise SendCloudApiError(msg=errors)
            return json_body
        except ApiError:
            raise
        except HTTPError, e:
            if e.code == 599:
                raise SendCloudApiError(msg=e.message)
            log.debug("http code: [%s] response body: [%s]" % (e.code, e.response.body))
            raise SendCloudApiError(msg=e.response.body, httpcode=e.code, httpmsg=e.response.body)
        except Exception, e:
            raise SendCloudApiError(msg=e.message)

    def part_url(self, api_path):
        api_url = self.api_url[:-1] if self.api_url.endswith("/") else self.api_url
        return "%s%s" % (api_url, api_path)


if __name__ == '__main__':
    content = """尊敬的爱手艺用户您好：

您已成功注册为爱手艺（http://www.ishouyi.com）用户，请激活您的账号：

http://www.ishouyi.com/activate?id=7884333333

爱手艺服务团队敬上

2014-09-11
"""
    api = SendCloudApi(api_user='postmaster@ishouyi.sendcloud.org', api_key='DYUfmAV8IXLj2iTV')
    try:
        print api.send_mail(['tufei8438@gmail.com'], '请激活您的爱手艺账户', content, 'admin@ishouyi.com', use_maillist=True)
    except SendCloudApiError, e:
        print e.msg
        print e.httpmsg
        print e.httpcode
                        #cc_users=['jeffy.junfu@gmail.com', 'zhangleipro@gmail.com'],
                        #resp_email_id=True, attachments=['/Users/tufei/Desktop/test.txt'])
