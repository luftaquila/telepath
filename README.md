TELEPATH
====================

TELEPATH는 디아블로3 오토 [ROS-BOT](https://www.ros-bot.com/)이 수집한 아이템 목록을 텔레그램으로 받아볼 수 있게 하는 크롤러입니다.  

TELEPATH is a crawler that allows user to receive Telegram messages if there is a item looted by Diablo 3 auto, [ROS-BOT](https://www.ros-bot.com/)

## 0. 실행 전 설정 Prerequisites
1. TELEPATH 다운로드 Download TELEPATH
    1. [TELEPATH 최신 릴리즈]()를 다운로드하고 압축을 해제합니다.  
Download [latest TELEPATH release]() and unzip it.

1. 크롬드라이버 다운로드 Download chromedriver
    * TELEPATH를 실행하기 위해서는 구글 크롬 및 크롬드라이버가 필요합니다.  
Google Chrome and chromedriver is necessary to run TELEPATH
    1. 크롬 - 도움말 - Chrome 정보에서 컴퓨터에 설치된 크롬의 버전을 확인합니다.  
In Chrome - Help - Chrome info, check the version of your chrome.
    1. [크롬드라이버 다운로드](https://chromedriver.chromium.org/downloads)에서 자신의 크롬 버전에 맞는 크롬드라이버(chromedriver_win32.zip)를 다운로드합니다.  
[Download chromedriver](https://chromedriver.chromium.org/downloads) of your chrome version.
    1. 다운로드한 크롬드라이버의 압축을 풀어 나온 `chromedriver.exe` 파일을 앞서 TELEPATH 압축을 푼 폴더에 복사합니다. `telepath.exe`, `chromedriver.exe`와 `config.ini` 파일은 같은 폴더에 위치해야 합니다.  
Unzip and copy `chromedriver.exe` to the TELEPATH unzip folder. `telepath.exe`, `chromedriver.exe` and `config.ini` should be located in the same folder.
  
1. config.ini 설정 Configuration of config.ini
    1. 텔레그램 Chat ID Telegram Chat ID
        1. 텔레그램에서 [@telepath_luftaquila_bot](https://t.me/telepath_luftaquila_bot)을 추가하고, 대화를 시작합니다.  
Add [@telepath_luftaquila_bot](https://t.me/telepath_luftaquila_bot) to your Telegram and start conversation.
        1. 봇이 알려주는 채팅 ID 숫자를 `config.ini`의 `[user]` 섹션에 있는 `telegram=` 다음에 붙여넣습니다.  
Copy and paste your chat ID number after the `telegram=`, which located in `[user]` section of `config.ini`.
    
    1. ROS-BOT ID, PW
        1. 자신의 ROS-BOT ID, PW를 각각 `config.ini`의 `[user]` 섹션에 있는 `id=`와 `pw=`에 입력합니다.  
Enter your ROS-BOT ID and password to `id=` and `pw=`, which located in `[user]` section of `config.ini`.
    
    1. 새로고침 주기 Refresh rate
        1. `config.ini`의 `[rover]` 섹션에 있는 `refresh=` 다음에 TELEPATH의 새로고침 간격을 초 단위 숫자로 입력합니다.
Enter your TELEPATH's refresh rate in seconds after `refresh=`, which located in `[rover]` section of `config.ini`.

