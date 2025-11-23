import streamlit as st
import electromagnetism as eml
import numpy as np
import pandas as pd



st.set_page_config(page_title="Coil Model", page_icon="     🧲", layout="wide")

st.title("Coil Model Page")

Ratio = st.radio("Do you already have a Coil Path?", options=("Yes", "No"))
# Path = st.file_uploader("Upload your Coil file", type=["txt", "csv", "xlsx"])
if Ratio == "Yes":
    Path = st.file_uploader("Upload your Coil Path. The file must contain only numeric coordinates and separators." \
    " Do not include headers, titles, or text in any column. ", type=["txt", "csv", "xlsx"])
    if Path is not None: 
        type_of_file = Path.name.split(".")[-1]
        if type_of_file == "xlsx":
            df = pd.read_excel(Path)
        
        elif type_of_file in ("csv","txt"):
            df =pd.read_csv(Path,sep=r"[,\s;]+", engine='python')
        
        df = df.astype(float)
        df = np.array(df)
        # st.write(df)
        coilPath = np.array(df)
        st.success("Coil loaded successfully!")
        if coilPath.shape[0] == 3:
            coil = eml.models.coil.Coil(coilPath)
            st.warning("The Coil Path has been transposed to fit the required shape (N, 3). Please verify if the coordinates are correct.")
        else:
            coil = eml.models.coil.Coil(coilPath, invertRAxis=True)
        
        col1, col2 = st.columns([0.3, 0.7])   # ajuste as proporções se quiser

        with col1:
            st.subheader("Path")
            st.dataframe(pd.DataFrame(df, columns=["X", "Y", "Z"]) , use_container_width=True, height=350, )

        with col2:
            st.subheader("Visualization")
            fig = coil.plot(show=False)    # sua função/objeto que gera o Plotly Figure
            st.plotly_chart(fig, use_container_width=True)
        
        st.write("Coil Length (m): ", coil.length)
        p1_3d = st.radio("Do you want to calculate the Magnetic Field at a single point or across a set of points in space?", options=("1 point", "Array of points", "cloud of points"))
        if p1_3d == "1 point":
            method = st.selectbox("What integration method do you want to use to calculate the magnetic field using biot savart?", options=['Riemann', 'Simpson'])
            point = st.text_input("Point to calculate the magnetic field (x,y,z) - Only the numeric values separated by commas:", value="")
            current = st.text_input("Current (A) - Only the numeric value:", value="")
            
            if current and point != "":
                point = np.fromstring(point, sep=",", dtype=float)
                current = float(current)
                B = coil.biotSavart1p(r0=point, I=current, integration_method=method)

                dfB = pd.DataFrame(
                    {"value": [B[0], B[1], B[2], np.linalg.norm(B)]},
                    index=["Bx (T)", "By (T)", "Bz (T)", "|B| (T)"]
                )
                st.dataframe(dfB.style.format("{:.6e}"))
        elif p1_3d == "Array of points":
            method = st.selectbox("What integration method do you want to use to calculate the magnetic field using biot savart?", options=['Riemann', 'Simpson'])
            current = st.text_input("Current (A) - Only the numeric value:", value="")
            points_file = st.file_uploader("Upload your Points file. The file must contain only numeric coordinates and separators.", type=["txt", "csv", "xlsx"])
            points = st.text_input("Input the points directly as list of coordinates. Each point should be in the format [x,y,z] and separated by semicolon .\
                                    Example: [0,0,0]; [1,0,0]; [0,1,0]", value="")
            if points_file is not None and current != "" and points == "":#or points != "" and current != "":
                st.info("Calculating... This may take a few moments depending on the number of points and the coil complexity.")
                type_of_file = points_file.name.split(".")[-1]
                if type_of_file == "xlsx":
                    df_points = pd.read_excel(points_file)
                
                elif type_of_file in ("csv","txt"):
                    df_points =pd.read_csv(points_file,sep=r"[,\s;]+", engine='python')
                
                df_points = df_points.astype(float)
                points_array = np.array(df_points)
                # else:else:
                #fzr o caso de points inseridos manualmente e conferir se estçao no formato certo ou se precisa usar o invertAxis
                
                current = float(current)
                arr = coil.biotSavart3d(points_array, integration_method=method,  I=current, invertPAxis=False)
                # arr = np.asarray(B_array, dtype=float)
                if arr.shape[1] == 6:
                    pass                     # já está (N,6)
                elif arr.shape[0] == 6:
                    arr = arr.T              # era (6,N) → vira (N,6)
                else:
                    raise ValueError(f"Expected (N,6) or (6,N), got {arr.shape}")


                dfB = pd.DataFrame(arr, columns=["x", "y", "z", "Bx (T)", "By (T)", "Bz (T)"])
                dfB["|B| (T)"] = np.linalg.norm(dfB[["Bx (T)", "By (T)", "Bz (T)"]].to_numpy(), axis=1)
                st.dataframe(dfB.style.format("{:.6e}"))

            if points != "" and current != "" and points_file is None:
                st.info("Calculating... This may take a few moments depending on the number of points and the coil complexity.")
                points_list = []
                # Split by space or comma
                points = points.split(';')
                for point in points:
                    point = np.fromstring(point.strip('[]') , sep=",", dtype=float)
                    points_list.append(point)
                points_array = np.array(points_list)
                current = float(current)
                B_array = coil.biotSavart3d(points_array, integration_method=method,  I=current, invertPAxis=False)
                arr = np.asarray(B_array, dtype=float)
                
                if arr.shape[1] == 6:
                    pass                     # já está (N,6)
                elif arr.shape[0] == 6:
                    arr = arr.T              # era (6,N) → vira (N,6)
                else:
                    raise ValueError(f"Expected (N,6) or (6,N), got {arr.shape}")


                dfB = pd.DataFrame(arr, columns=["x", "y", "z", "Bx (T)", "By (T)", "Bz (T)"])
                dfB["|B| (T)"] = np.linalg.norm(dfB[["Bx (T)", "By (T)", "Bz (T)"]].to_numpy(), axis=1)
                st.dataframe(dfB.style.format("{:.6e}"))
                
            if points_file is not None and points != "":
                raise ValueError("Please provide either a points file or direct points input, not both.")


                    # point_str = part.strip('[]')  # Remove brackets
                    # point = np.fromstring(point_str, sep=",", dtype=float)
                    # points_list.append(point)
                
            
            # fig = coil.plot(show=False)          # agora NÃO abre nova guia
            # st.plotly_chart(fig, use_container_width=True)
        
        elif p1_3d == "cloud of points":
            padding = st.text_input("How much do you want the cloud to surpasse the coil dimensions?", value="1.0")
            n = st.text_input("How many points do you want in the cloud in each direction? (If the value defined is 10, there'll be 1000 points)", value="10")
            method = st.selectbox("What integration method do you want to use to calculate the magnetic field using biot savart?", options=['Riemann', 'Simpson'])
            plane_axis_opt = st.selectbox("Do you want to highlight a specific plane?", options=["None", "x", "y", "z"], index=0)
            plane_value_str = st.text_input("Plane position (leave empty to use the middle of the domain)",value="")
            plane_thickness_str = st.text_input("Plane thickness (0 = one grid step)",value="0.0")
            current = st.text_input("Current (A) - Only the numeric value:", value="")

            if current != "":
                padding = float(padding)
                n = int(n)
                current = float(current)
                if plane_axis_opt == "None":   
                    plane_axis = None 
                else:
                    plane_axis = plane_axis_opt

                if plane_value_str == "":
                    plane_value = "mid"          # usa plano no meio
                else:
                    plane_value = float(plane_value_str)

                plane_thickness = float(plane_thickness_str)

                fig, b, space = coil.cloud(padding, n = n, i = current, integration_method=method, plane_axis=plane_axis, plane_thickness=plane_thickness, plane_value=plane_value, show=False)
                st.plotly_chart(fig, use_container_width=True)
                arr = np.asarray(b, dtype=float)
                
                if arr.shape[1] == 7:
                    pass                     # já está (N,6)
                elif arr.shape[0] == 7:
                    arr = arr.T              # era (6,N) → vira (N,6)
                else:
                    raise ValueError(f"Expected (N,7) or (7,N), got {arr.shape}")
                
                dfB = pd.DataFrame(arr, columns=["x", "y", "z", "Bx (T)", "By (T)", "Bz (T)", "|B| (T)"])
                st.dataframe(dfB.style.format("{:.6e}"))


        quest = st.radio("Do you want to calculate the Resistance of the coil?", options=("Yes", "No"))
        if quest == "Yes":
            if st.radio("Do you have the cross sectional area of your coil?", options=("Yes", "No")) == "Yes":
                area = st.text_input("Cross Sectional Area (m²) - Only the numeric value:", value="")
                resistivity = st.text_input("Resistivity (Ohm meter) - Only the numeric value:", value="1.68e-8")
                if area and resistivity != "":
                    resistivity = float(resistivity)
                    area = float(area)
                    coil.crossSectionalArea = area
                    coil.resistivity =  resistivity
                    resistance = coil.resistance
                    st.write("Resistance of the coil (Ohms): ", resistance)
                    st.write("dissipated potency (W): ", coil.dissipationPotency(float(current)))

            else:
                st.info("Let's Calculate the Cross Sectional Area of your coil!")
                format = st.selectbox("Select the format of your coil's cross section:", options=("Circle", "Square", "Rectangle"))
                fillRatio = st.slider("Fill Ratio (0 to 1)", min_value=0.0, max_value=1.0, value=1.0, step=0.01, format="%.2f")
                if format == "Circle":
                    radius = st.text_input("Radius (m)", value="")
                    if radius != "":
                        radius = float(radius)
                        CrossSec = eml.mathematics.geometry.crossSectionalArea(fill_ratio=fillRatio, radius=radius)
                        area = CrossSec
                        resistivity = st.text_input("Resistivity (Ohm meter) - Only the numeric value:", value="1.68e-8")
                        if area and resistivity != "":
                            resistivity = float(resistivity)
                            area = float(area)
                            coil.crossSectionalArea = area
                            coil.resistivity = resistivity
                            resistance = coil.resistance
                            st.write("Resistance of the coil (Ohms): ", resistance)
                            st.write("dissipated potency (W): ", coil.dissipationPotency(float(current)))
                elif format == "Square":
                    side = st.text_input("Side (m)", value="")
                    if side != "":
                        side = float(side)
                        CrossSec = eml.mathematics.geometry.crossSectionalArea(fill_ratio=fillRatio, side=side)
                        area = CrossSec
                        resistivity = st.text_input("Resistivity (Ohm meter) - Only the numeric value:", value="1.68e-8")
                        if area and resistivity != "":
                            resistivity = float(resistivity)
                            area = float(area)
                            coil.crossSectionalArea = area
                            coil.resistivity = resistivity
                            resistance = coil.resistance
                            st.write("Resistance of the coil (Ohms): ", resistance)
                            st.write("dissipated potency (W): ", coil.dissipationPotency(current))

                elif format == "Rectangle":
                    height = st.text_input("Height (m)", value="")
                    width = st.text_input("Width (m)", value="")
                    if height and width != "":
                        height = float(height)
                        width = float(width)
                        CrossSec = eml.mathematics.geometry.crossSectionalArea(fill_ratio=fillRatio, height=height, width=width)
                        area = CrossSec
                        resistivity = st.text_input("Resistivity (Ohm meter) - Only the numeric value:", value="1.68e-8")
                        if area and resistivity != "":
                            resistivity = float(resistivity)
                            area = float(area)
                            coil.crossSectionalArea = area
                            coil.resistivity = resistivity
                            resistance = coil.resistance
                            st.write("Resistance of the coil (Ohms): ", resistance)
                            st.write("dissipated potency (W): ", coil.dissipationPotency(current))
               
                
        else:
            pass
            
if Ratio == "No":
        st.info("Let's generate your coil path!")
        shape = st.selectbox("What type of coil do you want to generate?", options=("Line", "Arch", "Solenoid",  "RaceTrack wire", "Racetrack 2D", "Racetrack 3D"))

        if shape == "Line":
            initial_point = st.text_input("Coordenates of the initial Point (x,y,z) - Only the numeric values separated by commas:", value="")
            final_point = st.text_input("Coordenates of final Point (x,y,z) - Only the numeric values separated by commas:", value="")
            length = st.text_input("Maximum length of segment (Optional). Default is 0.1", value="0.1")
            num_points = st.text_input("Number of Points - Only the numeric value: (Optional)"  , value="")
            if initial_point and final_point != "":
                initial_point = np.fromstring(initial_point, sep=",", dtype=float)
                final_point = np.fromstring(final_point, sep=",", dtype=float)
                if num_points == "":
                    num_points = None
                else:
                    num_points = int(num_points)
                if length == "":
                    length = 0.1
                length = float(length)
                coil = eml.mathematics.geometry.line(initial_point, final_point, max_seg_len=length, n_points=num_points)
                st.success("Coil Path generated successfully!")
                st.dataframe(pd.DataFrame(coil, columns=['X','Y','Z']))
                st.download_button(label="Download Coil Path as .txt", data=pd.DataFrame(coil).to_csv(index=False).encode('utf-8'), file_name='Line_coil_path.txt', mime='text/csv')

                coil = eml.models.coil.Coil(coil, invertRAxis=True)
                fig = coil.plot(show=False)    # sua função/objeto que gera o Plot
                st.plotly_chart(fig, use_container_width=True)
                msg = "After downloading the coil path, return to the top and set 'Yes' to upload your coil path file and use it in calculations."
                st.markdown(f"### {msg}")                
        if shape == "Arch":
            center = st.text_input("Coordenates of the Center (x,y,z) - Only the numeric values separated by commas:", value="")
            radius = st.text_input("Radius - Only the numeric value:", value="")
            start_angle = st.text_input("Starting Angle (radians) - Only the numeric value:", value="")
            angle = st.text_input("Total Angle (radians) to sweep - Only the numeric value:", value="")
            length = st.text_input("Maximum length of segment (Optional). Default is 0.1", value="0.1")
            num_points = st.text_input("Number of Points - Only the numeric value: (Optional)"  , value="")
            Anticlockwise = st.checkbox("Anti Clockwise Direction?", value= False)

            if center and radius and start_angle and angle != "":
                center = np.fromstring(center, sep=",", dtype=float)
                radius = float(radius)
                start_angle = float(start_angle)
                angle = float(angle)
                if length == "":
                    length = 0.1
                length = float(length)
                if num_points == "":
                    num_points = None
                else:
                    num_points = int(num_points)
                if Anticlockwise:
                    coil = eml.mathematics.geometry.arc(center, radius, start_angle, angle, max_seg_len=length, n_points=num_points, anticlockwise=True)
                else:
                    coil = eml.mathematics.geometry.arc(center, radius, start_angle, angle, max_seg_len=length, n_points=num_points)
                st.success("Coil Path generated successfully!")
                st.dataframe(pd.DataFrame(coil, columns=['X','Y','Z']))
                st.download_button(label="Download Coil Path as .txt", data=pd.DataFrame(coil).to_csv(index=False).encode('utf-8'), file_name='Arch_coil_path.txt', mime='text/csv')

                coil = eml.models.coil.Coil(coil, invertRAxis=True)
                fig = coil.plot(show=False)    # sua função/objeto que gera o Plot
                st.plotly_chart(fig, use_container_width=True)
                msg = "After downloading the coil path, return to the top and set 'Yes' to upload your coil path file and use it in calculations."
                st.markdown(f"### {msg}")    
        if shape == "Solenoid":
            n_turns = st.text_input("Number of Turns - Only the numeric value:", value="")
            Pa = st.text_input("Z Initial Point - Only the numeric values:", value="")
            Pb = st.text_input("Z Final Point - Only the numeric values:", value="")
            radius = st.text_input("Radius - Only the numeric value:", value="")
            length = st.text_input("Maximum length of segment (Optional). Default is 0.1", value="0.1")
            if n_turns and Pa and Pb and radius != "":
                n_turns = int(n_turns)
                Pa = float(Pa)      # ⬅ vira escalar, igual ao VSCode
                Pb = float(Pb)    # ⬅ vira escalar, igual ao VSCode 
                radius = float(radius)
                if length == "":
                    length = 0.1
                length = float(length)
                solenoid = eml.models.coil.Solenoid(n_turns, Pa, Pb, radius, max_seg_len=length, invertRAxis=True)
                coilPath = solenoid.coilPath   
                st.success("Coil Path generated successfully!")
                st.dataframe(pd.DataFrame(coilPath, columns=['X','Y','Z']))
                st.download_button(label="Download Coil Path as .txt", data=pd.DataFrame(coilPath).to_csv(index=False).encode('utf-8'), file_name='Solenoid_coil_path.txt', mime='text/csv')

                fig = solenoid.plot(show=False)    # sua função/objeto que gera o Plot
                st.plotly_chart(fig, use_container_width=True)
                st.subheader("After downloading the coil path, return to the top and set 'Yes' to upload your coil path file and use it in calculations.") 
        
        if shape == "RaceTrack wire":
            center = st.text_input("Coordenates of the Center (x,y,z) - Only the numeric values separated by commas:", value="")
            width = st.text_input("Width - Only the numeric value:", value="")
            length = st.text_input("Length - Only the numeric value:", value="")
            int_radius = st.text_input("Internal Radius of the curve - Only the numeric value:", value="")
            max_length = st.text_input("Maximum length of segment (Optional). Default is 0.1", value="0.1")
            if center and width and length and int_radius != "":
                center = np.fromstring(center, sep=",", dtype=float)
                width = float(width)
                length = float(length)
                int_radius = float(int_radius)
                if max_length == "":
                    max_length = 0.1
                length = float(length)
                racetrack = eml.mathematics.geometry.race_track(center, width, length, max_length, int_radius)
                st.success("Coil Path generated successfully!")
                st.dataframe(pd.DataFrame(racetrack, columns=['X','Y','Z']))
                st.download_button(label="Download Coil Path as .txt", data=pd.DataFrame(racetrack).to_csv(index=False).encode('utf-8'), file_name='RaceTrack_coil_path.txt', mime='text/csv')
                coil = eml.models.coil.Coil(racetrack, invertRAxis=True)
                fig = coil.plot(show=False)    # sua função/objeto que gera o Plot
                st.plotly_chart(fig, use_container_width=True)
                st.subheader("After downloading the coil path, return to the top and set 'Yes' to upload your coil path file and use it in calculations.")
        if shape == "Racetrack 2D":
            center = st.text_input("Coordenates of the Center (x,y,z) - Only the numeric values separated by commas:", value="")
            width = st.text_input("Internal Width - Only the numeric value:", value="")
            length = st.text_input("Internal Length - Only the numeric value:", value="")
            int_radius = st.text_input("Internal Radius of the curve - Only the numeric value:", value="")
            max_length = st.text_input("Maximum length of segment (Optional). Default is 0.1", value="0.1")
            thickness = st.text_input("Thickness of the Coil - Only the numeric value:", value="")
            if center and width and length and int_radius and thickness != "":
                center = np.fromstring(center, sep=",", dtype=float)
                width = float(width)
                length = float(length)
                int_radius = float(int_radius)
                thickness = float(thickness)
                if max_length == "":
                    max_length = 0.1
                max_length = float(max_length)
                racetrack2D = eml.mathematics.geometry.racetrack2d(center, width, length, max_length, int_radius, thickness)
                st.success("Coil Path generated successfully!")
                st.dataframe(pd.DataFrame(racetrack2D, columns=['X','Y','Z']))
                st.download_button(label="Download Coil Path as .txt", data=pd.DataFrame(racetrack2D).to_csv(index=False).encode('utf-8'), file_name='RaceTrack2D_coil_path.txt', mime='text/csv')
                coil = eml.models.coil.Coil(racetrack2D, invertRAxis=True)
                fig = coil.plot(show=False)    # sua função/objeto que gera o Plot
                st.plotly_chart(fig, use_container_width=True)
                st.subheader("After downloading the coil path, return to the top and set 'Yes' to upload your coil path file and use it in calculations.")

        if shape == "Racetrack 3D":
            center = st.text_input("Coordenates of the Center (x,y,z) - Only the numeric values separated by commas:", value="")
            width = st.text_input("Internal Width - Only the numeric value:", value="")
            length = st.text_input("Internal Length - Only the numeric value:", value="")
            int_radius = st.text_input("Internal Radius of the curve - Only the numeric value:", value="")
            max_length = st.text_input("Maximum length of segment (Optional). Default is 0.1", value="0.1")
            thickness = st.text_input("Thickness of the Coil - Only the numeric value:", value="")
            height = st.text_input("Height of the Coil - Only the numeric value:", value="")
            if center and width and length and int_radius and thickness and height != "":
                center = np.fromstring(center, sep=",", dtype=float)
                width = float(width)
                length = float(length)
                int_radius = float(int_radius)
                thickness = float(thickness)
                height = float(height)
                if max_length == "":
                    max_length = 0.1
                max_length = float(max_length)
                racetrack3D = eml.mathematics.geometry.racetrack3d(center, width, length, max_length, int_radius, thickness, height)
                st.success("Coil Path generated successfully!")
                st.dataframe(pd.DataFrame(racetrack3D, columns=['X','Y','Z']))
                st.download_button(label="Download Coil Path as .txt", data=pd.DataFrame(racetrack3D).to_csv(index=False).encode('utf-8'), file_name='RaceTrack3D_coil_path.txt', mime='text/csv')
                coil = eml.models.coil.Coil(racetrack3D, invertRAxis=True)
                fig = coil.plot(show=False)    # sua função/objeto que gera o Plot
                st.plotly_chart(fig, use_container_width=True)
                st.subheader("After downloading the coil path, return to the top and set 'Yes' to upload your coil path file and use it in calculations.")
# else:
#     coilPath = np.array(Path)
#     st.dataframe(coilPath)
#     coil = eml.models.coil.Coil(coilPath)
    
    

# df = st.dataframe(
# text_input("Enter the Coil Path:", value="C:/path/to/your/coil.txt")
# )            st.write("Arch Coil to be implemented soon!")