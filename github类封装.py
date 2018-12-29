import requests
from lxml import etree


class GithubLogin(object):
    def __init__(self):
        # 登录页get请求URL
        self.login_url = 'https://github.com/login'
        # 登录post提交URL
        self.do_login_url  = 'https://github.com/session'
        # github个人主页
        self.profile_url = 'https://github.com/settings/profile'
        # 登录页headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Referer': 'https://github.com',
            'Origin': 'https://github.com',
            'Host': 'github.com'
        }
        self.s = requests.Session()

    def get_csrf_token(self):
        """
        请求表单页,获取authenticity_token（csrf token）
        :return: {str}  'lkweufjLKSJDIW*#LSKJ'
        """
        resp = self.s.get(url=self.login_url,headers=self.headers)
        html_content = resp.text
        dom = etree.HTML(html_content)
        pattern = '//input[@name="authenticity_token"]/@value'
        authenticity_token = dom.xpath(pattern)[0]
        return authenticity_token

    def login(self):

        session_args = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.get_csrf_token(),
            'login': '账号',
            'password': '密码' ,
        }
        # 登录 post 提交表单
        res_index = self.s.post(url=self.do_login_url, headers=self.headers, data=session_args)
        if res_index.status_code == requests.codes.ok:
            self.repository(res_index.text)

        # 请求个人中心页面
        res_profile = self.s.get(url=self.profile_url, headers=self.headers)
        if res_profile.status_code == requests.codes.ok:
            self.getProfile(res_profile.text)

    def repository(self, text):

        res_obj = etree.HTML(text)
        repo_list = res_obj.xpath('//div[@class="Box-body"]/ul/li//a/@href')
        for repo in repo_list:
            print(repo)

    def getProfile(self, text):
        res_obj = etree.HTML(text)
        username = res_obj.xpath(
            '//*[@id="user_profile_name"]/@value')[0]
        print("用户名：", username)
        email = res_obj.xpath('//select[@id="user_profile_email"]/option/text()')[1]
        print("邮箱：", email)

if __name__ == '__main__':
    gitrun = GithubLogin()
    gitrun.login()
