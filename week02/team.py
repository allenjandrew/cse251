"""
Course: CSE 251 
Lesson: L02 Team Activity
File:   team.py
Author: <Add name here>

Purpose: Playing Card API calls
Website is: http://deckofcardsapi.com

Instructions:

- Review instructions in I-Learn.

"""

from collections.abc import Callable, Iterable, Mapping
from datetime import datetime, timedelta
import threading
from typing import Any
import requests
import json

# Include cse 251 common Python files
from cse251 import *

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_thread(threading.Thread):
    # TODO - Add code to make an API call and return the results
    # https://realpython.com/python-requests/

    # Constructor
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.data = {}
    
    # On Start
    def run(self):
        response = requests.get(self.url)
        if response.status_code == 200: # if this is a valid response:
            self.data = response.json()
            # print(self.data)

class Deck:

    # Constructor
    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52
        # self.draw_card()


    def reshuffle(self):
        print('Reshuffle Deck')
        # TODO - add call to reshuffle
        thread = Request_thread(f"https://deckofcardsapi.com/api/deck/{self.id}/shuffle/")
        thread.start()
        thread.join()
        self.deck = thread.data
        # print(self.deck)


    def draw_card(self):
        # TODO add call to get a card
        thread = Request_thread(f"https://deckofcardsapi.com/api/deck/{self.id}/draw/?count=1")
        thread.start()
        thread.join()
        self.card = thread.data['cards'][0]
        # print(self.card)
        self.remaining = thread.data["remaining"]
        # print(self.remaining)
        return f"{self.card['value'].capitalize()} of {self.card['suit'].capitalize()}"

    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = 'vmog8j8tu4vy' # this id will be invalid after 2 weeks

    # Testing Code >>>>>
    deck = Deck(deck_id)
    for i in range(55):
        card = deck.draw_endless()
        print(f'card {i + 1}: {card}', flush=True)
    print()
    # <<<<<<<<<<<<<<<<<<

    # runner = Request_thread(deck_id)