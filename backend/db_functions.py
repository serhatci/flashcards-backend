"""Provides functions for Database methods"""


def organize_user_data(user_data):
    """Organize user data suitable for front end request
    """
    titles = [{'str': item['title'], 'camelCase': camel_case(
        item['title'])} for item in user_data['topics']]
    flashcards = [{item['title']: [item['flashcards']]}
                  for item in user_data['topics']]
    return {'username': user_data['userName'],
            'titles': titles,
            'flashcards': flashcards}


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
