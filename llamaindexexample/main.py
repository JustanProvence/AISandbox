from llama_index import (
    ServiceContext,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    set_global_service_context,
)
from llama_index.llms import Ollama

# llm 
llm = Ollama(model="mistral", request_timeout=30.0)

documents = SimpleDirectoryReader("data").load_data()

# ServiceContext is a bundle of commonly used 
# resources used during the indexing and 
# querying stage 
service_context = (
    ServiceContext.from_defaults(
        llm=llm, 
        embed_model="local:BAAI/bge-small-en-v1.5", 
        chunk_size=300
    )
)
set_global_service_context(service_context)

# Node represents a “chunk” of a source Document
nodes = (
    service_context
    .node_parser
    .get_nodes_from_documents(documents)
)

# offers core abstractions around storage of Nodes, 
# indices, and vectors
storage_context = StorageContext.from_defaults()
storage_context.docstore.add_documents(nodes)

# Create the vectorstore index
index = (
    VectorStoreIndex.from_documents(
        documents, 
        storage_context=storage_context, 
        llm=llm
        )
)
query_engine = index.as_query_engine()

# Query the index
query="""What did the author do growing up?"""
response = query_engine.query(query)
print(response)