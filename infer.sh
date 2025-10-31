export MINERU_MODEL_SOURCE=modelscope

export MINERU_MIN_BATCH_INFERENCE_SIZE=16

mineru -p images/ -o infer_output/mineru/ -b vlm-transformers -d cuda

mineru -p images/ -o infer_output/mineru/ -b pipeline -d cuda:1