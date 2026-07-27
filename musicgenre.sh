#!/bin/bash

if [ $# -lt 1 ]; then
        echo "One argument required, provide path to directory or to file"
	exit
elif [ $# -gt 1 ]; then
        echo "Too many arguments, only 1 is accepted"
        exit
else
	if [ -f "/home/docker/sounds/$1" ]; then
		file="/home/docker/sounds/$1"
		name=`awk -F "[/]" '{print $NF}' <<< $file`
		ffmpeg -loglevel quiet -i $file image.wav
		read genre prob <<< "$(python3 genreprediction.py image.wav)"
		echo "Predicted genre of $name is $genre with probability $prob"
		`rm image.wav`
	elif [ -d "/home/docker/sounds/$1" ]; then
		for i in /home/docker/sounds/"$1"/*; do
			file="$i"
			name=`awk -F "[/]" '{print $NF}' <<< $file`
			ffmpeg -loglevel quiet -i $file image.wav
			read genre prob <<< "$(python3 genreprediction.py image.wav)"
			echo "Predicted genre for $name is $genre with probability $prob"
			`rm image.wav`
		done
	else
		echo "Argument is not a valid path"
		exit
	fi
fi
