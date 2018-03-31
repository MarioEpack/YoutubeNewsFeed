# -*- coding: utf-8 -*-

import os, sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
PART = 'contentDetails'
VIDEO_URL = 'https://www.youtube.com/watch?v='
MAX_RESULTS = 10
CHANNEL_ID = 'UCQn1FqrR2OCjSe6Nl4GlVHw'


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


# always just specify the channel_id to get the feed
def channels_list_by_id(client, **kwargs):
    response = client.channels().list(
        **kwargs
    ).execute()
    return response


def get_upload_id_from_channel_response(response):
    return response.get("items")[0].get("contentDetails").get("relatedPlaylists").get("uploads")


def get_titles_from_playlist_items_response(response):
    return response.get("items")[0].get(u'snippet').get(u'title')


def get_video_ids_from_playlist_items_response(response):
    return response.get("items")[0].get(u'snippet').get(u'resourceId').get(u'videoId')


def playlist_items_list_by_playlist_id(client, **kwargs):
    response = client.playlistItems().list(
        **kwargs
    ).execute()
    return response


if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    client = get_authenticated_service()
    # channel request
    channel_response = channels_list_by_id(client, id=CHANNEL_ID, part=PART)  # Raon Lee Singer
    uploads_id = get_upload_id_from_channel_response(channel_response)
    # playlist_items request
    playlist_items_response = playlist_items_list_by_playlist_id(client, part='snippet',maxResults=MAX_RESULTS, playlistId=uploads_id)
    video_title = get_titles_from_playlist_items_response(playlist_items_response)
    video_id = get_video_ids_from_playlist_items_response(playlist_items_response)
    print video_title, VIDEO_URL + video_id


