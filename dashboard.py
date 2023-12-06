# Import libraries yang dibutuhkan
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Menyiapkan DataFrame yang akan digunakan untuk membuat visualisasi data
def create_average(df):
    average_review_score_by_state = df.groupby("customer_state")["review_score"].mean().sort_values(ascending=False)
    return average_review_score_by_state

def create_revenue(df):
    revenue = df.groupby("product_category_name")["payment_value"].sum().sort_values(ascending=False)
    return revenue

# Load berkas final_data.csv sebagai sebuah DataFrame
final_df = pd.read_csv("final_data.csv")

# Membuat dashboard yang interaktif 
datetime_col = ["order_purchase_timestamp", "order_delivered_customer_date"]
final_df.sort_values(by="order_purchase_timestamp", inplace=True)
final_df.reset_index(inplace=True)
for column in datetime_col:
    final_df[column] = pd.to_datetime(final_df[column])
min_date = final_df["order_purchase_timestamp"].min()
max_date = final_df["order_purchase_timestamp"].max()

with st.sidebar:
    st.image("./Olist_logo.jpg")
    start_date, end_date = st.date_input(
        label="Time Span",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Helper function disimpan ke dalam main_df
main_df = final_df[(final_df["order_purchase_timestamp"] >= str(start_date)) & (final_df["order_purchase_timestamp"] <= str(end_date))]
# Proses untuk memanggil helper function yang telah dibuat sebelumnya
average_review_score_by_state = create_average(main_df)
revenue = create_revenue(main_df)

# Membuat header pada dashboard
st.image('./Olist_image.png')
st.header('Olist E-Commerce Public Statistics')

# Visualisasi Rata-rata Review Score per State
st.subheader('Average Review Score by State')
fig, ax = plt.subplots(figsize=(12, 6))
average_review_score_by_state.plot(kind='bar', color='lightblue', ax=ax)
ax.set_title('Average Review Scores by State (Overall)')
ax.set_xlabel('State')
ax.set_ylabel('Average Review Score')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
st.pyplot(fig)

# Visualisasi 5 Rata-rata Review Score Terbaik dan Terburuk per State
st.subheader('Top 5 Best and Worst Average Review Score by State')
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ['lightblue', 'lightgray', 'lightgray', 'lightgray', 'lightgray']
    best_review = average_review_score_by_state.head(5).reset_index()
    sns.barplot(
        data=best_review,
        x='customer_state',
        y='review_score',
        palette=colors,
        ax=ax,
        width=0.5
    )
    ax.set_title("Best 5 Average Review Score by State", loc="center", fontsize=40)
    ax.set_ylabel('Average Review Score', fontsize=20)
    ax.set_xlabel('State', fontsize=20)
    ax.tick_params(axis='x', labelsize=18)
    ax.tick_params(axis='y', labelsize=15)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ['lightgray', 'lightgray', 'lightgray', 'lightgray', 'red']
    worst_review = average_review_score_by_state.tail(5).reset_index()
    sns.barplot(
        data=worst_review,
        x='customer_state',
        y='review_score',
        palette=colors,
        ax=ax,
        width=0.5
    )
    ax.set_title("Worst 5 Average Review Score by State", loc="center", fontsize=40)
    ax.set_ylabel('Average Review Score', fontsize=20)
    ax.set_xlabel('State', fontsize=20)
    ax.invert_xaxis()
    ax.tick_params(axis='x', labelsize=18)
    ax.tick_params(axis='y', labelsize=15)
    st.pyplot(fig)

# Visualisasi kategori barang (product category) dengan revenue paling banyak dan sedikit
st.subheader('5 Highest and Lowest Product Categories Revenue')
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ['lightblue', 'lightgray', 'lightgray', 'lightgray', 'lightgray']
    best_revenue = revenue.head(5).reset_index()
    sns.barplot(
        data=best_revenue,
        x='product_category_name',
        y='payment_value',
        palette=colors,
        ax=ax,
        width=0.5
    )
    ax.set_title("5 Product Categories with Highest Revenue", loc="center", fontsize=40)
    ax.set_ylabel('Revenue', fontsize=20)
    ax.set_xlabel('Product Category', fontsize=20)
    ax.tick_params(axis='x', labelsize=18)
    ax.tick_params(axis='y', labelsize=15)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ['lightgray', 'lightgray', 'lightgray', 'lightgray', 'red']
    worst_revenue = revenue.tail(5).reset_index()
    sns.barplot(
        data=worst_revenue,
        x='product_category_name',
        y='payment_value',
        palette=colors,
        ax=ax,
        width=0.5
    )
    ax.set_title("5 Product Categories with Lowest Revenue", loc="center", fontsize=40)
    ax.set_ylabel('Revenue', fontsize=20)
    ax.set_xlabel('Product Category', fontsize=20)
    ax.invert_xaxis()
    ax.tick_params(axis='x', labelsize=18)
    ax.tick_params(axis='y', labelsize=15)
    st.pyplot(fig)

# Membuat metric untuk melihat total revenue per hari
total_revenue_per_day = main_df.groupby(main_df["order_purchase_timestamp"].dt.date)["payment_value"].sum().rename("Total Revenue")
total_revenue = format_currency(total_revenue_per_day.sum(), "R$", locale='pt_BR')
st.metric("Total Revenue", value=total_revenue)