import wget, os, subprocess
try:
	os.remove("peri-auto.wget")
except FileNotFoundError:
	pass

try:
	with open('prefs.txt') as f:
		targetURL = f.readline().strip()
	wget.download(targetURL, "peri-auto.wget")


	with open('peri-auto.wget', 'r') as veryrawsource:
		rawsource = veryrawsource.read().replace('\n', '')
	startpos = 33 + rawsource.find("{&quot;broadcastIds&quot;:[&quot;")
	segment = rawsource[startpos:]
	endpos = segment.find("]") - 6
	segment = segment[:endpos]
	results = segment.split('&quot;,&quot;')

	print('')
	print('Broadcasts found on',targetURL,":",len(results))
	
	golist = []
	entry = ""
	
	with open('prefs.txt', 'r') as veryrawsource:
		rawsource = veryrawsource.read().replace('\n', '')
	for entry in results:
		if rawsource.find(str(entry)) is -1:
			cleanup = "https://www.pscp.tv/w/" + entry
			golist.append(cleanup)
	print('Broadcasts not already in prefs.txt:',len(golist))

	if len(golist) > 0:
		open('todolist.txt', 'w').close()
		for entry in golist:
			with open('todolist.txt', 'a') as final:
				final.write('\n'+entry)
		print('List written')

		subprocess.call(["youtube-dl","-o","%(upload_date)s-%(title)s-%(id)s.%(ext)s","-x","--audio-format","m4a","--audio-quality","64K","--batch-file","todolist.txt"])

		with open('prefs.txt', 'a') as final:
			final.write('\n')
		for entry in golist:
			with open('prefs.txt', 'a') as final:
				final.write('\n'+entry)
		with open('backuplistofseenURLs.txt', 'a') as final:
			final.write('\n')
		for entry in golist:
			with open('backuplistofseenURLs.txt', 'a') as final:
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

	else:
		print('No new prospects, ending.')

except FileNotFoundError:
	print("prefs.txt created, change the first line to the URL of the Periscoper you're trying to download from. Below the first line, paste in URLs of any broadcasts you've already seen, and don't want to download!")
	with open('prefs.txt', 'a') as f:
		f.write("https://www.periscope.tv/ABC/\n-----Above this line is the Periscoper's URL you want to download, and below are any broadcasts you've already seen-----\n")