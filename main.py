# test virtual env python=3.8
# pip install bs4
# pip install pyautogui
# pip install selenium
# pip install chromedriver-autoinstaller
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
import chromedriver_autoinstaller
import subprocess
import pyautogui
import os.path
import glob
import time


#이 부분이 민감하다면 처음 시작할 때, 중단점으로 켜진 크롬창에서 로그인 후 종료하면 이후 자동로그인
user_id = "구글 아이디"
user_pw = "비밀번호"

url = ""
pathname = r"C:\Users\kwansu\Desktop\auto_jamboard_background_setting\save\*"
# 만들 슬라이드의 시작번호와 끝번호 
# ex) [22:62] -> 22쪽부터 최대 20슬라이드로 41쪽까지의 슬라이드가 생성
start_page = 33
end_page = 48

MAX_SLIDE_NUM = 19
JS_DROP_FILES = "var c=arguments,b=c[0],k=c[1];c=c[2];for(var d=b.ownerDocument||document,l=0;;){var e=b.getBoundingClientRect(),g=e.left+(k||e.width/2),h=e.top+(c||e.height/2),f=d.elementFromPoint(g,h);if(f&&b.contains(f))break;if(1<++l)throw b=Error('Element not interactable'),b.code=15,b;b.scrollIntoView({behavior:'instant',block:'center',inline:'center'})}var a=d.createElement('INPUT');a.setAttribute('type','file');a.setAttribute('multiple','');a.setAttribute('style','position:fixed;z-index:2147483647;left:0;top:0;');a.onchange=function(b){a.parentElement.removeChild(a);b.stopPropagation();var c={constructor:DataTransfer,effectAllowed:'all',dropEffect:'none',types:['Files'],files:a.files,setData:function(){},getData:function(){},clearData:function(){},setDragImage:function(){}};window.DataTransferItemList&&(c.items=Object.setPrototypeOf(Array.prototype.map.call(a.files,function(a){return{constructor:DataTransferItem,kind:'file',type:a.type,getAsFile:function(){return a},getAsString:function(b){var c=new FileReader;c.onload=function(a){b(a.target.result)};c.readAsText(a)}}}),{constructor:DataTransferItemList,add:function(){},clear:function(){},remove:function(){}}));['dragenter','dragover','drop'].forEach(function(a){var b=d.createEvent('DragEvent');b.initMouseEvent(a,!0,!0,d.defaultView,0,0,0,g,h,!1,!1,!1,!1,0,null);Object.setPrototypeOf(b,null);b.dataTransfer=c;Object.setPrototypeOf(b,DragEvent.prototype);f.dispatchEvent(b)})};d.documentElement.appendChild(a);a.getBoundingClientRect();return a;"

def drop_files(element, files, offsetX=0, offsetY=0):
    driver = element.parent
    isLocal = not driver._is_remote or '127.0.0.1' in driver.command_executor._url
    paths = []
    
    # ensure files are present, and upload to the remote server if session is remote
    for file in (files if isinstance(files, list) else [files]) :
        if not os.path.isfile(file) :
            raise FileNotFoundError(file)
        paths.append(file if isLocal else element._upload(file))
    
    value = '\n'.join(paths)
    elm_input = driver.execute_script(JS_DROP_FILES, element, offsetX, offsetY)
    elm_input._execute('sendKeysToElement', {'value': [value], 'text': value})


WebElement.drop_files = drop_files

subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동

option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
driver.implicitly_wait(10)
driver.get(url)


# 로그인
before_login = False
soup = BeautifulSoup(driver.page_source, "html.parser")
if soup.select_one('.gb_1.gb_2.gb_1d.gb_1c'):
    time.sleep(1)   # wait a process
    driver.find_element_by_class_name('gb_1.gb_2.gb_1d.gb_1c').click()
    driver.implicitly_wait(10)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    before_login = soup.select_one('#identifierId') == None

    driver.back()
    driver.implicitly_wait(10)

    time.sleep(1)
    driver.find_element_by_class_name('gb_1.gb_2.gb_1d.gb_1c').click()
    driver.implicitly_wait(10)

    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    if before_login == False:
        pyautogui.write(user_id)
        pyautogui.press('tab', presses=3)   # Press the Tab key 3 times
        time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)
    pyautogui.write(user_pw)
    pyautogui.press('enter')
    time.sleep(3)
    driver.implicitly_wait(5)
    time.sleep(2)


# 버튼 매핑
next_page = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div/div[3]')
create_page = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div/div[4]')

background_setting = driver.find_element_by_id('frameBackgroundButton')
background_setting.click()
driver.implicitly_wait(3)

add_img_id = None
soup = BeautifulSoup(driver.page_source, "html.parser")
for e in soup.select('.goog-palette-cell'):
    if e.attrs["aria-label"] == "이미지":
        add_img_id = e.attrs["id"]

add_img = driver.find_element_by_id(add_img_id)
#add_img = driver.find_element_by_xpath('/html/body/div[20]/div/table/tbody/tr[2]/td[4]')

add_img.click()
driver.implicitly_wait(3)

frame_id = driver.find_elements_by_css_selector('iframe')[-1].get_attribute('name')
driver.switch_to.frame(frame_id)
dropzone = driver.find_element_by_class_name('Y7Vyje')
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div/div[3]').click()
driver.switch_to.parent_frame()


def set_background(img_path): # 배경 추가
    background_setting.click()
    driver.implicitly_wait(3)

    add_img.click()
    driver.implicitly_wait(3)

    driver.switch_to.frame(frame_id)
    dropzone.drop_files(img_path)
    driver.implicitly_wait(10)
    time.sleep(1)
    driver.switch_to.parent_frame()


def add_page():   # 페이지 추가
    for _ in range(10): # 무한루프를 방지하기위해 while대신 for문
        try:
            if create_page.get_attribute("aria-hidden") == "true":
                next_page.click()
            else:
                create_page.click()
        except:
            continue
        break
    else:   # break가 아닌 모든 for문을 돈 경우, 즉 뭔가 문제가 생긴경우
        raise Exception

    driver.implicitly_wait(3)


time.sleep(10)
path_list = glob.glob(pathname)
for i, path in enumerate(path_list[start_page-1:min(start_page+MAX_SLIDE_NUM, end_page)]):
    set_background(path)
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    if i < 19:
        add_page()

driver.close()
driver.quit()