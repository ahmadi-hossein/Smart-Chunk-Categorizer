import os
import spacy
import streamlit as st

# Install SpaCy model if not already installed
try:
    spacy.load("en_core_web_sm")
except Exception as e:
    st.warning(f"SpaCy model 'en_core_web_sm' not found. Attempting to download it.")
    os.system("python -m spacy download en_core_web_sm")
    st.warning("SpaCy model 'en_core_web_sm' has been downloaded. Please reload the app.")

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Function to categorize and chunk the sentence into meaningful groups
def categorize_chunks(text):
    doc = nlp(text)
    chunks = []
    current_chunk = []
    
    for token in doc:
        if token.dep_ in {"compound", "amod", "nsubj", "dobj", "pobj", "attr", "prep"} or \
           token.pos_ in {"NOUN", "PROPN", "ADJ", "VERB", "ADV"}:
            current_chunk.append(token.text)
        elif current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            if token.pos_ in {"VERB", "ADV"}:
                chunks.append(token.text)
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# Function to format the chunks for display
def format_chunks(chunks):
    formatted_text = ""
    for chunk in chunks:
        first_word = nlp(chunk)[0]
        if first_word.pos_ == "VERB":
            color = "orange"  # Verbs
        elif first_word.pos_ in {"NOUN", "PROPN"}:
            color = "blue"  # Nouns
        elif first_word.pos_ in {"ADJ", "ADV"}:
            color = "purple"  # Adjectives and Adverbs
        else:
            color = "green"  # Other parts of speech
        
        formatted_text += f'<span style="color:{color}; font-weight:bold; display:block; margin-bottom:5px;">{chunk}</span>'
    
    return formatted_text

# Streamlit interface
st.title("Smart Chunk Categorizer by Hossein Ahmadi")
user_input = st.text_area("Enter a sentence to analyze and categorize:")

if user_input:
    chunks = categorize_chunks(user_input)
    formatted_output = format_chunks(chunks)
    st.markdown(f"<p>{formatted_output}</p>", unsafe_allow_html=True)
