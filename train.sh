#!/usr/bin/env bash
###########################################################
# Change the following values to train a new model.
# type: the name of the new model, only affects the saved file name.
# dataset: the name of the dataset, as was preprocessed using preprocess.sh
# test_data: by default, points to the validation set, since this is the set that
#   will be evaluated after each training iteration. If you wish to test
#   on the final (held-out) test set, change 'val' to 'test'.
type=cs_dataset_cm
dataset_name=cs_dataset_cm
data_dir=data/${dataset_name}
data=${data_dir}/${dataset_name}
test_data=${data_dir}/${dataset_name}.val.c2v
model_dir=models/${type}

mkdir -p models/${model_dir}
set -e
python -u code2vec.py --data ${data} --test ${test_data} --save ${model_dir}/saved_model
#python3 -u code2vec.py --data ${data} --test ${test_data} --save ${model_dir}/saved_model --save_w2v ${model_dir}/tokens.txt
#--data 'data/cs_dataset/cs_dataset' --test 'data/cs_dataset/cs_dataset.val.c2v' --save 'models/cs_dataset/saved_model'
