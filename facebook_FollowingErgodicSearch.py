# facebook 基于用户关注人员的遍历搜索
# Updatad by chai, 2023.5.27

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from zhconv import convert
import time
import requests


def until_it(css_ele):
    try:
        driver.find_element(By.CSS_SELECTOR, value=css_ele)
        return
    except:
        driver.execute_script("window.scrollBy(0,2000)")
        until_it(css_ele)


def enter():

    # 模拟登录
    username = driver.find_element(By.CSS_SELECTOR, value = r'div[class = "xod5an3"] > div > label > div > div > input')
    password = driver.find_element(By.CSS_SELECTOR, value = r'div[class = "x1c436fg"] > div > label > div > div > input')
    username.send_keys("你的账号")
    password.send_keys("你的密码")
    password.send_keys(Keys.RETURN)
    driver.implicitly_wait(10)


def crawl_followings(target_url):
    driver.implicitly_wait(10)
    print("\n")
    print(target_url)

    # 点击粉丝
    href_followers = target_url + '/followers'
    css_followers = 'a[href="' + href_followers + '"]'
    try:
        frs = driver.find_element(By.CSS_SELECTOR, value = css_followers)
    except:
        driver.back()
        return
    driver.execute_script("arguments[0].click();", frs)
    time.sleep(1)
    driver.execute_script("window.scrollBy(0,500)")
    driver.implicitly_wait(10)

    # 点击关注
    href_following = target_url + '/following'
    css_following = 'a[href="'+ href_following +'"]'
    try:
        fo = driver.find_element(By.CSS_SELECTOR, value = css_following)
    except:
        driver.back()
        return
    driver.execute_script("arguments[0].click();", fo)
    driver.implicitly_wait(10)

    # 滑到加载出所有关注
    temp = 0
    num_fo_id = 1
    while (temp != num_fo_id):
        temp = num_fo_id
        # print(temp)
        driver.execute_script("window.scrollBy(0,1000)")
        time.sleep(1)
        fo_id = driver.find_elements(By.CSS_SELECTOR,
                                     value=r'span[class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u"]')
        num_fo_id = len(fo_id)
        # print(num_fo_id)
    driver.implicitly_wait(10)

    # 输出id
    fo_id_list = []
    for j in range(1, num_fo_id + 1):
        fo_id_list.append(fo_id[j - 1].text)
        fo_id_list[j - 1].encode('utf-8_sig').decode("utf-8")
        print(convert(fo_id_list[j - 1], 'zh-cn'))

    # 去到下一位
    css_list_ = 'div[class="x78zum5 x1q0g3np x1a02dak x1qughib"] > div > div[class="x1iyjqo2 x1pi30zi"] > div > a'
    list_ = driver.find_elements(By.CSS_SELECTOR, value=css_list_)
    num_list = len(list_)

    for i in range(1, num_list + 1):
        # print(i)
        css_list_ = 'div[class="x78zum5 x1q0g3np x1a02dak x1qughib"] > div > div[class="x1iyjqo2 x1pi30zi"] > div > a'
        list_ = driver.find_elements(By.CSS_SELECTOR, value=css_list_)
        url = list_[i - 1].get_attribute('href')
        # print(url)
        driver.execute_script("arguments[0].click();", list_[i - 1])

        # 递归到下一位
        crawl_followings(url)
        print("return!")
        time.sleep(1)


if __name__ == "__main__":
    # 创建浏览器进入目标主页
    try:
        options = webdriver.ChromeOptions()

        # 取消通知；取消加载图片
        prefs = {
            'profile.default_content_setting_values': {
                'notifications': 2
            },
            "profile.managed_default_content_settings.images": 2
        }
        options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(options=options)

        # 启动浏览器进入目标主页
        target_url = '目标主页url'
        driver.get(target_url)
        driver.maximize_window()
    except:
        print("不要怀疑自己！是网速不行！")
    driver.implicitly_wait(10)

    enter();
    crawl_followings(target_url);



