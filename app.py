import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import pandas as pd
import os
import openweather
import utils
import base64

cwd=os.getcwd()
#set the intial page configuration
image=Image.open(os.path.join(cwd, 'images\img1.png'))
st.set_page_config(page_title="Musically", layout="wide",page_icon=image, initial_sidebar_state="expanded")

#loads the CSS file
css_file = os.path.join(cwd, 'style.css')
utils.local_css(css_file)

#so that app starts from the home mode only
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = 'home'

#Home Page
def home_page():
    st.markdown("<h1 style='text-align: center; color: white;'>Welcome to Musically!</h1>", unsafe_allow_html=True)
    utils.set_png_as_page_bg(os.path.join(cwd, 'images\img3.png'))
    st.markdown('---')
    st.markdown("<h4 style='text-align: center; color: white';>Your Music Buddy!</h4>", unsafe_allow_html=True)

if 'got_feedback' not in st.session_state:
    st.session_state.got_feedback = False

#To get more recommendations if the user liked the top track
def add_feedback(track_uri):
    st.markdown("<h4 style='text-align: left; color: black';>You may also like this:</h4>", unsafe_allow_html=True)
    uris=utils.n_neighbors_uri_audio(track_uri)
    tracks = utils.get_tracks_for_display(uris)
    if len(tracks)==0:
        st.write("Oops! No similar song found")
    for track in tracks:
        components.html(track, height=80)
    st.session_state.got_feedback = True

#Discover Yourself page
def discover_page():
    utils.set_png_as_page_bg(os.path.join(cwd, 'images\img2.png'))
    st.markdown("<h1 style='text-align: center; color: black;'>Discover Yourself</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: left; color: black';>All Time Hits</h4>", unsafe_allow_html=True)
    uris=utils.get_top_tracks()
    tracks = utils.get_tracks_for_display(uris)
    with st.container():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([0.5, 3, 0.5, 3, 0.5, 3, 0.5])
        for i, (track, uri) in enumerate(zip(tracks, uris)):
                if i%3==0:
                    with col2:
                        components.html(
                            track,
                            height=400,
                        )
                        if st.button("Like", key=uri):
                            add_feedback(uri)
                elif i%3==1:
                    with col4:
                        components.html(
                            track,
                            height=400,
                        )
                        if st.button("Like", key=uri):
                            add_feedback(uri)
                elif i%3==2:
                    with col6:
                        components.html(
                            track,
                            height=400,
                        )
                        if st.button("Like", key=uri):
                            add_feedback(uri)

weather_id=0

#Weather Tunes page
def weather_recommendation():
    global weather_id
    # utils.set_png_as_page_bg(os.path.join(cwd, 'images\img4.png'))
    utils.set_png_as_page_bg(r'C:\Users\anany.DESKTOP-OVOHHUN\OneDrive\Documents\MS Engage\music-recommendation-system\streamlitapp\images\img4.png')
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: black;'>Weather Tunes</h1>", unsafe_allow_html=True)
    st.write("Are you someone whose music tastes get affected by the weather around you? Well then, you're just at the right place!")
    city=st.text_input('Enter a city')
    if city:
        weather = openweather.getweather(city)
        if  weather == 800:
            weather_id = 0  #sunny
        if weather == 8:
            weather_id = 1  #windy
        elif weather == 2 or weather == 3 or  weather == 5:
            weather_id = 2  #rain
        elif weather == 6 or weather == 7:
            weather_id = 3  #snow
        st.markdown('## Recommendations')
        uris = utils.get_weather_recommendations(weather_id)
        tracks = utils.get_tracks_for_display(uris)
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([1,2,1,2,1])    
            for i, track in enumerate(tracks):
                if i%2==0:
                    with col2:
                        components.html(
                            track,
                            height=400,
                        )
                else:
                    with col4:
                        components.html(
                            track,
                            height=400,
                        )

def feedback_page():
    st.markdown("<br>", unsafe_allow_html=True)
    """
    ### Let us know what you think of our website:
    
    """
    st.markdown("<br>", unsafe_allow_html=True)
    name=st.text_input('Enter your name')
    feedback=st.text_area('Give feedback')
    st.write('Thank you for visting our website!')

def my_sidebar():
    with st.sidebar:
        st.info('**Music Recommendation System**')
        home_button = st.button("Home")
        discover_button = st.button('Discover Yourself')
        weather_button = st.button('Weather Tunes')
        feedback_button = st.button('Give Feedback')
        if home_button:
            st.session_state.app_mode = 'home'
        if weather_button:
            st.session_state.app_mode = 'weather'
        if discover_button:
            st.session_state.app_mode = 'discover'
        if feedback_button:
            st.session_state.app_mode = 'feedback'

    

def main():
    my_sidebar()
    if st.session_state.app_mode == 'home':
        home_page()
    if st.session_state.app_mode == 'weather':
        weather_recommendation()
    if st.session_state.app_mode == 'discover':
        discover_page()
    if st.session_state.app_mode == 'feedback' :
        feedback_page()

if __name__ == '__main__':
    main()