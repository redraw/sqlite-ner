# sqlite-ner

Create a new table with entities extracted from source columns using [spacy](https://spacy.io) NER features.

```bash
usage: sqlite-ner [-h] [--model MODEL]
                  db_path table_name source_columns [source_columns ...]

positional arguments:
  db_path
  table_name
  source_columns

optional arguments:
  -h, --help      show this help message and exit
  --model MODEL   spaCy model to use (default: es_core_news_sm)
```
