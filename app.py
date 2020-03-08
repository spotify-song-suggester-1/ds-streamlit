# imports
import altair as alt
import requests
import streamlit as st
import urllib
import pandas as pd

# url to pull from
base_url = 'https://spotify-api-ds.herokuapp.com/'

def main():

    # all sidebar stuff

    # title
    title = st.sidebar.markdown('## spotify recommender')
    subtiitle = st.sidebar.markdown('streamlit frontend')

    # query spotify for songs
    user_input = st.sidebar.text_input("search spotify for a song.", '4\'33"')

    query_response = requests.get(base_url+'query/'+urllib.parse.quote(user_input)).json()


    # get a list of songs, and a dict to map them to ids
    songdict = {}
    songs = []
    for element in query_response:
        songdict[element['track_name']+', '+element['artist_name']] = element['track_id']
        songs.append(element['track_name']+', '+element['artist_name'])


    # have user choose a track
    song = st.sidebar.selectbox("choose a track.", songs)

    recommendation_response = requests.get(base_url+'recommend/'+songdict[song]).json()

    # team info
    st.sidebar.markdown('')
    st.sidebar.markdown('find us elsewhere:')
    st.sidebar.markdown('[tally wiesenberg](https://www.github.com/tallywiesenberg)')
    st.sidebar.markdown('[charles vanchieri](https://www.github.com/cvanchieri)')
    st.sidebar.markdown('[krista shepard](https://www.github.com/kryssyco)')
    st.sidebar.markdown('[sanjay krishna](https://www.github.com/sanjaykmenon)')
    st.sidebar.markdown('[connor sanderford](https://www.github.com/crsanderford)')


    # features we want to display
    featurelist = ['acousticness', 'danceability', 'energy',
                'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
                'speechiness', 'time_signature', 'valence']
    featurediffs = [feature + '_diff' for feature in featurelist]


    # make plots for every recommended song
    for element in recommendation_response:

        st.write(element['track_name'] + ', ' +element['artist_name'])
        st.write('genre: ', element['genre'])

        # plotting the original values
        labelstoplot = []
        valuestoplot = []

        difflabelstoplot = []
        diffvaluestoplot = []

        labels, values = zip(*element.items())
        
        # plotting the original values
        for ii in range(0,len(labels)):
            if labels[ii] in featurelist:
                labelstoplot.append(labels[ii])
                valuestoplot.append(values[ii])
            if labels[ii] in featurediffs:
                difflabelstoplot.append(labels[ii])
                diffvaluestoplot.append(values[ii])

        source = pd.DataFrame({
        'labels': labelstoplot,
        'recommended_values': valuestoplot,
        'diffs': diffvaluestoplot
                            })


        chart_normal = alt.Chart(source, title='feature values').mark_bar().encode(
                                                        x=alt.X('labels', title=None, sort=None),
                                                        y=alt.Y('recommended_values', title=None, sort=None),
                                                        color=alt.Color('recommended_values', title=None, scale=alt.Scale(scheme="goldorange")),
                                                        tooltip=[alt.Tooltip('recommended_values', title=None)]
            ).configure_mark(opacity=0.8).properties(width=700, height=400)
                                                    

        st.altair_chart(chart_normal)

        # plotting percent differences
        source['origin_song_values'] = source['recommended_values'] - source['diffs']
        source['percent_diffs'] = source['diffs']/source['origin_song_values']

        chart_diffs = alt.Chart(source, title='feature differences').mark_bar().encode(
                                                        x=alt.X('labels', title=None, sort=None),
                                                        y=alt.Y('percent_diffs', title=None, sort=None),
                                                        color=alt.Color('percent_diffs', title=None, scale=alt.Scale(scheme="goldorange")),
                                                        tooltip=[alt.Tooltip('percent_diffs', title=None)]
            ).configure_mark(opacity=0.8).properties(width=700, height=400)
                                                    

        st.altair_chart(chart_diffs)

if __name__ == "__main__":
    main()
    


