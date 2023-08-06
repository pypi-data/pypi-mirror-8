# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from estnltk.javaprocess import JavaProcess, JAVARES_PATH
from estnltk.textprocessor import TextProcessor
from estnltk.core import JsonPaths
from estnltk.names import *

from pprint import pprint

import os
import json
import datetime


RENAMING_MAP = {
    'temporalFunction': TMX_TEMP_FUNCTION,
    'anchorTimeID': TMX_ANCHOR,
    'beginPoint': TMX_BEGINPOINT,
    'endPoint': TMX_ENDPOINT,
}

class TimexTagger(JavaProcess, TextProcessor):
    
    def __init__(self):
        JavaProcess.__init__(self, 'Ajavt.jar', ['-pyvabamorf', '-r', os.path.join(JAVARES_PATH, 'reeglid.xml')])

    def process_json(self, corpus, **kwargs):
        process_as_whole = kwargs.get('process_as_whole', False)
        if process_as_whole:
            # Process all the sentences together
            return self.process_sentences(corpus, process_json=True)
        # Process each sentence independently 
        for sentence_ptr in JsonPaths.words.find(corpus):
            self.process_words(sentence_ptr.value, **kwargs)
        return corpus

    def process_corpus(self, corpus, **kwargs):
        process_as_whole = kwargs.get('process_as_whole', False)
        if process_as_whole:
            # Process all the sentences together
            return self.process_sentences(corpus, process_json=False)
        # Process each sentence independently 
        for sentence in corpus.sentences:
            self.process_words(sentence[WORDS], **kwargs)
        return corpus

    def process_words(self, words, **kwargs):
        remove_unnormalized_timexes = kwargs.get('remove_unnormalized_timexes', True)
        creation_date = kwargs.get('creation_date', datetime.datetime.now())
        creation_date = creation_date.strftime('%Y-%m-%dT%H:%M')
        sentence = {
            'dct': creation_date,
            WORDS: words
            }
        processed_words = self.rename_attributes(json.loads(self.process_line(json.dumps(sentence)))[WORDS])
        if remove_unnormalized_timexes:
            processed_words = self.remove_timexes_with_no_value_type(processed_words)
        for w, p in zip(words, processed_words):
            if TIMEXES in p:
                w[TIMEXES] = p[TIMEXES]
        return words

    # Processes all the sentences together
    def process_sentences(self, corpus, process_json=False, **kwargs):
        remove_unnormalized_timexes = kwargs.get('remove_unnormalized_timexes', True)
        creation_date = kwargs.get('creation_date', datetime.datetime.now())
        creation_date = creation_date.strftime('%Y-%m-%dT%H:%M')
        document = {
            'dct': creation_date,
            SENTENCES: corpus.sentences \
                       if not process_json else \
                       [ {WORDS:sentence_ptr.value} for sentence_ptr in JsonPaths.words.find(corpus) ]
        }
        processed_sentences = json.loads(self.process_line(json.dumps(document)))[SENTENCES]
        for input_sentence, processed_sentence in zip(document[SENTENCES], processed_sentences):
            processed_sentence = self.rename_attributes( processed_sentence[WORDS] )
            if remove_unnormalized_timexes:
                processed_sentence = self.remove_timexes_with_no_value_type(processed_sentence)
            for i in range(len( input_sentence[WORDS] )):
                input_word = input_sentence[WORDS][i]
                processed_word = processed_sentence[i]
                if TIMEXES in processed_word:
                    input_word[TIMEXES] = processed_word[TIMEXES]
        return corpus

    def rename_attributes(self, sentence):
        for word in sentence:
            if TIMEXES in word:
                for timex in word[TIMEXES]:
                    # rename javaStyle to python_style
                    for oldKey, newKey in RENAMING_MAP.items():
                        if oldKey in timex:
                            timex[newKey] = timex[oldKey]
                            del timex[oldKey]
                    # trim "t" from id and anchor time
                    for k, v in timex.items():
                        if k in [TMX_ID, TMX_ANCHOR] and isinstance(v, str) and v.startswith('t'):
                            timex[k] = int(v[1:])
        return sentence

    # Removes timexes that have no value or type specified
    # ( e.g. anaphoric references 'samal ajal', 'tol ajal' etc. that were left unsolved )
    def remove_timexes_with_no_value_type(self, sentence):
        seenTimexes     = dict()
        timexesToRemove = dict()
        for word in sentence:
            if TIMEXES in word:
                newTimexes = []
                for timex in word[TIMEXES]:
                    if timex[TMX_ID] not in seenTimexes:
                        seenTimexes[timex[TMX_ID]] = 1
                        if TMX_TYPE not in timex or TMX_VALUE not in timex:
                            timexesToRemove[timex[TMX_ID]] = 1
                        else:
                            newTimexes.append( timex )
                    elif timex[TMX_ID] in seenTimexes and timex[TMX_ID] not in timexesToRemove:
                        newTimexes.append( timex )
                if newTimexes:
                    word[TIMEXES] = newTimexes
                else:
                    del word[TIMEXES]
        return sentence
