import streamlit as st

from app.src.data_prep import load


def main():
    df = load()

    st.dataframe(df)


if __name__ == "__main__":
    main()
