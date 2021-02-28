"""Provides functions for Database methods"""


def combine(user_info, user_flashcards):
    """Combines username, user topics and flashcards to a single dict
    """
    username = {"username": user_info['username']}
    titles = {"titles":
              [
                  {"str": i["title"],
                   "camelCase":camel_case(i["title"])}
                  for i in user_info['topics']
              ]}
    return {**username, **titles, **user_flashcards}


def camel_case(word):
    """Converts words or sentences to camelCase
    """
    snake = ''.join(x.capitalize() for x in word.split(' '))
    return (snake[0].lower() + snake[1:])


def compare_topics(existing_topics, new_topics):
    """Creates new topics of user for updating DB"""
    remaining = [item for item in existing_topics if item['title']
                 in new_topics]
    new_titles = list(
        set(new_topics) - set([topic['title'] for topic in remaining]))
    new_topics = [{'title': new_topic, 'flashcards': []}
                  for new_topic in new_titles]
    return new_topics + remaining
