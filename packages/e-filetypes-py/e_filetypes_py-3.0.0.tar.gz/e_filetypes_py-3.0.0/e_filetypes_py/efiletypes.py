import os
from . import helpers
import secrets

def get_file_header(path: str, passkey: str) -> dict:
    """
    Reads the file header of an encrypted file and returns the file header.

    Args:
        path (str): Path to the encrypted file. Must be an e-# file.
        passkey (str): Passkey used to encrypt the file header. Must be the same passkey used to encrypt the file.

    Returns:
        dict: File header   

    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file is not encrypted  

    Usage:
        >>> from e_filetypes_py import efiletypes
        >>> efiletypes.get_file_header('path/to/file.e-#', 'passkey')
        {'foo': 'bar'}   
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File '{path}' does not exist. Is there a typo?")
    try:
        return helpers.read_file_header(path, passkey)
    except ValueError:
        raise ValueError(f"File '{path}' is not encrypted. Please use encrypt the file to an EType first.")
    except Exception:
        raise Exception(f"Failed to read file header for '{path}'.")
    
def encrypt(path: str, passkey: str, metadata: dict = {}, keep_file: bool = True, chunking: bool = True, chunk_size: int = 10, ignore_encrypted: bool = False) -> None:
    """
    Encrypts a file with a passkey and optional metadata using AES-GCM/256, which is good for encrypting large amounts of data.

    Args:
        path (str): Path to the file to be encrypted
        passkey (str): Passkey used to encrypt the file
        metadata (dict, optional): Metadata to be encrypted with the file. Defaults to {}.
        keep_file (bool, optional): If True, the original file will be kept. Defaults to True.
        chunking (bool, optional): If True, the file will be encrypted in chunks. Defaults to True.
        chunk_size (int, optional): Size of the chunks in MB. Defaults to 10.

    Raises:
        FileNotFoundError: If the file does not exist
        Exception: The process failed for an unknown reason   

    Usage:
        >>> from e_filetypes_py import efiletypes
        >>> efiletypes.encrypt('path/to/file', 'passkey')
    """

    if not os.path.isfile(path):
        raise FileNotFoundError(f"File '{path}' does not exist. Is there a typo?")
    try:
        helpers.encrypt_file(path=path, passkey=passkey, metadata=metadata, keep_file=keep_file, chunking=chunking, chunk_size=chunk_size, ignore_encrypted=ignore_encrypted)
    except Exception:
        raise Exception(f"Failed to read file header for '{path}'.")

def encrypt_folder(path: str, passkey: str, metadata: dict = {}, keep_file: bool = True, chunking: bool = True, chunk_size: int = 10, recursive: bool = False, ignore_encrypted: bool = False) -> None:
    """
    Encrypts a folder with a passkey and optional metadata using AES-GCM/256. This will encrypt all files in the folder. You can enable recursive mode by setting the `recursive` parameter to True. All files will be encrypted using the same passkey.

    Args:
        path (str): Path to the files to be encrypted
        passkey (str): Passkey used to encrypt the files
        metadata (dict, optional): Metadata to be encrypted with the file. Defaults to {}.
        keep_file (bool, optional): If True, the original files will be kept. Defaults to True.
        chunking (bool, optional): If True, the files will be encrypted in chunks. Defaults to True.
        chunk_size (int, optional): Size of the chunks in MB. Defaults to 10.
        recursive (bool, optional): If True, files in sub-folders will also be encrypted. Defaults to False.
        ignore_encrypted (bool, optional): If True, encrypted files will be skipped. Defaults to False.

    Raises:
        FileNotFoundError: If the folder does not exist
        Exception: The process failed for an unknown reason   

    Usage:
        >>> from e_filetypes_py import efiletypes
        >>> efiletypes.encrypt_folder('path/to/folder', 'passkey')
    """

    if not os.path.isdir(path):
        raise FileNotFoundError(f"Folder '{path}' does not exist. Is there a typo?")
    try:
        if recursive:
            for root, _, files in os.walk(path):
                for file in files:
                    helpers.encrypt_file(path=os.path.join(root, file), passkey=passkey, metadata=metadata, keep_file=keep_file, chunking=chunking, chunk_size=chunk_size, ignore_encrypted=ignore_encrypted)
        else:
            for file in os.listdir(path):
                if os.path.isfile(os.path.join(path, file)):
                    helpers.encrypt_file(path=os.path.join(path, file), passkey=passkey, metadata=metadata, keep_file=keep_file, chunking=chunking, chunk_size=chunk_size, ignore_encrypted=ignore_encrypted)
                else:
                    continue
    except Exception:
        raise Exception(f"Failed to encrypt '{path}'.")

def decrypt(path: str, passkey: str, keep_file: bool = True, ignore_existing: bool = False) -> None:
    """
    Decrypts an e-# file with a passkey.


    Args:
        path (str): Path to the file to be decrypted. Must be an e-# file.
        passkey (str): Passkey used to encrypt the file
        keep_file (bool, optional): If True, the original file will be kept. Defaults to True.
        ignore_existing (bool, optional): If True, the file will be decrypted even if it already exists. Defaults to False.

    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file is not encrypted
        Exception: The process failed for an unknown reason

    Usage:
        >>> from e_filetypes_py import efiletypes
        >>> efiletypes.decrypt('path/to/file.e-#', 'passkey')
    """

    if not os.path.isfile(path):
        raise FileNotFoundError(f"File '{path}' does not exist. Is there a typo?")
    try:
        helpers.decrypt_file(path=path, passkey=passkey, keep_file=keep_file, ignore_existing=ignore_existing)
    except ValueError:
        raise ValueError(f"File '{path}' is not encrypted. Please use encrypt the file to an EType first.")
    except Exception:
        raise Exception(f"Failed to read file header for '{path}'.")

def decrypt_folder(path: str, passkey: str, keep_file=True, recursive: bool = False, ignore_existing: bool = False) -> None:
    """
    Decrypts an e-# file with a passkey.


    Args:
        path (str): Path to the folder to be decrypted. Must be a directory containing e-# files.
        passkey (str): Passkey used to encrypt the files.
        keep_file (bool, optional): If True, the original file will be kept. Defaults to True.
        recursive (bool, optional): If True, files in sub-folders will also be decrypted. Defaults to False.
        ignore_existing (bool, optional): If True, files that have already been decrypted will be skipped. Defaults to False.

    Raises:
        FileNotFoundError: If the folder does not exist.
        ValueError: If the file is not encrypted.
        Exception: The process failed for an unknown reason.

    Usage:
        >>> from e_filetypes_py import efiletypes
        >>> efiletypes.decrypt_folder('path/to/folder.e-#', 'passkey')
    """

    if not os.path.isdir(path):
        raise FileNotFoundError(f"Folder '{path}' does not exist. Is there a typo?")
    try:
        if recursive:
            for root, _, files in os.walk(path):
                for file in files:
                    helpers.decrypt_file(path=os.path.join(root, file), passkey=passkey, keep_file=keep_file, ignore_existing=ignore_existing)
        else:
            for file in os.listdir(path):
                if os.path.isfile(os.path.join(path, file)):
                    helpers.decrypt_file(path=os.path.join(path, file), passkey=passkey, keep_file=keep_file, ignore_existing=ignore_existing)
                else:
                    continue
    except ValueError:
        raise ValueError(f"Folder '{path}' is not encrypted. Please use encrypt the folder to an EType first.")
    except Exception:
        raise Exception(f"Failed to read file header for '{path}'.")

def generate_passkey(length: int = 32) -> str:
    """
    Generates a 32 character passkey for use in encrypting files.

    Args:
        length (int, optional): Length of the passkey. Defaults to 32.

    Returns:
        str: Passkey

    Usage:
        >>> from e_filetypes_py import efiletypes
        >>> efiletypes.generate_passkey()
        'passkey'
    """
    return secrets.token_hex(length)

def generate_passphrase(length: int = 8) -> str:
    """
    Generates a 8 word passphrase for use in encrypting files.

    Args:
        length (int, optional): Length of the passphrase. in words. Defaults to 8.
    Returns:
        str: Passphrase

    Usage:
        >>> from e_filetypes_py import efiletypes
        >>> efiletypes.generate_passphrase()
        'passphrase passphrase passphrase passphrase passphrase passphrase passphrase passphrase'
    """
    # wordlist is sourced from linux /usr/share/dict/words
    with open(os.path.join(os.path.dirname(__file__), 'library', 'words.txt')) as f:
        words = [word.strip() for word in f]
    return ' '.join([secrets.choice(words).lower().replace("'", "").strip() for _ in range(length)])

