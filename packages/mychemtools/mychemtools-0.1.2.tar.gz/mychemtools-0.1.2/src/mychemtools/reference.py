import streamlit as st

def reference_page():
    st.title("Reference and Tools that We Used")
    st.markdown("1. [HuggingFace transformer](https://huggingface.co/docs/transformers/index) for running model pipeline")
    st.markdown("2. [T5-base model](https://blog.research.google/2020/02/exploring-transfer-learning-with-t5.html) for our language model architecture")
    st.markdown("3. [PubChempy](https://pubchempy.readthedocs.io/en/latest/) for checking chemical name and structure")
    st.markdown("4. [Distilling Step-by-Step](https://arxiv.org/abs/2305.02301) methods for training model ")
