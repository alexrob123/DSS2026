uv run evaluate.py tp-xml-dtd
uv run evaluate.py tp-dom \
    --ref-py ./evaluation/utils/eval_dom.py \
    --test-xml ./evaluation/utils/eval_dom.xml
uv run evaluate.py tp-json
uv run evaluate.py agg