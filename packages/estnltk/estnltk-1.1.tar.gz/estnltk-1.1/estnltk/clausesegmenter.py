# -*- coding: utf-8 -*-

'''
Wrapper class around Java-based clause segmenter (Osalausestaja). 
Allows to process results sentence by sentence. 
'''
from __future__ import unicode_literals, print_function

from estnltk.core import JsonPaths
from estnltk.names import *
from estnltk.javaprocess import JavaProcess
from estnltk.textprocessor import TextProcessor

from copy import deepcopy
from pprint import pprint

import json
import os.path
import re

CLAUSE_ANNOT = 'clauseAnnotation'

class ClauseSegmenter(JavaProcess, TextProcessor):
    ''' Wrapper class around Java-based clause segmenter (Osalausestaja). 
        Allows to process results sentence by sentence. 
        ''' 
    
    def __init__(self):
        JavaProcess.__init__(self, 'Osalau.jar', ['-pyvabamorf'])
        
    def process_corpus(self, corpus, **kwargs):
        for sentence in corpus.sentences:
            self.mark_annotations(sentence)
        return corpus
        
    def process_json(self, corpus, **kwargs):
        for sentence in JsonPaths.words.find(corpus):
            sentence.value = self.mark_annotations({WORDS: sentence.value})[WORDS]
        return corpus
    
    def detect_annotations(self, sentence):
        prep_sentence = self.prepare_sentence(sentence)
        result = json.loads(self.process_line(prep_sentence))
        words = self.annotate_indices(result[WORDS])
        return self.rename_annotations(words)
    
    def mark_annotations(self, sentence):
        annotations = self.detect_annotations(sentence)
        assert len(sentence[WORDS]) == len(annotations)
        for w, a in zip(sentence[WORDS], annotations):
            for k, v in a.items():
                w[k] = v
        return sentence
    
    def prepare_sentence(self, sentence):
        '''Prepare the sentence for segment detection.'''
        # depending on how the morphological analysis was added, there may be
        # phonetic markup. Remove it, if it exists.
        for word in sentence[WORDS]:
            for analysis in word[ANALYSIS]:
                analysis[ROOT] = analysis[ROOT].replace('~', '')
                analysis[ROOT] = re.sub('[?<\]]([aioueöäõü])', '\\1', analysis[ROOT])
        return json.dumps(sentence)
    
        
    def annotate_indices(self, sentence):
        '''Add clause indexes to already annotated sentence.'''
        max_index = 0
        max_depth = 1
        stack_of_indexes = [ max_index ]
        for token in sentence:
            if CLAUSE_ANNOT not in token:
                token[CLAUSE_IDX] = stack_of_indexes[-1]
            else:
                # Alustavad märgendused
                for annotation in token[CLAUSE_ANNOT]:
                    if annotation == "KIILU_ALGUS":
                        # Liigume sügavamale, alustame järgmist kiilu
                        max_index += 1
                        stack_of_indexes.append(max_index)
                        if (len(stack_of_indexes) > max_depth):
                            max_depth = len(stack_of_indexes)
                token[CLAUSE_IDX] = stack_of_indexes[-1]
                # Lõpetavad märgendused
                for annotation in token[CLAUSE_ANNOT]:
                    if annotation == "KINDEL_PIIR":
                        # Liigume edasi samal tasandil, alustame järgmist osalauset
                        max_index += 1
                        stack_of_indexes[-1] = max_index
                    elif annotation == "KIILU_LOPP":
                        # Taandume sügavusest, sulgeme ühe kiilu
                        stack_of_indexes.pop()
        return sentence
        
    def rename_annotations(self, sentence):
        '''Function that renames and restructures clause information.'''
        annotations = []
        for token in sentence:
            data = {CLAUSE_IDX: token[CLAUSE_IDX]}
            if CLAUSE_ANNOT in token:
                if 'KINDEL_PIIR' in token[CLAUSE_ANNOT]:
                    data[CLAUSE_ANNOTATION] = CLAUSE_BOUNDARY
                elif 'KIILU_ALGUS' in token[CLAUSE_ANNOT]:
                    data[CLAUSE_ANNOTATION] = EMBEDDED_CLAUSE_START
                elif 'KIILU_LOPP' in token[CLAUSE_ANNOT]:
                    data[CLAUSE_ANNOTATION] = EMBEDDED_CLAUSE_END
            annotations.append(data)
        return annotations
