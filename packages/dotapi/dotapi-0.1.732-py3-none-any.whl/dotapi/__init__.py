from .config import setup_config
from .models import get_model_cost_map, initialize_model_lists
from .constants import (
    MyLocal, api_base, headers, api_version, organization,
    config_path, secret_manager_client, open_ai_embedding_models,
    model_list, provider_list, models_by_provider
)
from .timeout import timeout
from .testing import *  # Replace with actual import statements
from .utils import (
    client, exception_type, get_optional_params,
    modify_integration, token_counter, cost_per_token,
    completion_cost, get_anyllm_params, Logging, acreate,
    get_model_list, completion_with_split_tests, get_max_tokens,
    register_prompt_template, validate_environment, check_valid_key,
    get_llm_provider, completion_with_config
)
from .main import *  # Replace with actual import statements
from .integrations import *  # Replace with actual import statements
from .exceptions import (
    AuthenticationError, InvalidRequestError, RateLimitError,
    ServiceUnavailableError, OpenAIError, ContextWindowExceededError,
    BudgetExceededError
)
from .budget_manager import BudgetManager

# Importing lists for various models
from .constants import (
    open_ai_chat_completion_models, open_ai_text_completion_models,
    cohere_models, anthropic_models, openrouter_models,
    vertex_chat_models, vertex_code_chat_models, vertex_text_models,
    vertex_code_text_models, ai21_models, nlp_cloud_models,
    aleph_alpha_models, replicate_models, huggingface_models,
    together_ai_models, baseten_models, petals_models,
    bedrock_models, ollama_models
)

# Load configurations
config = setup_config()

# Expose all configuration variables at the module level
globals().update(config)

# Fetch model cost map and initialize model lists
model_cost = get_model_cost_map()
initialize_model_lists(model_cost)

# Define thread-local storage for user data
_thread_context = MyLocal()

# Define remaining variables and data structures
custom_prompt_dict:Dict[str, dict] = {}

def identify(event_details):
    # Store user in thread local data
    if "user" in event_details:
        _thread_context.user = event_details["user"]

__all__ = [
    'setup_config',
    'get_model_cost_map',
    'initialize_model_lists',
    'MyLocal',
    'api_base',
    'headers',
    'api_version',
    'organization',
    'config_path',
    'secret_manager_client',
    'open_ai_embedding_models',
    'model_list',
    'provider_list',
    'models_by_provider',
    'timeout',
    'client',
    'exception_type',
    'get_optional_params',
    'modify_integration',
    'token_counter',
    'cost_per_token',
    'completion_cost',
    'get_anyllm_params',
    'Logging',
    'acreate',
    'get_model_list',
    'completion_with_split_tests',
    'get_max_tokens',
    'register_prompt_template',
    'validate_environment',
    'check_valid_key',
    'get_llm_provider',
    'completion_with_config',
    'AuthenticationError',
    'InvalidRequestError',
    'RateLimitError',
    'ServiceUnavailableError',
    'OpenAIError',
    'ContextWindowExceededError',
    'BudgetExceededError',
    'BudgetManager',
    'identify',
    'custom_prompt_dict',
]
