import asyncio
import json
import os
import sys
from langchain_experimental.text_splitter import SemanticChunker
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

file_path = "/Users/kasie/논문/baby_dad.pdf"

async def main():
    loader = PyPDFLoader(file_path=file_path)
    pages = []
    async for page in loader.alazy_load():
        pages.append(page)

    text_splitter = SemanticChunker(OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY))
    docs = text_splitter.split_documents(pages)

    print("총 청크 수:", len(docs))
    print(docs[0].page_content)
    chunks_data = []

    for i in docs:
        print(i.metadata, i.page_content, "-"*100)
        chunks_data.append({
        "content": i.page_content,
        "metadata": i.metadata
    })
    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks_data, f, ensure_ascii=False, indent=2)

    

# 실행
asyncio.run(main())