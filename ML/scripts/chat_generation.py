from langchain.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from dotenv import load_dotenv
import os

# load_dotenv("../../.env")
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

os.environ["PINECONE_ENVIRONMENT"] = "gcp-starter"
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "medical-chatbot"
index = pc.Index(index_name)

DOCS_DIR = "../medical-docs/"

def store_chunks_in_database():
    all_chunks = []

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=450, chunk_overlap=100)
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    for dirpath, _, filenames in os.walk(DOCS_DIR):
        for file in filenames:
            if file.endswith(".pdf"):
                pdf_path = os.path.abspath(os.path.join(dirpath, file))
                loader = PyPDFLoader(pdf_path)
                documents = loader.load()

                for doc in documents:
                    doc.metadata["source"] = pdf_path

                chunks = text_splitter.split_documents(documents)
                all_chunks.extend(chunks)

    vector_store = PineconeVectorStore.from_texts(
        texts=[chunk.page_content for chunk in all_chunks],
        index_name=index_name,
        embedding=embedding
    )
    print(f"Successfully stored {len(all_chunks)} chunks in Pinecone.")

    return vector_store

vector_store = store_chunks_in_database()

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

CUSTOM_PROMPT = PromptTemplate(
    template="""You are an AI assistant that provides direct and informative answers.
Follow these rules:
1. DO NOT use phrases like "Based on the given text" or "According to the text."
2. DO NOT use bullet points, markdown, or structured formatting—respond in a natural paragraph format.
3. Keep responses concise yet detailed.
4. Avoid unnecessary introductions or disclaimers.

Context: {context}
Question: {question}
Answer:""",
    input_variables=["context", "question"],
)

chain = ConversationalRetrievalChain.from_llm(
    llm, retriever=vector_store.as_retriever(), memory=memory,
    combine_docs_chain_kwargs={"prompt": CUSTOM_PROMPT} 
)


def text_generation(query):
    try:
        answer = chain.invoke({"question": query})
        return answer.get("answer")
    except Exception as e:
        return f"Error during text generation: {str(e)}"