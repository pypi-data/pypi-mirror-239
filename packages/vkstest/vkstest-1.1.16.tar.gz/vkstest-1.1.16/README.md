**Package Name:** MW_CLI

**Author:** Vikash Kumar Shrivastva

**Package URL:** https://github.com/

**Built using:** Merriam-Webster API - https://DictionaryAPI.com

This repository contains scripts which allow you to access definitions from Merriam-Webster's online dictionary through command line tools. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*This package MUST be installed on Python versions 3.8 or later*

You will also need to get MW API Key.
To get the API Key follow the following steps:
**Step1:** visit "https://www.dictionaryapi.com/". 
**Step2:** Click on "Dev Center" 
**Step3:** Sign-Up and generate API Key. 

Make sure to save the API key as you will need to set that as environment variable. 

This command line utility will only work with the "collegiate" reference API.
 - On Linux /  Mac OS:
export MW_API_KEY=<API_KEY>


### Installation
To check and modify the code as per your use case. Feel free to clone or download this repository to your local machine.

To use the CLI functionality of this package follow the following steps:
Step1: Install the CLI using pip command. 

    'pip install mw_cli'
Step2: Set the MW API key as `MW_API_KEY` environment variable.:

    export MW_API_KEY=<MW_API_KEY>
For Example if your API Key is `lskdjlsfjdslfdjslfdjsldfsf` then 

    export MW_API_KEY=lskdjlsfjdslfdjslfdjsldfsf

## Scripts

### MW_Response

This script will retrieve the definition for the word passed into the function. In this case, the word passed in is "exercise".

```
ˈek-sər-ˌsīz (noun): the act of bringing into play or realizing in action
```
