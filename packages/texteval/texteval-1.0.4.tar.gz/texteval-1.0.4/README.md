# Text Eval

A tiny python package to find the sentence similarity metrics.

## Getting started

### Installing
```bash
$ pip install texteval
```

### Usage
```python
from texteval.evaluate import Evaluator

system_summary = "John really loves data science very much and studies it a lot."
input_text = "John very much loves data science and enjoys it a lot."

evaluator = Evaluator()
res = evaluator.rouge_evaluation(input_text,system_summary)
print(res)
```

