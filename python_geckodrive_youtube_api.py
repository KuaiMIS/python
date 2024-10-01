import random
import time
from googleapiclient.discovery import build
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

# 你的 API Key
API_KEY = 'google_api_key'

# 設定 geckodriver 路徑
geckodriver_path = r'D:\Python\geckodriver-v0.35.0-win32\geckodriver.exe'  # 替換為你的 geckodriver 完整路徑

# 設定 Firefox 的路徑
firefox_options = Options()
firefox_options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"  # 替換為你的 Firefox 路徑

# 設定 Selenium 使用的 Firefox 瀏覽器
service = FirefoxService(executable_path=geckodriver_path)
driver = webdriver.Firefox(service=service, options=firefox_options)

# 打開 Firefox 時設定為全螢幕
driver.maximize_window()

# 建立 YouTube API 客戶端
youtube = build('youtube', 'v3', developerKey=API_KEY)

# 定義關鍵字列表
keywords = ['keyword1', 'keyword2', 'keyword2']

# 遍歷每個關鍵字進行查詢
for keyword in keywords:
    print(f"正在搜尋關鍵字: {keyword}\n")
    
    # 使用關鍵字查詢
    search_response = youtube.search().list(
        q=keyword,
        part='snippet',
        maxResults=30  # 每個關鍵字返回 30 筆資料
    ).execute()

    # 列出結果並依次打開非頻道或播放清單的影片
    for i, item in enumerate(search_response['items']):
        if item['id']['kind'] == 'youtube#video':
            print(f"{i + 1}. Title: {item['snippet']['title']}")
            print(f"   Channel: {item['snippet']['channelTitle']}")
            print(f"   Description: {item['snippet']['description']}")
            video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            print(f"   URL: {video_url}\n")

            # 打開影片頁面
            driver.get(video_url)

            # 等待網頁加載
            time.sleep(5)

            # 設定為劇院模式
            try:
                theater_mode_button = driver.find_element(By.CSS_SELECTOR, "button.ytp-size-button")
                theater_mode_button.click()
                print("劇院模式啟用...")
                time.sleep(2)  # 等待模式切換
            except Exception as e:
                print(f"劇院模式按鈕未找到: {e}")

            # 確保影片播放中，如果影片沒自動播放，再次嘗試點擊播放按鈕
            try:
                play_button = driver.find_element(By.CSS_SELECTOR, "button.ytp-play-button")
                if "ytp-play-button" in play_button.get_attribute("class"):
                    play_button.click()  # 點擊播放按鈕
                    print("影片已開始播放...")
            except Exception as e:
                print(f"播放按鈕未找到或已播放: {e}")

            # 確認影片是否播放並保持播放狀態
            time.sleep(2)  # 等待一段時間確認播放狀態
            try:
                video_state = driver.execute_script("return document.querySelector('.video-stream').paused")
                if video_state:
                    # 影片暫停，再次點擊播放
                    play_button = driver.find_element(By.CSS_SELECTOR, "button.ytp-play-button")
                    play_button.click()
                    print("影片暫停，已重新播放...")
            except Exception as e:
                print(f"無法確認影片狀態或影片未能繼續播放: {e}")

            # 隨機等待 30 到 60 秒
            play_time = random.randint(30, 60)
            print(f"隨機播放 {play_time} 秒...")
            time.sleep(play_time)

            # 關閉視窗
            driver.close()

            # 重新打開瀏覽器以繼續查看下一個影片
            driver = webdriver.Firefox(service=service, options=firefox_options)
            driver.maximize_window()

        elif item['id']['kind'] == 'youtube#playlist':
            print(f"{i + 1}. Title: {item['snippet']['title']} (播放清單)")
            print(f"   Channel: {item['snippet']['channelTitle']}")
            print(f"   Description: {item['snippet']['description']}")
            print(f"   URL: https://www.youtube.com/playlist?list={item['id']['playlistId']}\n")
        elif item['id']['kind'] == 'youtube#channel':
            print(f"{i + 1}. Channel: {item['snippet']['channelTitle']} (頻道)")
            print(f"   Description: {item['snippet']['description']}")
            print(f"   URL: https://www.youtube.com/channel/{item['id']['channelId']}\n")

# 程式執行完畢後，關閉瀏覽器
driver.quit()
