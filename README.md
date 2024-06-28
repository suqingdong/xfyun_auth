# 科大讯飞API接口通用鉴权

## 安装
```bash
python3 -m pip install -U xfyun-auth
```

## 使用
```python
from xfyun_auth import XFYunAuth

# 初始化
auth = XFYunAuth(
    api_url='one_api_url',
    method='POST',
    api_key='your_api_key',
    api_secret='your_api_secret'
)

# 使用环境变量 `XFYUN_API_KEY` 和 `XFYUN_API_SECRET`
auth = XFYunAuth(api_url='one_api_url', method='POST')

# 使用生成的URL
print(auth.auth_url)

```

## 示例

> [通用文字识别](https://www.xfyun.cn/doc/words/universal_character_recognition/API.html)

```python
import os

import dotenv
import requests
from xfyun_auth import XFYunAuth

dotenv.load_dotenv()  # 加载.env文件: XFYUN_API_KEY, XFYUN_API_SECRET, XFYUN_APP_ID


url = 'https://api.xf-yun.com/v1/private/sf8e6aca1'
auth = XFYunAuth(api_url=url, method='POST')

with open('path/to/image.jpg', 'rb') as f:
    image_bytes = f.read()

payload = {
    "header": {
        "app_id": os.environ["XFYUN_APP_ID"],
        "status": 3,
    },
    "parameter": {
        "s824758f1": {
            "category": "ch_en_public_cloud",
            "result": {
                "encoding": "utf8",
                "compress": "raw",
                "format": "json"
            }
        }
    },
    "payload": {
        "s824758f1_data_1": {
            "encoding": "jpg",
            "status": 3,
            "image": str(base64.b64encode(image_bytes), 'UTF-8'),
        }
    }
}

response = requests.post(auth.auth_url, json=payload)

text = response.json()['payload']['result']['text']

json_string = base64.b64decode(text).decode().strip('\x00')

data = json.loads(json_string)
print(data)
```
