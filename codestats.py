#!/usr/bin/env python3

# codestats - Code Stats
# Copyright (C) 2024 Ray Mentose.

v = '0.0.1'
man = """
codestats - Code Stats
Copyright (C) 2024 Ray Mentose.

Usage:
--
  codestats      arg1          arg2
  ---------      ----          ----
  codestats      project-dir   .py
  codestats      project-dir   .py,.md,.js,.cc

  codestats      man|help|-h|--help|-v

--

"""

import os
import re
import sys

from subprocess import check_output, CalledProcessError

def escape_for_csv(input):
  """Prepares the given input for csv output"""
  if isinstance(input, str):
    # escape a double quote (") with additional double quote ("")
    value = input.replace('"', '""')
    value = '"' + value + '"'
    return value
  else:
    return input


def preserve_keys(data, pres):
  """Preserves only the list of keys in 'pres' for given dict 'data'"""
  resp = []
  for d in data:
    resp.append({key: d[key] for key in pres if key in d})
  return resp

def process_codestats(dir, exts):
  """Get code stats for project directory (dir) and file extensions (exts)"""
  # dir = os.path.abspath(os.path.expanduser(dir))

  grep_exts = "-e '" + "$' -e '".join(re.sub('\\.','\\.',exts).strip(',').split(',')) + "$'"
  cmd = f"cd {dir} && git ls-files | grep {grep_exts} | sed 's| |\\\\ |g' | xargs wc -l"

  try:
    out = check_output(cmd, shell=True, encoding='utf-8')
  except CalledProcessError as e:
    out = e

  print(out)

def main():

  if len(sys.argv) == 1:
    print('For usage info, use the man or help (-h) options.')

  elif sys.argv[1] in ('man','help','-h','--help'):
    print(man.strip())

  elif sys.argv[1] in ('-v','--version'):
    print(f'Version: {v}')

  elif len(sys.argv) == 3:
    process_codestats(sys.argv[1], sys.argv[2])

  elif len(sys.argv) == 2:
    print('Please also specify file extensions: .py,.md etc. For details see help.')

  else:
    print('Incorrect usage. Please use man or help for options.')


if __name__ == '__main__':
  main()
