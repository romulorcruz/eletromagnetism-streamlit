import streamlit as st

st.title("How to use SciMagNet")
st.markdown(    
    """
    Go to the page "Coil" in section "Package" to use the interface. If want to use package direct in python, install the package using: pip install scimagnet or acesss the repository at https://github.com/romulorcruz/SciMagnet-lib 
    """
)

st.header("About the project")
st.markdown(
    """
    This app was created as part of the development of a Python library for the simulation of electromagnets used at CNPEM.
    The library allows users to generate coil geometries (such as solenoids and racetracks), compute magnetic field, length, resistance and dissipated power, and visualize the results in 3D.
    The main goal is to standardize and speed up the initial design and validation of new magnets, avoiding the need to rewrite analysis scripts every time a new geometry is studied.
    By offering a simple graphical interface built with Streamlit, this site makes the package accessible both to users who are familiar with Python and to those who are not, providing 
    a single place to load or generate coils, run calculations and explore interactive plots of the magnetic field."""
)
st.header("Who we are")
st.markdown(
    """
    This project was developed by Marco Túlio Lima Rodrigues and Rômulo Emanuel Rabelo Cruz, undergraduate students at Ilum – School of Science (CNPEM), currently in the 4th semester.


    SciMag and SciMagNet are being developed by two undergraduate students at **Ilum – School of Science (CNPEM)**, currently in the 4th semester:

    - **Marco Túlio Lima Rodrigues**
    - **Rômulo Emanuel Rabelo Cruz**

    This project is part of a **Research Initiation** discipline and is carried out within the  
    **Adjunct Directorate for Technology (DAT)**, in collaboration with the groups:

    - **SME – Magnetic and Electromagnetic Systems**
    - **COM – Computing with Mathematical Optimization**

    We are advised and supported by the following collaborators:

    - **Andrei Guinancio de Carvalho Pereira** – COM
    - **Eduardo Moraes Ferrari** – COM  
    - **Ivan Prearo** – PhD student at Unicamp
    - **João Henrique Ramos da Silva** – Master's student at **Universität Rostock** 
    - **Lucas Henrique Francisco** – SME  
    - **Sofia Garcia Telles Brito** – COM  

    Together with our supervisors, we are building an open, extensible tool to support the design and analysis of electromagnets used in CNPEM’s scientific facilities.

"""

)

st.info("If you have any questions, suggestions, or would like to contribute to the project, please feel free to reach out to us at romulorabelocruz@gmail.com or marcotlr2312@gmail.com.")
st.markdown(
    """
    <hr>
    <p style="text-align:center; font-size:0.8rem; opacity:0.7;">
    Interface for the SciMagNet library · Ilum / CNPEM – DAT / SME / COM
    </p>
    """,
    unsafe_allow_html=True,
)