#!/usr/bin/env bash
#
# Script to extract names and aliases from Freebase RDF dump

#DUMP=/data/disk2/kaharjan/kaharFreebaseData/fb-rdf-10k-head.nt # SETME
#DUMP=/data/disk2/kaharjan/kaharFreebaseData/fb-10M-head.txt # SETME
echo "Usage: filename lang(freebase gzip file name  without extenstion .gz"



FILE=$1
FN=`echo $FILE | sed 's/.*\///'`

grep 'China' $FILE >$FILE.China

cat $FILE.China | cut -f1,3 \
    | cut -f1,3 \
    | sed 's/<http\:\/\/rdf\.freebase\.com\/ns\/\([^>]*\)>/\1/' \
    >$FILE.China.terse

MIDS=$FILE.China.mid
cat $FILE.China | sed 's/^<http\:\/\/rdf\.freebase\.com\/ns\/\(m\.[^>]*\)>.*/\1/' \
    > $MIDS


python extract.py \
    $DUMP.gz \
    $MIDS.gz \
    $NAMES \
    $ALIASES\
    $2
gzip $NAMES
gzip $ALIASES
gzip $NMES$2
gzip $ALIASE$2

gunzip -c $NAMES.gz \
    | cut -f1,3 \
    | sed 's/<http\:\/\/rdf\.freebase\.com\/ns\/\([^>]*\)>/\1/' \
    > $NAMES.terse
gzip $NAMES.terse

gunzip -c $ALIASES.gz \
    | cut -f1,3 \
    | sed 's/<http\:\/\/rdf\.freebase\.com\/ns\/\([^>]*\)>/\1/' \
    > $ALIASES.terse
gzip $ALIASES.terse

gunzip -c $ENWP.gz \
    | cut -f1,3 \
    | sed 's/^<http\:\/\/rdf\.freebase\.com\/ns\/\([^>]*\)>/\1/' \
    | sed 's/<http\:\/\/en\.wikipedia\.org\/wiki\/\([^>]*\)>$/\1/' \
    > $ENWP.terse
gzip $ENWP.terse


