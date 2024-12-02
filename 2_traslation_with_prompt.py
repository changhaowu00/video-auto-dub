import openai


def chat(prompt):
    # No key needed; Neptyne provides one:
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "assistant",
                "content": prompt,
            },
        ],
    )
    return completion.choices[0].message.content