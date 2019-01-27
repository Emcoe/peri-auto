
import os
import subprocess
import wget

try:
    os.remove("peri-auto.wget")
except FileNotFoundError:
    pass

try:
    with open('prefs.txt') as f:
        targetURL = f.readline().strip()
    catchupflag = False
except FileNotFoundError:
    catchupflag = True
    newtarget = input("Welcome to peri-auto! Just for the first time, what is "
                      "the name username of the Periscoper you're following? "
                      "For 'https://www.periscope.tv/ABC/' you would type "
                      "'ABC' (without quotemarks): ")
# How to handle incorrect username input?
    targetURL = "https://www.periscope.tv/" + newtarget + "/"

wget.download(targetURL,
              "peri-auto.wget")

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
print('Broadcasts found on', targetURL, ":", resultsnum)

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
    with open('prefs.txt', 'a') as f:
        f.write("https://www.periscope.tv/" + newtarget + "/\n-----Above this "
                "line is the Periscoper's URL, and below are any broadcasts "
                "you've already seen-----\n")

with open('prefs.txt', 'r') as veryrawsource:
    rawsource = veryrawsource.read().replace('\n', '')

if catchupflag is False:
    for entry in results:
        if rawsource.find(str(entry)) is -1:
            cleanup = "https://www.pscp.tv/w/" + entry
            golist.append(cleanup)
    print('Broadcasts not already in prefs.txt:', len(golist))
else:
    for entry in results:
        if rawsource.find(str(entry)) is -1:
            cleanup = "https://www.pscp.tv/w/" + entry
            golist.append(cleanup)
        golist = golist[:int(catchup)]

if len(golist) > 0:
    open('todolist.txt', 'w').close()
    for entry in golist:
        with open("todolist.txt", 'a') as final:
            final.write('\n'+entry)

    subprocess.call(["youtube-dl", "-o",
                     "%(upload_date)s-%(title)s-%(id)s.%(ext)s",
                     "-x", "--audio-format", "m4a", "--audio-quality",
                     "64K", "--batch-file", "todolist.txt"])

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
