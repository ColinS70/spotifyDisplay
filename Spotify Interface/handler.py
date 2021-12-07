#Song Image:
#Song Name
#    Song Popularity
#    Danceability
#    Energy

#    Album Name
#    Release Date
#    Total Tracks

#Artist Image:
#    Artist Name
#    Artist Popularity
#Layout for data on website


#Website will post ajax to backend
#backend will hang until song changes
#On change backend will render temp and send back
#The ajax will replace data then call itself
#Then process repeats

import spotifyApi


def handle():
	songData = spotifyApi.getData(0)
	artData = spotifyApi.getData(1)
	audioFeatures = spotifyApi.getData(2)
	if(songData == 0 or artData == 0 or audioFeatures == 0):
		print('Nothing playing')
		return(0,0,0,0,0,0,0,0,0,0,0)
	#Download images
	artImgLoc = spotifyApi.getData(3)
	covImgLoc = spotifyApi.getData(4)

	songName = songData.get('songName')
	songPop = songData.get('trackPopularity')
	dance = audioFeatures.get('danceability')
	energy = audioFeatures.get('energy')
	albName = songData.get('albumName')
	relDate = songData.get('albumReleaseDate')
	totalTracks = songData.get('totalTracks')

	artName = songData.get('artistName')
	artPopularity = artData.get('artistPopularity')

	return(songName,songPop,dance,energy,albName,relDate,totalTracks,artName,artPopularity,artImgLoc,covImgLoc)