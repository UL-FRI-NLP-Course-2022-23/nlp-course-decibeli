# Natural language processing course 2022/23: `Literacy situation models knowledge base creation`

This repository contains source code and [article](/article/Literacy_situation_models_knowledge_base_creation.pdf) for a group project created as part of Natural Language Processing course at the Faculty of Computer and Information Science at the University of Ljubljana.

## Repository structure

-   `article` contains article.
-   `data` contains data used for implementation and testing.
-   `src` contains source code.

Team members:

-   Jan Bajt, 63170046, jb3976@student.uni-lj.si
-   Anže Habjan, 63170110, ah0233@student.uni-lj.si
-   Tadej Stanonik, 63170268, ts6103@student.uni-lj.si

Group public acronym/name: `83a8x2ru5235qlm9`

## Installation

1. conda create -n nlp python=3.8
2. conda activate nlp
3. pip install -r requirements.txt
4. python -m spacy download en_core_web_sm
5. python -m spacy download en_core_web_lg

## CoreNLP Server

To get family relations triplets using CoreNLP you need first to download CoreNLP from [Download page](https://stanfordnlp.github.io/CoreNLP/download.html).
Then open the `cmd` in the directory where you downloaded the CoreNLP and run `java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000`.
After that you need to modify the `server_url` in `core_nlp.py` file to the IP value of the host where the server runs.

## Reproducing results

### Relationship extraction

Set `FRE_TYPE` and `NER` variables in file `src/pipeline.py` accordingly. This sets the type of Family relation extraction model (either `LUKE` or `coreNLP`) and the type of named entitiy recognition (`spacy`, `nltk` or `stanza`).

Run the file `src/pipeline.py` which will produce entity relationship triplets from each of the five books in a seperate file. The location of these files is depenedant upon `FRE_TYPE` and `NER` variables. If `FRE_TYPE=luke` and `NER=nltk`, these files will reside in folder `data/triplets/luke/nltk`.

### Evaluation

Before evaluation entity triplets files from each book have to be merged into a single file, this can be done using the following command:

```bash
python ./src/merge_csv.py /path/to/folder merged_file_name.csv
```

This command will create a `merged_file_name.csv` file in the `/path/to/folder`.

For evaluation use the `merged_file_name.csv` and `eval.py` python script. Change the `PREDICTIONS_FILENAME` variable to point to the `merged_file_name.csv`, then run `eval.py`. If everything was set up correctly, you should see a similar output:

```
SKIPS:482
TP: 65, FP: 279, FN: 70
------------------
Precision: 0.18895348837209303
Recall: 0.48148148148148145
F1: 0.27139874739039666
```
