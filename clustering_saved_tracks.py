import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sklearn.cluster import KMeans

USER_ID="kb4i3142gp4ku5jbjs9d9j119"

def gettrackid(results, trackids):
    for idx, item in enumerate(results['items']):
        track = item['track']
        #print(idx, track['id'])
        trackids.append(track['id'])

scope = "user-library-read playlist-modify-private playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))



"""""""""""""""""""""""""""""""""""
get saved trackids and features
"""""""""""""""""""""""""""""""""""
features = []
for i in range(4):
    saved_tracks = []
    saved_tracks = sp.current_user_saved_tracks(limit=50, offset=i*50)
    saved_tracks_id = []
    gettrackid(saved_tracks, saved_tracks_id)

    features.extend(sp.audio_features(tracks=saved_tracks_id))

features_df = pd.DataFrame.from_dict(features)

# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# print(features_df)

features_set = features_df.loc[:, [
    'danceability', 
    'energy', 
    'key', 
    'loudness', 
    'speechiness', 
    'acousticness', 
    'instrumentalness', 
    'liveness', 
    'valence',  
    'tempo']]

pred = KMeans(n_clusters=4).fit_predict(features_set)
print(pred)
print(pred.size)



"""""""""""""""""""""""""""""""""""
print results
"""""""""""""""""""""""""""""""""""
features_df['group'] = pred

features_0 = features_df[features_df['group'] == 0]['id']
features_1 = features_df[features_df['group'] == 1]['id']
features_2 = features_df[features_df['group'] == 2]['id']
features_3 = features_df[features_df['group'] == 3]['id']

sp.user_playlist_create(user=USER_ID, 
                        name="4", 
                        description="created by spotipy")
sp.user_playlist_create(user=USER_ID,
                        name="3",
                        description="created by spotipy"
                        )
sp.user_playlist_create(user=USER_ID, 
                        name="2", 
                        description="created by spotipy")
sp.user_playlist_create(user=USER_ID,
                        name="1",
                        description="created by spotipy"
                        )
playlists = sp.user_playlists(user=USER_ID)
pid0 = list(playlists['items'])[0]['id']
pid1 = list(playlists['items'])[1]['id']
pid2 = list(playlists['items'])[2]['id']
pid3 = list(playlists['items'])[3]['id']

sp.user_playlist_add_tracks(user=USER_ID, playlist_id=pid0, tracks=features_0)
sp.user_playlist_add_tracks(user=USER_ID, playlist_id=pid1, tracks=features_1)
sp.user_playlist_add_tracks(user=USER_ID, playlist_id=pid2, tracks=features_2)
sp.user_playlist_add_tracks(user=USER_ID, playlist_id=pid3, tracks=features_3)

