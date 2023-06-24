
def parseHWIDfromlink(link):
    return link.replace("https://flux.li/windows/start.php?HWID=","")

def parseHWIDfromandroidlink(link):
    return link.replace("https://fluxteam.net/android/checkpoint/start.php?HWID=","")