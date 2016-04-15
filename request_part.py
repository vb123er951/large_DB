import requests
from bs4 import BeautifulSoup

# get information from website
req = requests.get('http://e-iot.iot.gov.tw/EIot/ajax/TEvent/nFreewaySpeed.aspx?Freeway=N5')
soup = BeautifulSoup(req.text, 'html.parser')
from_to = soup.find_all("td", {"class" : "content_6"})
#print (from_to[1].text)
speed = soup.find_all("font")

# save in data structure
N_start = []
N_final = []
N_speed = []
S_start = []
S_final = []
S_speed = []
total = []
result = []
num = 7

for n in range(29):
    if n<14:
        if n%2 == 0:
            N_start.append(from_to[n+1].text)
        else:
            N_final.append(from_to[n+1].text)
    # n == 14 skip
    if n>14:
        if n%2 == 1:
            S_start.append(from_to[n+1].text)
        else:
            S_final.append(from_to[n+1].text)
for m in range(16):
    if m%8 == 0:
        continue
    if m<8:
        N_speed.append(speed[m].text.strip())
    else:
        S_speed.append(speed[m].text.strip())
for n in range(7):
    s = "北上 "+N_start[n]+" "+N_final[n]+" "+N_speed[n]
    total.append(s)
for n in range(7):
    s = "南下 "+S_start[n]+" "+S_final[n]+" "+S_speed[n]
    total.append(s)
#print (total)

# reading from file a.txt, each 5 mins
fr = open('a.txt', 'r', encoding = 'UTF-8')
i = 0
Ncount = 0;
Scount = 0;
# if speed doesn't change and <= 40 means 擁塞, post up
# if not, means 順暢
while True:
    line = fr.readline()
    if not line: break
    if i < 7:
        if line[:len(line)-1] == N_speed[i]:
            if int(N_speed[i]) <= 40:
                Ncount += 1
                payload = {'robot_id': '108143422899450', 'content': total[i], 'lng': '120', 'lat': '23'}
                req = requests.post("http://52.192.20.250/chat/create/robot/", data=payload)
                print (req.status_code)
    if i >= 7 & i < 14:
        if line[:len(line)-1] == S_speed[i-7]:
            if int(S_speed[i-7]) <= 40:
                Scount += 1
                payload = {'robot_id': '108143422899450', 'content': total[i], 'lng': '120', 'lat': '23'}
                req = requests.post("http://52.192.20.250/chat/create/robot/", data=payload)
                print (req.status_code)
    i += 1
if Ncount == 0 & Scount == 0:
    payload = {'robot_id': '108143422899450', 'content': '全線順暢', 'lng': '120', 'lat': '23'}
    req = requests.post("http://52.192.20.250/chat/create/robot/", data=payload)
    print (req.status_code)
else:
    Ncount = 0
    Scount = 0
    payload = {'robot_id': '108143422899450', 'content': '其他順暢', 'lng': '120', 'lat': '23'}
    req = requests.post("http://52.192.20.250/chat/create/robot/", data=payload)
    print (req.status_code)
fr.close()

# post
#for i in range(7):
#    payload = {'robot_id': '108143422899450', 'content': total[i], 'lng': '120', 'lat': '23'}
#    req = requests.post("http://52.192.20.250/chat/create/robot/", data=payload)
#    print (req.status_code)

# writing in file a.txt
fw = open('a.txt', 'w', encoding = 'UTF-8')
for i in range(7):
    fw.write(N_speed[i]+"\n")
for i in range(7):
    fw.write(S_speed[i]+"\n")
fw.close()
