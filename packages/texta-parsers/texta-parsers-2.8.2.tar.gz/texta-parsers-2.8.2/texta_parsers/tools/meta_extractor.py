import regex as re
import os
from typing import List, Union
from datetime import datetime
from dateutil import parser


class MetaExtractor:
    def __init__(self, meta: dict, file_path: str, date_format: str = "%Y-%m-%dT%H:%M:%S.%f"):
        self.__meta: dict = meta
        self.__file_path: str = file_path
        self.__compiled_patterns: dict = {}
        self.__output_date_format: str = date_format


    def _get_fields_by_keyword(self, keyword: str) -> List[str]:
        if keyword not in self.__compiled_patterns:
            self.__compiled_patterns[keyword] = re.compile(keyword, re.IGNORECASE)

        compiled_pattern = self.__compiled_patterns.get(keyword)
        candidates = []
        for field in self.__meta.keys():
            if compiled_pattern.search(field):
                candidates.append(field)
        return candidates

    def _get_meta_value(self, field_names: str, empty_value):
        try:
            out = self.__meta.get(field_names[0], empty_value)
        except:
            out = empty_value
        return out

    def _reformat_date(self, date_string: str) -> str:
        try:
            dt = parser.parse(date_string)
            output_date = dt.strftime(self.__output_date_format)
        except Exception as e:
            output_date = None
        return output_date

    def _get_strings(self, elem: Union[str, List[str]], lst: List[str] = []):
        if isinstance(elem, str):
            lst.append(elem)
        elif isinstance(elem, list):
            for e in elem:
                self._get_strings(e, lst)
        return lst

    @property
    def creation_date_fields(self):
        return self._get_fields_by_keyword("create|^date$")

    @property
    def modification_date_fields(self):
        field_candidates_raw = self._get_fields_by_keyword("modified")
        to_exclude = ["File Modified Date", "by"]
        exclude_pattern = "|".join(to_exclude)
        field_candidates = [
            c for c in field_candidates_raw
            if not re.search(exclude_pattern, c, re.IGNORECASE)
        ]

        return field_candidates

    @property
    def author_fields(self):
        return self._get_fields_by_keyword("author")

    @property
    def title_fields(self):
        return self._get_fields_by_keyword("title")

    @property
    def content_type_fields(self):
        return self._get_fields_by_keyword("content-type|content type")

    @property
    def producer_fields(self):
        return self._get_fields_by_keyword("producer")

    @property
    def parser_fields(self):
        return self._get_fields_by_keyword("x-parsed-by")

    @property
    def parsers_used(self) -> List[str]:
        parsers_used_raw = self._get_meta_value(self.parser_fields, [])
        parsers_used = self._get_strings(parsers_used_raw)
        # One parser can occur multiple times, but we currently output only
        # one occurrence for each
        return list(set(parsers_used))


    @property
    def creation_date(self) -> str:
        created_date_raw = self._get_meta_value(self.creation_date_fields, None)
        created_date = self._reformat_date(created_date_raw)
        return created_date

    @property
    def modification_date(self) -> str:
        modified_date_raw = self._get_meta_value(self.modification_date_fields, None)
        modified_date = self._reformat_date(modified_date_raw)
        return modified_date

    @property
    def file_modification_date(self) -> str:
        mod_time = os.path.getmtime(self.__file_path)
        mt = datetime.fromtimestamp(mod_time)
        file_modified_date = mt.strftime(self.__output_date_format)

        return file_modified_date

    @property
    def author(self) -> str:
        return self._get_meta_value(self.author_fields, "")

    @property
    def title(self) -> str:
        return self._get_meta_value(self.title_fields, "")

    @property
    def content_type(self) -> List[str]:
        return self._get_meta_value(self.content_type_fields, [])

    @property
    def producer(self) -> str:
        return self._get_meta_value(self.producer_fields, "")

    @property
    def file_size_kb(self) -> float:
        file_size = os.path.getsize(self.__file_path)
        file_size_kb = file_size / 1024.0
        return file_size_kb

    @property
    def ocr_applied(self) -> bool:
        # Unfortunately usage of TesseractOCRParser isn't
        # always an indicator for OCR
        parsers_used = self.parsers_used
        if "org.apache.tika.parser.ocr.TesseractOCRParser" in parsers_used:
            return True
        return False

    @property
    def meta(self):
        _meta = {
            "created_date": self.creation_date,
            "modified_date": self.modification_date,
            "file_modified_date": self.file_modification_date,
            "author": self.author,
            "title": self.title,
            "content_type": self.content_type,
            "producer": self.producer,
            "file_size_kb": self.file_size_kb
        }
        return _meta
