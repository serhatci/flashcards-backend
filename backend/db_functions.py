"""Provides functions for Database methods"""


def combine(user_info, user_flashcards):
    "combines username, user topics and flashcards to a single dict"
    username = {"username": user_info['username']}
    titles = {"titles":
              [
                  {"str": i["title"],
                   "camelCase":camel_case(i["title"])}
                  for i in user_info['topics']
              ]}
    return {**username, **titles, **user_flashcards}


def camel_case(word):
    """converts words or sentences to camelCase"""
    snake = ''.join(x.capitalize() for x in word.split(' '))
    return (snake[0].lower() + snake[1:])
