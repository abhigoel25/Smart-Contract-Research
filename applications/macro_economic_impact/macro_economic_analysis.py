import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel, Field
from typing import Optional
from agentics import AG
import datetime
import asyncio
from agentics.core.atype import import_pydantic_from_string, get_pydantic_fields
from pydantic_model_builder import pydantic_model_bulilder_ui, import_pydantic_from_string
import os
from pathlib import Path


def macro_economic_analysis_ui():
    st.markdown(
        """
        This application performs macro-economic analysis using market data.
        You can select or build an output Pydantic Type to focus the analysis.
        """
    )



    if "market_dataset" not in st.session_state:
        st.session_state.market_dataset = AG.from_csv("/Users/gliozzo/Code/agentics911/agentics/data/macro_economic_analysis/market_factors_new.csv")

    if "market_dataset_index" not in st.session_state:
        st.session_state.market_dataset_index={s.Date : i for i, s in enumerate(st.session_state.market_dataset.states)}

    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "NA"

    start = datetime.date(2008, 7, 1)
    end = datetime.date(2025, 10, 3)

    st.markdown("#### Select exsiting model")

    st.session_state.selected_model = st.selectbox("Predefined Models", options=os.listdir(Path(__file__).resolve().parent / "predefined_types") + ["NA"], key="predefined_model")
    load_model = st.button("Load Model")
    
    if load_model and st.session_state.selected_model!="NA":
        with open(Path(__file__).resolve().parent / "predefined_types" / st.session_state.selected_model, "r") as f:
            code = f.read()
            st.session_state.pydantic_class = import_pydantic_from_string(code)
            st.session_state.fields = get_pydantic_fields(st.session_state.pydantic_class)

        

    with st.form("Selection"):
    
        selected_start = st.selectbox("start date", options=sorted(st.session_state.market_dataset_index.keys()), index=0)
        selected_end = st.selectbox("end date", options=sorted(st.session_state.market_dataset_index.keys()), index=0)
        #type_code = st.text_area("Insert a Pydantic Type to focus your analysis", value=example_class, height=300)
        areduce_batch_size = st.number_input("areduce_batch_size", value=10, min_value=1, max_value=50, step=1)
        
        market_sentiment_analysis= st.form_submit_button("Perform Market Sentiment Analysis")
    if market_sentiment_analysis:
       
        start_index= st.session_state.market_dataset_index[str(selected_start)]
        end_index= st.session_state.market_dataset_index[str(selected_end)]

        sentiment = asyncio.run((AG(atype=st.session_state.pydantic_class,
                                    transduction_type="areduce",
                                    areduce_batch_size=areduce_batch_size) \
                                << st.session_state.market_dataset.filter_states(
                                    start=start_index, end=end_index+1)))
   
        st.write(sentiment.pretty_print())
        st.write(sentiment.areduce_batches)
