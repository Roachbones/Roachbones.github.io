#! /bin/bash

for i in *.jpg; do
    convert "$i" -thumbnail 1000 "thumb/$i";
done;

for i in *.webp; do
    convert "$i" -thumbnail 1000 "thumb/$i";
done;
