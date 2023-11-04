# import sys, os
# import traceback
# sys.path.insert(0, os.path.abspath('../..'))  # Adds the parent directory to the system path
# import anyllm
# from anyllm import embedding, completion

# anyllm.api_base = "https://oai.hconeai.com/v1"
# anyllm.headers = {"Helicone-Auth": f"Bearer {os.getenv('HELICONE_API_KEY')}"}

# response = anyllm.completion(
#     model="gpt-3.5-turbo",
#     messages=[{"role": "user", "content": "how does a court case get to the Supreme Court?"}]
# )

# print(response)
