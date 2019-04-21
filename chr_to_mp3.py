#to use the following functions,you should input 'pip3 install baidu-aip' at the terminal

from aip import AipSpeech
import os
""" 你的 APPID AK SK """
APP_ID = '16007034'
API_KEY = '9cVZDkCrl0sZP3wpQlMeqZq2'
SECRET_KEY = 'lGTYdBrcomGUAgfPCt2jrYO9Rg68IMAB'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
def change_to_mp3(content='请输入要转换的文字内容，这是默认测试内容',turn=1,mp3_name='17k'):
    result  = client.synthesis(content, 'zh', 1, {
        'vol': 5,'per':0
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('auido.mp3', 'wb') as f:
            f.write(result)
        if turn:
            os.system("gnome-terminal -e 'ffmpeg -y  -i auido.mp3  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s.pcm '"%(mp3_name))

    
