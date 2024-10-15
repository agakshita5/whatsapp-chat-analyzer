from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extracter = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != 'Overall': # specific User
        df = df[df['user'] == selected_user] # change df accordingly

    # 1. no. of msgs
    num_messages = df.shape[0]

    # 2. no. of words
    words = []
    for message in df['message']:
        words.extend(message.split())  # message.split(' ') --> list of word

    # 3. no. of media
    media_patterns = ['image omitted', 'audio omitted', 'document omitted', 'sticker omitted', 'GIF omitted', 'Contact card omitted']
    num_media_messages = df[df['message'].str.contains('|'.join(media_patterns), regex=True)].shape[0]

    # 4. no. of links
    links_lst=[]
    for message in df['message']:
        links_lst.extend(extracter.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links_lst)


def fetch_most_busy_user(df):
    x = df['user'].value_counts().head()
    busyUsers_df = round((df['user'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns={'index':'name', 'count': 'percent'})
    return x, busyUsers_df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall': # specific User
        df = df[df['user'] == selected_user] # change df accordingly

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    temp = df[df['user'] != 'group_notifications']
    media_patterns = ['image omitted', 'audio omitted', 'document omitted', 'sticker omitted', 'GIF omitted',
                      'Contact card omitted']
    temp = temp[~ temp['message'].str.contains('|'.join(media_patterns), regex=True)]

    def remove_stopwords(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        y = [word for word in y if word != '\u200e']
        return " ".join(y)

    wc= WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message']= temp['message'].apply(remove_stopwords)
    message_text = temp['message'].str.cat(sep=' ')
    if message_text:
        wc_df= wc.generate(message_text)
        return wc_df
    else:
        # default_img = np.zeros((300, 300, 3))  # Create a blank white image
        # return default_img
        # st.write("No text found for this user. Please select another user or wait for them to send a message.")
        return None
def fetch_most_common_words(selected_user, df):
    if selected_user != 'Overall': # specific User
        df = df[df['user'] == selected_user] # change df accordingly

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    temp = df[df['user'] != 'group_notifications']
    media_patterns = ['image omitted', 'audio omitted', 'document omitted', 'sticker omitted', 'GIF omitted',
                      'Contact card omitted']
    temp = temp[~ temp['message'].str.contains('|'.join(media_patterns), regex=True)]

    words = []
    for message in temp['message']:  # temp with no grp_not and media omitted msgs
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    words = [word for word in words if word != '\u200e']
    most_common_df= pd.DataFrame(Counter(words).most_common(), columns=['word', 'count'])
    return most_common_df.head(20)

def emoji_analysis(selected_user, df):
    if selected_user != 'Overall': # specific User
        df = df[df['user'] == selected_user] # change df accordingly

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df= pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall': # specific User
        df = df[df['user'] == selected_user] # change df accordingly

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall': # specific User
        df = df[df['user'] == selected_user] # change df accordingly

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall': # specific User
        df = df[df['user'] == selected_user] # change df accordingly

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall': # specific User
        df = df[df['user'] == selected_user] # change df accordingly

    return df['month'].value_counts()

def weekly_activity_heatmap(selected_user, df):
    if selected_user != 'Overall': # specific User
        df = df[df['user'] == selected_user] # change df accordingly

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap