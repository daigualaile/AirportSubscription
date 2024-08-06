import requests
import json
from bs4 import BeautifulSoup
import urllib.parse

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def checkin(account):
    session = requests.session()
    url = account['url']
    email = account['email']
    passwd = account['passwd']

    login_url = f'{url}/auth/login'
    check_url = f'{url}/user/checkin'
    user_url = f'{url}/user'

    header = {
        'origin': url,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }
    data = {
        'email': email,
        'passwd': passwd
    }

    try:
        print(f'正在为账号 {email} 进行登录...')
        response = json.loads(session.post(url=login_url, headers=header, data=data).text)
        print(response)
        print(response['msg'])

        # 进行签到
        result = json.loads(session.post(url=check_url, headers=header).text)
        print(result['msg'])

        # 获取用户页面并解析订阅链接
        user_page = session.get(url=user_url, headers=header)
        soup = BeautifulSoup(user_page.text, 'html.parser')
        sub_link = soup.find('a', {'data-clipboard-text': True})
        if sub_link:
            subscription_url = sub_link['data-clipboard-text']
            print(f"订阅链接: {subscription_url}")
        else:
            subscription_url = ""
            print("未找到订阅链接")

        return f"账号 {email}: {result['msg']}", subscription_url
    except Exception as e:
        error_msg = f"账号 {email} 操作失败: {str(e)}"
        print(error_msg)
        return error_msg, ""

def merge_subscriptions(subscription_urls):
    # 使用 subconverter 服务合并订阅链接
    subconverter_url = "https://sub.xeton.dev/sub"
    params = {
        'target': 'clash',  # 可以根据需要更改目标格式
        'url': '|'.join(subscription_urls),
        'insert': 'false',
        'config': 'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online.ini',
        'emoji': 'true',
        'list': 'false',
        'udp': 'false',
        'tfo': 'false',
        'scv': 'false',
        'fdn': 'false',
        'sort': 'false'
    }
    response = requests.get(subconverter_url, params=params)
    if response.status_code == 200:
        return response.url
    else:
        return "合并订阅失败"

def main():
    config = load_config()
    SCKEY = config['SCKEY']

    all_results = []
    subscription_urls = []

    for account in config['accounts']:
        result, sub_url = checkin(account)
        all_results.append(result)
        if sub_url:
            subscription_urls.append(sub_url)

    # 合并订阅链接
    if subscription_urls:
        merged_subscription = merge_subscriptions(subscription_urls)
        all_results.append(f"\n合并后的订阅链接: {merged_subscription}")

    # 合并所有结果
    content = "\n\n".join(all_results)

    # 进行推送
    if SCKEY:
        push_url = f'https://sctapi.ftqq.com/{SCKEY}.send?title=机场签到&desp={urllib.parse.quote(content)}'
        requests.post(url=push_url)
        print('推送成功')
    else:
        print('未配置 SCKEY，跳过推送')

    print("所有账号签到完成")
    print(content)

if __name__ == "__main__":
    main()
