# Semi-Structured Data

This repo supports the **Semi-Structured Data** course at **Université Paris-Dauphine** for L3 IM2D (Informatique Mathématiques Décision Données).

### Evaluation

Evaluation is run through the `evaluate.py` function. Pre-requisites are a `students.csv` with a `name` attribute, and a `submission` directory with students submissions in corresponding subdir (`tp1`, `tp2`, ...) with the naming convention `name.zip`.

```bash
uv run evaluate.py -s ./students.csv -h ./submission --tp 1
```
