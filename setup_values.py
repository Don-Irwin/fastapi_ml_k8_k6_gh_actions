import sys, getopt,os,smtplib,time
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import subprocess
import random
from utility import Utility as util
from pathlib import Path

def main():

    u = util()

    python_api_address = os.getenv("python_api_address")
    if python_api_address is not None:

        l_template_files = ["load.js.template"]
        l_output_files = ["load.js"]
        d_tokens_to_replace = {"<ipaddress/>":python_api_address}

        i = 0 
        while i<len(l_template_files):
            template_file = l_template_files[i]
            output_file = l_output_files[i]
            output_template       = os.path.join(u.get_this_dir(),template_file)
            out_file        = os.path.join(u.get_this_dir(),output_file)
            template_text  = u.get_data_from_file(output_template)
            for token in d_tokens_to_replace:
                replace_value = d_tokens_to_replace[token]
                template_text=template_text.replace(token,replace_value)
            u.write_text_to_file(out_file,template_text)
            print(out_file)
            i = i +1




main()

