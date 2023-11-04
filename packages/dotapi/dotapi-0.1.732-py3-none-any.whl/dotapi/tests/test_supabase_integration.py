# #### What this tests ####
# #    This tests if logging to the supabase integration actually works
# # pytest mistakes intentional bad calls as failed tests -> [TODO] fix this
# import sys, os
# import traceback
# import pytest

# sys.path.insert(0, os.path.abspath('../..'))  # Adds the parent directory to the system path
# import anyllm
# from anyllm import embedding, completion

# anyllm.input_callback = ["supabase"]
# anyllm.success_callback = ["supabase"]
# anyllm.failure_callback = ["supabase"]

# # anyllm.modify_integration("supabase",{"table_name": "test_table"})

# anyllm.set_verbose = True

# user_message = "Hello, how are you?"
# messages = [{ "content": user_message,"role": "user"}]


# #openai call
# response = completion(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hi 👋 - i'm openai"}])

# fix
# #bad request call
# response = completion(model="chatgpt-test", messages=[{"role": "user", "content": "Hi 👋 - i'm a bad request"}])
