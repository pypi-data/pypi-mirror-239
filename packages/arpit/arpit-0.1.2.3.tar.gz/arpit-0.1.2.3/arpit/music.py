import sys, time, os 
from .utils import play_audio, path_convertor
import json

def load_animation(load_str, counttime): 
	load_str = "Loading my favourite song..."
	ls_len = len(load_str) 

	animation = "|/-\\"
	anicount = 0
	
	counttime = counttime
	i = 0					

	while (counttime != 50):
		time.sleep(0.075) 
							
		load_str_list = list(load_str) 
		
		x = ord(load_str_list[i]) 
		y = 0							

		if x != 32 and x != 46:			 
			if x>90: 
				y = x-32
			else: 
				y = x + 32
			load_str_list[i]= chr(y) 
		
		res =''			 
		for j in range(ls_len): 
			res = res + load_str_list[j] 
			
		sys.stdout.write("\r"+res + animation[anicount]) 
		sys.stdout.flush() 

		load_str = res 

		anicount = (anicount + 1)% 4
		i =(i + 1)% ls_len 
		counttime = counttime + 1
    
	if os.name =="nt":
		os.system("cls")

def get_music_data():
    with open(path_convertor('assets/data.json')) as json_file:
        data = json.load(json_file)
        
    return data["music"]["name"], data["music"]["artist"]


def main():
    name, artist = get_music_data()

    load_animation(load_str="Loading my favourite song...", counttime=50)
    
    sys.stdout.write(f"\n\nPlaying {name} by {artist}\n") 
    play_audio('assets/sunday.mp3')