page = "?vl[page]={}&mid=SubmissionsList"
skins = "https://gamebanana.com/skins/games/297"
sounds = "https://gamebanana.com/sounds/games/297"
sprays = "https://gamebanana.com/sprays/games/297"
effects = "https://gamebanana.com/effects/games/297"
count = 100

from tqdm import tqdm
import requests
from random import randint
from bs4 import BeautifulSoup
from pyunpack import Archive

cSkins = int(count*0.4)
cSounds = int(count*0.3)
cEffects = int(count*0.2)
count -= cSkins
count -= cSounds
count -= cEffects
cSprays = count

print("Downloading", cSkins, "Weapon Skins")
print("Downloading", cSounds, "Sounds")
print("Downloading", cEffects, "Effects")
print("Downloading", cSprays, "Sprays")

def downloadQuota(count, url):
	quota = count
	while quota > 0:
		html = requests.get(url + page.format(randint(1,400))).text
		soup = BeautifulSoup(html, "html.parser")
		try:
			for mod in soup.select("records > record"):
				modPage = mod.select("a.Name")[0].get("href")
				modPage = requests.get(modPage).text
				soup = BeautifulSoup(modPage, "html.parser")
				modFileName = soup.select("div.FileInfo > span > code")[0].string
				modPage = soup.select(".SmallManualDownloadIcon")[0].parent.get("href")
				modPage = requests.get(modPage).text
				soup = BeautifulSoup(modPage, "html.parser")
				download = soup.select(".SmallManualDownloadIcon")[0].parent.get("href")
				print("downloading", modFileName, "with url", download)
				filename = "./custom/TF2AutoMod/"+modFileName
				# NOTE the stream=True parameter below
				with requests.get(download, stream=True) as r:
					r.raise_for_status()
					with open(filename, 'wb') as f:
						for chunk in tqdm(r.iter_content(chunk_size=1024), unit="KB", desc=filename): 
							if chunk: # filter out keep-alive new chunks
								f.write(chunk)
				if modFileName.endswith(".zip") or modFileName.endswith(".rar"):
					Archive(filename).extractall('../')
				quota -= 1
		except Exception as e:
			print(e)

downloadQuota(cSkins, skins)
downloadQuota(cSounds, sounds)
downloadQuota(cEffects, effects)
downloadQuota(cSprays, sprays)

