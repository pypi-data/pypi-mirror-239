import os
from typing import Optional, List, Union, Dict
from dotapi.caching import Cache

def setup_config():
    config = {
        "input_callback": [],
        "success_callback": [],
        "failure_callback": [],
        "set_verbose": False,
        "email": None,  # for hosted dashboard. Learn more - https://docs.dotagent.dev/anyllm/debugging/hosted_debugging
        "token": None,  # for hosted dashboard. Learn more - https://docs.dotagent.dev/anyllm/debugging/hosted_debugging
        "telemetry": True,
        "max_tokens": 256,  # OpenAI Defaults
        "retry": True,
        "api_key": None,
        "openai_key": None,
        "azure_key": None,
        "anthropic_key": None,
        "replicate_key": None,
        "cohere_key": None,
        "ai21_key": None,
        "openrouter_key": None,
        "huggingface_key": None,
        "vertex_project": None,
        "vertex_location": None,
        "togetherai_api_key": None,
        "baseten_key": None,
        "aleph_alpha_key": None,
        "nlp_cloud_key": None,
        "use_client": False,
        "logging": True,
        "caching": False,  # deprecated soon
        "caching_with_models": False,  # if you want the caching key to be model + prompt # deprecated soon
        "cache": None,  # cache object
        "model_alias_map": {},
        "max_budget": 0.0,  # set the max budget across all providers
        "_current_cost": 0,  # private variable, used if max budget is set 
        "error_logs": {}
    }

    # Return all configuration variables as a dictionary for easy access
    return config
