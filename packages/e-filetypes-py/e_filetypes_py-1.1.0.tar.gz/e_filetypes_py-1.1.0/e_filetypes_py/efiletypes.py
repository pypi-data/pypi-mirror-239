import os
from . import helpers

def get_file_header(path: str, passkey: str) -> dict:
    """
    Reads the file header of an encrypted file and returns the file header.

    Args:
        path (str): Path to the encrypted file. Must be an e-* file.
        passkey (str): Passkey used to encrypt the file header. Must be the same passkey used to encrypt the file.

    Returns:
        dict: File header   

    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file is not encrypted  

    Usage:
        >>> from e_filetypes_py import efiletypes
        >>> efiletypes.get_file_header('path/to/file.e-*', 'passkey')
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
    
def encrypt(path: str, passkey: str, metadata: dict = {}, keep_file: bool = True, chunking: bool = True, chunk_size: int = 10) -> None:
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
        {'path': 'path/to/file.e-*', 'metadata': {'foo': 'bar'}} 
    """

    if not os.path.isfile(path):
        raise FileNotFoundError(f"File '{path}' does not exist. Is there a typo?")
    try:
        helpers.encrypt_file(path=path, passkey=passkey, metadata=metadata, keep_file=keep_file, chunking=chunking, chunk_size=chunk_size)
    except ValueError:
        raise ValueError(f"File '{path}' is not encrypted. Please use encrypt the file to an EType first.")
    except Exception:
        raise Exception(f"Failed to read file header for '{path}'.")

def decrypt(path: str, passkey: str, keep_file=True) -> None:
    """
    Decrypts an e-* file with a passkey.


    Args:
        path (str): Path to the file to be decrypted. Must be an e-* file.
        passkey (str): Passkey used to encrypt the file
        keep_file (bool, optional): If True, the original file will be kept. Defaults to True.

    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file is not encrypted
        Exception: The process failed for an unknown reason

    Usage:
        >>> from e_filetypes_py import efiletypes
        >>> efiletypes.decrypt('path/to/file.e-*', 'passkey')
        {'path': 'path/to/file', 'metadata': {'foo': 'bar'}}
    """

    if not os.path.isfile(path):
        raise FileNotFoundError(f"File '{path}' does not exist. Is there a typo?")
    try:
        helpers.decrypt_file(path=path, passkey=passkey, keep_file=keep_file)
    except ValueError:
        raise ValueError(f"File '{path}' is not encrypted. Please use encrypt the file to an EType first.")
    except Exception:
        raise Exception(f"Failed to read file header for '{path}'.")


