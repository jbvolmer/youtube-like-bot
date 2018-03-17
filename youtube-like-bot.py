#! /usr/local/bin/python3
# infinite chill / 2017

# This sample shows how to rate a list of videos with a list of clients
# this is a proof of concept code and has not been tested

# Sample usage:
#	make
#   ./youtube-like-bot.py --videoFile=/path/to/video_list.json --clientSecrets=/path/to/client_secrets

import argparse
import os
import re
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import glob
import sys
import urllib

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
RATINGS = ('like', 'dislike', 'none')


# Parse a videos id from the URL
def get_video_id(video_url):
		query = urllib.parse(video_url)
		if query.hostname == 'youtu.be':
				return query.path[1:]
		if query.hostname in ('www.youtube.com', 'youtube.com'):
				if query.path == '/watch':
						p = parse_qs(query.query)
						return p['v'][0]
				if query.path[:7] == '/embed/':
						return query.path.split('/')[2]
				if query.path[:3] == '/v/':
						return query.path.split('/')[2]
		return None

# Authorize the request and store authorization credentials.
def get_authenticated_service(client_secret_file):
	flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
	credentials = flow.run_console()
	return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

# Add the video rating. This code sets the rating to 'like,' but you could
# also support an additional option that supports values of 'like' and
# 'dislike.'
def like_video(youtube, video_id, mode='like'):
	youtube.videos().rate(
		id=video_id,
		rating=mode
	).execute()

# Main driver function
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--videoFile', default='video_list.json',
		help='Path to json file with a list of videos.')
	parser.add_argument('--clientSecrets', default='video_list.json',
		help='Path to directory full of client secret files.')
	parser.add_argument('--rating', default='like',
		choices=RATINGS,
		help='Indicates whether the rating is "like", "dislike", or "none".')
	args = parser.parse_args()

	# get videos list
	video_ids=[]
	try:
		video_url_file=open(args.videoFile,'r')
		for video in video_url_file:
			video_id=get_video_id(video)
			print(video)
			print(video_id)
			video_ids.append(video_id)
			video_url_file.close()
	except Exception as ex:
		print(ex)
		sys.exit(0)

	# for each client secret file found
	all_client_secrets=glob.glob(os.path.join(args.clientSecrets,"*.json"))
	for client_secret_file in all_client_secrets:
		# connect to youtube
		try:
			youtube = get_authenticated_service(client_secret_file)
		except Exception as ex:
			print(ex)
			sys.exit(0)
		# like each video in list
		for video in video_ids:
			try:
				like_video(youtube, video, args.rating)
			except Exception as ex:
				print(ex)
				sys.exit(0)
			else:
				print('%s has been added for video %s using client %s' % (args.rating, video, client_secret_file))

