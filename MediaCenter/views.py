from django.shortcuts import render
from subprocess import Popen, PIPE
import eyed3
import os

# Since the player process's stdin is going to be written to by functions that are called independent of one another, they cannot be pure
# player_process will be passed between functions as a global variable 
player_process = None

class Song:

# Contains the important information about a particular song, what one would usually see in some sort of music player app, also contains
# url and path to file
# TODO find out how the hell to handle a file with actual underscores
    def __init__(self, filename, directory):
        self.filename = filename
        self.directory = directory
        self.url = '/MediaCenter/MusicLibrary/play/'+replace_all(filename, ' ','_')+'/'
        tags = eyed3.load(directory + filename).tag
        self.artist = tags.artist
        self.album = tags.album
        self.title = tags.title
        self.track_number = tags.track_num

def get_songs(path):
    # Get list of song objects from the /Media/music directory
    # Search directory for song files
    song_files = [files for dirpath, dirnames, files in os.walk(os.path.abspath(path))][0]
    # return song objects created from each file (excluding the logfiles created by omxplayer
    return [Song(filename, path) for filename in song_files if filename != 'omxplayer.log' and filename != 'omxplayer.old.log']

def replace_all(string, target, replacement):
    # Hackish, ugly way of finding all instances of 'target' in 'string' and replacing them with 'replacement'
    no_target = string.split(target)
    if len(no_target) > 1:
        new_string = ''
        l_nt=len(no_target)
        for substring_number in range(0,l_nt-1):
            new_string += no_target[substring_number]+replacement
        new_string += no_target[substring_number+1]
    else:
        new_string = string
    return new_string

def media_center(request):
    return render(request, 'MediaCenter.html', {})
    
def music_library(request):
    # Get better way to find path (using os)
    song_list = get_songs('/home/pi/piHomeServer/Media/music/')
    return render(request, 'MusicLibrary.html', {'song_list' : song_list})

def play_media(media_path):
    return Popen(["omxplayer", media_path], stdin=PIPE, stdout=PIPE)

def music_player(request, song):            
    action = None
    global player_process
    if not player_process:
        if '_' in song:
            formatted_song = replace_all(song, '_',' ')
        else:
            formatted_song = song
        player_process = play_media('/home/pi/piHomeServer/Media/music/'+formatted_song)
    else:
        if request.GET and 'action' in request.GET:
            action = request.GET['action']
            print('action %s' % action)
            if not action:
                action = False
            elif action == 'pause':
                player_process.stdin.write('p')
            elif action == 'play':
                player_process.stdin.write('p')
                action = None
            # entering the arrow keys in omxplayer's stdin causes the following actions
            elif action == 'stop':
                player_process.stdin.write('^[[A')
                player_process = None
                # Maybe just redirect the url
                return music_library(request)
            # What next, figure this out
            elif action == 'next':
                pass
            elif action == 'last':
                player_process.stdin.write('^[[B')
            elif action == 'fastforward':
                player_process.stdin.write('^[[C')
            elif action == 'rewind':
                player_process.stdin.write('^[[D')
            else:
                action == 'invalid'
        else:
            print('action not in url')
    return render(request, 'MusicPlayer.html', {'song':song, 'action':action})
