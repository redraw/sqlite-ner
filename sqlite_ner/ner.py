import argparse

import sqlite_utils
from tqdm import tqdm


def create(db_path, table_name, source_columns, model="es_core_news_sm"):
    """
    Create a new table with entities extracted from the source columns
    """
    print("Loading spacy...")
    import spacy
    try:
        nlp = spacy.load(model)
    except OSError:
        print("Downloading model...")
        spacy.cli.download(model)
        nlp = spacy.load(model)

    db = sqlite_utils.Database(db_path)
    entities_table_name = f"{table_name}_entities"

    for pk, row in tqdm(db[table_name].pks_and_rows_where(), total=db[table_name].count):
        # create doc from source columns
        doc = nlp(" ".join([row[column] for column in source_columns]))
        # extract entities
        ents = set((ent.text, ent.label_) for ent in doc.ents)
        # insert entities into table
        fk_name = f"{table_name}_id"
        db[entities_table_name].insert_all(
            [
                {
                    fk_name: pk,
                    "text": text,
                    "label": label,
                }
                for text, label in ents
            ],
            pk="id",
            foreign_keys=(fk_name, table_name),
        )


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("db_path")
    parser.add_argument("table_name")
    parser.add_argument("source_columns", nargs="+")
    parser.add_argument("--model", default="es_core_news_sm", help="spaCy model to use (default: es_core_news_sm)")
    args = parser.parse_args()
    create(
        args.db_path,
        args.table_name,
        args.source_columns,
        model=args.model,
    )

if __name__ == "__main__":
    cli()
