Package Name: MW_CLI
Author: Vikash Kumar Shrivastva
Package URL: https://github.com/

Built using: Merriam-Webster API - https://DictionaryAPI.com

This repository contains scripts which allow you to access definitions from Merriam-Webster's online dictionary through command line tools. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*This package MUST be installed on Python versions 3.8 or later*

You will also need to visit:"https://www.dictionaryapi.com/". Click on "Dev Center" and sign-up. Make sure you make note of your API keys as you will need to set that as environment variable. The following command will help to set the environment variable:
```
1. export MW_API_KEY=<API_KEY>
```

 The current version will only work properly with the "collegiate" reference API, so this line should not be modified. 


 - On Linux /  Mac OS:
export MW_API_KEY=<API_KEY>


### Installing

Clone or download this repository to your local machine. You can also install from PyPI with the following command:

    'pip install mw_cli'

## Scripts

### MW_Response

This first script will retrieve the definition for the word passed into the function. In this case, the word passed in is "exercise".

```
ˈek-sər-ˌsīz (noun): the act of bringing into play or realizing in action
```
