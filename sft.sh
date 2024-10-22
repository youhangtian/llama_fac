export CUDA_VISIBLE_DEVICES=4,5,6,7
export PYTHONPATH=$PYTHONPATH:/home/tyh/git/LLaMA-Factory/src

python -c 'from llamafactory.cli import main; main()' train ./config/llava_lora_sft.yaml
python -c 'from llamafactory.cli import main; main()' export ./config/llava_lora_merge.yaml
