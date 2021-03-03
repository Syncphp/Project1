"""
************************************************************************************************************************
* Student Name: ""                                                                                           *
* Project Name: Project 1 - Streamlit + New York Times API + JSON Documents                                            *
* Due Date: 2/27/2021                                                                                                  *
* Last Updated: 2/19/2021                                                                                              *
************************************************************************************************************************
"""


import streamlit as st
import numpy as np
import pandas as pd
import requests
import main_functions
import json
import requests
import nltk
from nltk import sent_tokenize, word_tokenize
#nltk.download("punkt")
#nltk.download("stopwords")
from nltk.probability import  FreqDist
from nltk.corpus import stopwords
from pprint import pprint
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def topics(options):
    url = "https://api.nytimes.com/svc/topstories/v2/" + options + ".json?api-key=" + apiKey()
    response = requests.get(url).json()
    main_functions.save_to_file(response,"JSON_Files/response.json")


def apiKey():
    api_key_dic = main_functions.read_from_file("JSON_Files/api_key.json")
    api_key = api_key_dic["my_key"]
    return api_key

def freqDistribution(fdist3):
    chart_data = pd.DataFrame(
        fdist3.most_common(10),
        columns=["Words", "Count"])
    chart_data = chart_data.rename(columns={'Words': 'index'}).set_index('index')
    st.line_chart(chart_data)

def wordCloud(str1):
    wordcloud = WordCloud(width=800, height=400).generate(str1)
    plt.figure(figsize=(20, 10))
    fig, ax = plt.subplots()
    plt.imshow(wordcloud)
    ax.set_axis_off()
    st.write(fig)

def articlePart(article_set,days):
    url1 = "https://api.nytimes.com/svc/mostpopular/v2/" + article_set + "/" + days + ".json?api-key=" + apiKey()
    articles = requests.get(url1).json()
    main_functions.save_to_file(articles, "JSON_Files/articles.json")


st.title("COP 4813 - Web Application Programming")
st.header("Project 1")

options = st.selectbox("Select one of the following topics", ["","arts", "automobiles", "books", "business", "fashion",
                                                              "food", "health", "home", "insider", "magazine", "movies",
                                                              "nyregion", "obituaries","opinion", "politics", "realestate",
                                                              "science", "sports", "sundayreview", "technology","theater",
                                                              "t-magazine", "travel", "upshot", "us", "world"])
if options:
    topics(options)
    st.success("You selected the " + options + " topic.")


selection = st.checkbox("Click here to generate frequency distribution")

my_articles = main_functions.read_from_file("JSON_Files/response.json")

str1 = ""

for i in my_articles["results"]:
  str1 = str1 + i["abstract"]


sentences = sent_tokenize(str1)
words = word_tokenize(str1)
fdist = FreqDist(words)


words_no_punc = [] 

for w in words:
    if w.isalpha():
        words_no_punc.append(w.lower())


fdist2 = FreqDist(words_no_punc)

stopwords = stopwords.words("english")

clean_words = []

for w in words_no_punc:
    if w not in stopwords:
        clean_words.append(w)


fdist3 = FreqDist(clean_words)

if selection:
    freqDistribution(fdist3)


selection1 = st.checkbox("Click here to generate word cloud")

if selection1:
    wordCloud(str1)

article_set = st.selectbox("Select your preferred set of articles",["","emailed","shared","viewed"])

days = st.selectbox("Select the period of time (Last days)",["","1","7","30"])

if article_set and days:
    articlePart(article_set,days)
    my_articles1 = main_functions.read_from_file("JSON_Files/articles.json")
    str2 = ""

    for i in my_articles1["results"]:
        str2 = str2 + i["abstract"]

    wordCloud(str2)
