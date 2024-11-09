# 鉴于有大量更好用的项目出现, 本项目将不再被更新。

# JD Cookie 获取器
### 仅在青龙v2.11.3测试通过

### [点击这里进行下载](https://github.com/ljpkok/JD_Cookie_QL_Uploader/releases)

## 简介
本项目是一个用于获取JD（京东）Cookie的工具，并能够自动更新到青龙面板。它使用Python脚本通过模拟浏览器登录京东网站来获取用户的Cookie，然后利用青龙面板的API将Cookie更新至环境变量中。

## 主要用途
- **获取JD Cookie**：使用验证码登录京东网站，获取用户的Cookie。
- **更新青龙面板环境变量**：将获取到的JD Cookie自动更新到青龙面板的环境变量中，便于其他脚本使用。

## 灵感来源
本项目的部分代码来源于[huaisha1224](https://github.com/huaisha1224/Get_JDCookie)的原始代码和CSDN博客文章：[青龙面板教程(三)：OpenApi](https://blog.csdn.net/wsfsp_4/article/details/128316982)。

## 安装指南
1. 克隆本项目到本地：
2. 安装所需的Python库：
`pip install pyppeteer requests`

## 使用说明
1. 获取您的青龙面板地址`address`、`client_id`和`client_secret`。 获取方法[参考](https://blog.csdn.net/wsfsp_4/article/details/128316982)
2. 打开打包好的`exe`文件或`python jd_cookie_uploader.py`， 
3. 在弹出的新窗口中使用手机号和验证码登录京东网站。
4. 登录成功后，等待程序自动更新Cookie至青龙面板环境变量中。

## 运行截图
![JD Login Screenshot](https://github.com/ljpkok/JD_Cookie_QL_Uploader/blob/master/images/jd_login.png?raw=true)

![exe](https://github.com/ljpkok/JD_Cookie_QL_Uploader/blob/master/images/exe.png?raw=true)

## 注意事项
- 确保您的青龙面板可正常访问且`client_id`和`client_secret`正确无误。

## 贡献指南
欢迎通过GitHub提交问题报告和拉取请求以帮助改进此项目。

---

## Star History

<a href="https://star-history.com/#ljpkok/JD_Cookie_QL_Uploader&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=ljpkok/JD_Cookie_QL_Uploader&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=ljpkok/JD_Cookie_QL_Uploader&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=ljpkok/JD_Cookie_QL_Uploader&type=Date" />
 </picture>
</a>
