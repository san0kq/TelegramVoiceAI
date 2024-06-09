from services.api_services import openai_client


async def get_mood_by_photo(photo_url: str) -> str:
    response = await openai_client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {
            'role': 'user',
            'content': [
                {'type': 'text', 'text': 'What is the mood of the person in the photo? Answer with one word. If there is no person, simply answer 0.'},
                {
                'type': 'image_url',
                'image_url': {
                    'url': photo_url,
                },
                },
            ],
            }
        ],
        max_tokens=15,
    )

    return response.choices[0].message.content
