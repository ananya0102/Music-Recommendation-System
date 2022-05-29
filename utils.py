import streamlit as st
import pandas as pd
import base64
from sklearn.neighbors import NearestNeighbors

#loads the CSS file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

#used to set a custom image as a background
def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

#loads the csv file
def load_data():
    df = pd.read_csv(r"C:\Users\anany.DESKTOP-OVOHHUN\OneDrive\Documents\MS Engage\music-recommendation-system\streamlitapp\filtered_track_df.csv") #change the location
    df['genres'] = df.genres.apply(lambda x: [i[1:-1] for i in str(x)[1:-1].split(", ")])
    exploded_track_df = df.explode("genres")
    return exploded_track_df

data=load_data()
#sort the values by popularity before using it any further
data=data.sort_values(by='popularity', ascending=False)[:5000]
data=data.drop_duplicates(subset='uri', keep='first', inplace=False)

def get_weather_recommendations(x):
    global data
    #assign weights to audio features based on the weather conditions
    a=0 
    i=0  
    v=0 
    if x==0: #sunny
        i=0.25
        a=0.25
        v=1
    elif x==1: #windy
        i=0.75
        a=0.25
        v=0.75
    elif x==2: #rain
        i=0.5
        a=1
        v=0.25
    elif x==3: #snow
        i=1
        a=0.5
        v=0.5
    acousticness = data['acousticness'].tolist()
    valence = data['valence'].tolist()
    instrumentalness = data['instrumentalness'].tolist()
    uri=data['uri'].tolist()
    total=list(zip(uri, acousticness, valence, instrumentalness))
    #we sort the values obtained based on weights and audio features
    sorted_total=sorted([(t[0], (t[1]*a+t[2]*v+t[3]*i)) for t in total], key=lambda sort_key: sort_key[1], reverse=True)
    uris=[x[0] for x in sorted_total[:10]]
    return uris

#helper function to get the list of urls only
def get_top_tracks():
    uris=data['uri'].tolist()
    return uris[:9]  #for now it recommends top 9 songs only based on popularity

#helper function to display the recommendations
def get_tracks_for_display(uris):
    tracks=[]
    for uri in uris:
            track = """<iframe src="https://open.spotify.com/embed/track/{}" width="260" height="300" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(uri)
            tracks.append(track)
    return tracks

#audio features based on which K nearnest neighbours are calculated
audio_feats = ["acousticness", "danceability", "energy", "instrumentalness", "valence"]
def n_neighbors_uri_audio(track_uri):
    idx=data[data['uri']==track_uri]
    genre=idx['genres'].to_numpy()
    #to ensure we get songs of the same genre only
    genre_data = data[data["genres"]==genre[0]]
    neigh = NearestNeighbors()
    neigh.fit(genre_data[audio_feats].to_numpy())
    a=(idx['acousticness'].to_numpy())[0]
    d=(idx['danceability'].to_numpy())[0]
    e=(idx['energy'].to_numpy())[0]
    i=(idx['instrumentalness'].to_numpy())[0]
    v=(idx['valence'].to_numpy())[0]
    test_feat = [a, d, e, i, v]
    #get K nearest neighbour model recommendation of songs 
    n_neighbors = neigh.kneighbors([test_feat], n_neighbors=len(genre_data), return_distance=False)[0]

    uris = genre_data.iloc[n_neighbors]["uri"].tolist()
    return uris[1:6]  #in order to remove the first recommendation, which is the song itself
