# issue: deal with the situation that a series do not have same amount of subtitle for each episode
# issue: check that whether the series have subtitle or not first
# issue: finish the comments and the alerts
# check the encode type before writing into srt
import urllib.request
import json
import os


class SubRequest:
    def __init__(self, aid):
        self.multiRequest(aid)
        self.aid = aid

    def __str__(self):
        with open(f'data/{self.aid}/content.txt') as f:
            return str(f.readlines())

    def singleRequest(self, aid, cid = None):
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
            data = json.loads(serial)
            if data['code'] != 0:
                return []
            return data['data']['pages']

    def subtitleRequest(self, url):
        response = urllib.request.urlopen(url)
        serial = response.read().decode('utf-8')
        data = json.loads(serial)
        return data

    def saveToSrt(self, data, lan, file_name, aid):
        sub = data['body']
        count = 1
        with open(f'data/{aid}/{file_name}-{lan}.srt', 'w') as f:
            pass
        for line in sub:
            from_ = self.parseTime(line['from'])
            to_ = self.parseTime(line['to'])
            content = line['content']
            with open(f'data/{aid}/{file_name}-{lan}.srt', 'a+', newline='', encoding='utf-8') as f:
                f.write(f'{count}\n\n')
                f.write(f'{from_} -> {to_}\n\n')
                f.write(str(content))
                f.write('\n\n')
            count += 1
        print(f"{file_name}-{lan}.srt successfully written")
        with open(f'data/{aid}/content.txt', 'a+', newline='') as f:
            f.write(f'{file_name}-{lan}.srt\n')
                
    def parseTime(self, time):
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

    def multiRequest(self, aid):
        '''
        多次请求，针对分p的情况'''
        pages = self.singleRequest(aid)
        names = {}
        subtitle = []
        for i in pages:
            names[i['page']] = i['part'].replace(' ', '_')
            subtitle.append(self.singleRequest(aid, i['cid']))
        mkdir(f'data/{aid}')
        with open(f'data/{aid}/content.txt', 'w') as f:
            pass
        for i in range(len(subtitle)):
            j = subtitle[i]
            for k in j.keys():
                data = self.subtitleRequest(j[k])
                print(names[i+1])
                self.saveToSrt(data, k, names[i+1], aid)
    

def mkdir(path):
    current = str(os.path.abspath('.'))
    isexists = os.path.exists(current+'/'+path)
    if isexists:
        print('Folder exists')
    else:
        os.mkdir(current+'/'+path)
        print('Folder create successfully')

if __name__ == "__main__":
    print(SubRequest(45936507))