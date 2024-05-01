import asyncio
from pyppeteer import launch

from ql import QL


def find_cookie(cookies: str) -> str:
    """提取pt_key和pt_pin
    """
    pt_pin = pt_key = None
    for item in cookies.split('; '):
        if 'pt_pin' in item:
            pt_pin = item
        if 'pt_key' in item:
            pt_key = item
    if pt_pin and pt_key:
        jd_cookie = f"{pt_pin};{pt_key};"
        print("Cookie:", jd_cookie)
        return jd_cookie
    return None


# 获取JD Cookie的函数
async def get_jd_cookie() -> (bool, str):
    browser = await launch(headless=False, dumpio=True, autoClose=False,
                           args=['--no-sandbox', '--window-size=1000,800', '--disable-infobars'])

    # 创建隐私浏览器上下文
    context = await browser.createIncognitoBrowserContext()

    # 关闭默认打开的第一个标签页
    pages = await browser.pages()
    if pages:
        await pages[0].close()

    # 在隐私上下文中打开新的页面
    page = await context.newPage()
    await page.setViewport({'width': 1000, 'height': 800})
    await page.goto('https://home.m.jd.com/myJd/home.action', {'timeout': 1000 * 60})

    try:
        await page.waitFor(1000)
        elm = await page.waitForXPath('//*[@id="myHeader"]', timeout=0)
        if elm:
            cookie = await page.cookies()
            cookies_temp = ['{}={}'.format(i["name"], i["value"]) for i in cookie]
            cookies = '; '.join(cookies_temp)
            jd_cookie = find_cookie(cookies)
            if jd_cookie:
                return True, jd_cookie
            else:
                return False, "Cookie not found."
        else:
            return False, "Login element not found."
    except Exception as e:
        print(f"Error during cookie retrieval: {e}")
        return False, f"Error during cookie retrieval: {str(e)}"
    finally:
        await browser.close()  # 确保无论如何都关闭浏览器


# 更新JD Cookie到青龙面板
def update_jd_cookie_to_ql(ql, jd_cookie, remark):
    status, envs = ql.getEnvs()  # 获取所有环境变量
    for env in envs:
        if env['remarks'] == remark:  # 判断是否存在相同备注
            old_env = env  # 保存旧的JD_COOKIE
            _id = old_env['id']  # 获取旧的JD_COOKIE的ID
            # 删除旧的JD_COOKIE
            ql.deleteEnvs([_id])  # 调用删除环境变量的方法

            env = [{
                "name": old_env['name'],
                "value": str(jd_cookie),
                "remarks": remark
            }]
            # 新增JD_COOKIE
            ql.addEnvs(env)  # 调用新增环境变量的方法
            return True

    # 如果不存在相同备注，则新增JD_COOKIE
    env = [
        {
            "name": "JD_COOKIE",
            "value": str(jd_cookie),
            "remarks": remark
        }
    ]
    # 新增JD_COOKIE
    ql.addEnvs(env)  # 调用新增环境变量的方法
    return True

if __name__ == "__main__":
    # 初始化青龙API
    address = "http://192.168.100.XXX:XXXX"
    client_id = "XXXXXX"
    client_secret = "XXXXX_XXXXXXXXX"
    remark = "XXXXX"
    ql = QL(address, client_id, client_secret)
    print(ql.auth)
    print(ql.getEnvs()[1])
    # 获取JD Cookie
    success, jd_cookie = asyncio.get_event_loop().run_until_complete(get_jd_cookie())
    if jd_cookie.find("pt_pin=") != -1:
        remark = jd_cookie[jd_cookie.find("pt_pin=") + 7:jd_cookie.find(";", jd_cookie.find("pt_pin="))]
        print(remark)
    # 更新JD Cookie到青龙面板
    update_jd_cookie_to_ql(ql, jd_cookie, remark)
