import os
import sys
import json
from datetime import datetime
from os import system, name
from time import sleep
import copy
import threading
import imp
import glob
import shutil
from pathlib import Path
import re
import unicodedata
from contextlib import contextmanager
import base64



class Utility:
    '''
    Utility class to handle things that all of the other classes may need.  File / screen access etc.
    '''

    CONNECTION_STRINGS = None
    

    screen_width = 76
    def __init__(self):
        self.bozo ="bozo"
        self.screen_width = 76
        global CONNECTION_STRINGS

    # define our clear function
    def clear(self):
        # for windows
        if name == 'nt':
            _ = system('cls')
        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')

    def count_files_in_two_directories(self,dir1,dir2):
        file_count_1 = len(list(Path(dir1).rglob("*")))
        file_count_2 = len(list(Path(dir2).rglob("*")))
        return file_count_1,file_count_2

    def file_content_from_file_list(self,file_loc_dict):
        return_data_dict = dict()
        
        for key in file_loc_dict.keys():
            data = self.get_data_from_file(file_loc_dict[key])
            return_data_dict[key] = data
        
        return return_data_dict


    def data_frames_from_file_list(self,file_loc_dict):
        pandas_return_dict = dict()
        
        for key in file_loc_dict.keys():
            df = pd.read_csv(file_loc_dict[key])
            df.rename(columns={x: x.replace(' ', '_').lower() for x in df.columns}, inplace=True)
            df.rename(columns={x: x.replace(':', '_').lower() for x in df.columns}, inplace=True)
            df.rename(columns={x: x.replace('__', '_').lower() for x in df.columns}, inplace=True)
            #df = df.apply(lambda x: x.str.lower() if x.dtype=='object' else x)
            pandas_return_dict[key] = df
        
        return pandas_return_dict

    def load_subdirs_into_dict(self,parent_directory,filetype=None,get_content=True):
        output_dict = {}
        list_of_dicts = []

        output_counter = 0
        last_subdir_key =""
        for dirname, subdirList, fileList in os.walk(parent_directory):
             
            for file in fileList:
                this_dict = {}
                subdir_key = str(os.path.basename(dirname))
                if output_counter == 0:

                    output_dict[subdir_key] = ""
                    list_of_dicts = []

                if output_counter > 0 and (str(subdir_key) != str(last_subdir_key)):
                    output_dict[last_subdir_key] = list_of_dicts
                    list_of_dicts = []
                    output_dict[subdir_key] = ""
                
                if filetype is not None and file.lower().endswith(filetype.lower()):
                    file = file
                else:
                    continue
                this_dict[str(os.path.basename(file))] = str(os.path.join(dirname, file))
                if get_content:
                    fido="dido"
                    this_dict[str(os.path.basename(file)) + "_content"] = self.get_data_from_file(os.path.join(dirname, file))
                list_of_dicts.append(this_dict)
                output_counter= output_counter+1
                # print(os.path.join(dirname, file))
                # print(subdir_key)
                # print(last_subdir_key)
                last_subdir_key = subdir_key

        output_dict[last_subdir_key] = list_of_dicts

        #print(output_dict)

        file_name = os.path.join(self.get_this_dir(),"debug_text_output","queries.json")
        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))

        with open(file_name, "w") as outfile:
            outfile.write(json.dumps(output_dict,indent=3))


        return output_dict

    def write_dict_to_json(self,file_name,output_dict):
        #file_name = os.path.join(self.get_this_dir(),"debug_text_output","queries.json")
        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))

        with open(file_name, "w") as outfile:
            outfile.write(json.dumps(output_dict,indent=3))

            
    def load_directory_files(self,
                        directory=None,
                        file_filter=None,
                        print_files=False,
                        print_file_names_only=True,
                        return_pandas_data_frames=False,
                        skip_list=None,
                        load_data_files_into_strings=False
                       ):
        
        if file_filter is None:
            file_filter = "*.*"
        if directory is None:
            directory = self.get_this_dir()
            
        glob_path = os.path.join(directory,file_filter)
        files_in_directory = glob.glob(glob_path)
        
        file_names_only = []
        
        file_loc_dict = dict()
        
        for file in files_in_directory:
            if skip_list is not None:
                if os.path.basename(file) in skip_list:
                    continue
            file_names_only.append(os.path.basename(file))
            file_loc_dict[os.path.basename(file)] = file
            if print_files == True:
                print(file)
                
        if print_file_names_only == True:
            for file in file_names_only:
                print(file)
        
        pandas_dict = None
        
        
        if return_pandas_data_frames == True:

            pandas_dict = self.data_frames_from_file_list(file_loc_dict)

        if load_data_files_into_strings == True:
            file_content_dict = self.file_content_from_file_list(file_loc_dict)
            
        return files_in_directory, file_names_only, file_loc_dict, pandas_dict, file_content_dict
            
    

    def get_data_from_file(self,str_file_name,current_dir=False,encoding=None):
        '''
        Read an entire file and push the data back.
        :param str_file_name:
        :return:
        '''
        if current_dir==True:
            str_file_name = os.path.join(self.get_this_dir(),str_file_name)
        # print("*"*12)
        # print(str_file_name)
        # print("*"*12)
        if encoding is None:
            with open(str_file_name, 'r') as file:
                data = file.read()
            return data
        else:
            with open(str_file_name, encoding=encoding, mode='r') as file:
                data = file.read()
            return data

    def get_data_from_file_into_list_by_line(self,str_file_name,current_dir=False,encoding=None):
        file_data = self.get_data_from_file(str_file_name=str_file_name,current_dir=current_dir,encoding=encoding)
        return file_data.split("\n")

    def has_sub_directories(self,directory):
        for it in os.scandir(directory):
            if it.is_dir():
                return True

    def get_this_dir(self):
        '''
        Return the working directory.
        :return:
        '''
        thisdir = os.getcwd()
        return thisdir
    
    def get_file_size(self,file):
        return(os.stat(file).st_size)
    
    def nukefile(self,file_name):
        with self.suppress_stdout():
            try:
                os.remove(file_name)
            except OSError as e:
                print("Error: %s : %s" % (file_name, e.strerror))


    def nukepath(self,dir_path):
        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))

    def mkdir(self,dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def get_today_day_id(self):
        return datetime.date.today().strftime('%Y%m%d')

    def slugify(self,value, allow_unicode=False):
        """
        Taken from https://github.com/django/django/blob/master/django/utils/text.py
        Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
        dashes to single dashes. Remove characters that aren't alphanumerics,
        underscores, or hyphens. Convert to lowercase. Also strip leading and
        trailing whitespace, dashes, and underscores.
        """
        value = str(value)
        if allow_unicode:
            value = unicodedata.normalize('NFKC', value)
        else:
            value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub(r'[^\w\s-]', '', value.lower())
        return re.sub(r'[-\s]+', '-', value).strip('-_')

    @contextmanager
    def suppress_stdout(self):
        with open(os.devnull, "w") as devnull:
            old_stdout = sys.stdout
            sys.stdout = devnull
            try:  
                yield
            finally:
                sys.stdout = old_stdout

    def write_text_to_file(self,output_file_name,output_string):
        with open(output_file_name, "w") as outfile:
            outfile.write(output_string)

    def read_binary_file_to_base64_string(self,file_name):
        encoded_string = ""
        with open(file_name, "rb") as binary_file:
            encoded_string = base64.encodebytes(binary_file.read()).decode('utf-8')
        return encoded_string
        
    def get_embedded_image_tag_from_image_file(self,file_name,align=None):
        #print(file_name)
        img_text_data = self.read_binary_file_to_base64_string(file_name)
        extension = os.path.splitext(os.path.basename(file_name))[1]
        return self.get_embedded_image_tag_from_base64_string(img_text_data,extension,align)

    def get_embedded_image_tag_from_base64_string(self,img_text_data,extension,align=None):
        #print(file_name)
        if align is not None:
            img_tag = "<img align=\"{}\" src=\"data:image/{};base64,{}\" />".format(align,extension.lower(),img_text_data)
        else:
            img_tag = "<img src=\"data:image/{};base64,{}\" />".format(extension.lower(),img_text_data)
        return img_tag

    def get_embedded_href_tag_from_image_file(self,file_name,align=None):
        #print(file_name)
        binary_text_data = self.read_binary_file_to_base64_string(file_name)
        file_name = os.path.basename(file_name)
        return self.get_embedded_href_tag_from_base64_string(binary_text_data,file_name)

    def get_embedded_href_tag_from_base64_string(self,binary_text_data,filename,align=None):
        #print(file_name)
        if align is not None:
            href_tag = "<a align=\"{}\" href=\"data:application/octet-stream;base64,{}\"  download=\"{}\" >Download: {}</a>".format(align,binary_text_data,filename,filename)
        else:
            href_tag = "<a href=\"data:application/octet-stream;base64,{}\" download=\"{}\" >Download: {}</a>".format(binary_text_data,filename,filename)
        return href_tag