This program 
- gets path as a parameter from Terminal run command: "python3 main.py \\path"
- creates a root \JPG folder. All other folders and files will be created inside this JPG folder
- reads MP4 files in the root folder (from the run command)
- Extract mid part of each frame as a Jpeg, this technique to avoid any subtitling to other graphic elements to compare
- Creates a folder for each video file and put all frames in related folder
- Build CSV with hashes for each Video titles and put it in related folder
- Combine all CSV into one file for easier analysis
- Takes small batch/sequence of hashes from a first item and compare with all other hashes
- Provide a list of matches only if group of hashes will match with group of hashes fir another file

