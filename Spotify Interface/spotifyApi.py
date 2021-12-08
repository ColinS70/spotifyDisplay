import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os
import time
import urllib.request
import shutil
#Import librarys


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
#This just takes the response from getting infromation about the users current song and takes the needed portions, adds the to a dict, and returns them 


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
#This is just getting information about the artists, getting the useful information and returning it. 

def downloadImage(url,fName):
	urllib.request.urlretrieve(url,str(fName))
#Small function to download images

def getAudioFeatures(sp,trackID):
	features = sp.audio_features(trackID)
	features = features[0]
	return(features)
#Get audio features

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




lastSong = ''
def getData(actType):
	global lastSong
	#0 = currentSongData = artistData = audioFeatures = download song cover = download artist cover
	#1 = is a song playing?
	#2 = should I update?
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='359093842e6c4c24bf94099d1195b391',
													client_secret='0a2a8d2ea7da4916bd0a02f328043187',
													redirect_uri='http://localhost:8080',
													scope='user-read-currently-playing'))
	#Define credentials for the spotify dev app, (you need spoityf premium to access endpoints)
	
	if(actType == 0):
		songData = getCurrentSongData(sp)
		artistData = getArtistData(sp,(songData.get('artistName')))
		audioFeatures = getAudioFeatures(sp,(songData.get('songId')))
		songId = songData.get('songId')
		songCoverImage = songData.get('albumCover')
		artistCoverImage = artistData.get('artistImage')
		songImageUrl = 'static/images/' + songId + '.jpg'
		artistImageUrl = 'static/images/' + songId + 'alb' + '.jpg'
		#Get all needed data


		shutil.rmtree('static/images')
		os.mkdir('static/images')
		downloadImage(songCoverImage,songImageUrl)
		downloadImage(artistCoverImage,artistImageUrl)
		outDict = {}
		songName = songData.get('songName')
		songPop = songData.get('trackPopularity')
		dance = audioFeatures.get('danceability')
		energy = audioFeatures.get('energy')
		albName = songData.get('albumName')
		relDate = songData.get('albumReleaseDate')
		totalTracks = songData.get('totalTracks')
		artName = songData.get('artistName')
		artPopularity = artistData.get('artistPopularity')
		artImgLoc = songImageUrl
		covImgLoc = artistImageUrl
		outDict = {'songName':songName,'songPop':songPop,'dance':dance,'energy':energy,'albName':albName,'relDate':relDate,'totalTracks':totalTracks,'artName':artName,'artPopularity':artPopularity,'artImgLoc':artImgLoc,'covImgLoc':covImgLoc}
		return(outDict)
		#Download the new images and delete old ones, then assemble a dictionary will only data that is used in website and return it

	elif(actType == 1):
		songData = getCurrentSongData(sp)
		if(songData == 0):
			return(0)
		else:
			return(1)
	#Just check if a song is playing
	elif(actType == 2):
		songData = getCurrentSongData(sp)
		songName = songData.get('songName')
		if(songName != lastSong):
			lastSong = songName
			return(0)
		else:
			return(1)
	#Check if the song is diffenrt than the last time you checked, this is used to determine when website needs to update