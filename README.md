# Natural language processing course 2022/23: `Literacy situation models knowledge base creation`

This repository contains source code and [article](/article/Literacy_situation_models_knowledge_base_creation.pdf) for a group project created as part of Natural Language Processing course at the Faculty of Computer and Information Science at the University of Ljubljana.

## Repository strcture

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
4. <em>(pip install allennlp==2.9.3 allennlp-models==2.9.3 cached-path==1.1.2) &#8594; OPCIJSKO: glede na to, da allennlp itak ne dela</em>
5. python -m spacy download en_core_web_sm
