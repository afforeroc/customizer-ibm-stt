#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Customizer models/actions for a IBM Speech To Text instance."""
# $ python3 customizer.py .banistmo words get

import os
import sys
import json
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


def instantiate_stt(api_key, api_url):
    """Instantiate an IBM Speech To Text API."""
    authenticator = IAMAuthenticator(api_key)
    stt = SpeechToTextV1(authenticator=authenticator)
    stt.set_service_url(api_url)
    return stt


def get_custom_id(stt, custom_type):
    if custom_type == 'language':
        response = stt.list_language_models().get_result()
    elif custom_type == 'acoustic':
        response = stt.list_acoustic_models().get_result()
    else:
        print("The custom type is not 'language' or 'acoustic'")
        sys.exit(1)
    
    if len(response['customizations']) == 0:
        print("The IBM STT instance don't have custom models")
        sys.exit(1)
    elif len(response['customizations']) == 1:
        custom_id = response['customizations'][0]['customization_id']
    else: #len > 1
        print(f'Custom {custom_type} models')
        custom_ids = []
        for elem in response['customizations']:
            print(json.dumps(elem, indent=4))
            custom_ids.append(elem['customization_id'])
        
        custom_id = input(f'{custom_type} customization id: ')
        if custom_id not in custom_ids:
            print(f'The id {custom_id} not in available custom models')
            sys.exit(1)
    return custom_id


def main():
    """Customizer of an IBM Speech to Text instance."""
    custom_type = sys.argv[1] # e.g. lang
    action = sys.argv[2] # e.g. get

    base_lang = "es-CO_NarrowbandModel"

    title_scrip('IBM STT Customizer')
    api_key = "HbStGsW0y-hDhpIeokfgatJbR_ANcrYxbK0XzUgWGy1l"
    api_url = "https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/08d0094f-65c1-4396-b6d5-de0bbfaa5b99"
    stt = instantiate_stt(api_key, api_url)

    if custom_type == "language":
        if action == 'create':
            new_lang_model = input('New custom language model: ')
            language_model = stt.create_language_model(new_lang_model, base_lang).get_result()
            print(json.dumps(language_model, indent=4))
        elif action == "list":
            language_models = stt.list_language_models().get_result()
            print(json.dumps(language_models, indent=4))
        elif action in ['get', 'delete', 'train', 'reset', 'upgrade']:
            custom_id = get_custom_id(stt, custom_type)
            if action == "get":
                language_model = stt.get_language_model(custom_id).get_result()
                print(json.dumps(language_model, indent=4))
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
    elif custom_type == "acoustic":
        if action == 'create':
            new_acoustic_model = input('New custom acoustic model: ')
            acoustic_model = stt.create_acoustic_model(new_acoustic_model, base_lang).get_result()
            print(json.dumps(acoustic_model, indent=4))
        elif action == "list":
            acoustic_models = stt.list_acoustic_models().get_result()
            print(json.dumps(acoustic_models, indent=4))
        elif action in ['get', 'delete', 'train', 'reset', 'upgrade']:
            custom_id = get_custom_id(stt, custom_type)
            if action == "get":
                acoustic_model = stt.get_acoustic_model(custom_id).get_result()
                print(json.dumps(acoustic_model, indent=4))
            elif action == "delete":
                stt.delete_acoustic_model(custom_id)
            elif action == "train":
                stt.train_acoustic_model(custom_id)
            elif action == "reset":
                stt.reset_acoustic_model(custom_id)
            elif action == "upgrade":
                stt.upgrade_acoustic_model(custom_id)
        else:
            print("'{}' is not valid custom acoustic action.".format(action))
    elif custom_type == "corpora":
        if action in ['list', 'add', 'get', 'delete']:
            custom_id = get_custom_id(stt, 'language')
            if action == "list":
                corpora = stt.list_corpora(custom_id).get_result()
                print(json.dumps(corpora, indent=2))
            elif action == "add":
                corpus_filepath = input('Corpus filepath: ')
                with open(corpus_filepath, 'rb') as corpus_file:
                    corpus_name, _ = os.path.splitext(os.path.basename(corpus_filepath))
                    stt.add_corpus(custom_id, corpus_name, corpus_file, allow_overwrite=True)
            elif action == "get":
                corpus_name = input('corpus name: ')
                corpus = stt.get_corpus(custom_id, corpus_name).get_result()
                print(json.dumps(corpus, indent=2))
            elif action == "delete":
                corpus_name = input('corpus name: ')
                stt.delete_corpus(custom_id, corpus_name)
        else:
            print("'{}' is not valid as a custom corpora action.".format(action))
    
    elif custom_type == 'words':
        if action in ['list', 'add', 'get', 'delete']:
            custom_id = get_custom_id(stt, 'language')
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
