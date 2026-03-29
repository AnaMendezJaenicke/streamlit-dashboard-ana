import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ana Mendez", layout="wide")

st.title("Ana Mendez")
st.markdown("Airbnb Dashboard")

df = pd.read_csv("airbnb.csv")

st.sidebar.header("Filters")

room_types = st.sidebar.multiselect(
    "Listing type",
    df["room_type"].unique(),
    default=df["room_type"].unique()
)

price_range = st.sidebar.slider(
    "Price range",
    int(df["price"].min()),
    int(df["price"].max()),
    (50, 300)
)

filtered_df = df[
    (df["room_type"].isin(room_types)) &
    (df["price"] >= price_range[0]) &
    (df["price"] <= price_range[1])
]

col1, col2 = st.columns(2)

with col1:
    st.metric("Listings", len(filtered_df))

with col2:
    st.metric("Average price", round(filtered_df["price"].mean(), 2))

tab1, tab2 = st.tabs(["Dashboard", "Data"])

with tab1:
    fig1 = px.bar(
        filtered_df.groupby("room_type").size().reset_index(name="count"),
        x="room_type",
        y="count",
        title="Listings by type"
    )
    st.plotly_chart(fig1)

    fig2 = px.scatter(
        filtered_df,
        x="number_of_reviews",
        y="price",
        color="room_type",
        title="Reviews vs Price"
    )
    st.plotly_chart(fig2)

with tab2:
    st.dataframe(filtered_df)