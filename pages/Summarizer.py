import streamlit as st
from headerfooter import footer,Disclaimer,JobSearch,Getlogo
st.set_page_config(page_title = "Summarizer",
                    layout='centered',
                    initial_sidebar_state = "expanded")

col1, col2 = st.columns([60,40],gap="medium",vertical_alignment="bottom")
with col1:
    st.header("Summary")
with col2:
    if st.button("Home",use_container_width=True):
        st.switch_page("Home.py")
st.write("---")

def Summariser(wall_of_text):
    import torch
    from transformers import pipeline

    hf_name = "pszemraj/led-base-book-summary"

    summarizer = pipeline(
        "summarization",
        hf_name,
        device=0 if torch.cuda.is_available() else -1,
    )

    with st.spinner("Running the model... just few seconds more...."):
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
    wall_of_text =  st.text_area('''Enter the text here to summarise: \n
Example: This Article is extracted from URL: https://www.gesetze-im-internet.de/englisch_gg/englisch_gg.html
                                 '''
                                 , '''
                        Article 23
[European Union – Protection of basic rights – Principle of subsidiarity]

(1) With a view to establishing a united Europe, the Federal Republic of Germany shall participate in the development of the European Union that is committed to democratic, social and federal principles, to the rule of law and to the principle of subsidiarity and that guarantees a level of protection of basic rights essentially comparable to that afforded by this Basic Law. To this end the Federation may transfer sovereign powers by a law with the consent of the Bundesrat. The establishment of the European Union, as well as changes in its treaty foundations and comparable regulations that amend or supplement this Basic Law or make such amendments or supplements possible, shall be subject to paragraphs (2) and (3) of Article 79.

(1a) The Bundestag and the Bundesrat shall have the right to bring an action before the Court of Justice of the European Union to challenge a legislative act of the European Union for infringing the principle of subsidiarity. The Bundestag is obliged to initiate such an action at the request of one quarter of its Members. By a statute requiring the consent of the Bundesrat, exceptions to the first sentence of paragraph (2) of Article 42 and the first sentence of paragraph (3) of Article 52 may be authorised for the exercise of the rights granted to the Bundestag and the Bundesrat under the contractual foundations of the European Union.

(2) The Bundestag and, through the Bundesrat, the Länder shall participate in matters concerning the European Union. The Federal Government shall notify the Bundestag and the Bundesrat of such matters comprehensively and as early as possible.

(3) Before participating in legislative acts of the European Union, the Federal Government shall provide the Bundestag with an opportunity to state its position. The Federal Government shall take the position of the Bundestag into account during the negotiations. Details shall be regulated by a law.

(4) The Bundesrat shall participate in the decision-making process of the Federation insofar as it would have been competent to do so in a comparable domestic matter or insofar as the subject falls within the domestic competence of the Länder.

(5) Insofar as, in an area within the exclusive competence of the Federation, interests of the Länder are affected and in other matters, insofar as the Federation has legislative power, the Federal Government shall take the position of the Bundesrat into account. To the extent that the legislative powers of the Länder, the structure of Land authorities, or Land administrative procedures are primarily affected, the position of the Bundesrat shall receive prime consideration in the formation of the political will of the Federation; this process shall be consistent with the responsibility of the Federation for the nation as a whole. In matters that may result in increased expenditures or reduced revenues for the Federation, the consent of the Federal Government shall be required.

(6) When legislative powers exclusive to the Länder concerning matters of school education, culture or broadcasting are primarily affected, the exercise of the rights belonging to the Federal Republic of Germany as a member state of the European Union shall be delegated by the Federation to a representative of the Länder designated by the Bundesrat. These rights shall be exercised with the participation of, and in coordination with, the Federal Government; their exercise shall be consistent with the responsibility of the Federation for the nation as a whole.

(7) Details regarding paragraphs (4) to (6) of this Article shall be regulated by a law requiring the consent of the Bundesrat.
                    ''')
    submit = st.button("Generate")

    if submit:
        st.write(Summariser(wall_of_text))

Disclaimer()
st.markdown(footer,unsafe_allow_html=True)
JobSearch()
Getlogo()