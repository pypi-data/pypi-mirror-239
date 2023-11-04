# Password_Manager

Password Manager is a command-line tool that allows you to securely store and retrieve passwords for various services.
 It provides encryption for password storage and includes features for generating secure passwords.


## Installation

To use the Password Manager, you need to install it first. You can do this using pip:

```bash
$ pip install pass_manager


# Usage 

### Generating an Encryption Key

$ pass_manager --action generate_key


### Setting the Master Password

$ pass_manager --action set_master_password --master_password [YOUR_MASTER_PASSWORD]


### Storing a Password

$ pass_manager --action store --service [SERVICE] --password [PASSWORD] --master_password [YOUR_MASTER_PASSWORD]


### Retrieving a Password

$ pass_manager --action retrieve --service [SERVICE] --master_password [YOUR_MASTER_PASSWORD]


### Generating a Secure Password

$ pass_manager --action generate_password --password_length 16




###### I can't resolve error while retrieving passwords