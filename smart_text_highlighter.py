import streamlit as st
import spacy

# Load SpaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    st.error(f"Error loading SpaCy model: {str(e)}")
    st.stop()

# Function to categorize and chunk the sentence into meaningful groups
def categorize_chunks(text):
    doc = nlp(text)
    chunks = []
    
    # This will store the current chunk being formed
    current_chunk = []
    
    for token in doc:
        # Define dependencies and POS that should be grouped together for meaningful phrases
        if token.dep_ in {"compound", "amod", "nsubj", "dobj", "pobj", "attr", "prep"} or \
           token.pos_ in {"NOUN", "PROPN", "ADJ", "VERB", "ADV"}:
            current_chunk.append(token.text)
        elif current_chunk:  # If we have a chunk and the next token doesn't fit, finalize the chunk
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            
            # Add standalone tokens like verbs or adverbs if they're significant
            if token.pos_ in {"VERB", "ADV"}:
                chunks.append(token.text)
    
    # Add the last chunk if there's any remaining
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# Function to format the chunks for display
def format_chunks(chunks):
    formatted_text = ""
    for chunk in chunks:
        # Color the chunk based on the part of speech of the first word in the chunk
        first_word = nlp(chunk)[0]
        if first_word.pos_ == "VERB":
            color = "orange"  # Verbs
        elif first_word.pos_ in {"NOUN", "PROPN"}:
            color = "blue"  # Nouns
        elif first_word.pos_ in {"ADJ", "ADV"}:
            color = "purple"  # Adjectives and Adverbs
        else:
            color = "green"  # Other parts of speech
        
        # Format each chunk as a separate row with color
        formatted_text += f'<span style="color:{color}; font-weight:bold; display:block; margin-bottom:5px;">{chunk}</span>'
    
    return formatted_text

# Streamlit interface
st.title("Smart Chunk Categorizer by Hossein Ahmadi")
user_input = st.text_area("Enter a sentence to analyze and categorize:")

if user_input:
    chunks = categorize_chunks(user_input)
    formatted_output = format_chunks(chunks)
    st.markdown(f"<p>{formatted_output}</p>", unsafe_allow_html=True)
