export CUDA_VISIBLE_DEVICES=1


for model_name in "incoder-1b" "codegen-2b" "polycoder"; do
    python generate.py \
    --model $model_name\
    --bs 1 \
    --temperature 0.7 \
    --constract_prompt "add_demo" \

done


