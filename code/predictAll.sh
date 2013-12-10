#! /bin/bash

files="dataset_*.fa"
lookup="lookup.dat"

echo "start: $(date)"
for file in $files
do
  nr=$(echo "$file" | sed -r "s/.*dataset_(.*).fa/\1/ig")
  echo "$nr"
  python __main__.py -f "$file" -k "$lookup" -v 31 --fast > "../results${nr}b.dat"
  exit
done

wait
echo "end: $(date)"
