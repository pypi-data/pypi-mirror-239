import sys
from fastapi import FastAPI
from langserve import add_routes
from rag_chroma_private import chain as rag_chroma_private_chain


app = FastAPI()


add_routes(app, rag_chroma_private_chain, path="/rag-chroma-private")

if __name__ == "__main__":
    from platform import python_version
    print(python_version())

    print(sys.path)
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
