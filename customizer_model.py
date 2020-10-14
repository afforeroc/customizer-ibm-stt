#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Customizer models/actions for a IBM Speech To Text instance."""

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


def load_env(env_file):
    """Load authentication settings for SST service."""
    dotenv_path = os.path.join(os.path.dirname(__file__), env_file)
    load_dotenv(dotenv_path)
    api_key = os.getenv('API_KEY')
    url_service = os.getenv('API_URL')
    return api_key, url_service


def instantiate_stt(api_key, url_service):
    """Instantiate an IBM Speech To Text API."""
    authenticator = IAMAuthenticator(api_key)
    stt = SpeechToTextV1(authenticator=authenticator)
    stt.set_service_url(url_service)
    return stt


def custom_language_model(stt, action, model_id=None, model=None, lang=None):
    """Custom language model actions."""
    if action == "create model":
        language_model = stt.create_language_model(model, lang).get_result()
        print(json.dumps(language_model, indent=2))
    elif action == "list models":
        language_models = stt.list_language_models().get_result()
        print(json.dumps(language_models, indent=2))
    elif action == "get model":
        language_model = stt.get_language_model(model_id).get_result()
        print(json.dumps(language_model, indent=2))
    elif action == "delete model":
        stt.delete_language_model(model_id)
    elif action == "train model":
        stt.train_language_model(model_id)
    elif action == "reset model":
        stt.reset_language_model(model_id)
    elif action == "upgrade model":
        stt.upgrade_language_model(model_id)
    else:
        print(f"'{action}' is not valid as a custom language model action.")


def custom_corpora(stt, action, model_id, corpus=None, corpus_pathfile=None):
    """Custom corpora actions of a custom language model."""
    if action == "list corpora":
        corpora = stt.list_corpora(model_id).get_result()
        print(json.dumps(corpora, indent=2))
    elif action == "add corpus":
        with open(corpus_pathfile, 'rb') as corpus_file:
            stt.add_corpus(model_id, corpus, corpus_file, allow_overwrite=True)
    elif action == "get corpus":
        corpus = stt.get_corpus(model_id, corpus).get_result()
        print(json.dumps(corpus, indent=2))
    elif action == "delete corpus":
        stt.delete_corpus(model_id, corpus)
    else:
        print(f"'{action}' is not valid as a custom corpora action.")


def custom_words(stt, action, model_id, word=None, words=None):
    """Custom words actions of a custom language model."""
    if action == "list words":
        words = stt.list_words(model_id).get_result()
        print(json.dumps(words, indent=2))
    elif action == "add words":
        stt.add_words(model_id, words)
    elif action == "add word":
        stt.add_words(model_id, word)
    elif action == "get word":
        word = stt.get_word(model_id, word).get_result()
        print(json.dumps(word, indent=2))
    elif action == "delete word":
        stt.delete_word(model_id, word)
    else:
        print(f"'{action}' is not valid as a custom words action.")


def custom_grammar(stt, action, model_id, grammar=None, grammar_pathfile=None):
    """Custom grammar actions of a custom language model."""
    if action == "list grammars":
        grammars = stt.list_grammars(model_id).get_result()
        print(json.dumps(grammars, indent=2))
    elif action == "add grammar":
        with open(grammar_pathfile, 'rb') as grammar_file:
            c_type = "application/srgs"
            stt.add_grammar(model_id,
                            grammar,
                            grammar_file,
                            content_type=c_type)
    elif action == "get grammar":
        grammar = stt.get_grammar(model_id, grammar).get_result()
        print(json.dumps(grammar, indent=2))
    elif action == "delete grammar":
        stt.delete_grammar(model_id, grammar)
    else:
        print(f"'{action}' is not valid as a custom grammar action.")


def custom_acoustic_model(stt, action, model_id=None, model=None, lang=None):
    """Custom acoustic model actions."""
    if action == "create model":
        acoustic_model = stt.create_acoustic_model(model, lang).get_result()
        print(json.dumps(acoustic_model, indent=2))
    elif action == "list models":
        acoustic_models = stt.list_acoustic_models().get_result()
        print(json.dumps(acoustic_models, indent=2))
    elif action == "get model":
        acoustic_model = stt.get_acoustic_model(model_id).get_result()
        print(json.dumps(acoustic_model, indent=2))
    elif action == "delete model":
        stt.delete_acoustic_model(model_id)
    elif action == "train model":
        stt.train_acoustic_model(model_id)
    elif action == "reset model":
        stt.reset_acoustic_model(model_id)
    elif action == "upgrade model":
        stt.upgrade_acoustic_model(model_id)
    else:
        print(f"'{action}' is not valid as a custom acoustic model action.")


def custom_audios(stt, action, model_id, audio=None, audio_pathfile=None):
    """Custom audio resource actions of a custom acoustic model."""
    if action == "list audio":
        audio_resources = stt.list_audio(model_id).get_result()
        print(json.dumps(audio_resources, indent=2))
    elif action == "add audio":
        c_type = "audio/mp3"
        with open(audio_pathfile, 'rb') as audio_file:
            stt.add_audio(model_id, audio, audio_file, content_type=c_type)
    elif action == "get audio":
        audio_listing = stt.get_audio(model_id, audio).get_result()
        print(json.dumps(audio_listing, indent=2))
    elif action == "delete audio":
        stt.delete_audio(model_id, audio)
    else:
        print(f"'{action}' is not valid as a custom audio resource action.")


def main():
    """Customizer of an IBM Speech to Text instance."""
    num_args = 2
    check_num_args(num_args, sys.argv)  # Check the number of script arguments.
    env_file = sys.argv[1]
    excel_file = sys.argv[2]
    title_scrip('IBM STT customizer')

    api_key, url_service = load_env(env_file)
    stt = instantiate_stt(api_key, url_service)

    # --- CUSTOM LANGUAGE MODELS ---
    #----------------------------------------------------------------------------
    #lang_model = "IGS lang model"
    #co_lang="CO_NarrowbandModel"
    #custom_language_model(stt, "create model", model=lang_model, lang=co_lang)
    #----------------------------------------------------------------------------
    #custom_language_model(stt, "list models")
    #----------------------------------------------------------------------------
    #lang_id = "7fa5d91f-be33-4903-9c26-8b0bdeb3fb2f"
    #custom_language_model(stt, "get model", model_id=lang_id)
    #custom_language_model(stt, "delete model", model_id=lang_id)
    #custom_language_model(stt, "train model", model_id=lang_id)
    #custom_language_model(stt, "reset model", model_id=lang_id)
    #custom_language_model(stt, "upgrade model", model_id=lang_id)


    # --- CUSTOM CORPORA ---
    #----------------------------------------------------------------------------
    lang_id = "7fa5d91f-be33-4903-9c26-8b0bdeb3fb2f"
    #custom_language_model(stt, "get model", model_id=lang_id)

    # -- Delete corpus --
    #custom_corpora(stt, "delete corpus", lang_id, corpus="express-2020-09-08")
    #custom_corpora(stt, "list corpora", lang_id)
    #custom_language_model(stt, "reset model", model_id=lang_id)
    
    # -- Add corpus --
    #custom_corpora(stt, "add corpus", lang_id, corpus="express-2020-09-08", corpus_pathfile="corpora/express-2020-09-08.txt")
    #custom_corpora(stt, "list corpora", lang_id)
    #custom_corpora(stt, "get corpus", lang_id, "express-2020-09-08") # Check if status is analyzed

    # -- Train model
    #custom_language_model(stt, "train model", model_id=lang_id)
    
    # -- Check status
    custom_language_model(stt, "get model", model_id=lang_id)
    custom_words(stt, "list words", model_id=lang_id)


    # --- CUSTOM ACOUSTIC MODELS ---
    #----------------------------------------------------------------------------
    #ac_model = "IGS acoustic model"
    #co_lang="CO_NarrowbandModel"
    #custom_acoustic_model(stt, "create model", model=ac_model, lang=co_lang)
    #----------------------------------------------------------------------------
    #custom_acoustic_model(stt, "list models")
    #----------------------------------------------------------------------------
    #ac_id = "2dab4986-8c28-4f0c-bc0c-8bfafc64f966"
    #custom_acoustic_model(stt, "get model", model_id=ac_id)
    #custom_acoustic_model(stt, "delete model", model_id=ac_id)
    #custom_acoustic_model(stt, "train model", model_id=ac_id)
    #custom_acoustic_model(stt, "reset model", model_id=ac_id)
    #custom_acoustic_model(stt, "upgrade model", model_id=ac_id)


if __name__ == '__main__':
    main()
