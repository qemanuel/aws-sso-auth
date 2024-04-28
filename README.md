# AWS SSO Profiles config dump
Python script to automatically create the aws-cli profiles config file.

## Requirements
| Name | Version |
|------|---------|
| python | >= 3.x |
| pip3 |
| aws-cli | >= 2.0 |

## Usage
1. Install dependencies `pip3 install -r requirements.txt`
2. Create the `.env` file based on `example.env`
3. Exec the script `python3 main.py`
4. The profiles config file will be created in **$FILE_PATH**, default `./config`