import json

from services.api_services import openai_client
from data_access.dal import UserDAL
from data_access.dto import ValueDTO
from data_access.exceptions import (
    ValueAlreadyExistsError,
    AddValueError,
    GetValueError
)


async def validate_value(result: str) -> bool:
    if result.isdigit():
        return bool(int(result))
    else:
        return False
    

async def save_value(value: str, user_id: int) -> bool:
    messages = [
        {'role': 'system',
         'content': (
            f'Can "{value}" be such a key life goal for a person? '
            f'If yes, pass 1 to the function; if no, pass 0.'
        )}
    ]
    tools = [
        {
            'type': 'function',
            'function': {
                'name': 'validate_value',
                'description': ('Function for pass the validation '
                                'result of a given key value '
                                'and return boolean'),
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'result': {
                            'type': 'string',
                            'description': 'Validation result',
                        }
                    },
                    'required': ['result'],
                },
            },
        }
    ]

    response = await openai_client.chat.completions.create(
        model='gpt-4o',
        messages=messages,
        tools=tools,
        tool_choice={
            'type': 'function',
            'function': {'name': 'validate_value'}
        }
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {
            'validate_value': validate_value,
        }
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = await function_to_call(
                result=function_args.get('result')
            )

        if function_response:
            dal = UserDAL()
            data = ValueDTO(
                user_id=user_id,
                value=value
            )
            try:
                await dal.add_value(data=data)
                return True
            
            except (AddValueError, GetValueError, ValueAlreadyExistsError):
                pass
    
    return False
