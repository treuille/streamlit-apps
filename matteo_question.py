import streamlit as st
import string

# with st.echo():
#     def st_grid(row_headers, column_headers, content):
#         n_cols = len(column_headers)
#         elements = st.beta_columns(n_cols + 1)
#         for element, header in zip(elements[1:], column_headers):
#             element.markdown(header)
#         for row_index, header in enumerate(row_headers):
#             elements = st.beta_columns(n_cols + 1)
#             elements[0].markdown(header)
#             for col_index, element in enumerate(elements[1:]):
#                 element.markdown(content[row_index * n_cols + col_index])

with st.echo():
    import numpy as np

    def st_grid(row_headers, column_headers, content):
        grid = np.array([st.beta_columns(len(column_headers) + 1)
                for _ in range(len(row_headers) + 1)])
        for element, header in zip(grid[0,1:], column_headers):
             element.markdown(header)
        for element, header in zip(grid[1:,0], row_headers):
             element.markdown(header)
        for element, value in zip(grid[1:,1:].flat, content):
             element.markdown(value)

n_rows = st.sidebar.number_input('Rows', 1, 26, 10)
n_cols = st.sidebar.number_input('Columns', 1, 26, 10)

row_headers = string.ascii_lowercase[:n_rows]
column_headers = string.ascii_uppercase[:n_cols]
content = range(n_rows * n_cols)
st_grid(row_headers, column_headers, content)
