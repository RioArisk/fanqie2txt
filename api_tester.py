import requests
import json

def test_api():
    url = "https://mssdk.bytedance.com/web/common?msToken=pVaf0IVDo3S8cn3bPfZGzQWCsEGdlYsfuffG2KyaVaMFzRKtaBrwRULIl_iEtK4D2LooiUR5YpkHubLP4lOpsUXBtdL3yYvR-pOuMC7gbBODVqs80ZZA4vsq6b0f0LbsqDM%3D"

    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6,da;q=0.5',
        'content-type': 'text/plain;charset=UTF-8',
        'cookie': 'ttwid=1%7CYkB4WgvBHuRT8mcgw2vz0RCSxghHDjbG4AJ4I7hmKbc%7C1755246487%7C0aa976844c08df2dda1be1139084d86d7f1f8654a4252e038a8d927a2db8d746; sessionid=03455814da399b8709f1da0faa99839a',
        'origin': 'https://fanqienovel.com',
        'priority': 'u=1, i',
        'referer': 'https://fanqienovel.com/',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0'
    }

    payload = {
        "magic": 538969122,
        "version": 1,
        "dataType": 8,
        "strData": "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"
    }

    response = requests.post(url, headers=headers, json=payload)

    print(response.status_code)
    try:
        print(response.json())
    except json.JSONDecodeError:
        print(response.text)

if __name__ == '__main__':
    test_api()
