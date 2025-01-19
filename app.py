import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Set the page configuration to wide
st.set_page_config(layout="wide")

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('df_all.csv')

# Set the title of the Streamlit app
st.title('Peer-reviewed Papers on AI and Hypertrophic Cardiomyopathy')
st.write('''
         PubMed Search Parameters:\n
         Keywords: Machine learning terms such as “deep learning,” “neural network*,” “machine learning,” “transformer*,” “gradient boost*,” and “artificial intelligence.”\n
         Conditions: Medical terms including “hypertrophic cardiomyopath*” and “hypertrophic obstructive cardiomyopath*.”
         ''')

# Create a two-column layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("HCM Filters")
    hcm_title_col, hcm_title_select_col = st.columns([1, 3])
    hcm_title_col.write("HCM in Title")
    hcm_in_title = hcm_title_select_col.selectbox('', options=['Ignore', 'Yes', 'No'], key='hcm_title', help="Filter by HCM in Title", label_visibility="collapsed")

    hcm_abstract_col, hcm_abstract_select_col = st.columns([1, 3])
    hcm_abstract_col.write("HCM in Abstract")
    hcm_in_abstract = hcm_abstract_select_col.selectbox('', options=['Ignore', 'Yes', 'No'], key='hcm_abstract', help="Filter by HCM in Abstract", label_visibility="collapsed")

    st.subheader("ECG Filters")
    ecg_title_col, ecg_title_select_col = st.columns([1, 3])
    ecg_title_col.write("ECG in Title")
    ecg_in_title = ecg_title_select_col.selectbox('', options=['Ignore', 'Yes', 'No'], key='ecg_title', help="Filter by ECG in Title", label_visibility="collapsed")

    ecg_abstract_col, ecg_abstract_select_col = st.columns([1, 3])
    ecg_abstract_col.write("ECG in Abstract")
    ecg_in_abstract = ecg_abstract_select_col.selectbox('', options=['Ignore', 'Yes', 'No'], key='ecg_abstract', help="Filter by ECG in Abstract", label_visibility="collapsed")

    # Apply filters
    filtered_df = df.copy()

    if hcm_in_title != 'Ignore':
        filtered_df = filtered_df[filtered_df['HCM_In_Title'] == hcm_in_title]

    if hcm_in_abstract != 'Ignore':
        filtered_df = filtered_df[filtered_df['HCM_In_Abstract'] == hcm_in_abstract]

    if ecg_in_title != 'Ignore':
        filtered_df = filtered_df[filtered_df['ECG_In_Title'] == ecg_in_title]

    if ecg_in_abstract != 'Ignore':
        filtered_df = filtered_df[filtered_df['ECG_In_Abstract'] == ecg_in_abstract]

    # Display the number of papers in the resulting table
    st.write(f"Number of papers: {filtered_df.shape[0]}")

    # Add a heading above the table
    st.markdown("### Click for details")

    # Display the filtered DataFrame in the Streamlit app using AgGrid
    gb = GridOptionsBuilder.from_dataframe(filtered_df)
    gb.configure_pagination(paginationAutoPageSize=True)  # Add pagination
    gb.configure_side_bar()  # Add a sidebar
    gb.configure_selection('single')  # Enable single row selection

    # Hide specific columns
    gb.configure_columns(['HCM_In_Title', 'HCM_In_Abstract', 'ECG_In_Title', 'ECG_In_Abstract'], hide=True)

    # Set column widths
    gb.configure_column('PMID', width=200, flex=1)
    gb.configure_column('TI', width=400, flex=2)
    gb.configure_column('AB', width=400, flex=2)

    gridOptions = gb.build()

    grid_response = AgGrid(
        filtered_df,
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        theme='streamlit',  # Use a valid theme
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        allow_unsafe_jscode=True,  # Set it to True to allow jsfunction to be injected
    )

# Get the selected row
selected_row = grid_response['selected_rows']

with col2:
    # Display the title and abstract of the selected paper
    if selected_row:
        pmid = selected_row[0]['PMID']
        title = selected_row[0]['TI']
        abstract = selected_row[0]['AB']

        # Highlight "ECG" and "Electro" in the title and abstract
        def highlight_text(text):
            text = text.replace("ECG", '<span style="background-color: yellow">ECG</span>')
            text = text.replace("Electro", '<span style="background-color: yellow">Electro</span>')
            return text

        highlighted_title = highlight_text(title)
        highlighted_abstract = highlight_text(abstract)

        st.write("### Selected Paper")
        st.markdown(f"[Link to PubMed Article](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)")
        st.markdown(f"**Title:** {highlighted_title}", unsafe_allow_html=True)
        st.markdown(f"**Abstract:** {highlighted_abstract}", unsafe_allow_html=True)