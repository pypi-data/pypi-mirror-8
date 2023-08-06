# -*- coding: utf-8 -*-

"""Module which holds Wordnet class for annotating corpus.
"""

import os, sys
from core import JsonPaths

from estnltk.wordnet import wn

PYVABAMORF_TO_WORDNET_POS_MAP = {'A': wn.ADJ,'S': wn.NOUN, 'V': wn.VERB, 'D': wn.ADV}

class Wordnet(object):
  """Annotates `analysis` entries in corpus with queried Estonian WordNet data.
  
  Example
  -------
    wn = Wordnet()
    
    wn(corpus,variants=True, var_literal=True) # annotates 'analysis' entries with all the variants and their literals for every synset    
  """
  
  def __call__(self, corpus, **kwargs):
    """Annotates `analysis` entries in `corpus` with a list of lemmas` synsets and queried WordNet data in a 'wordnet' entry.
    
    Note
    ----
      Annotates every `analysis` entry with a `wordnet`:{`synsets`:[..]}.
    
    Parameters
    ----------
    corpus : dict
      Representation of a corpus in a disassembled form for automatic text analysis with word-level `analysis` entry.
      E.g. corpus disassembled into paragraphs, sentences, words ({'paragraphs':[{'sentences':[{'words':[{'analysis':{...}},..]},..]},..]}).
    
    Keyword parameters    
    ------------------  
    pos : boolean, optional
      If True, annotates each synset with a correspnding `pos` (part-of-speech) tag.
    variants : boolean, optional
      If True, annotates each synset with a list of all its variants' (lemmas') literals.
    var_sense : boolean, optional
      If True and `variants` is True, annotates each variant/lemma with its sense number.
    var_definition : boolean, optional
      If True and `variants` is True, annotates each variant/lemma with its definition. Definitions often missing in WordNet.
    var_examples : boolean, optional
      If True and `variants` is True, annotates each variant/lemma with a list of its examples. Examples often missing in WordNet.
    relations : list of str, optional
      Holds interested relations. Legal relations are as follows:
    `antonym`, `be_in_state`, `belongs_to_class`, `causes`, `fuzzynym`, `has_holo_location`, `has_holo_madeof`, `has_holo_member`,
    `has_holo_part`, `has_holo_portion`, `has_holonym`, `has_hyperonym`, `has_hyponym`, `has_instance`, `has_mero_location`,
    `has_mero_madeof`, `has_mero_member`, `has_mero_part`, `has_mero_portion`, `has_meronym`, `has_subevent`, `has_xpos_hyperonym`,
    `has_xpos_hyponym`, `involved`, `involved_agent`, `involved_instrument`, `involved_location`, `involved_patient`,
    `involved_target_direction`, `is_caused_by`, `is_subevent_of`, `near_antonym`, `near_synonym`, `role`, `role_agent`, `role_instrument`,
    `role_location`, `role_patient`, `role_target_direction`, `state_of`, `xpos_fuzzynym`, `xpos_near_antonym`, `xpos_near_synonym`.
      Annotates each synset with related synsets' indices with respect to queried relations.
    
    Returns
    -------
    dict
      In-place annotated `corpus`.
    
    """
    
    analysis_matches = JsonPaths.analysis.find(corpus)


    for analysis_match in analysis_matches:
      
      for candidate in analysis_match.value:

    if candidate['partofspeech'] not in PYVABAMORF_TO_WORDNET_POS_MAP:
      # Wordnet does't contain any data about the given lemma and pos combination - won't annotate.
      continue
    
    wordnet_obj = {}

    candidate_synsets = [({'id':synset.id},synset) for synset in wn.synsets(candidate['lemma'],pos=PYVABAMORF_TO_WORDNET_POS_MAP[candidate['partofspeech']])]
    
    for synset_dict,synset in candidate_synsets:
      
      if 'pos' in kwargs:
        if kwargs['pos']:
          synset_dict['pos'] = synset.pos
    
      if 'variants' in kwargs:
        if kwargs['variants']:
          variants = [({'literal':variant.literal},variant) for variant in synset.get_variants()]
          
          for variant_dict,variant in variants:
        
        if 'var_sense' in kwargs:
          if kwargs['var_sense']:
            variant_dict['sense'] = variant.sense
          
        if 'var_definition' in kwargs:
          if kwargs['var_definition']:
            variant_dict['definition'] = variant.definition
          
        if 'var_examples' in kwargs:
          if kwargs['var_examples']:
            variant_dict['examples'] = variant.examples
          
          synset_dict['variants'] = [variant_dict for variant_dict,_ in variants]
      
    wordnet_obj['synsets'] = [synset_dict for synset_dict,_ in candidate_synsets]
      
    if 'relations' in kwargs:
      if len(kwargs['relations']):
        
        relations_dict = {}
        
        for relation_str in kwargs['relations']:
          related_synsets = [{'id':synset.id} for synset in synset.get_related_synsets(relation_str)]
          
          relations_dict[relation_str] = [synset_dict for synset_dict,_ in related_synsets]
      
        wordnet_obj['relations'] = relations_dict
    
    if 'ancestors_by' in kwargs:
      if len(kwargs['ancestors_by']):
        
        ancestors_dict = {}
        
        for ancestor_str in kwargs['ancestors_by']:
          ancestors = [{'id':synset.id} for synset in synset.get_ancestors(relation_str)]
          
          ancestors_dict[relation_str] = ancestors
          
        wordnet_obj['ancestors_by'] = ancestors_dict
    
    candidate['wordnet'] = wordnet_obj
      
    return corpus
    
    
  def annotate_synsets(self, corpus):
    """Annotates `analysis` entries in `corpus` with a list of lemmas` synsets in a 'wordnet' entry.
    
    Note
    ----
      Equivalent to self(corpus)
    
    """
    return self(corpus)
