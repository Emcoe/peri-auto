import wget, os, subprocess
try:
	os.remove("periscope-automatordownload.wget")
except FileNotFoundError:
	print('No periscope-automatordownload.wget to delete, moving on...')

try:
	with open('prefs.txt') as f:
		targetURL = f.readline().strip()
	wget.download(targetURL, "periscope-automatordownload.wget")
except FileNotFoundError:
	print("prefs.txt created, change the first line to the URL of the Periscoper you're trying to download from. Below the first line, paste in URLS of any broadcasts you've already seen, and don't want to download!")
	with open('prefs.txt', 'a') as f:
		f.write("https://www.periscope.tv/ABC/\n")

with open('periscope-automatordownload.wget', 'r') as veryrawsource:
	rawsource = veryrawsource.read().replace('\n', '')

startpos = 117 + rawsource.find(",&quot;UserBroadcastHistoryCache&quot;:{&quot;histories&quot;:{&quot;11880259&quot;:{&quot;broadcastIds&quot;:[")
segment = rawsource[startpos:]
endpos = segment.find("]") - 6
segment = segment[:endpos]

results = segment.split('&quot;,&quot;')

print('')
print('Prospects found:',len(results))

golist = []
entry = ""

with open('prefs.txt', 'r') as veryrawsource:
	rawsource = veryrawsource.read().replace('\n', '')

for entry in results:
	if rawsource.find(str(entry)) is -1:
		cleanup = "https://www.pscp.tv/w/" + entry
		golist.append(cleanup)

print('Prospects that are new:',len(golist))

if len(golist) > 0:
	open('\\\\\\\\\todolist.txt', 'w').close()
		for entry in golist:
		with open('\\\\\\\\\todolist.txt', 'a') as final:
			final.write('\n'+entry)
	with open('\\\\\\\\\completedlist.txt', 'a') as final:
		final.write('\n')	
	for entry in golist:
		with open('\\\\\\\\\completedlist.txt', 'a') as final:
			final.write('\n'+entry)
	with open('\\\\\\\\\completedlistbackup.txt', 'a') as final: ##Backup list part 1
			final.write('\n')
	for entry in golist:  ##Backup list part 2
		with open('\\\\\\\\\completedlistbackup.txt', 'a') as final:
			final.write('\n'+entry)
	print('Lists written')
	subprocess.call(["youtube-dl","-o","\\\\\\\\\targetdirectory/%(upload_date)s-%(title)s-%(id)s.%(ext)s","-x","--audio-format","m4a","--audio-quality","64K","--batch-file","\\\\\\\\\todolist.txt"])
	print('Success!')
else:
	print('No new prospects, ending.')