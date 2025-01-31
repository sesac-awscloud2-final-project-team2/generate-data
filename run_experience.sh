for json_file in logs/trip/*.json; do
    python __run__.py prompt/exp_prompt_1.yaml experience "$json_file"
done

