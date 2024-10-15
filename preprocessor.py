import re
import pandas as pd

def preprocess(data):
    pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\]\s'

    dates = re.findall(pattern, data)
    msgs = re.split(pattern, data)[1:]

    dates = [date.replace('[', '').replace(']', '') for date in dates]

    df = pd.DataFrame({'user_msg': msgs, 'date': dates})
    # converting date to datetime object
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %H:%M:%S ', dayfirst=True)

    def identify_group_notification(message):
        # Check if the message starts with a specific pattern indicating a group notification
        group_notification_patterns = [
            "You created group",
            "You removed",
            "You added",
            "Messages and calls are end-to-end encrypted.",
            "You created group",
            "Group name changed to",
            "has joined the group",
            "was added",
            "joined using this group's invite link",
            "has been made an admin",
            "Group description changed",
            "Invite link to this group has been updated",
            "Group media sharing has been turned off/on"
        ]
        for pattern in group_notification_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return True
        return False

    users = []
    messages = []
    for message in df['user_msg']:
        if identify_group_notification(message):
            users.append('group_notifications')
            messages.append(message)
        else:
            entry = re.split(r'([\w\W]+?):\s', message)
            users.append(entry[1])
            messages.append(entry[2])

    df['user'] = users
    df['message'] = messages
    df.drop('user_msg', axis='columns', inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['second'] = df['date'].dt.second

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + ' - ' + str('00'))
        elif hour == 0:
            period.append(str('00') + ' - ' + str(hour + 1))
        else:
            period.append(str(hour) + ' - ' + str(hour + 1))
    df['period'] = period

    return df