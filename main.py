import sys
import requests
import json
from bs4 import BeautifulSoup
import urllib.parse
import os


def load_config():
    accounts_json = os.environ.get('ACCOUNTS', '[]')
    print(accounts_json)
    if not accounts_json:
        print("警告: ACCOUNTS 环境变量为空")
    try:
        accounts = json.loads(accounts_json)
    except json.JSONDecodeError:
        print("错误: ACCOUNTS 环境变量格式不正确")
        accounts = []

    config = {
        "accounts": accounts,
        "SCKEY": os.environ.get('SCKEY', '')
    }
    return config


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
        response = session.post(url=login_url, headers=header, data=data)
        response.raise_for_status()
        response_data = response.json()
        print(response_data['msg'])

        # 进行签到
        result = session.post(url=check_url, headers=header)
        result.raise_for_status()
        result_data = result.json()
        print(result_data['msg'])

        # 获取用户页面并解析订阅链接
        user_page = session.get(url=user_url, headers=header)
        user_page.raise_for_status()
        soup = BeautifulSoup(user_page.text, 'html.parser')
        sub_link = soup.find('a', {'data-clipboard-text': True})
        if sub_link:
            subscription_url = sub_link['data-clipboard-text']
            print(f"订阅链接: {subscription_url}")
        else:
            subscription_url = ""
            print("未找到订阅链接")

        return f"账号 {email}: {result_data['msg']}", subscription_url
    except requests.RequestException as e:
        error_msg = f"账号 {email} 操作失败: {str(e)}"
        print(error_msg)
        return error_msg, ""


def merge_subscriptions(subscription_urls):
    subconverter_url = "https://sub.xeton.dev/sub"
    params = {
        'target': 'clash',
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
    try:
        response = requests.get(subconverter_url, params=params)
        response.raise_for_status()
        return response.url
    except requests.RequestException as e:
        print(f"合并订阅失败: {str(e)}")
        return "合并订阅失败"


def main():
    print("开始执行签到脚本...")
    config = load_config()
    SCKEY = config.get('SCKEY')

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
        try:
            push_url = f'https://sctapi.ftqq.com/{SCKEY}.send?title=机场签到&desp={urllib.parse.quote(content)}'
            response = requests.post(url=push_url)
            response.raise_for_status()
            print('推送成功')
        except requests.RequestException as e:
            print(f'推送失败: {str(e)}')
    else:
        print('未配置 SCKEY，跳过推送')

    print("所有账号签到完成")
    print(content)


if __name__ == "__main__":
    sys.stdout = open('output.log', 'w')
    main()
    sys.stdout.close()
