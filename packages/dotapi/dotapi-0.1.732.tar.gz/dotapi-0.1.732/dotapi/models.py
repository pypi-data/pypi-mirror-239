from .constants import (
    open_ai_chat_completion_models,
    open_ai_text_completion_models,
    cohere_models,
    anthropic_models,
    openrouter_models,
    vertex_text_models,
    vertex_code_text_models,
    vertex_chat_models,
    vertex_code_chat_models,
    ai21_models,
    nlp_cloud_models,
    aleph_alpha_models
)
import requests

def get_model_cost_map():
    url = "https://raw.githubusercontent.com/BerriAI/anyllm/main/model_prices_and_context_window.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if request is unsuccessful
        content = response.json()
        return content
    except requests.exceptions.RequestException as e:
        return {}
    except:
        return {}

def initialize_model_lists(model_cost):
    for key, value in model_cost.items():
        if value.get('anyllm_provider') == 'openai':
            open_ai_chat_completion_models.append(key)
        elif value.get('anyllm_provider') == 'text-completion-openai':
            open_ai_text_completion_models.append(key)
        elif value.get('anyllm_provider') == 'cohere':
            cohere_models.append(key)
        elif value.get('anyllm_provider') == 'anthropic':
            anthropic_models.append(key)
        elif value.get('anyllm_provider') == 'openrouter':
            split_string = key.split('/', 1)
            openrouter_models.append(split_string[1])
        elif value.get('anyllm_provider') == 'vertex_ai-text-models':
            vertex_text_models.append(key)
        elif value.get('anyllm_provider') == 'vertex_ai-code-text-models':
            vertex_code_text_models.append(key)
        elif value.get('anyllm_provider') == 'vertex_ai-chat-models':
            vertex_chat_models.append(key)
        elif value.get('anyllm_provider') == 'vertex_ai-code-chat-models':
            vertex_code_chat_models.append(key)
        elif value.get('anyllm_provider') == 'ai21':
            ai21_models.append(key)
        elif value.get('anyllm_provider') == 'nlp_cloud':
            nlp_cloud_models.append(key)
        elif value.get('anyllm_provider') == 'aleph_alpha':
            aleph_alpha_models.append(key)

# Fetch model cost map and initialize model lists
model_cost = get_model_cost_map()
initialize_model_lists(model_cost)
