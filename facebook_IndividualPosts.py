# facebook 爬取个人资料及帖子内容
# Updatad by chai, 2023.5.13

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from zhconv import convert
import time


def enter_target():
    # 模拟登录
    driver.implicitly_wait(10)
    username = driver.find_element(By.CSS_SELECTOR, value=r'div[class = "xod5an3"] > div > label > div > div > input')
    password = driver.find_element(By.CSS_SELECTOR, value=r'div[class = "x1c436fg"] > div > label > div > div > input')
    username.send_keys("你的账号")
    password.send_keys("你的密码")
    password.send_keys(Keys.RETURN)
    driver.implicitly_wait(10)


def introduction():
    # 个人资料
    itr = driver.find_element(By.CSS_SELECTOR,
                              value=r'span[class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u"]')
    print("个人资料")
    print(itr.text)
    print("\n")


def expansion(i):
    # 点击展开
    try:
        css_unfold = 'div[aria-posinset="' + str(
            i) + '"] > div > div > div > div > div > div > div > div > div > div > div > div > div[class="xu06os2 x1ok221b"] > span > div > div[style="text-align: start;"] > div[role="button"]'
        unfold = driver.find_element(By.CSS_SELECTOR, value=css_unfold)
        if not unfold:
            css_unfold = 'div[aria-posinset="' + str(
                i) + '"] > div > div > div > div > div > div > div > div > div > div > div > div > div[class="xu06os2 x1ok221b"] > span > div > div > div[role="button"]'
            unfold = driver.find_element(By.CSS_SELECTOR, value=css_unfold)

        driver.execute_script("arguments[0].click();", unfold)
    except:
        print()


def posttext(i):
    # 爬取文字
    try:
        css_text = 'div[aria-posinset="' + str(
            i) + '"] > div > div > div > div > div > div > div > div > div > div > div > div > div[class="xu06os2 x1ok221b"] > span > div > div[style="text-align: start;"]'
        text = driver.find_elements(By.CSS_SELECTOR, value=css_text)
        if not text:
            css_text = 'div[aria-posinset="' + str(
                i) + '"] > div > div > div > div > div > div > div > div > div > div > div > div > div[class="xu06os2 x1ok221b"] > span > div > div'
            text = driver.find_elements(By.CSS_SELECTOR, value=css_text)

        num_text = len(text)
        text_list = []
        for j in range(1, num_text + 1):
            text_list.append(text[j - 1].text)
            text_list[j - 1].encode('utf-8_sig').decode("utf-8")
            print(convert(text_list[j - 1], 'zh-cn'))
    except:
        print("无文字")


def postlikes(i):
    # 爬取点赞
    css_likes = 'div[aria-posinset="' + str(
        i) + '"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > span > div > span[class="xt0b8zv x1jx94hy xrbpyxo xl423tq"] > span > span'
    likes = driver.find_element(By.CSS_SELECTOR, value=css_likes)
    print(likes.text)


def postimg(i):
    # 爬取图片
    try:
        # 图片超过5张
        # 获取帖子图片数量
        css_more_img = 'div[aria-posinset="' + str(
            i) + '"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > a > div > div[class="x17z8epw x579bpy x1s688f x2b8uid"]'
        num_more_img = driver.find_element(By.CSS_SELECTOR, value=css_more_img)
        img_filter = filter(str.isdigit, num_more_img.text)
        more_img_list = list(img_filter)
        more_img_str = "".join(more_img_list)
        more_img_num = int(more_img_str)
        # 点击第一个照片
        css_img = 'div[aria-posinset="' + str(
            i) + '"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > a > div > div > div > img'
        img = driver.find_elements(By.CSS_SELECTOR, value=css_img)
        driver.execute_script("arguments[0].click();", img[0])
        driver.implicitly_wait(2)
        # 点击下一张
        css_next = 'div[aria-label="下一张"]'
        next = driver.find_element(By.CSS_SELECTOR, value=css_next)
        # 获取所有照片
        for j in range(1, more_img_num + 4):
            time.sleep(0.5)
            css_dst_img = 'img[class="x1bwycvy x193iq5w x4fas0m x19kjcj4"]'
            dst_img = driver.find_element(By.CSS_SELECTOR, value=css_dst_img)
            img_url = dst_img.get_attribute('src')
            print(img_url)
            driver.execute_script("arguments[0].click();", next)
            driver.implicitly_wait(3)
        # 点击关闭
        css_close = 'div[class="x1i10hfl x6umtig x1b1mbwd xaqea5y xav7gou x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x87ps6o x1lku1pv x1a2a7pz x6s0dn4 x14yjl9h xudhj91 x18nykt9 xww2gxu x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xl56j7k xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1vqgdyp x100vrsf x18l40ae x14ctfv"]'
        close = driver.find_element(By.CSS_SELECTOR, value=css_close)
        driver.execute_script("arguments[0].click();", close)

    # 帖子图片不超过5张
    except:
        try:
            css_img = 'div[aria-posinset="' + str(
                i) + '"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > a > div > div > div > img'
            img = driver.find_elements(By.CSS_SELECTOR, value=css_img)
            if not img:
                css_img = 'div[aria-posinset="' + str(
                    i) + '"] > div > div > div > div > div > div > div > div > div > div > div > a > div > div > div > div > img'
                img = driver.find_elements(By.CSS_SELECTOR, value=css_img)

            num_img = len(img)
            for j in range(1, num_img + 1):

                # 点击高清图片
                driver.execute_script("arguments[0].click();", img[j - 1])
                driver.implicitly_wait(2)
                try:
                    css_dst_img = 'img[class="x1bwycvy x193iq5w x4fas0m x19kjcj4"]'
                    dst_img = driver.find_element(By.CSS_SELECTOR, value=css_dst_img)
                    img_url = dst_img.get_attribute('src')
                    print(img_url)
                except:
                    print("非正常图片")

                # 点击关闭
                css_close = 'div[class="x1i10hfl x6umtig x1b1mbwd xaqea5y xav7gou x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x87ps6o x1lku1pv x1a2a7pz x6s0dn4 x14yjl9h xudhj91 x18nykt9 xww2gxu x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xl56j7k xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1vqgdyp x100vrsf x18l40ae x14ctfv"]'
                close = driver.find_element(By.CSS_SELECTOR, value=css_close)
                driver.execute_script("arguments[0].click();", close)

        except:
            print("无图片")


def crawlposts(num):
    # 爬取num个帖子
    for i in range(1, num + 1):
        post_list = []
        s = '第' + str(i) + '个帖子的内容为：'
        print(s)
        # 模拟滚轮往下滚
        driver.execute_script("window.scrollBy(0,500)")
        driver.implicitly_wait(3)
        css_post = 'div[aria-posinset="' + str(i) + '"]'
        # 判断第i个帖子是否出现
        present = []
        while (not present):
            driver.execute_script("window.scrollBy(0,500)")
            driver.implicitly_wait(1)
            try:
                present = driver.find_element(By.CSS_SELECTOR, value=css_post)
            except:
                present = []
        time.sleep(0.5)

        expansion(i)
        posttext(i)
        postlikes(i)
        postimg(i)

        print("\n")


if __name__ == "__main__":

    url = '目标主页url'
    # 创建浏览器进入目标主页
    try:
        options = webdriver.ChromeOptions()
        # 取消通知
        prefs = {
            'profile.default_content_setting_values': {
                'notifications': 2
            }
        }
        options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(options=options)
        # 启动浏览器进入目标主页
        target_url = url
        driver.get(target_url)
        driver.maximize_window()
    except:
        print("不要怀疑自己！是网速不行！")

    enter_target()
    introduction()
    crawlposts(10)

    print("\n")
    print("over!")

