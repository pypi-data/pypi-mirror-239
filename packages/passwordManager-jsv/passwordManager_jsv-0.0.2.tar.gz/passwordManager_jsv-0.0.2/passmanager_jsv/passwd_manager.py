from cryptography.fernet import Fernet
import argparse
import os
import secrets
import string


class PasswordManager:
    def __init__(self):
        self.master_key = None
        with open('key.key','wb') as key_file:
            keys=(Fernet.generate_key())
            key_file.write(keys)
        with open('key.key','rb') as key_file:
            key=key_file.read()
            self.master_key=Fernet(key)

    def set_master_password(self, master_password):
        # self.master_key = Fernet(Fernet.generate_key())

        self.master_password = master_password.encode()

    def encrypt_password(self, password):
        return self.master_key.encrypt(password.encode())

    def decrypt_password(self, encrypted_password):
        return self.master_key.decrypt(encrypted_password).decode()

    def generate_password(self, length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        if length < 8:
            raise ValueError("Password length must be at least 8 characters.")
        return ''.join(secrets.choice(characters) for _ in range(length))

    def store_password(self, service, password):
        encrypted_password = self.encrypt_password(password)
        with open('passwords.txt', 'a') as file:
            file.write(f"{service}: {encrypted_password}\n")

    def retrieve_password(self, service):
        with open('passwords.txt', 'r') as file:
            for line in file:
                entry = line.split(': ')
                if entry[0] == service:
                    encrypted_password = entry[1]
                    return self.decrypt_password(encrypted_password)
            return None


def main():
    parser = argparse.ArgumentParser(description="Password Manager")
    parser.add_argument(
        '--action', choices=['store', 'retrieve', 'generate'], help='Operation to perform', required=True)
    parser.add_argument('--master-password', help='Master password')
    parser.add_argument('--service', help='Service name')
    parser.add_argument('--password', help='Password')
    parser.add_argument('--length', type=int, default=12,
                        help='Length of generated password')

    args = parser.parse_args()
    password_manager = PasswordManager()

    if args.action == 'store':
        if not args.master_password or not args.service or not args.password:
            print("Please provide master password, service, and password to store.")
        else:
            password_manager.set_master_password(args.master_password)
            password_manager.store_password(args.service, args.password)
            print("Password stored successfully.")

    elif args.action == 'retrieve':
        if not args.master_password or not args.service:
            print("Please provide master password and service to retrieve password.")
        else:
            password_manager.set_master_password(args.master_password)
            password = password_manager.retrieve_password(args.service)
            if password:
                print(f"Retrieved password for {args.service}: {password}")
            else:
                print(f"No password found for {args.service}.")

    elif args.action == 'generate':
        if not args.master_password:
            print("Please provide master password to generate a password.")
        else:
            password_manager.set_master_password(args.master_password)
            generated_password = password_manager.generate_password(
                args.length)
            print(f"Generated Password: {generated_password}")


if __name__ == '__main__':
    main()

