import subprocess
import unicodedata
import re
import os
import hashlib
import shutil
from enum import Enum
from texta_parsers.settings import META_FIELD
from texta_parsers.tools.extension import Extension

class ParserOutputType(Enum):
     EMAIL = 1
     COLLECTION = 2
     FILE = 3

def get_output_type(item, index_per_collection: bool = False):
    #item is from email generator in the form of (email_dict, [attachment_dict])
    #can not check extension here because input can come directly from email parser as well
    #which does not have that field
    if(type(item) == tuple):
        return ParserOutputType.EMAIL
    #item is from docparser generator, find type by checking extension
    else:
        extension = item[META_FIELD]["extension"]
        if(extension in Extension.COLLECTION_EXTENSIONS) and index_per_collection:
            return ParserOutputType.COLLECTION
        else:
            return ParserOutputType.FILE


def check_digidoc_exists():
    try:
        p = subprocess.run(["digidoc-tool"], stdout=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False


def create_hash(s: str):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def slugify(value, allow_unicode: bool = False) -> str:
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[.]+", "_", value.lower())
    value = re.sub(r"[^\w\s-]", "", value.lower())
    value = re.sub(r"[-\s]+", "_", value).strip("-_")
    return value


def validate_encoding(file_path: str, temp_dir: str, extension: str):
    try:
        # just try, if encoding the file path into utf-8 works
        # to validate compatibility with Tika, but no need
        # to actually convert it
        file_path.encode("utf-8")
        return_path = file_path
        valid_encoding = True

    except UnicodeEncodeError:
        # if file name is in a weird encoding, copy the file into
        # a temp dir with corrected file name
        slug_path = slugify(file_path)
        hashed_name = create_hash(slug_path)
        temp_file_path = os.path.join(temp_dir, f"{hashed_name}{extension}")
        shutil.copyfile(file_path, temp_file_path)
        return_path = temp_file_path
        valid_encoding = False
    return (return_path, valid_encoding)
