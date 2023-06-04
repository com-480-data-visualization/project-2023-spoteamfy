"""
    Preprocessing of the data from the Million Playlist Dataset (MPD) to extract the playlists and the tracks they contain.

    usage:
        First you need to download the dataset from https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge/dataset_files
        Then you need to unzip the file and put the folder "mpd.slice.*" in the folder "data" in the same directory as this file.
        python3 preprocessing.py ../data 0
        python3 preprocessing.py ../data 1
        python3 preprocessing.py ../data 2

"""
import sys
import json
import re
import collections
import os
import numpy as np
import pandas as pd

data = []

def process_mpd(path, nb_slice, count_max=333):
    count = 0
    filenames = os.listdir(path)

    #Select only the files we want to process
    if nb_slice == 2 :
        filenames = filenames[nb_slice*count_max:]
    else : 
        filenames = filenames[nb_slice*count_max:((nb_slice+1)*count_max) - 1]
    
    #For each file in the directory
    for filename in sorted(filenames):
        print(count, '/', len(filenames))

        #List which contains data for the processed file
        if filename.startswith("mpd.slice.") and filename.endswith(".json"):

            #Read file
            fullpath = os.sep.join((path, filename))
            f = open(fullpath)
            js = f.read()
            f.close()
            mpd_slice = json.loads(js)

            #Preprocess each playlist in the file
            for playlist in mpd_slice["playlists"]:
                process_playlist(playlist)

            count += 1

    print(count, "files processed")
    
    #Save the data in a csv file
    data_numpy = np.array(data)
    data_df = pd.DataFrame(data_numpy, columns = ['id_playlist', 'name_playlist', 'id_track', 'name_track'])
    data_df.to_csv('playlist_'+str(nb_slice+1)+'.csv', index=False)

    print("File saved")

def process_playlist(playlist):
    
    #Retrieve id and name of the playlist
    id_playlist, name_playlist = playlist["pid"], playlist["name"]
    print("Processing playlist: ", id_playlist, name_playlist)

    for track in playlist["tracks"]:
        id_track, name_track = track["track_uri"], track["track_name"]
        data.append([id_playlist, name_playlist, id_track, name_track])

if __name__ == "__main__":
    quick = False
    path = sys.argv[1]
    nb_slice = int(sys.argv[2])
    process_mpd(path, nb_slice)
