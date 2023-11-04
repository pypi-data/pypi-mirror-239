# Load
from langchain.chat_models import ChatOllama
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import GPT4AllEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import GitLoader

loader = GitLoader(
    # clone_url="https://github.com/langchain-ai/langchain",
    repo_path="/Users/lee/projects/echo-keeper/",
    file_filter=lambda file_path: "local-dev" not in file_path,
    branch="main",
)
data = loader.load()
print(len(data))

filenames = []
for file in data:
    filenames.append(file.metadata['file_path'])

with open('files_in_repo.txt', 'w') as f:
    f.write("\n".join(filenames))
# Split

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

# Add to vectorDB
vectorstore = Chroma.from_documents(
    documents=all_splits,
    collection_name="rag-private",
    embedding=GPT4AllEmbeddings(),
)
retriever = vectorstore.as_retriever()

# Prompt
# Optionally, pull from the Hub
# from langchain import hub
# prompt = hub.pull("rlm/rag-prompt")
# Or, define your own:
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# LLM
# Select the LLM that you downloaded
llama2_7b = "llama2:7b-chat"
codellama = "codellama:latest"
model = ChatOllama(model=codellama)

# RAG chain
chain = (
    RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
    | prompt
    | model
    | StrOutputParser()
)


# Add typing for input
class Question(BaseModel):
    __root__: str


chain = chain.with_types(input_type=Question)
