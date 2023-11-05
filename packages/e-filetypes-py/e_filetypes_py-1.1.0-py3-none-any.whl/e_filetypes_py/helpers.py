import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import json

def generate_key(passkey: str, salt: bytes, iterations: int = 100000) -> bytes:
    """
    Generates a key from a passkey and salt. The key is used to encrypt and decrypt files.

    Args:
        passkey (str): Passkey used to generate the key.
        salt (str): Salt used to generate the key.

    Returns:
        bytes: Key used to encrypt and decrypt files

    Usage:
        >>> from e_filetypes_py import helpers
        >>> import os
        >>> salt = os.urandom(16)
        >>> key = helpers.generate_key('passkey', salt)
        >>> key
        b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
    """

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(passkey.encode())

def encrypt_data(data: bytes, passkey: str) -> bytes:
    """
    Encrypts data using AES-GCM, which is good for encrypting large amounts of data.

    Args:
        data (bytes): Data to be encrypted
        key (bytes): Key used to encrypt the data

    Returns:
        bytes: Encrypted data

    Usage:
        >>> from e_filetypes_py import helpers
        >>> import os
        >>> salt = os.urandom(16)
        >>> key = helpers.generate_key('passkey', salt)
        >>> data = b'\x00' * (10485760)  # 10MB of null bytes
        >>> encrypted_data = helpers.encrypt_data(data, key)
        >>> encrypted_data
        b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
    """
    salt = os.urandom(16)
    key = generate_key(passkey, salt)
    aesgcm = AESGCM(key) 
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, data, None)

    encrypted_data = base64.b64encode(salt + nonce + ciphertext)
    return encrypted_data

def write_file_header(path: str, passkey: str, metadata: dict = {}) -> None:
    """
    Writes the file header of an encrypted file. The first 512 bytes of the file are reserved for the file header. Writes 'e-*' as a way to distinguish the file and then encrypts any metadata into the file header.

    Args:
        path (str): Path to the encrypted file
        metadata (dict): Metadata to be encrypted into the file header. Defaults to an empty dictionary. Common metadata includes the name of the file, the author, the date, and a description.
        passkey (str): Passkey used to encrypt the file header. Must be the same passkey used to encrypt the file.

    Raises:
        FileNotFoundError: If the file does not exist
        Exception: The process failed for an unknown reason

    Usage:
        >>> from e_filetypes_py import helpers
        >>> import os
        >>> salt = os.urandom(16)
        >>> key = helpers.generate_key('passkey', salt)
        >>> helpers.write_file_header('path/to/file.e-*', key, {'foo': 'bar'})
    """

    if not os.path.isfile(path):
        raise FileNotFoundError(f"File '{path}' does not exist. Is there a typo?")
    try:
        with open(path, 'rb+') as f:
            f.seek(0)
            f.write(b'e-*')
            f.seek(3)
            metadata_json = json.dumps(metadata)
            encrypted_metadata = encrypt_data(metadata_json.encode(), passkey)
            f.write(encrypted_metadata.ljust(512, b'\0'))
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{path}' does not exist. Is there a typo?")
    except Exception:
        raise Exception(f"Failed to write file header for '{path}'.")

def read_file_header(path: str, passkey: str) -> dict:
    """
    Reads the file header of an encrypted file and returns the file header.

    Args:
        path (str): Path to the encrypted file
        passkey (str): Passkey used to encrypt the file header. Must be the same passkey used to encrypt the file.

    Returns:
        dict: File header   

    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file is not encrypted
        Exception: The process failed for an unknown reason

    Usage:
        >>> from e_filetypes_py import helpers
        >>> import os
        >>> salt = os.urandom(16)
        >>> key = helpers.generate_key('passkey', salt)
        >>> helpers.read_file_header('path/to/file.e-*', key)
        {'foo': 'bar'}
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File '{path}' does not exist. Is there a typo?")
    try:
        with open(path, 'rb') as f:
            file_header = f.read(3)
            if file_header != b'e-*':
                raise ValueError(f"File '{path}' is not encrypted. Please use encrypt the file to an EType first.")
            f.seek(3)
            header_bytes = f.read(512)[:-3] # e-* must have a header of 512 bytes
            header_encrypted = base64.b64decode(header_bytes)
            salt = header_encrypted[:16]
            nonce = header_encrypted[16:28]
            ciphertext = header_encrypted[28:]
            key = generate_key(passkey, salt)
            aesgcm = AESGCM(key)
            try:
                decrypted = aesgcm.decrypt(nonce, ciphertext, None)
                header_json = json.loads(decrypted)
                return header_json
            except ValueError:
                raise ValueError(f"Incorrect passkey for '{path}'.")
            except Exception:
                raise Exception(f"Failed to read file header for '{path}'.")
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{path}' does not exist. Is there a typo?")
    except json.decoder.JSONDecodeError:
        raise ValueError(f"File '{path}' is not encrypted. Please use encrypt the file to an EType first.")
    except UnicodeDecodeError:
        raise ValueError(f"File '{path}' is not encrypted. Please use encrypt the file to an EType first.")
    except Exception:
        raise ValueError(f"File '{path}' is not encrypted. Please use encrypt the file to an EType first.")
    
def encrypt_file(path: str, passkey: str, metadata: dict = {}, keep_file: bool = True, chunking: bool = True, chunk_size: int = 10) -> None:
    """ 
    Encrypts a file using AES-GCM, which is good for encrypting large amounts of data.

    Args:
        path (str): Path to the file to be encrypted
        passkey (str): Passkey used to encrypt the file
        metadata (dict): Metadata to be encrypted into the file header. Defaults to an empty dictionary. Common metadata includes the name of the file, the author, the date, and a description.
        keep_file (bool): If True, the original file will be kept. If False, the original file will be deleted. Defaults to True.
        chunking (bool): If True, the file will be encrypted in chunks. If False, the file will be encrypted all at once. Fails for files over `2.14GB`. Defaults to True.
        chunk_size (int): Size of each chunk in bytes. Defaults to 10 MB.

    Raises:
        FileNotFoundError: If the file does not exist
        Exception: The process failed for an unknown reason

    Usage:
        >>> from e_filetypes_py import helpers
        >>> import os
        >>> salt = os.urandom(16)
        >>> key = helpers.generate_key('passkey', salt)
        >>> helpers.encrypt_file('path/to/file', key, {'foo': 'bar'})
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File '{path}' does not exist. Is there a typo?")
    with open(path, 'rb') as f:
        file_header = f.read(3)
        if file_header == b'e-*':
            raise ValueError(f"File '{path}' is already encrypted. Please use decrypt_file() to decrypt the file.")
    
    absolute_path = os.path.abspath(path)
    directory, file_name = os.path.split(absolute_path)
    base_name, extension = os.path.splitext(file_name)
    full_metadata = {"file_name": file_name, "original_extension": extension, "original_size": os.path.getsize(path), **metadata}

    new_path = os.path.join(directory, base_name + '.e-*')

    if chunking:
        with open(new_path, 'wb') as f:
            write_file_header(path=new_path, passkey=passkey, metadata=full_metadata)
            with open(path, 'rb') as og_f:
                # write chunks after header
                f.seek(3)
                f.seek(512)
                file_size = os.path.getsize(path)
                start_byte = 0
                while start_byte < file_size:
                    og_f.seek(start_byte)
                    full_chunk_size = min((chunk_size * 1024 * 1024), file_size - start_byte + 1)
                    chunk = og_f.read(full_chunk_size)
                    if not chunk:
                        break
                    encrypted_chunk = encrypt_data(chunk, passkey)
                    f.write(encrypted_chunk)
                    start_byte += full_chunk_size
    else:
        with open(new_path, 'wb') as f:
            write_file_header(path=new_path, passkey=passkey, metadata=full_metadata)
            with open(path, 'rb') as og_f:
                f.seek(3)
                f.seek(512)
                data = og_f.read()
                encrypted_data = encrypt_data(data, passkey)
                f.write(encrypted_data)
    if not keep_file:
        os.remove(path)

def decrypt_file(path: str, passkey: str, keep_file=True) -> None:
    """
    Decrypts an encrypted file using AES-GCM

    Args:
        path (str): Path to the encrypted file
        passkey (str): Passkey used to decrypt the file
        keep_file (bool): If True, the original file will be kept. If False, the original file will be deleted. Defaults to True.

    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file is not encrypted
        Exception: The process failed for an unknown reason

    Usage:
        >>> from e_filetypes_py import helpers
        >>> import os
        >>> salt = os.urandom(16)
        >>> key = helpers.generate_key('passkey', salt)
        >>> helpers.decrypt_file('path/to/file.e-*', key)
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File '{path}' does not exist. Is there a typo?")
    try:
        with open(path, 'rb') as f:
            file_header = f.read(3)
            if file_header != b'e-*':
                raise ValueError(f"File '{path}' is not encrypted. Please use encrypt the file to an EType first.")
            file_bytes = f.read()[509:] # e-* must have a header of 512 bytes - 3 bytes for descriptor, read everything afterwards
            file_bytes = base64.b64decode(file_bytes)
            salt = file_bytes[:16]
            nonce = file_bytes[16:28]
            ciphertext = file_bytes[28:]
            key = generate_key(passkey, salt)
            aesgcm = AESGCM(key)
            try:
                decrypted = aesgcm.decrypt(nonce, ciphertext, None)
                metadata = read_file_header(path, passkey)
                name = metadata['file_name']
                absolute_path = os.path.abspath(path)
                directory, _ = os.path.split(absolute_path)
                new_path = os.path.join(directory, (name))
                with open(new_path, 'wb+') as og_f:
                    og_f.write(decrypted)
            except ValueError:
                raise ValueError(f"Incorrect passkey for '{path}'.")
            except Exception:
                raise Exception(f"Failed to read file header for '{path}'.")
            
        if not keep_file:
            os.remove(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{path}' does not exist. Is there a typo?")
    except json.decoder.JSONDecodeError:
        raise ValueError(f"File '{path}' is not encrypted. Please use encrypt the file to an EType first.")
    except UnicodeDecodeError:
        raise ValueError(f"File '{path}' is not encrypted. Please use encrypt the file to an EType first.")
    except Exception:
        raise ValueError(f"File '{path}' is not encrypted. Please use encrypt the file to an EType first.")

    


