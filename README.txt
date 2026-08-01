The purpose of the image is to predict the music genre of a song, using a ML model trained with tensorflow. It can predict both a single sound file, or a 

The code to build the image is: docker build -f exam.image -t genre-prediction:default .

The image has been built starting from python:3.12 and by installing ffmpeg using apt-get commands, together with update, upgrade, autoclean and autoremove. Then I used phyton3 pip install to iclude in the image the packages for tensorflow-cpu, torch-2.11.0, torchaudio.2.11.0, torchcoded-0.12.0 and numpy. The versions of the packages have been chosen in order for them to be compatible to one another, otherwise the code wouldn't work. I subsequently copy inside the /home/docker (as a Docker User) the files musicgenre.sh, containing the code to read the files, call the phyton code, then pritn the outputs on the terminal, genreprediction.py, containing the code that actual turns the sound files in images and then uses the model to predict its genre, the genre_prediction.keras, that cotains the model, and the config_model.json, that contains the parameters used to predict the model.

To run it instead do: docker run -v <path_to_the_directory_with_the_sound_files>:/home/docker/sounds/ genre-prediction:default <name_of_file_or_directory>

If no modification has been made to the github directory during the download, in place of <path_to_the_directory_with_the_sound_files> you can write $PWD/sounds and in place of <name_of_file_or_directory> either "rock.00007.wav" if you want to predict a single file, or "sounds" if you want to predict a directory full of sounds.

The code of the .sh file is explained below:

The first lines check the amount of arguments given to the image, they must be exactly one, therefore you will receive an error message if you put zero or more than one. If the number of argument is correct the code then checks whether the argument is a file, a directory or none of them. In the last case it will give an error message, instead in the first two it will call the phyton file on the argument (if the argument is a directory, it will perform a loop on all the files inside it). Before this however, I use ffmpeg to convert them all in .wav type files (if the input is not a sound file, the code will return error and skip that file) as the model has been trained on them, therefore it performs better with those. The python file then passes as output the name of the predicted genre and the probability of that prediction, which are then printed out in the terminal, after some text editing using "awk".

As for the genreprediction.py, its code can be visualised by opening the MusicgenreML.ipynb, found inside the colabfiles folder. In the same way also the code of Genreprediction.ipynb, that contains the training of the model.
