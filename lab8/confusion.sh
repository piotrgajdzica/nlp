DATASET=$1
MODEL=$2
ROOT=/root
echo Normalizing dataset $DATASET...
awk 'BEGIN{FS=OFS="\t"}{ $1 = "__label__" tolower($1) }1' $DATASET > $ROOT/norm
cut -f 1 -d$'\t' $ROOT/norm > $ROOT/normlabels

echo Calculating predictions...
 /home/piotrek/v0.2.0/fastText-0.2.0/build/fasttext predict $MODEL $DATASET > $ROOT/pexp
python ./fasttext_confusion_matrix.py $ROOT/normlabels $ROOT/pexp