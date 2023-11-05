import json 
import re 
import os
from abstract_utilities import read_from_file
from abstract_utilities.json_utils import get_any_value,safe_read_from_json
class FileCollator:
    def __init__(self,files_list,key_value=None):
        self.files_list=files_list or []
        self.key_value=key_value or []
    def get_gollated_responses(self,files_list=None,key_value=None):
        if files_list == None:
            files_list=self.files_list
        if key_value == None:
            key_value=self.key_value
        files = self.get_json_data(files_list,key_value=key_value)
        collated_string = self.collate_responses(files)
        return collated_string
    def collate_responses(self,files_list):
        collate_str=''
        nix_list=[]
        for each in files_list:
            lowest = self.get_oldest_first(files_list,nix_list=nix_list)
            nix_list.append(lowest[0])
            collate_str +='\n'+str(files_list[lowest[0]]["value"])
        return collate_str
    @staticmethod
    def get_json_data(files_list,key_value=None):
        if key_value == None:
            if hasattr(self,'key_value'):
                key_value=self.key_value
            key_value = key_value or 'query_response'
        files = []
        for file_path in files_list:
            data = safe_read_from_json(file_path)
            api_response = get_any_value(get_any_value(data,key_value,'query_response'),'api_response')
            response = get_any_value(data,'response')
            created=get_any_value(response ,'created')
            if isinstance(created,list):
                if len(created)>0:
                    created=created[0]
            files.append({'created':int(created),"value":api_response})
        return files
    @staticmethod
    def get_oldest_first(json_list,nix_list=[]):
        lowest=[None,None]
        input(json_list)
        for i,values in enumerate(json_list):
            if i not in nix_list:
                if lowest[0] == None:
                    lowest=[i,int(values['created'])]
                elif int(values['created']) < int(lowest[1]):
                    lowest=[i,int(values['created'])]
        return lowest


def read_from_file_with_multiple_encodings(file_path, encodings=None):
    COMMON_ENCODINGS = [
    'utf-8', 
    'utf-16', 
    'utf-16-be', 
    'utf-16-le', 
    'utf-32', 
    'utf-32-be', 
    'utf-32-le',
    'ISO-8859-1', # also known as latin1
    'ISO-8859-2', # Central and Eastern European languages 
    'ISO-8859-3', 
    'ISO-8859-4',
    'ISO-8859-5', # Cyrillic alphabet
    'ISO-8859-6', # Arabic
    'ISO-8859-7', # Greek
    'ISO-8859-8', # Hebrew
    'ISO-8859-9', # Turkish
    'ISO-8859-10',
    'ISO-8859-13',
    'ISO-8859-14',
    'ISO-8859-15',
    'ISO-8859-16',
    'windows-1250',
    'windows-1251',
    'windows-1252',
    'windows-1253',
    'windows-1254',
    'windows-1255',
    'windows-1256',
    'windows-1257',
    'windows-1258',
    'big5',
    'big5hkscs',
    'cp037',
    'cp424',
    'cp437',
    'cp500',
    'cp720',
    'cp737',
    'cp775',
    'cp850',
    'cp852',
    'cp855',
    'cp856',
    'cp857',
    'cp858',
    'cp860',
    'cp861',
    'cp862',
    'cp863',
    'cp864',
    'cp865',
    'cp866',
    'cp869',
    'cp874',
    'cp875',
    'cp932',
    'cp949',
    'cp950',
    'cp1006',
    'cp1026',
    'cp1140',
    'cp1256',
    'euc_jp',
    'euc_jis_2004',
    'euc_jisx0213',
    'euc_kr',
    'gb2312',
    'gbk',
    'gb18030',
    'hz',
    'iso2022_jp',
    'iso2022_jp_1',
    'iso2022_jp_2',
    'iso2022_jp_2004',
    'iso2022_jp_3',
    'iso2022_jp_ext',
    'iso2022_kr',
    'latin_1',
    'koi8_r',
    'koi8_t',
    'koi8_u',
    'mac_cyrillic',
    'mac_greek',
    'mac_iceland',
    'mac_latin2',
    'mac_roman',
    'mac_turkish',
    'ptcp154',
    'shift_jis',
    'shift_jis_2004',
    'shift_jisx0213',
    'utf_32_be',
    'utf_32_le',
    'utf_16_be',
    'utf_16_le',
    'utf_7',
    'utf_8_sig',
    'latin-1']
    if encodings is None:
        encodings = COMMON_ENCODINGS

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue  # Try the next encoding if decoding fails

    # If none of the encodings work, return None or handle the error as needed
    return None
from docx import Document

def read_docx(file_path):
    # Load the document
    doc = Document(file_path)
    
    # Read and print each paragraph in the document
    text = ''
    for paragraph in doc.paragraphs:
        text+='\n'+paragraph
    return eatAll(text,['\n','',' ','\t'])
