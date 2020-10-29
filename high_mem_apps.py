"""Parse which of our apps take a lot of memory"""

import streamlit as st
import numpy as np
import pandas as pd
import io

# Remove the file_uploader deprecation warning.
st.set_option('deprecation.showfileUploaderEncoding', False)

# App title
"# High memory apps"

# The dataframe fields
MEMORY_BYTES = 'MEMORY(bytes)'
MEMORY_MB = 'Memory (Mb)'

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


