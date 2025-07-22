import streamlit as st
from headerfooter import footer,Disclaimer,JobSearch,Getlogo

st.set_page_config(page_title = "Contact Doctor",
                    layout='centered',
                    initial_sidebar_state = "expanded")

col1, col2 = st.columns([60,40],gap="medium",vertical_alignment="bottom")
with col1:
    st.header("Contact Doctor")
with col2:
    if st.button("Home",use_container_width=True):
        st.switch_page("Home.py")
st.write("---")


def ContactDoctor(user_text):
    import transformers, torch

    #model_id = "ContactDoctor/Bio-Medical-Llama-3-8B"
    model_id = "ContactDoctor/Bio-Medical-Llama-3-2-1B-CoT-012025"

    with st.spinner("Running the model... just few seconds more...."):
    
        pipeline = transformers.pipeline( "text-generation", model=model_id, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto", )

        messages = [ {"role": "system", "content": "You are an expert trained on healthcare and biomedical domain!"}, 
                     {"role": "user", "content": "I'm a 35-year-old male and for the past few months, I've been experiencing fatigue, increased sensitivity to cold, and dry, itchy skin. What is the diagnosis here?"},
                    ]

        prompt = pipeline.tokenizer.apply_chat_template( messages, tokenize=False, add_generation_prompt=True )

        terminators = [ pipeline.tokenizer.eos_token_id, pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>") ]

        outputs = pipeline( prompt, max_new_tokens=256, eos_token_id=terminators, do_sample=True, temperature=0.6, top_p=0.9, ) 

        return outputs[0]["generated_text"][len(prompt):]
        #print(outputs[0]["generated_text"][len(prompt):])

with st.container(border=True):
    user_text =  st.text_area(''' Note: This model is for demonstration purpose only, please consult doctor for medical advise. \n
                              Enter the text here to summarise: \n ''', 
                              '''I'm a 35-year-old male and for the past few months, I've been experiencing fatigue, increased sensitivity to cold, and dry, itchy skin. What is the diagnosis here?''')
    submit = st.button("Generate")

    if submit:
        st.write(ContactDoctor(user_text))

Disclaimer()
st.markdown(footer,unsafe_allow_html=True)
JobSearch()
#Getlogo()