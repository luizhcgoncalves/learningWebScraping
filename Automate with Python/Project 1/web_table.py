# pip install pandas
import pandas as pd

episodes = pd.read_html('https://en.wikipedia.org/wiki/List_of_The_Simpsons_episodes_(seasons_1%E2%80%9320)')
# return the list of all tables in the website