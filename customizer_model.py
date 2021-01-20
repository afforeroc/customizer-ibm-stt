#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Customizer models/actions for a IBM Speech To Text instance."""
# $ python3 customizer.py .banistmo words get

import os
import sys
import json
from dotenv import load_dotenv
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def title_scrip(title):
    """Print script title between two bars."""
    print(title.center(2 * len(title), '='))


def check_num_args(argv_size, *argv):
    """Check the number of script arguments."""
    if argv_size == len(*argv) - 1:
        print("Number of arguments is {}: OK".format(len(*argv) - 1))
    else:
        print("ERROR: Number of arguments should be {}".format(argv_size - 1))
        sys.exit(1)


def get_env(env_filepath, campaign, key):
    """Get env settings of a campaign."""
    f = open(env_filepath)
    data = json.load(f)
    f.close()
    if campaign in data:
        env = (data[campaign])[key]
    else:
        print('{} campaign does not exist'.format(campaign))
        sys.exit(1)
    return env


def instantiate_stt(stt_env):
    """Instantiate an IBM Speech To Text API."""
    authenticator = IAMAuthenticator(stt_env['api_key'])
    stt = SpeechToTextV1(authenticator=authenticator)
    stt.set_service_url(stt_env['api_url'])
    return stt

def get_custom_id(stt):
    response = stt.list_language_models().get_result()
    print(response)
    if len(response['customizations']) == 0:
        print("The IBM STT instance don't have custom models")
        sys.exit(1)
    elif len(response['customizations']) == 1:
        custom_id = response['customizations'][0]['customization_id']
    else: #len > 1
        print("Custom Models")
        custom_models = {}
        for elem in response['customizations']:
            customization_name = elem['name']
            customization_id = elem['customization_id']
            if customization_id not in custom_models:
                custom_models[customization_id] = customization_name
            print("{}: {}".format(customization_name, customization_id))
        
        custom_id = input('Customization ID: ')
        if custom_id not in custom_models:
            print('The id {} not in available custom models')
            sys.exit(1)
    return custom_id


def main():
    """Customizer of an IBM Speech to Text instance."""
    campaign = sys.argv[1] # e.g. igs_bancolombia_co
    custom_type = sys.argv[2] # e.g. words
    action = sys.argv[3] # e.g. get

    title_scrip('IBM STT Customizer')
    ibm_stt_env = get_env('config/default.json', campaign, 'ibm_stt')
    stt = instantiate_stt(ibm_stt_env)
    base_lang = 'es-CO_NarrowbandModel'

    if custom_type == "lang":
        if action == 'create':
            new_lang_model = input('New custom language model: ')
            language_model = stt.create_language_model(new_lang_model, base_lang).get_result()
            print(json.dumps(language_model, indent=2))
        elif action == "list":
            language_models = stt.list_language_models().get_result()
            print(json.dumps(language_models, indent=2))
        elif action in ['get', 'delete', 'train', 'reset', 'upgrade']:
            custom_id = get_custom_id(stt)
            if action == "get":
                language_model = stt.get_language_model(custom_id).get_result()
                print(json.dumps(language_model, indent=2))
            elif action == "delete":
                stt.delete_language_model(custom_id)
            elif action == "train":
                stt.train_language_model(custom_id)
            elif action == "reset":
                stt.reset_language_model(custom_id)
            elif action == "upgrade":
                stt.upgrade_language_model(custom_id)
        else:
            print("'{}' is not valid custom language action.".format(action))
    
    elif custom_type == "corpora":
        if action in ['list', 'add', 'get', 'delete']:
            custom_id = get_custom_id(stt)
            if action == "list":
                corpora = stt.list_corpora(custom_id).get_result()
                print(json.dumps(corpora, indent=2))
            elif action == "add":
                corpus_filepath = input('Corpus filepath: ')
                with open(corpus_filepath, 'rb') as corpus_file:
                    corpus_name, _ = os.path.splitext(os.path.basename(corpus_filepath))
                    stt.add_corpus(custom_id, corpus_name, corpus_file, allow_overwrite=True)
            elif action == "get":
                corpus = stt.get_corpus(custom_id, corpus).get_result()
                print(json.dumps(corpus, indent=2))
            elif action == "delete":
                stt.delete_corpus(custom_id, corpus)
        else:
            print("'{}' is not valid as a custom corpora action.".format(action))
    
    elif custom_type == 'words':
        if action in ['list', 'add', 'get', 'delete']:
            custom_id = get_custom_id(stt)
            if action == "list":
                words = stt.list_words(custom_id).get_result()
                print(json.dumps(words, indent=2))
            else: #action in ['add', 'get', 'delete']:
                word = input("Word: ")
                sounds = input("Sounds: ")
                print(word, sounds)
                if action == "add":
                    stt.add_word(custom_id, word, sounds_like=[sounds])
                elif action == "get":
                    word = stt.get_word(custom_id, word).get_result()
                    print(json.dumps(word, indent=2))
                elif action == "delete":
                    stt.delete_word(custom_id, word)
        else:
            print("'{}' is not valid as a custom words action.".format(action))

if __name__ == '__main__':
    main()
