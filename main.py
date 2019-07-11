# issue: deal with the situation that a series do not have same amount of subtitle for each episode
# issue: check that whether the series have subtitle or not first
# issue: finish the comments and the alerts
# check the encode type before writing into srt
import urllib.request
import json



def main():
    multiRequest()

def getInput():
    '''
    处理输入内容，防止非法输入'''
    while True:
        try:
            aid = input('请输入av号')
            break
        except:
            print('非法输入')
    return aid

def singleRequest(aid, cid = None):
    '''单次请求
    '''
    if cid:
        response = urllib.request.urlopen(f"https://api.bilibili.com/x/web-interface/view?aid={aid}&cid={cid}")
        serial = response.read().decode('utf-8')
        data = json.loads(serial)['data']
        subtitle = {}
        for i in data['subtitle']['list']:
            subtitle[i['lan']] = i['subtitle_url']
        return subtitle
    else:
        response = urllib.request.urlopen(f"https://api.bilibili.com/x/web-interface/view?aid={aid}")
        serial = response.read().decode('utf-8')
        data = json.loads(serial)['data']
        return data['pages']

def subtitleRequest(url):
    response = urllib.request.urlopen(url)
    serial = response.read().decode('utf-8')
    data = json.loads(serial)
    return data    

def saveToSrt(data, lan, file_name):
    sub = data['body']
    count = 1
    for line in sub:
        print(line)
        from_ = parseTime(line['from'])
        to_ = parseTime(line['to'])
        content = line['content']
        with open(f'{file_name}-{lan}.srt', 'a+', newline='', encoding='utf-8') as f:
            f.write(f'{count}\n\n')
            f.write(f'{from_} -> {to_}\n\n')
            f.write(str(content))
            f.write('\n\n')
        count += 1
            
def parseTime(time):
    lst = str(time).split('.')
    hour = '00'
    minute = '00'
    second = '00'
    milisecond = '00'
    if len(lst) == 0:
        pass
    else:
        if int(lst[0]) > 60:
            minute = str(int(lst[0])//60)
            second = str(int(lst[0])%60)
            if int(minute) > 60:
                hour = str(int(minute)//60)
                minute = str(int(minute)%60)
        else:
            second = str(lst[0])

    string = hour+':'+minute+':'+second+','+milisecond
    return string

def multiRequest():
    '''
    多次请求，针对分p的情况'''
    aid = getInput()
    aid = 45936507
    pages = singleRequest(aid)
    names = {}
    subtitle = []
    for i in pages:
        names[i['page']] = i['part']
        subtitle.append(singleRequest(aid, i['cid']))
    for i in range(len(subtitle)):
        j = subtitle[i]
        for k in j.keys():
            data = subtitleRequest(j[k])
            print(names[i+1])
            saveToSrt(data, k, names[i+1])


lan = {'en-US': '英语（美国）', 'zh-Hans': '中文（简体）'}



if __name__ == "__main__":
    main()