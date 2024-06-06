# GameMale-Automatic-tasks

一个0基础小白使用 ChatGPT 写出来的关于 GameMale 论坛自动签到的脚本，欢迎大佬随时修改优化这一坨屎山代码。

## 这个脚本有什么用？
每日登录 （**3血液**）
每日签到 （**根据签到时间获得随机的金币**）
每日访问 （**访问1次别人空间获得1金币，每日最多3次，最多获得3金币**）
每日表态 （**1次表态获得1血液，每日最多10次，最多获得10血液**）
每日汇总 （**以上任务完成后自动推送账户信息到Telegram机器人**）

## 使用说明

1. 在第8行设置你的cookies。
2. 在第148、149行设置你的TG BOT API和你的TG ID（推送每日用户消息）。
3. 在第169、170、171行设置你每天固定访问的3个用户的空间链接（获取金币）。

### 怎么获得cookies？

按 F12 打开开发者工具，获取cookies。

### 怎么获得TG BOT API？

参考：[如何创建Telegram Bot](https://tastones.com/stackoverflow/telegram-bot/getting-started-with-telegram-bot/create_a_bot_with_the_botfather/)。
你最终获得的HTTP API即为TG BOT API。

### 怎么获得TG ID？

访问：[Get User ID Bot](https://t.me/getuseridabstract_bot)。
这个机器人返回的数字就是你的TG ID。
