#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 14:26:42 2020

@author: davidmateos
"""
import spotipy
import spotipy.util as util

username= '' #your user id
scope = 'user-top-read'
token = util.prompt_for_user_token(username, scope)

new_artist_ids = []
my_top_artists = []
new_music_artists = []

if token:
    
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    response = sp.new_releases()
    
    while response:
    
        albums = response['albums']
        for i, item in enumerate(albums['items']):
            for j, artist in enumerate(item['artists']):
                new_artist_ids.append(artist['name'])

        if albums['next']:
            response = sp.next(albums)
        else:
            response = None 
    
    
    ranges = ['short_term', 'medium_term', 'long_term']
    for range in ranges:
        
        results = sp.current_user_top_artists(time_range=range, limit=50)
        for i, item in enumerate(results['items']):
            my_top_artists.append(item['name'])
    
    
    seen = set()  # only keep a unique list of artists
    for artist in my_top_artists:
        name = artist
    
        if name not in seen:
            seen.add(name)      
        
    my_top_artists = seen
    
    # find the overlap between new release artists and my top artists
    new_music_artists = [value for value in new_artist_ids if value in my_top_artists]
    
    # in case you're not lucky this week
    if len(new_music_artists) == 0:
        new_music_artists.append("Your top Artists have not released new music this week")

else:
    print("Can't get token for", username)
    
print(new_music_artists)

