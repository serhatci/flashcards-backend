"""Provides functions for Database methods"""


def frontend_user_data(user_data):
    """Convert user data to suitable format for frontend
    """
    titles = [{'str': item['title'], 'camelCase': camel_case(
        item['title'])} for item in user_data['topics']]
    flashcards = {camel_case(item['title']): item['flashcards']
                  for item in user_data['topics']}
    return {'username': user_data['userName'],
            'titles': titles,
            'flashcards': flashcards}


def backend_user_data(user_data):
    """Convert user data to suitable format for backend
    """
    # userID: currentUser.uid,
    # flashcard_titles: titles,
    # cards: flashcards,

    def matching_cards(title):
        try:
            return user_data['cards'][title]
        except KeyError:
            return []

    topics = [{'title': title['str'],
               'flashcards': matching_cards(title['camelCase'])}
              for title in user_data['flashcard_titles']]
    return user_data['userID'], topics


def camel_case(word):
    """Converts words or sentences to camelCase
    """
    snake = ''.join(x.capitalize() for x in word.split(' '))
    return (snake[0].lower() + snake[1:])
