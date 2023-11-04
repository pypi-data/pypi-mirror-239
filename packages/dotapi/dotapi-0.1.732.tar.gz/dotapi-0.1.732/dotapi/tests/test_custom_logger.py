### What this tests ####
import sys
import os

sys.path.insert(0, os.path.abspath('../..'))

from dotapi import completion, embedding
import dotapi

def custom_callback(
        kwargs,
        completion_response,
        start_time,
        end_time,
):
    print(
        "in custom callback func"
    )
    print("kwargs", kwargs)
    print(completion_response)
    print(start_time)
    print(end_time)
dotapi.success_callback = [custom_callback]


dotapi.set_verbose = True


# def test_chat_openai():
#     try:
#         response = completion(model="gpt-3.5-turbo",
#                               messages=[{
#                                   "role": "user",
#                                   "content": "Hi 👋 - i'm openai"
#                               }])

#         print(response)

#     except Exception as e:
#         print(e)


# test_chat_openai()
