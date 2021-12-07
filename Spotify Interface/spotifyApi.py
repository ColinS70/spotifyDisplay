import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os
import time
import urllib.request
import shutil


def getCurrentSongData(sp):
	result = sp.current_user_playing_track()
	if(result == None):
		return(0)
	itemResult = result.get('item')
	albumResult = itemResult.get('album')
	outDict = {}


	#Artist data ------------------------------------
	#Get artist name
	artistResult = albumResult.get('artists')
	artistResult = artistResult[0]
	artistName = artistResult.get('name')
	outDict['artistName'] = artistName

	#Get artist popularity
	popularity = itemResult.get('popularity')
	outDict['trackPopularity'] = popularity
	#------------------------------------------------


	#Song data --------------------------------------
	songName = itemResult.get('name')
	outDict['songName'] = songName
	#------------------------------------------------


	#Song id ----------------------------------------
	extUrl = itemResult.get('external_urls')
	urlStr = extUrl.get('spotify')
	urlStr = urlStr.replace('https://open.spotify.com/track/','')
	outDict['songId'] = urlStr
	#------------------------------------------------


	#Album data -------------------------------------
	#Get album name
	albumName = albumResult.get('name')
	outDict['albumName'] = albumName

	#Get album release date
	albumReleaseDate = albumResult.get('release_date')
	outDict['albumReleaseDate'] = albumReleaseDate

	#Get album type
	albumType = albumResult.get('album_type')
	outDict['albumType'] = albumType

	#Get toal tracks
	totalTracks = albumResult.get('total_tracks')
	outDict['totalTracks'] = totalTracks
	#-------------------------------------------------

	#Get album cover image ---------------------------
	imageResult = albumResult.get('images')
	imageResult = imageResult[0]
	albumCover = imageResult.get('url')
	outDict['albumCover'] = albumCover
	#-------------------------------------------------

	return(outDict)


def getArtistData(sp,name):
	searchResult = sp.search(q='artist:' + name, type='artist')
	outDict = {}

	artistsResult = searchResult.get('artists')
	itemResult = artistsResult.get('items')
	itemResult = itemResult[0]

	artistPopularity = itemResult.get('popularity')
	outDict['artistPopularity'] = artistPopularity

	artistUrl = itemResult.get('uri')
	outDict['artistUri'] = artistUrl

	imageResult = itemResult.get('images')
	imageResult = imageResult[0]

	artistImage = imageResult.get('url')
	outDict['artistImage'] = artistImage
	return(outDict)

def downloadImage(url,fName):
	urllib.request.urlretrieve(url,str(fName))

def getAudioFeatures(sp,trackID):
	features = sp.audio_features(trackID)
	features = features[0]
	return(features)

def buildDataTesting():
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='359093842e6c4c24bf94099d1195b391',
													client_secret='0a2a8d2ea7da4916bd0a02f328043187',
													redirect_uri='http://localhost:8080',
													scope='user-read-currently-playing'))
	songData = getCurrentSongData(sp)
	if(songData == 0):
		print('No Song Is Playing')
		return(0)
	#artImage = getArtistData(sp,(songData.get('artistName')))
	#artImgUrl = artImage.get('artistImage')
	print(songData)

	#print(artImgUrl)
	#downloadImage(artImgUrl,'artistImg.jpg')

	#albCover = songData.get('albumCover')
	#downloadImage(albCover,'albumCover.jpg')

#buildDataTesting()

def getData(actType):
	#0 = currentSongData
	#1 = artistData
	#2 = audioFeatures
	#3 = download song cover
	#4 = download artist cover
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='359093842e6c4c24bf94099d1195b391',
													client_secret='0a2a8d2ea7da4916bd0a02f328043187',
													redirect_uri='http://localhost:8080',
													scope='user-read-currently-playing'))
	songData = getCurrentSongData(sp)
	if(songData == 0):
		#If no song playing
		return(0)

	artName = songData.get('artistName')
	artistData = getArtistData(sp,artName)


	if(actType == 0):
		return(songData)
	elif(actType == 1):
		return(artistData)
	elif(actType == 2):
		trackId = songData.get('songId')
		return(getAudioFeatures(sp,trackId))
	elif(actType == 3):
		shutil.rmtree('static/images')
		os.mkdir('static/images')
		songCover = songData.get('albumCover')
		songId = songData.get('songId')
		fName = 'static/images/' + songId + '.jpg'
		downloadImage(songCover,fName)
		return(fName)
	elif(actType == 4):
		artImg = artistData.get('artistImage')
		songId = songData.get('songId')
		fName = 'static/images/' + songId + 'alb' + '.jpg'
		downloadImage(artImg,fName)
		return(fName)