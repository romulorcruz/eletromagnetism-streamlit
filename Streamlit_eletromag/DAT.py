import streamlit as st
import os  

current_dir = os.path.dirname(os.path.abspath(__file__))

# st.set_page_config(page_title="My Package App", page_icon="🧙🏼‍♂️")

# st.title("My Python Package Interface")

#-----------------Page setup-----------------

Documentation = st.Page(
    page="Pages/Documentation.py",
    title= "Main informations",
    icon= ":material/home:",
    default=True,
)

# about_page = st.Page(
#     page="Pages/About.py",
#     title= "About us",
#     icon= ":material/info:",
# )

coil_page = st.Page(
    page="Pages/Coil.py",
    title= "Coil",
    icon= ":material/bolt:",
)
IMG_PATH = os.path.join(current_dir, "assets", "Ilum.png")

with st.sidebar:
    st.image(IMG_PATH, use_container_width=True)

pg = st.navigation({
    "Info": [Documentation],
    "Package": [coil_page]})



pg.run()