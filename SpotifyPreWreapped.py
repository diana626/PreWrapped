import json
import sys
import os.path
import datetime

import numpy as np

class songInd:
    def __init__(self,artistName,trackName):
        self.artistName=artistName
        self.trackName = trackName
    def __eq__(self,other):
        result = (self.artistName == other.artistName and self.trackName == other.trackName)
        return result
class song:
    def __init__(self,endTime,artistName,trackName):
        self.endTime = endTime
        self.artistName = artistName
        self.trackName = trackName
        self.song = songInd(artistName,trackName)

year = datetime.date.today().year
trackHis = []
songList = []
minDate=datetime.date(datetime.MAXYEAR,1,1)
maxDate=datetime.date(datetime.MINYEAR,1,1)

#Important: change this to the directory where you've downloaded your spotify data to
fileLocation = "C:/Users/diana/OneDrive/Documents/Spotify data/New folder/my_spotify_data/MyData/"
fileNum=0
fileName = fileLocation+"StreamingHistory"+str(fileNum)+".json"
while os.path.exists(fileName):
    #add all the songs to an excel sheet
    i=0
    with open(fileName,encoding='utf-8') as json_file:
        data = json.load(json_file)    
        while i < len(data):
            if(data[i]['msPlayed'] >= 30000): #ignore any song that was listened to less than 30 seconds
                time = datetime.date.fromisoformat(data[i]['endTime'].split(" ")[0])
                track = data[i]['trackName']
                artist = data[i]['artistName']
                if(track != "Unknown Track" and artist != "Unknown Artist" and time.year==year): #these are local files that will not count towards your spotify wrapped
                    currSong = song(time,artist,track)
                    songList.append(currSong)
                    if(not trackHis.__contains__(currSong.song)):
                        trackHis.append(currSong.song)
                    minDate = min(minDate,time)
                    maxDate = max(maxDate,time)
            i += 1
    fileNum += 1
    fileName = fileLocation+"StreamingHistory"+str(fileNum)+".json"
#songList now contains all of the songs you listened to in the past year
currYear = datetime.datetime.now().year
#count the number of times you listened to each song
atw = 0
delta = maxDate-minDate
l = len(trackHis)
songMat = np.zeros((delta.days+1,l))
for sng in songList:
    d = sng.endTime - minDate
    ind = trackHis.index(sng.song)
    songMat[d.days,ind] = songMat[d.days,ind]+1
cumSong = np.cumsum(songMat,axis=0)
#make a line of the cumulative times you listened to a song
#estimate where that line will end up at the end of the year
#the highest line will be your max song
#find the number of days left in the year
#find the average number of times you listened to each song in a day
#multiply that by the remaining days left
#find the song that's that max of each song you listen to
#array with the days you listened to each song:
daysListen = np.where(cumSong==0,cumSong,1)
#array with the total number of days since you first listened to this song:
totalDaysListened = np.sum(daysListen,axis=0)
daysLeft = datetime.date.fromisoformat(str(year)+"-10-31")-maxDate #spotify wrapped only counts until October 31 
#need to estimate the average times you listen in a day
#TotalTimesListen/TotalDaysListened
totalTimesListened = cumSong[-1]
#TotalTimesListen is the final row in cumSong
avgTimesListen = totalTimesListened/totalDaysListened
daysLeftToListen = avgTimesListen*daysLeft.days
finalCount = totalTimesListened+daysLeftToListen
maxIndex = np.argmax(finalCount)
maxSong = trackHis[maxIndex]
print("Estimated top track: ")
print("Title: " + maxSong.trackName)
print("Artist: " + maxSong.artistName)

mostSong = np.argmax(totalTimesListened)
print("Song most listened to: ")
print("Title: " + trackHis[mostSong].trackName)
print("Artist: " + trackHis[mostSong].artistName)