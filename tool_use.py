# import boto3, json, math

# print("\n----Defining a tool and sending a message that will make Claude ask for tool use----\n")

# session = boto3.Session()
# bedrock = session.client(service_name='bedrock-runtime')

# tool_list = [
#     {
#         "toolSpec": {
#             "name": "cosine",
#             "description": "Calculate the cosine of x.",
#             "inputSchema": {
#                 "json": {
#                     "type": "object",
#                     "properties": {
#                         "x": {
#                             "type": "number",
#                             "description": "The number to pass to the function."
#                         }
#                     },
#                     "required": ["x"]
#                 }
#             }
#         }
#     }
# ]

# message_list = []

# initial_message = {
#     "role": "user",
#     "content": [
#         { "text": "What is the cosine of 7?" } 
#     ],
# }

# message_list.append(initial_message)

# response = bedrock.converse(
#     modelId="anthropic.claude-3-sonnet-20240229-v1:0",
#     messages=message_list,
#     inferenceConfig={
#         "maxTokens": 2000,
#         "temperature": 0
#     },
#     toolConfig={
#         "tools": tool_list
#     },
#     system=[{"text":"You must only do math by using a tool."}]
# )

# response_message = response['output']['message']
# print(json.dumps(response_message, indent=4))
# message_list.append(response_message)

# print("\n----Error handling - letting Claude know that tool use failed----\n")

# del message_list[-2:] #Remove the last request and response messages

# content_block = next((block for block in response_content_blocks if 'toolUse' in block), None)

# if content_block:
#     tool_use_block = content_block['toolUse']
    
#     error_tool_result = {
#         "toolResult": {
#             "toolUseId": tool_use_block['toolUseId'],
#             "content": [
#                 {
#                     "text": "invalid function: cosine"
#                 }
#             ],
#             "status": "error"
#         }
#     }
    
#     follow_up_message = {
#         "role": "user",
#         "content": [error_tool_result],
#     }
    
#     message_list.append(follow_up_message)
    
#     response = bedrock.converse(
#         modelId="anthropic.claude-3-sonnet-20240229-v1:0",
#         messages=message_list,
#         inferenceConfig={
#             "maxTokens": 2000,
#             "temperature": 0
#         },
#         toolConfig={
#             "tools": tool_list
#         },
#         system=[{"text":"You must only do math by using a tool."}]
#     )
    
#     response_message = response['output']['message']
#     print(json.dumps(response_message, indent=4))
#     message_list.append(response_message)


# print("\n----Passing the tool result back to Claude----\n")

# follow_up_content_blocks = []

# for content_block in response_content_blocks:
#     if 'toolUse' in content_block:
#         tool_use_block = content_block['toolUse']
#         tool_use_name = tool_use_block['name']
        
        
#         if tool_use_name == 'cosine':
#             tool_result_value = math.cos(tool_use_block['input']['x'])
            
#             follow_up_content_blocks.append({
#                 "toolResult": {
#                     "toolUseId": tool_use_block['toolUseId'],
#                     "content": [
#                         {
#                             "json": {
#                                 "result": tool_result_value
#                             }
#                         }
#                     ]
#                 }
#             })

# if len(follow_up_content_blocks) > 0:
    
#     follow_up_message = {
#         "role": "user",
#         "content": follow_up_content_blocks,
#     }
    
#     message_list.append(follow_up_message)

#     response = bedrock.converse(
#         modelId="anthropic.claude-3-sonnet-20240229-v1:0",
#         messages=message_list,
#         inferenceConfig={
#             "maxTokens": 2000,
#             "temperature": 0
#         },
#         toolConfig={
#             "tools": tool_list
#         },
#         system=[{"text":"You must only do math by using a tool."}]
#     )
    
#     response_message = response['output']['message']
    
#     message_list.append(response_message)
#     print(json.dumps(message_list, indent=4))


import os
import json
import math
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("\n----Defining a tool and sending a message that will make Claude ask for tool use----\n")

tool_list = [
    {
        "type": "function",
        "function": {
            "name": "cosine",
            "description": "Calculate the cosine of x.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "number",
                        "description": "The number to pass to the function."
                    }
                },
                "required": ["x"]
            }
        }
    }
]

message_list = [
    {"role": "system", "content": "You must only do math by using a tool."},
    {"role": "user", "content": "What is the cosine of 7?"}
]

response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # Use the appropriate model
    messages=message_list,
    tools=tool_list,
    tool_choice="auto",
    max_tokens=2000,
    temperature=0
)

response_message = response.choices[0].message
print(json.dumps(response_message.model_dump(), indent=4))
message_list.append(response_message.model_dump())

print("\n----Calling a function based on the tool_calls content.----\n")

if response_message.tool_calls:
    for tool_call in response_message.tool_calls:
        if tool_call.function.name == 'cosine':
            function_args = json.loads(tool_call.function.arguments)
            tool_result_value = math.cos(function_args['x'])
            print(f"Using tool {tool_call.function.name}")
            print(tool_result_value)
else:
    print(response_message.content)

print("\n----Passing the tool result back to the model----\n")

if response_message.tool_calls:
    for tool_call in response_message.tool_calls:
        if tool_call.function.name == 'cosine':
            function_args = json.loads(tool_call.function.arguments)
            tool_result_value = math.cos(function_args['x'])
            
            tool_response = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call.function.name,
                "content": json.dumps({"result": tool_result_value})
            }
            message_list.append(tool_response)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use the appropriate model
        messages=message_list,
        tools=tool_list,
        tool_choice="auto",
        max_tokens=2000,
        temperature=0
    )
    
    response_message = response.choices[0].message
    message_list.append(response_message.model_dump())
    print(json.dumps(message_list, indent=4))

print("\n----Error handling - letting the model know that tool use failed----\n")

# Remove the last two messages (request and response)
message_list = message_list[:-2]

if response_message.tool_calls:
    tool_call = response_message.tool_calls[0]
    
    error_tool_response = {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "name": tool_call.function.name,
        "content": "invalid function: cosine"
    }
    
    message_list.append(error_tool_response)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use the appropriate model
        messages=message_list,
        tools=tool_list,
        tool_choice="auto",
        max_tokens=2000,
        temperature=0
    )
    
    response_message = response.choices[0].message
    print(json.dumps(response_message.model_dump(), indent=4))
    message_list.append(response_message.model_dump())