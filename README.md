
# ChatRange

## Table of Contents
- [ChatRange](#project-title)
  - [Description](#description)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Configuration](#configuration)
  - [Examples](#examples)
  - [API Reference](#api-reference)
  - [Tests](#tests)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgements](#acknowledgements)
  - [Contact](#contact)
  - [Citation](#citation)

## Description
ChatRange is an innovative system designed to streamline the development and execution of cyber training exercises, specifically tabletop exercises. Traditionally, planning these exercises can take one to three months for an eight-hour session, according to NIST and MITRE estimates. This significant time and resource investment creates a gap, preventing companies from adequately training for critical events.

To address this issue, ChatRange leverages Autonomous AI agents and Large Language Models (LLMs) to automate the planning process. By utilizing external real-world information, the system can generate realistic scenarios, significantly reducing the preparation time and cost.

Implementation of ChatRange is straightforward, requiring only the provision of API keys. It employs a cloud delivery model, ensuring easy integration and scalability for organizations. ChatRange is the culmination of a Master Thesis (2024) from NTNU Gjøvik, reflecting cutting-edge research and development in the field of cyber training.

## Features
- Uses Autnonomous AI Agents (CrewAI) for content research
- Supports OpenAI, Groq and Local models with Litellm
- Graphical Interface using Streamlit


## Installation
Step-by-step instructions on how to install the project.


### Clone the repository
    git clone https://github.com/trackanstian/ChatRange-Public.git


### Navigate to the project directory
    cd yourproject


### Create a virtual environment
    python -m venv venv


### Activate the virtual environment

#### On Windows
    venv\Scripts\activate
#### On Unix or MacOS
    source venv/bin/activate

### Install dependencies
    pip install -r requirements.txt

### Create and edit .env file
    cp env.example .env

## Usage
How to use the project after installation.


### Example command to run the project (Windows)
    python -m streamlit run .\Start.py

### Example command to run the project (Linux)
    streamlit run Start.py

## Configuration
Information about any configuration settings and how to modify them.


### Services
The tools are available for each agent to use when performing the assigned tasks.
To be able to use chatRange you need to register on these sites and get API-keys. 
They are all free.

#### Search Tool
CrewAI includes search tools, and Serper fetches the top search results from Google, along with metadata and a short description of the page. 

##### Settings
API Key Required: Yes   
URL: https://serper.dev 


#### Exa Search
Exa search is a search and data fetching service specifically built for AI applications. This is a custom tool implemented in ChatRange, from LangChain. The tool provides access to three critical sub-tools used in ChatRange:

 - Search: Runs a semantic search for a webpage
 - Find Similar: Fines similar results based on a similar URL.
 - Get Contents: Gets the contents of a specific webpage along with its metadata.


##### Settings
API Key Required: Yes  
URL: https://exa.ai


#### GROQ
GROQ is a platform for performing inference against open source and limited models like Mistral and Lllama. This is optional for the platform and only if there is a need to run these models:

##### Settings
API Key Required: Yes  
URL: https://groq.com


#### REDIS
Redis is an in-memory data structure store used as a database, cache, and message broker, supporting various data structures such as strings, hashes, lists, sets, and more. This is used in ChatRange for presistance of training secenarios. The solution supports fakeredis, however this is only stored in memory when running the application.

##### Settings
API Key Required: Yes  
URL: https://app.redislabs.com/


#### OpenAI
OpenAi is a company providing access to GPT models for performing inference. This is a requirement for running the platform:

##### Settings
API Key Required: Yes  
URL: https://openai.com


## Config Files 
### GenDat/config/models.json
This file is used to define what models each step of ChatRange uses. There are three options defined with type:
 - OpenAI (openai) - This is used for GPT models which uses static prompting. Uses the OpenAI packages.
 - OpenAI Chat (openai_chat) - This is used for the agents when using OpenAI models. This is provided by Langchain Tools
 - Groq (groq) - Used when using the models Groq gives access to, E.g. Mixtral and llama
 - LiteLLM (litellm) - Use for local models. Experimental and not guaranteed to work! Uses the LangChain Tools package. Please read the docs: https://docs.litellm.ai/docs/proxy/quick_start

You can define up as many json config files you want. The active file name is defined with MODEL_FILE in the .env file. The price is used for calucation of total cost for the exercise. Must be manually defined in the config.

#### Example (Openai):   
    {
    "use": "exercise_objectives",
    "type":"openai",
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 2000,
    "price_in":0.0005,
    "price_out": 0.0015
    }

#### Example (OpenAI Chat):   
    {
    "use": "agent_threat_hunter",
    "type":"openai_chat",
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 2000,
    "price_in":0.0005,
    "price_out": 0.0015
    }

#### Example (Groq):   
    {
    "use": "agent_threat_hunter",
    "type":"groq",
    "model": "mixtral-8x7b-32768",
    "temperature": 0.7,
    "max_tokens": 1000,
    "price_in":0.0005,
    "price_out": 0.0015
    }

#### Example (LiteLLM Experimental):   
    {
    "use": "agent_threat_hunter",
    "type":"litellm",
    "model": "mixtral-8x7b-32768",
    "temperature": 0.7,
    "base_url": "http://0.0.0.0:4000",
    "price_in":0.0005,
    "price_out": 0.0015
    }

### env.example
Rename this file to .env and set the configuration settings:


    #SERVICES  
    SERPER_DEV_API_KEY=""  
    EXA_SEARCH_API_KEY=""  
    GROQ_API_KEY=""  
    OPENAI_API_KEY=""  

    #Set to true to print debug data  
    DEBUG=False  

    #Model config file - You must restart streamlit for env to load again   
    MODEL_FILE="models.json"   

    #Storage - Set REDIS_EMUALTOR to true to use the in-memory cache fakeredis  
    REDIS_EMULATOR=False  
    REDIS_HOST=  
    REDIS_PORT=13997  
    REDIS_DB=0  
    REDIS_PASSWORD=""  

### GenDat/crewai
This is the folder CrewAI uses for storage of the data files. Each file is stored in a unique folder with a UUID. This is the same UUID as in your Session ID in ChatRange UI. The folder is created when the first CrewAI team is finished.


## Contributing
Guidelines for contributing to the project.

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- [CrewAI](https://github.com/joaomdmoura/crewAI) for a aswesome implementation of Autnonomous AI Agents.
- [NTNU Gjøvik](https://www.ntnu.no/gjovik)
- [Norwegian Cyberrange](https://www.ntnu.no/ncr)

## Contact
Stian Storebø - [stian@trackan.com](mailto:stian@trackan.com)

Project Link: [https://chatrange.org](https://chatrange.org)


## Citation
Please use the following citation when referencing this project:

    @software{storebo_2024_chatrange,
    author       = {Stian Storebø},
    title        = {ChatRange},
    year         = 2024,
    url          = {https://github.com/trackanstian/ChatRange-Public},
    note         = {Master Thesis, NTNU Gjøvik},
    version      = {1.0}
    }


