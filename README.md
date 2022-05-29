# Music-Recommendation-System
This repository contains my submission for MS Engage 2022. I have worked on the Algorithms challenge and built a Music Recommendation System - Musically.

# Set Up and Installation
1. Datset used for preprocessing and analysis is given here : https://www.kaggle.com/saurabhshahane/spotgen-music-dataset
2. Download the dataset and extract all the files in a folder called 'Data' that is located in the current working directory.
4. Clone the repo in your current working directory.
5. In the terminal, give the command : streamlit run app.py
6. You're now all set to use Musically!

# Features
1. **Weather Tunes** : </br>
   This page uses OpenWeatherMap API to get weather conditions based on the city entered by the user. Songs are recommended from the dataset based on these weather   conditions.
         ![weather-tunes](https://user-images.githubusercontent.com/75329906/170872708-9cedf70e-43c8-4c03-b13a-33666dd15e04.jpeg)

2. **Discover Yourself** : </br>
  This page displays the most popular tracks from the dataset. If the user presses 'Like', then he is recommended more songs using the KNN Model.
         ![discover-yourself](https://user-images.githubusercontent.com/75329906/170872728-a2562886-da33-4791-8a99-df10e50f3237.jpeg)
