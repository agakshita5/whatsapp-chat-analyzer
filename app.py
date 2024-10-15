import streamlit
import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sn

streamlit.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data= bytes_data.decode('utf-8')

    df=preprocessor.preprocess(data)

    # fetch unique users
    user_list= df['user'].unique().tolist()
    # some changes to user_list
    user_list.remove('group_notifications')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user= st.sidebar.selectbox('Show analysis wrt', user_list)

    if st.sidebar.button('Show Analysis'):

        # top stats
        num_messages, words, num_media_messages, num_links= helper.fetch_stats(selected_user, df)
        st.title('Top Statistics')
        col1, col2, col3, col4= st.columns(4, vertical_alignment='bottom')

        with col1:
            st.markdown('<h3 style="font-weight: normal;"><div style="margin-top: 20px">Total Messages</div></h3>', unsafe_allow_html=True)
            st.title(num_messages)
        with col2:
            st.markdown('<h3 style="font-weight: normal;"><div style="margin-top: 20px">Total words</div></h3>', unsafe_allow_html=True)
            st.title(words)
        with col3:
            st.markdown('<h3 style="font-weight: normal;"><div style="margin-top: 20px">Media Shared</div></h3>', unsafe_allow_html=True)
            st.title(num_media_messages)
        with col4:
            st.markdown('<h3 style="font-weight: normal;"><div style="margin-top: 20px">Links Shared</div></h3>', unsafe_allow_html=True)
            st.title(num_links)

        # montly_timeline
        timeline_df = helper.monthly_timeline(selected_user, df)
        st.title('Monthly Timeline')

            # st.dataframe(timeline_df)
        fig, ax = plt.subplots()
        ax.plot(timeline_df['time'], timeline_df['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily_timeline
        daily_timeline = helper.daily_timeline(selected_user, df)
        st.title('Daily Timeline')
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='grey')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # fetching busiest users in the grp chat (Group Level)
        if  selected_user=='Overall':
            st.title('Most busy users')
            x, busyUsers_df= helper.fetch_most_busy_user(df)
            fig, ax= plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='#FF4B58')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(busyUsers_df)

        # activity map
        st.title('Activity Map')
        col1, col2= st.columns(2)

        with col1:
            st.header('Most Busy Day')
            busy_day= helper.week_activity_map(selected_user, df)
            fig, ax= plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header('Most Busy Month')
            busy_month= helper.month_activity_map(selected_user, df)
            fig, ax= plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # weekly activity map
        st.title('Weekly Activity Map')
        fig, ax= plt.subplots()
        user_map= helper.weekly_activity_heatmap(selected_user, df)
        ax = sn.heatmap(user_map)
        st.pyplot(fig)

        # WordCloud
        st.title('Wordcloud')
        wc_df= helper.create_wordcloud(selected_user, df)
        if wc_df!=None:
            fig, ax = plt.subplots()
            ax.imshow(wc_df)
            st.pyplot(fig)
        else:
            st.write("No text found for this user. Please select another user or wait for them to send a message.")

        # most common words
        most_common_df= helper.fetch_most_common_words(selected_user, df)
        fig, ax= plt.subplots()
        ax.barh(most_common_df['word'], most_common_df['count'], color='brown')
        # plt.xticks(rotation='vertical')
        st.title('Most common words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_analysis(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            if emoji_df.shape[0] > 0:
                st.dataframe(emoji_df)
            else:
                st.write('No emojis found in the messages.')
        with col2:
            if emoji_df.shape[0] > 0:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
                st.pyplot(fig)
            else:
                st.write("")


