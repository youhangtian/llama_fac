export CUDA_VISIBLE_DEVICES=2,3,4,5
export PYTHONPATH=$PYTHONPATH:/home/tyh/git/LLaMA-Factory/src

python -c 'from llamafactory.cli import main; main()' train ./config/vlm_lora_sft.yaml
python -c 'from llamafactory.cli import main; main()' export ./config/vlm_lora_merge.yaml
