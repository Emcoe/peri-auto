
import os
import subprocess
import wget
import youtube_dl

audiopath = ""
print('Peri-auto v1.1.5')


def print_lists():
    with open('prefs.txt', 'a') as final:
        final.write('\n')
    for entry in golist:
        with open('prefs.txt', 'a') as final:
            final.write('\n'+entry)
    with open("backuplistofseenURLs.txt", 'a') as final:
        final.write('\n')
    for entry in golist:
        with open("backuplistofseenURLs.txt", 'a') as final:
            final.write('\n'+entry)
    try:
        os.remove("peri-auto.wget")
    except FileNotFoundError:
        pass
    try:
        os.remove("todolist.txt")
    except FileNotFoundError:
        pass
    print('Success!')


def live_test(testURL):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
    live = False
    with ydl:
        liveresult = ydl.extract_info(
            testURL,
            download=False
            )
    if "hls" in liveresult['formats'][0]['format_id']:
        live = True
    return live


try:
    os.remove("peri-auto.wget")
except FileNotFoundError:
    pass

try:
    with open('prefs.txt') as f:
        targetURL = f.readline().strip()
        line2 = f.readline().strip()
        if line2[0:4] != "-----":
            audiopath = line2
    catchupflag = False
except FileNotFoundError:
    catchupflag = True
    newtarget = input("Welcome to peri-auto! Just for the first time, what is "
                      "the name username of the Periscoper you're following? "
                      "For 'https://www.periscope.tv/ABC/' you would type "
                      "'ABC' (without quotemarks): ")
# How to handle incorrect username input?
    targetURL = "https://www.periscope.tv/" + newtarget + "/"

wget.download(targetURL, "peri-auto.wget")

with open('peri-auto.wget',
          'r') as veryrawsource:
    rawsource = veryrawsource.read().replace('\n', '')
startpos = 33 + rawsource.find("{&quot;broadcastIds&quot;:[&quot;")
segment = rawsource[startpos:]
endpos = segment.find("]") - 6
segment = segment[:endpos]
results = segment.split('&quot;,&quot;')
resultsnum = len(results)

print('')

if live_test("https://www.pscp.tv/w/" + results[0]) is True:
    print("Skipping currently live broadcast")
    results = results[1:]

print('Archived broadcasts found on', targetURL, ":", resultsnum)

try:
    os.remove("peri-auto.wget")
except FileNotFoundError:
    pass


golist = []
entry = ""

if catchupflag is True:
    catchup = input("Peri-auto will get all new " + newtarget + " broadcasts "
                    "going forward, but since we're starting fresh, you can "
                    "choose to grab up to " + str(resultsnum) + " of their "
                    "previous broadcasts. How far back do you want to go? "
                    "Enter a number from 0-" + str(resultsnum) + ": ")
    while (int(catchup) > resultsnum) or (int(catchup) < 0):
        catchup = input("Please enter a number from 0-" + str(resultsnum)
                        + ": ")
    with open('prefs.txt',
              'a') as f:
        f.write("https://www.periscope.tv/" + newtarget + "/\n-----Above this "
                "line is the Periscoper's URL, and below are any broadcasts "
                "you've already seen-----\n")


with open('prefs.txt', 'r') \
        as veryrawsource:
    rawsource = veryrawsource.read().replace('\n', '')


for entry in results:
    if rawsource.find(str(entry)) is -1:
        golist.append("https://www.pscp.tv/w/" + entry)
if catchupflag is False:
    print('Broadcasts not already in prefs.txt:', len(golist))
else:
    golist = golist[:int(catchup)]

if len(golist) > 0:
    open('todolist.txt',
         'w').close()
    for entry in golist:
        with open("todolist.txt", 'a') as final:
            final.write('\n'+entry)

    if audiopath == "":
        importcommand = ["youtube-dl", "-x", "--audio-format",
                         "m4a", "--audio-quality", "64K", "--batch-file",
                         "todolist.txt"]
    else:
        importcommand = ["youtube-dl", "-o", audiopath, "-x",
                         "--audio-format", "m4a", "--audio-quality", "64K",
                         "--batch-file", "todolist.txt"]

    retries = 5
    count = 1
    while retries >= count:
        try:
            subprocess.check_call(importcommand)
            # print("Attempt", count, "succeeded, printing:")
            print_lists()
            # print("Attempt", count)
            break
        except subprocess.CalledProcessError:
            # print("Attempt", count, "failed")
            count += 1
