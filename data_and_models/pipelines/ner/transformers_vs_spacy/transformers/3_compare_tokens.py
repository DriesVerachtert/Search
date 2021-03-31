import pandas as pd
import spacy


nlp = spacy.load("en_core_web_lg", disable=["vocab", "ner"])


def unroll_rows(df):
    return pd.concat([pd.DataFrame(row.to_dict()) for i, row in df.iterrows()])


def poor_venn(set1, set2):
    print(f"[ {len(set1 - set2)} | {len(set1 & set2)} | {len(set2 - set1)} ]")


def lemma(word):
    return next(iter(nlp(word.lower()))).lemma_


df_train = pd.read_pickle("train_data.pkl")
df_test = pd.read_pickle("test_data.pkl")
with open("checkpoints/evaluate_transformers/test_predictions.txt") as fp:
    df_test["pred"] = [line.strip().split() for line in fp]


df_train_flat = unroll_rows(df_train)
df_test_flat = unroll_rows(df_test)

train_entities = set(df_train_flat.token[df_train_flat.entity_type != "O"])
test_entities = set(df_test_flat.token[df_test_flat.entity_type != "O"])
pred_entities = set(df_test_flat.token[df_test_flat.pred != "O"])

train_entities = set(map(lemma, train_entities))
test_entities = set(map(lemma, test_entities))
pred_entities = set(map(lemma, pred_entities))

print("{train, test, pred} = Unique token lemmata in the corresponding sets with an entity type that is not 'O'")
print()

print("train - test")
print(sorted(train_entities - test_entities))
print()

print("train - pred")
print(sorted(train_entities - pred_entities))
print()

print("test - train")
print(sorted(test_entities - train_entities))
print()

print("pred - train")
print(sorted(pred_entities - train_entities))
print()

print("len(train) =", len(train_entities))
print("len(test) =", len(test_entities))
print("len(pred) =", len(pred_entities))
print()

print("VENN: train vs. test")
poor_venn(train_entities, test_entities)
print("VENN: train vs. pred")
poor_venn(train_entities, pred_entities)
print("VENN: test vs. pred")
poor_venn(test_entities, pred_entities)
print()

print("How many of the unseen tokens were predicted?")
seen = test_entities & train_entities
unseen = test_entities - train_entities
print(f"Out of {len(unseen)} unseen tokens {len(unseen & pred_entities)} were predicted")
print(f"Out of {len(seen)} seen tokens {len(seen & pred_entities)} were predicted")
