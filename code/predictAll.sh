#! /bin/bash

files="../data/dataset_*.fa"
lookupPre="../data/lookup"
lookupSuf=".dat"

echo "start: $(date)"
for file in $files
do
  nr=$(echo "$file" | sed -r "s/..\/data\/dataset_(.*).fa/\1/ig")
  python __main__.py -f "$file" -k "$lookupPre$nr$lookupSuf" -v 31 > "../data/results${nr}.dat" &
done

wait
echo "results: $(date)"

# Merge results

grep "^T" ../data/results*.dat > result.dat

echo "Ready: $(date)"
