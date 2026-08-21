import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from transformers import pipeline
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

def build_and_run_rag():
    # 1. Take a short document (Wikipedia article about Mango)
    document = """
    A mango is an edible stone fruit produced by the tropical tree Mangifera indica. 
    It is believed to have originated in the region between northwestern Myanmar, Bangladesh, and northeastern India. 
    M. indica has been cultivated in South and Southeast Asia since ancient times resulting in two distinct types of modern mango cultivars: the "Indian type" and the "Southeast Asian type". 
    Other species in the genus Mangifera also produce edible fruits that are also called "mangoes", the majority of which are found in the Malesian ecoregion.

    Worldwide, there are several hundred cultivars of mango. Depending on the cultivar, mango fruit varies in size, shape, sweetness, skin color, and flesh color which may be pale yellow, gold, green, or orange. 
    The mango is the national fruit of India, Pakistan, and the Philippines, while the mango tree is the national tree of Bangladesh.

    Mangoes are widely used in cuisine. Sour, unripe mangoes are used in chutneys, athanu, pickles, dhals and other side dishes in Bengali cuisine, or may be eaten raw with salt, chili, or soy sauce. 
    A ripe mango contains approximately 84% water, 15% carbohydrates, 1% protein, and has negligible fat. The energy value per 100 g (3.5 oz) serving is 250 kJ (60 kcal). 
    Fresh mango contains only vitamin C and folate in significant amounts of the Daily Value, with 44% and 11% respectively.
    """

    print("Step 1 & 2: Loading document and splitting into chunks...")
    # 2. Split the text into chunks
    # Using character chunks to approximate roughly 50-100 words for this short demo text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=350, 
        chunk_overlap=50,
        length_function=len
    )
    chunks = text_splitter.split_text(document)
    print(f"-> Created {len(chunks)} chunks.")

    print("\nStep 3 & 4: Generating embeddings and storing in Chroma vector database...")
    # 3. Generate embeddings
    # 4. Store embeddings in a vector database (Chroma)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma.from_texts(chunks, embeddings)
    print("-> Vector database ready.")

    # 5. Accept a user query
    query = "What vitamins are in mango?"
    print(f"\nStep 5: User Query: '{query}'")

    print("\nStep 6: Retrieving the most relevant chunk from the database...")
    # 6. Retrieve the most relevant chunk(s) from the database
    retriever = vector_db.as_retriever(search_kwargs={"k": 1})
    retrieved_docs = retriever.invoke(query)
    retrieved_context = retrieved_docs[0].page_content

    print("\n================ RETRIEVED CHUNK ================")
    print(retrieved_context.strip())
    print("=================================================")

    print("\nStep 7: Combining retrieved text with the query and passing to LLM...")
    # 7. Combine retrieved text with the query and pass it to the LLM
    # We use a small local LLM (flan-t5-small) so it can run quickly without API keys
    hf_pipeline = pipeline("text-generation", model="gpt2", max_new_tokens=50, return_full_text=False)
    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    prompt_template = """
    Use the following context to answer the user's question. 
    If you don't know the answer, just say that you don't know.

    Context:
    {context}

    Question: {question}

    Answer:"""

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = prompt | llm

    print("\nStep 8: Generating final answer...\n")
    # 8. Generate a final answer
    final_answer = chain.invoke({"context": retrieved_context, "question": query})

    print("================ FINAL ANSWER ===================")
    print(final_answer.strip())
    print("=================================================")

if __name__ == "__main__":
    build_and_run_rag()
