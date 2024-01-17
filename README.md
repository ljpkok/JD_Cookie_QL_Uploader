# JD Cookie 获取器

## 简介
本项目是一个用于获取JD（京东）Cookie的工具，并能够自动更新到青龙面板。它使用Python脚本通过模拟浏览器登录京东网站来获取用户的Cookie，然后利用青龙面板的API将Cookie更新至环境变量中。

## 主要用途
- **自动获取JD Cookie**：自动登录京东网站，获取用户的Cookie。
- **更新青龙面板环境变量**：将获取到的JD Cookie自动更新到青龙面板的环境变量中，便于其他脚本使用。

## 灵感来源
本项目的灵感来源于[huaisha1224](https://github.com/huaisha1224)的原始代码和CSDN博客文章：[Python自动化之使用Pyppeteer模拟登陆京东获取cookie](https://blog.csdn.net/wsfsp_4/article/details/128316982)。

## 安装指南
1. 确保您的系统已安装Python环境。
2. 安装所需的Python库：

`pip install pyppeteer requests`

3. 克隆本项目到本地：

## 使用说明
1. 在`QL`类中填写您的青龙面板地址`address`、`client_id`和`client_secret`。 获取方法[参考](https://blog.csdn.net/wsfsp_4/article/details/128316982)
2. 选择你要更新的JD_COOKIE的备注,填写为`remark`。
2. 运行主脚本以获取JD Cookie并更新到青龙面板：

`python jd_cookie_upload.py`

## 注意事项
- 确保您的青龙面板可正常访问且`client_id`和`client_secret`正确无误。

## 贡献指南
欢迎通过GitHub提交问题报告和拉取请求以帮助改进此项目。

---
