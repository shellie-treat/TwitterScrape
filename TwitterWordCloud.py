import pandas as pd
import streamlit as st
import os 
from datetime import date
import snscrape
import streamlit_wordcloud as wordcloud
import matplotlib.pyplot as plt
from math import isnan
import PIL
import base64
from wordcloud import WordCloud
from wordcloud import STOPWORDS

def main():
	image=PIL.Image.open(r'evergrain.png')
	st.sidebar.image(image,use_column_width=True)    
	page = st.sidebar.selectbox("Choose a page", ["Twitter"])
	today = date.today()
	end_date = today
	from_date='2021-10-30'

	if page == "Homepage":
		st.write("WELCOME TO EVERGRAIN WORD CLOUDS")

	elif page == "Twitter":
		st.title("Evergrain Twitter Search")
		search_term = st.text_input('search term')
		if search_term:
			max_results = 500
			searchterm = "snscrape --format '{content!r}'"+ f" --max-results {max_results} --since {from_date} twitter-search '{search_term} until:{end_date}' > searchterm.txt"
			os.system(searchterm)
			df2 = pd.read_csv('searchterm.txt', names=['content'])
			data = df2.groupby(['content']).size().reset_index()
			st.markdown(get_data(data), unsafe_allow_html=True)
			tweet=data['content']
			tweet.to_csv('tweets.csv', encoding='utf-8', index=False)
			fields = ['content']
			text2 = pd.read_csv('tweets.csv', usecols=fields)
			text3 = ' '.join(text2['content'])
			stop_words = STOPWORDS.update(["https", "co","t"])
			wordcloud2 = WordCloud(stopwords = stop_words).generate(text3)
			plt.imshow(wordcloud2)
			plt.axis("off")
			plt.show()
			st.set_option('deprecation.showPyplotGlobalUse', False)
			st.pyplot(bbox_inches='tight')

			for row in df2['content'].iteritems():
				st.write(row)



def get_data(data):
	csv = data.to_csv().encode()
	b64 = base64.b64encode(csv).decode()
	href = f'<a href="data:file/csv;base64,{b64}" download="TwitterData.csv" target="_blank">Download csv file</a>'
	return href


if __name__ == "__main__":
    main()
