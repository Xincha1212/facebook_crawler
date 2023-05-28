# facebook 爬取个人相册高清照片
# Updatad by chai, 2023.5.13

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from zhconv import convert
import time
import datetime


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
    driver = webdriver.Chrome(options = options)
    # 启动浏览器进入目标主页
    target_url = '目标主页url'
    # target_url = target_url + "/photos"
    driver.get(target_url)
    driver.maximize_window()
except:
    print("不要怀疑自己！是网速不行！")
driver.implicitly_wait(10)

# 模拟登录
username = driver.find_element(By.CSS_SELECTOR, value = r'div[class = "xod5an3"] > div > label > div > div > input')
password = driver.find_element(By.CSS_SELECTOR, value = r'div[class = "x1c436fg"] > div > label > div > div > input')
username.send_keys("你的账号")
password.send_keys("你的密码")
password.send_keys(Keys.RETURN)
driver.implicitly_wait(10)

# 点击图库
lib = 'a[href="' + target_url + '/photos"] > div > span'
driver.find_element(By.CSS_SELECTOR, value = lib).click()
driver.implicitly_wait(10)
time.sleep(5)

# 拉到底端
count = 0
temp_height = 0
check_height = 1
print("正在拉向底端，请稍后。")
while True:
    driver.execute_script("window.scrollBy(0,1000)")
    time.sleep(1)
    temp_height = check_height
    check_height = driver.execute_script(
        "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
    check_height = check_height % 2000
    # print(check_height)
    if check_height == temp_height:
        count = count + 1
    if count == 3:
        break

# 爬取所有图片
css_img = 'a[class="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv x1lliihq x5yr21d x1n2onr6 xh8yej3"]'
img = driver.find_elements(By.CSS_SELECTOR, value = css_img)
driver.implicitly_wait(300)

num_img = len(img)
img_list = [];
for i in range(1, num_img + 1):
    poes = str(i / num_img * 100) + '%'

    # 点击进入大图
    driver.execute_script("arguments[0].click();", img[i-1])
    driver.implicitly_wait(10)

    # 获取高清图片链接
    try:
        css_dst_img = 'img[class="x1bwycvy x193iq5w x4fas0m x19kjcj4"]'
        dst_img = driver.find_element(By.CSS_SELECTOR, value = css_dst_img)
        img_url = dst_img.get_attribute('src')
        img_list.append(img_url)
        print(img_url)
        # print(poes)
    except:
        print("可能是3D图片或其他情况")
        # print(poes)

    # 点击关闭
    css_close = 'div[class="x1i10hfl x6umtig x1b1mbwd xaqea5y xav7gou x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x87ps6o x1lku1pv x1a2a7pz x6s0dn4 x14yjl9h xudhj91 x18nykt9 xww2gxu x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xl56j7k xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1vqgdyp x100vrsf x18l40ae x14ctfv"]'
    close = driver.find_element(By.CSS_SELECTOR, value = css_close)
    driver.execute_script("arguments[0].click();", close)
    driver.implicitly_wait(10)

print("over!")

