import requests
import re
import time
import html
from datetime import datetime
from bs4 import BeautifulSoup

# 设置请求头和cookies
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    "Cookie": "你的cookies"
}

# 定义获取签到值的函数
def get_formhash():
    try:
        response = requests.get("https://www.gamemale.com/", headers=headers)
        response.raise_for_status()
        formhash_match = re.search(r'formhash=([a-fA-F0-9]{8})', response.text)
        if formhash_match:
            formhash_value = formhash_match.group(1)
            return formhash_value
        else:
            return None
    except Exception as e:
        print(f'获取签到值失败：{e}')
        return None

# 定义执行签到的函数
def sign_in(formhash):
    try:
        if formhash:
            sign_url = f"https://www.gamemale.com/k_misign-sign.html?operation=qiandao&format=button&formhash={formhash}"
            response_sign = requests.get(sign_url, headers=headers)
            response_sign.raise_for_status()

            if '签到成功' in response_sign.text:
                return '签到成功'
            elif '今日已签' in response_sign.text:
                return '今日已签'
            else:
                return '签到失败'
        else:
            return '未找到 formhash 值'
    except Exception as e:
        print(f'签到失败：{e}')
        return '签到失败'

# 定义访问个人空间的函数
def visit_space(urls):
    for url in urls:
        attempts = 0
        while attempts < 3:
            try:
                response_space = requests.get(url, headers=headers)
                response_space.raise_for_status()
                if '个人空间' in response_space.text:
                    print(f'访问成功：{url}')
                    break
                else:
                    attempts += 1
                    print(f'访问失败，正在重试：{url}')
                    time.sleep(3)
            except Exception as e:
                attempts += 1
                print(f'访问失败，正在重试：{url}')
                time.sleep(3)

        if attempts == 3:
            print('连续访问失败，请重试')

# 定义获取个人信息的函数
def get_personal_info():
    try:
        info_url = "https://www.gamemale.com/home.php?mod=spacecp&ac=credit&op=base"
        response_info = requests.get(info_url, headers=headers)
        response_info.raise_for_status()

        journey_match = re.search(r'旅程:\s+(\d+)\s+km', response_info.text)
        blood_match = re.search(r'血液:\s+(\d+)\s+滴', response_info.text)
        if journey_match and blood_match:
            journey_distance = journey_match.group(1)
            blood_drops = blood_match.group(1)
            print(f'旅程: {journey_distance} km，血液: {blood_drops} 滴')
        else:
            print('未找到旅程和血液信息')
    except Exception as e:
        print(f'获取个人信息失败：{e}')

# 定义发送请求的函数
def send_request(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None

# 定义查找匹配的函数
def find_matches(pattern, text):
    return pattern.findall(text)

# 定义处理 URL 的函数
def process_urls(urls, headers, pattern):
    found_urls = set()
    for url in urls:
        response = send_request(url, headers)
        if response:
            matches = find_matches(pattern, response.text)
            found_urls.update(matches)
    return found_urls

# 定义推送信息的函数
def push_info():
    action_url = "https://www.gamemale.com/home.php?mod=spacecp&ac=credit&op=log&suboperation=creditrulelog"
    credit_url = "https://www.gamemale.com/home.php?mod=spacecp&ac=credit&op=base"
    action_response = requests.get(action_url, headers=headers)
    credit_response = requests.get(credit_url, headers=headers)
    action_soup = BeautifulSoup(action_response.text, 'html.parser')
    credit_soup = BeautifulSoup(credit_response.text, 'html.parser')

    table = action_soup.find('table', class_='dt')
    rows = table.find_all('tr')
    actions_info = ""
    for row in rows[1:]:
        cols = row.find_all('td')
        action_name = cols[0].text.strip()

        if action_name in ["信息表态", "访问别人空间", "每天登录"]:
            total_count = cols[1].text.strip()
            cycle_count = cols[2].text.strip()
            last_reward_time = cols[11].text.strip()
            actions_info += f"<b>{action_name}:</b>\n总次数 {total_count}\n周期次数 {cycle_count}\n最后奖励时间 {last_reward_time}\n\n"

    credit_list = credit_soup.find_all('ul', class_='creditl')[0].find_all('li')
    credit_info = ""
    for item in credit_list:
        label = item.find('em').text.strip()
        if label in ["金币:", "旅程:", "血液:"]:
            value = item.text.split(label)[-1].strip()
            credit_info += f"{label} {value}\n"

    username = credit_soup.find('div', class_='u-info-name').find('a').text.strip()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"\U00002600 <b>用户名:</b> {username}\n\U0001F550 <b>当前时间:</b> {current_time}\n\n<b>\U0001F527 动作信息:</b>\n{actions_info}\n\U0001F4D1 <b>账户信息:</b>\n{credit_info}"

    telegram_bot_token = "你的TG BOT API"
    telegram_user_id = "你的TG ID"
    telegram_api_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    params = {
        "chat_id": telegram_user_id,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(telegram_api_url, params=params)

# 主程序
def main():
    # 签到部分
    formhash_value = get_formhash()
    if formhash_value:
        print(f'成功获取到 formhash 值：{formhash_value}')
        result = sign_in(formhash_value)
        print(result)

        # 访问个人空间
        space_urls = [
            "找3个用户的空间链接丢在这里",
            "找3个用户的空间链接丢在这里",
            "找3个用户的空间链接丢在这里"
        ]
        visit_space(space_urls)

        # 获取个人信息
        get_personal_info()
    else:
        print('未找到 formhash 值')

    # 自动表态部分
    urls = [
        'https://www.gamemale.com/home.php?mod=space&do=blog&view=all&page=1',
        'https://www.gamemale.com/home.php?mod=space&do=blog&view=all&page=2',
        'https://www.gamemale.com/home.php?mod=space&do=blog&view=all&page=3'
    ]
    log_pattern = re.compile(r'https://www\.gamemale\.com/blog-\d{6}-\d{6}\.html')
    action_pattern = re.compile(r'https://www\.gamemale\.com/home\.php\?mod=spacecp&amp;ac=click&amp;op=add&amp;clickid=1&amp;idtype=blogid&amp;id=\d+&amp;hash=[a-zA-Z0-9]{32}&amp;handlekey=clickhandle')

    found_log_urls = process_urls(urls, headers, log_pattern)
    print("日志链接：")
    for url in found_log_urls:
        print(url)

    found_action_urls = []
    for log_url in found_log_urls:
        print(f"正在访问日志链接：{log_url}")
        time.sleep(1)
        response = send_request(log_url, headers)
        if response:
            print("搜索操作链接...")
            action_url_matches = find_matches(action_pattern, response.text)
            for match in action_url_matches:
                action_url = html.unescape(match)
                found_action_urls.append(action_url)

    print("操作链接：")
    for action_url in found_action_urls:
        print(f"正在访问操作链接：{action_url}")
        time.sleep(1)
        action_response = send_request(action_url, headers)
        if action_response:
            print(f"状态码：{action_response.status_code}")
            print(f"响应内容：{action_response.text[:100]}...")

    # 推送信息部分
    push_info()

if __name__ == "__main__":
    main()
