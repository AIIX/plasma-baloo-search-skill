import re
import sys
import subprocess
import json
import requests
import unidecode
import dbus
from adapt.intent import IntentBuilder
from os.path import join, dirname
from string import Template
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.skills.context import *
from mycroft.util import read_stripped_lines
from mycroft.util.log import getLogger
from mycroft.messagebus.message import Message

__author__ = 'Aix'

LOGGER = getLogger(__name__)

class PlasmaBalooSearch(MycroftSkill):
    def __init__(self):
        super(PlasmaBalooSearch, self).__init__(name="PlasmaBalooSearch")
        self.term_index = dirname(__file__) + '/term.json'

    @intent_handler(IntentBuilder("BalooSearchIntent").require("LocalSearchKeyword").build())
    def handle_local_baloo_search_context_intent(self, message):
        utterance = message.data.get('utterance').lower()
        utterance = utterance.replace(message.data.get('LocalSearchKeyword'), '')
        searchString = utterance.split(" ")
        getTerm = self.filterTerm(searchString[1])
        searchTerm = 'baloosearch {0} {1}'.format(getTerm, searchString[2])
        subresult = subprocess.Popen(searchTerm, stdout=subprocess.PIPE, shell=True)
        resultblock = subresult.communicate()[0].splitlines()
        speakblock = "Displaying {0} search results".format(getTerm)
        self.speak(speakblock)
        self.enclosure.ws.emit(Message("balooObject", {'desktop': {'data': resultblock, 'searchType': getTerm}}))

    def filterTerm(self, keywords):
        keyword = keywords.lower()
        with open(self.term_index) as json_data:
            vdict = json.load(json_data)
            if keyword in vdict["audio"]:
                return "type:audio"
            elif keyword in vdict["video"]:
                return "type:video"
            elif keyword in vdict["image"]:
                return "type:image"
            elif keyword in vdict["document"]:
                return "type:document"
            elif keyword in vdict["spreadsheet"]:
                return "type:spreadsheet"
            elif keyword in vdict["presentation"]:
                return "type:presentation"
            elif keyword in vdict["text"]:
                return "type:text"
            elif keyword in vdict["archive"]:
                return "type:archive"
            else:
                return ""
    
    def stop(self):
        pass
    
def create_skill():
    return PlasmaBalooSearch()
