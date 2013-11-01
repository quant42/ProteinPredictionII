#!/bin/bash
scriptdir=/usr/lib/hhsuite/scripts/

$scriptdir/splitfasta.pl pp2/genes_UniProt.fasta
mv *.seq pp2/
$scriptdir/multithread.pl 'pp2/*.seq' 'hhblits -i $file -d /mnt/project/rost_db/hhblits/uniprot20 -oa3m $name.a3m' -cpu 4
$scriptdir/multithread.pl 'pp2/*.a3m' $scriptdir/'addss.pl $file' -cpu 4
$scriptdir/hhblitsdb.pl -o pp2/ -ia3m pp2/ -cpu 4
