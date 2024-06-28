import os
import hmac
import base64
import hashlib
import textwrap
from urllib.parse import urlencode, urlparse

from .util import generate_rfc1123_date


class XFYunAuth(object):
    """
    讯飞开放平台认证类
    """

    def __init__(self,
                 api_url,
                 api_key=os.environ.get('XFYUN_API_KEY'),
                 api_secret=os.environ.get('XFYUN_API_SECRET'),
                 method='GET',
                 algorithm='hmac-sha256'):
        """
        :param api_url: 请求地址
        :param api_key: 应用的API Key，默认为环境变量中的`XFYUN_API_KEY`
        :param api_secret: 应用的API Secret，默认为环境变量中的`XFYUN_API_SECRET`
        :param method: 请求方法，默认为`GET`
        :param algorithm: 签名算法，默认为`hmac-sha256`
        """
        self.api_url = api_url
        self.api_key = api_key
        self.api_secret = api_secret
        self.method = method
        self.algorithm = algorithm

        self.api_host = urlparse(api_url).netloc
        self.api_path = urlparse(api_url).path

        self.rfc1123_date = generate_rfc1123_date()

        self._auth_url = None

    def generate_signature(self):
        """
        生成签名
        """

        signature_origin = textwrap.dedent(f'''
            host: {self.api_host}
            date: {self.rfc1123_date}
            {self.method} {self.api_path} HTTP/1.1
        ''').strip()

        signature_sha = hmac.new(
            self.api_secret.encode(),
            signature_origin.encode(),
            digestmod=hashlib.sha256
        ).digest()
        signature_sha_base64 = base64.b64encode(signature_sha).decode()
        return signature_sha_base64

    def generate_authorization(self):
        """
        生成认证信息
        """
        authorization_payload = {
            'api_key': self.api_key,
            'algorithm': self.algorithm,
            'headers': 'host date request-line',
            'signature': self.generate_signature(),
        }
        authorization_origin = ', '.join(
            f'{k}="{v}"' for k, v in authorization_payload.items())
        authorization = base64.b64encode(
            authorization_origin.encode()).decode()
        return authorization

    def generate_auth_url(self):
        """
        生成带认证信息的请求地址
        """

        payload = {
            'authorization': self.generate_authorization(),
            'date': self.rfc1123_date,
            'host': self.api_host
        }
        auth_url = self.api_url + '?' + urlencode(payload)
        return auth_url

    @property
    def auth_url(self):
        if not self._auth_url:
            self._auth_url = self.generate_auth_url()
        return self._auth_url

    def __repr__(self):
        return f'<XFYunAuth {self.api_url}>'


if __name__ == '__main__':
    import os
    import dotenv

    dotenv.load_dotenv()
    auth = XFYunAuth(
        api_url=os.environ['api_url'],
        method=os.environ.get('method', 'GET'),
    )
    print(auth.auth_url)
