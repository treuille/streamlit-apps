"""Parse which of our apps take a lot of memory"""

import streamlit as st
import numpy as np
import pandas as pd
import re
import collections

# Remove the file_uploader deprecation warning.
st.set_option('deprecation.showfileUploaderEncoding', False)

# App title
"# High memory apps"

# The dataframe fields
APP_NAME = 'NAME'
MEMORY_BYTES = 'MEMORY(bytes)'
MEMORY_MB = 'Memory (Mb)'
APP_USER = 'user'
APP_REPO = 'repo'
APP_BRANCH = 'branch'
APP_PATH = 'path'
APP_ID = 'app_id'
APP_URL = 'url'

# Additional app fields
StreamlitApp = collections.namedtuple('StreamlitApp',
    [APP_USER, APP_REPO, APP_BRANCH, APP_PATH, APP_URL])

# App conversion regular expressios
file_buffer = st.file_uploader('Upload the list of apps.', type='txt', encoding='utf8')
df = pd.read_csv(file_buffer, delim_whitespace=True)

# Check to see whether all the memory ends in "Mi"
ends_with_mi = np.vectorize(lambda s: s.endswith('Mi'))
assert np.all(ends_with_mi(df[MEMORY_BYTES])), \
    'All memory values must end with "Mi"'

# Convert the memory field to a number of mb,
# assuming all memory values end in "Mi"
to_mb = np.vectorize(lambda s: int(s[:-2]))
df[MEMORY_MB] = to_mb(df[MEMORY_BYTES])
df.sort_values(MEMORY_MB, inplace=True, ascending=False)
st.write(df)

# Find my own apps 
is_my_app = np.vectorize(lambda s: 'treuille' in s)
df = df[is_my_app(df[APP_NAME])]
"Just my apps"
df,
st.write(list(df[APP_NAME]))

# Parse out my apps
# user / repo / branch / path / url

RE_APP_NAME = re.compile(
    r'app-(?P<user>\w+)' + \
    r'--(?P<repo>(\w+(-\w+)*))' + \
    r'(--(?P<branch>(\w+(-\w+)*)))?' + \
    r'(--(?P<path>(\w+(-\w+)*)))?' + \
    r'--(?P<app_id>(\w+(-\w+)*))') 

RE_USER = r'app-(?P<user>\w+)'
RE_REPO = r'--(?P<repo>(\w+(-\w+)*))'
RE_BRANCH = r'(--(?P<branch>(\w+(-\w+)*)))?'
RE_PATH = r'--(?P<path>\w+)--(?P<app_id>\w+(-\w+)*)'
RE_APP_NAME = re.compile(f'{RE_USER}{RE_REPO}{RE_BRANCH}{RE_PATH}')
    
#     r'(--(?P<branch>(\w+(-\w+)*)))?' + \
#     r'(()|
#     r'(--(?P<path>(\w+(-\w+)*)))?' + \
#     r'--(?P<app_id>(\w+(-\w+)*))') 

def parse_app_name(app_name):
    # Parse the app name using the regular expression
    match = RE_APP_NAME.match(app_name)
    if match == None:
        return {}
    coords = match.groupdict()

    # The default branch is master.
    if coords[APP_BRANCH] == None:
        coords[APP_BRANCH] = 'master'

    # Demunge the path
    # coords[APP_PATH] = coords[APP_PATH].replace('_', '/').replace('0', '_') + '.py'

    # Construct the URL
    coords[APP_URL] = f'https://share.streamlit.io/{coords[APP_USER]}'
    coords[APP_URL] += f'/{coords[APP_REPO]}'
    coords[APP_URL] += f'/{coords[APP_BRANCH]}'
    coords[APP_URL] += f'/{coords[APP_PATH]}'
    
    # All done!
    return coords

for app_name in df[APP_NAME]:
    st.write(app_name)
    st.write(parse_app_name(app_name))
