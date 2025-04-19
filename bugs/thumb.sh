#! /bin/bash

for i in *.jpg; do
    convert "$i" -thumbnail 1000 "thumbs/$i";
done;
