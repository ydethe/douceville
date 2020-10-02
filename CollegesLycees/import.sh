#! /bin/sh


rsync -avzP --sparse --exclude '*.DS_Store*' py:/home/ydethe/Downloads/CollegesLycees/CollegesLycees/ ../CollegesLycees

# python import_etablissements.py

