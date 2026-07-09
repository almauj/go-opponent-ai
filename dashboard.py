import streamlit as st
import pandas as pd
import sqlite3 as sq

DB_NAME = "go_analytics.db"

st.set_page_config(page_title="Go Opponent AI", layout="wide")
st.title("Go Machine Learning and Analytics Dashboard ")
st.subheader("For tracking personal growth in addition to a custom algorithmic opponent")

conn = sq.connect(DB_NAME)
try:
    df = pd.read_sql_query("SELECT * FROM game_history", conn)
    df_traits = pd.read_sql_query("SELECT * FROM bot_traits", conn)
except:
    df = pd.DataFrame() # Empty if table is not initialized yet
    df_traits = pd.DataFrame()
conn.close()

if df.empty:
    st.info("No games have been logged yet.")
else:
    # Summary cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Matches Played", len(df))

    with col2: 
        player_wins = len(df[df['winner'].str.lower() == 'player'])
        calc_wins = (player_wins / len(df)) * 100
        st.metric("Your Win Rate", f"{round(calc_wins, 2)}%")

    with col3:
        st.metric("Max Moves Record", int(df['total_moves'].max()))

    st.markdown("---")

    # Chart sections
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.write("### Win/Loss Breakdown")
        win_counts = df['winner'].value_counts()
        st.bar_chart(win_counts)
        
    with chart_col2:
        st.write("### Capture Trends Over Time")
        chart_data = df[['player_captures'], ['bot_captures']]
        st.line_chart(chart_data)
    
    st.markdown("---")
    # Bot personality evolution
    st.write("### Bot Personality Evolution By Traits")
    if not df_traits.empty:
        st.line_chart(df_traits[['aggression', 'defense']])