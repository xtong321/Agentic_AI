llm-rag-ollama-demo/
  ├─ data/                 # original docs (your knowledge db)
  │   ├─ doc1.md
  │   ├─ doc2.pdf
  │   └─ ...
  ├─ vectordb/             # vector database (automatic generate)
  ├─ .env                  # env variables (optional)
  ├─ requirements.txt
  ├─ ingest.py             # build/update vector db
  └─ chat_rag.py           # QA-entry (RAG)


usage steps (from zero to be able to ask)

- prepare data
put your docs (Markdown / TXT / PDF) into data/ folder

- install dependences 
bash
pip install -r requirements.txt

- ensure Ollama work normal
bash
ollama pull llama3
ollama run llama3

- build vectordb
bash
python ingest.py

- launch RAG QA
bash
python chat_rag.py

- then you can ask:
“Summarize the key ideas in my notes about RAG.”
“What are the main trade-offs of using Ollama for local inference?”
“Based on my docs, what are the steps to deploy this system?”