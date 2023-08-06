#!/bin/sh



if [ $# -lt 1 ]
then
echo "$0 genome"
fi

BASE_CHRS="\
chr1 \
chr2 \
chr3 \
chr4 \
chr5 \
chr6 \
chr7 \
chr8 \
chr9 \
chr10 \
chr11 \
chr12 \
chr13 \
chr14 \
chr15 \
chr16 \
chr17 \
chr18 \
chr19 \
chr20 \
chr21 \
chr22 \
chrX \
chrY \
chrM"

get() {
    file=$1
    if ! wget --version >/dev/null 2>/dev/null ; then
        if ! curl --version >/dev/null 2>/dev/null ; then
            echo "Please install wget or curl somewhere in your PATH"
            exit 1
        fi
        curl -o `basename $1` $1
        return $?
    else
        wget $1
        return $?
    fi
}


genome=$1
if [[ $genome == hg18 ]]; 
then
    for c in $BASE_CHRS
    do  
       get 'ftp://hgdownload.cse.ucsc.edu/goldenPath/hg18/chromosomes/'${c}.fa.gz || (echo "Error getting $c" && exit 1)
       gunzip ${c}.fa.gz || (echo "Error getting $c" && exit 1)
    done
    cat *fa > hg18.fa
    rm chr*fa
elif [[ $genome == hg19 ]];
then
    for c in $BASE_CHRS
    do  
       get 'ftp://hgdownload.cse.ucsc.edu/goldenPath/hg19/chromosomes/'${c}.fa.gz || (echo "Error getting $c" && exit 1)
       gunzip ${c}.fa.gz || (echo "Error getting $c" && exit 1)
    done
    cat *fa > hg19.fa
    rm chr*fa
fi
