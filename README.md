
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
ChatRange is created to help companies and organizations develop cyber training exercises (Tabletop) using Large language models and Autnonomous AI Agents. The system is a result of a Master Thesis (2024) from NTNU Gjøvik.

## Features
- Uses Autnonomous AI Agents (CrewAI) for content research
- Supports OpenAI, Groq and Local models with Litellm
- Graphical Interface using Streamlit


## Installation
Step-by-step instructions on how to install the project.


### Clone the repository
https://github.com/trackanstian/ChatRange-Public.git


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


## Usage
How to use the project after installation.


### Example command to run the project (Windows)
python -m streamlit run .\Start.py

### Example command to run the project (Linux)
python -m streamlit run .\Start.py

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


### Config File - env.example
Rename this file to .env and set the configuration settings:


    #SERVICES  
    SERPER_DEV_API_KEY=""  
    EXA_SEARCH_API_KEY=""  
    GROQ_API_KEY=""  
    OPENAI_API_KEY=""  

    #Set to true to print debug data  
    DEBUG=true  

    #Storage - Set REDIS_EMUALTOR to true to use the in-memory cache fakeredis  
    REDIS_EMULATOR=False  
    REDIS_HOST=  
    REDIS_PORT=13997  
    REDIS_DB=0  
    REDIS_PASSWORD=""  


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


