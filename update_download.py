import streamlit as st
import pandas as pd

def show_update_download():
    st.title("⬇️ Download & Update History")

    st.subheader("Download Datasets")
    for fname, label in [
        ("invoices_data.json","Invoices"),
        ("jobs_data.json","Jobs"),
        ("customers_data.json","Customers"),
        ("estimates_data.json","Estimates"),
    ]:
        try:
            with open(fname, "r", encoding="utf-8") as f:
                st.download_button(label=f"Download {label}", data=f.read(),
                                   file_name=fname, mime="application/json")
        except Exception:
            st.warning(f"{fname} not found.")

    st.subheader("Update History")
    try:
        hist = pd.read_csv("update_history.csv")
        st.dataframe(hist, use_container_width=True)
    except Exception:
        st.info("No update history file found.")
