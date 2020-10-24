#coding:utf-8
import time
import os
import sys
import json
import urllib
import urllib.request
import re
import shutil

#设置UA，防止屏蔽
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; rv:60.0) Gecko/20100101 Firefox/60.0')]
urllib.request.install_opener(opener)

try:
    url = "https://www.youtube.com/c/%E3%82%86%E3%81%82%E3%81%A1%E3%82%83%E3%82%93%E3%81%AD%E3%82%8B0825/videos"
    html = urllib.request.urlopen(url,timeout=5).read().decode('utf-8')
    infore = re.compile(r'window\["ytInitialData"\] = *(.+?});',re.DOTALL)
    matchObj = infore.findall(html)
    if len(matchObj) == 0:
        print("not found video")
        exit(-1)
    infoAll = json.loads(matchObj[0])
    vlist = infoAll['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['gridRenderer']['items']
    for v in vlist:
        print("=============select one video===============")
        try:
            v = v['gridVideoRenderer']
            print("published "+v['publishedTimeText']['simpleText'])
            if "hours ago" in v['publishedTimeText']['simpleText'] or "minutes ago" in v['publishedTimeText']['simpleText'] or "minute ago" in v['publishedTimeText']['simpleText']:
                print('=========================')
                print("https://www.youtube.com/watch?v="+v['videoId'])
                print(v['thumbnail']['thumbnails'][len(v['thumbnail']['thumbnails'])-1]['url'])
                print(v['title']['runs'][0]['text'])
                print(v['publishedTimeText']['simpleText'])
                print("=======start download==========")
                os.system("youtube-dl --cookies y/cookies.txt "+"https://www.youtube.com/watch?v="+v['videoId'])
                print("=======download end=========")
                filename = ""
                list_file = os.listdir("./")
                for i in range(0,len(list_file)):
                    path = os.path.join("./",list_file[i])
                    if os.path.isfile(path) and (path.endswith(".mp4") or path.endswith(".mkv")):
                        filename = path
                        break
                if filename == "":
                    print("file not found")
                    continue
                print("file found:"+filename+".   move it")
                shutil.move(filename,'./y/'+time.strftime("[%Y-%m-%d]", time.localtime())+filename[2:])
                filename = './y/'+time.strftime("[%Y-%m-%d]", time.localtime())+filename[2:]
                print("=========start upload video========")
                os.system('rclone copy "'+filename+'" remote:others/for_share/video/yua --log-level INFO')
                os.system('rclone copy "'+filename+'" home:hd/y2b --log-level INFO')
                os.remove(filename)
                print("===========upload cover===========")
                filename = filename+".jpg"
                urllib.request.urlretrieve(v['thumbnail']['thumbnails'][len(v['thumbnail']['thumbnails'])-1]['url'],filename)
                os.system('rclone copy "'+filename+'" remote:others/for_share/video/yua --log-level INFO')
                os.remove(filename)
                print("===========done===========")
        except Exception as e:
            print(e)

except Exception as e:
    print(e)
    exit(-1)


