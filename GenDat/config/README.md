#Configuration File Explanation

This README provides details about the configuration file that defines various agents, their models, parameters, and pricing for a specific use case. Each entry in the configuration file represents a unique agent designed to perform a specific task using an OpenAI model.

##Configuration Structure

The configuration file is a JSON array, where each object in the array contains the following fields:

    use: A descriptive name for the specific use case or agent.
    type: The type of OpenAI model being used (openai or openai_chat).
    model: The specific model version being utilized.
    temperature: A parameter controlling the creativity of the model's responses (0.7 in all cases here).
    max_tokens: The maximum number of tokens the model is allowed to generate in a single response.
    price_in: The cost per token for input.
    price_out: The cost per token for output.

##Examples
###Static prompt
{
    "use": "exercise_objectives",
    "type":"openai",
    "model": "gpt-3.5-turbo-0125",
    "temperature": 0.7,
    "max_tokens": 2000,
    "price_in":0.0005,
    "price_out": 0.0015
},
{
    "use": "get_questions",
    "type":"openai",
    "model": "gpt-4o",
    "temperature": 0.7,
    "max_tokens": 4000,
    "price_in":0.005,
    "price_out": 0.015
}
    {
        "use": "get_questions",
        "type":"openai",
        "model": "gpt-4-turbo",
        "temperature": 0.7,
        "max_tokens": 4000,
        "price_in":0.01,
        "price_out": 0.03
    }


###Agent
{
    "use": "agent_data_expert",
    "type":"openai_chat",
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 4000,
    "price_in":0.0005,
    "price_out": 0.0015
},
