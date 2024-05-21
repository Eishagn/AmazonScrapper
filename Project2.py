from cryptography.fernet import Fernet

def decrypt_file(key, input_file, output_file):
    # Read encrypted data from input file
    with open(input_file, 'rb') as f:
        ciphertext = f.read()

    # Decrypt ciphertext
    cipher = Fernet(key)
    plaintext = cipher.decrypt(ciphertext)

    # Write decrypted data to output file
    with open(output_file, 'wb') as f:
        f.write(plaintext)

# Provide the encryption key
encryption_key = input("Enter the encryption key: ")
key = bytes.fromhex(encryption_key)

# Specify the encrypted file and the output file for decrypted data
encrypted_file = 'encrypted_kurti.csv'
decrypted_file = 'decrypted_kurti.csv'

# Decrypt the encrypted file
decrypt_file(key, encrypted_file, decrypted_file)

print("File decrypted successfully.")
print("Decrypted file:", decrypted_file)
