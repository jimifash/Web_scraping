# In streamlit_app.py

import pandas as pd
from Music_Recommendation import recommend, df_new
import streamlit as st

data = df_new
df = pd.DataFrame(data)

def main():
    st.title("Music Recommendation System")

    selected_song = st.sidebar.selectbox("Select a song:", df['song_name'])

    st.subheader("Selected Song Details:")
    selected_song_details = df[df['song_name'] == selected_song]
    st.write(selected_song_details)

    recommendations = recommend(selected_song)

    st.subheader("Recommended Songs:")
    if "Song not found" in recommendations:
        st.error("Song not found. Please try another.")
    else:
        # Display recommended songs with a styled layout
        for recommended_song in recommendations:
            st.markdown(f"### {recommended_song}")

if __name__ == "__main__":
    main()
