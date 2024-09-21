import streamlit as st

st.header("Summary")
if st.button("Home"):
    st.switch_page("Home.py")


def Summariser(wall_of_text):
    import torch
    from transformers import pipeline

    hf_name = "pszemraj/led-base-book-summary"

    summarizer = pipeline(
        "summarization",
        hf_name,
        device="cuda:1" #device=0 if torch.cuda.is_available() else -1,
    )

    result = summarizer(
        wall_of_text,
        min_length=8,
        max_length=256,
        no_repeat_ngram_size=3,
        encoder_no_repeat_ngram_size=3,
        repetition_penalty=3.5,
        num_beams=4,
        do_sample=False,
        early_stopping=True,
    )
    #print(result[0]["generated_text"])
    print(result[0])
    return result

with st.container(border=True):
    wall_of_text =  st.text_area("Enter the text here to summarise:")
    submit = st.button("Generate")

    if submit:
        st.write(Summariser(wall_of_text))