#!/bin/sh

numtests=1000

if [ 1 -le $# ]
then
    numtests=$1
fi

tmp=$(mktemp -d)

for i in $(seq 1 $numtests)
do
    echo $i > "$tmp/$i.$i"
done

./randomiser "$tmp"

for f in "$tmp"/*
do
    echo "Testing $f" 
    base=$(basename -- "$f")
    id=${base##*.}
    if [ "$id" != "$(cat $f)" ]
    then
        echo "$f does not match!" >&2 
        exit 1
    fi
    rm $f
done

rmdir "$tmp"

echo "Randomised $numtests files while keeping their contents intact!"
