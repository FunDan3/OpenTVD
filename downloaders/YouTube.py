import pytube

def check_url(url):
	try:
		pytube.YouTube(url)
		return True
	except Exception:
		return False
