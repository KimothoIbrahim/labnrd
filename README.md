# labnrd
An Analytical Chemistry instruments' locator and listing application.

## Introduction
The Labnrd project is a collation project seeking to build a database of physical locations where researchers and research students can access usage. Institutions can list and bill their instruments accordingly to make them available to a wider audience of potential users of their services.

For the deployed app https://www.characterize.tech

**Key Features:**
Quick search instruments by name or listing institution.
Mpesa payment integration.
All your orders/listings in a single Dashboard.

## Installation
Labnrd is built in Python3.0

To run a local copy:
1. Clone the repository:

   ```bash
   git clone https://github.com/KimothoIbrahim/labnrd.git

2. Navigate to project directory

   cd labnerdWorkingDirectory

3. Install required dependencies

   pip install -r requirements.txt

## Usage
  run locally ./labnerd.py
  or
  host with gunicorn
    'gunicorn --bind 0.0.0.0:8000 labnerd:app'

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact Information
For support and inquiries, please contact me at kimothoibrahim@yahoo.com

## Acknowledgements
Kimotho Ibrahim

libraries
PIL
Flask, wtf, forms, login.
