import streamlit as st
import numpy as np
from algorithm.fuzzy_logic import FuzzyLogic
from algorithm.visualizer import TemperatureVisualizer
from algorithm.visualizer import SoilMoistureVisualizer
from algorithm.visualizer import LightIntensityVisualizer
from algorithm.visualizer import WateringSpeedVisualizer
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title='Hệ thống tưới cây tự động', page_icon='./images/logo.png')
st.image(image='./images/logo.png', width=100)
st.title('Hệ thống tưới cây tự động')

st.markdown(
    f"""
        <style>
            /* Make the default header of streamlit invisible */
            .css-18ni7ap.e8zbici2 {{
                opacity: 0
            }}

            /* Make the default footer of streamlit invisible */
            .css-h5rgaw.egzxvld1 {{
            opacity: 0
            }}

            /* Change width and padding of the page */
            .block-container.css-91z34k.egzxvld4 {{
                width: 100%;
                padding: 0.5rem 1rem 10rem;
                # max-width: none;
            }}

            /* Change padding of the pages list in the sidebar */
            .css-wjbhl0, .css-hied5v {{
                padding-top: 2rem;
                padding-bottom: 0.25rem;
            }}

            .text {{
                font-size: 20px
            }}

            .center {{
                text-align: center
            }}

            .text.center {{
                font-size: 25px

            }}
        </style>
        """, unsafe_allow_html=True
    )

submitted = False
temperature_input = 0
soil_moisture_input = 0
light_intensity_input = 0

with st.sidebar:

    # A workaround using st.session_state and callback to keep input value during navigating through other pages
    if "page1" not in st.session_state:
        st.session_state.page1 = {'is_first_load': True, 'temperature': 20.0, 'soil_moisture': 50.0, 'light_intensity': 500.0}

    for k, v in st.session_state.items():
        st.session_state[k] = v

    def submit_temperature():
        st.session_state.page1['temperature'] = st.session_state.temperature_input_value

    def submit_soil_moisture():
        st.session_state.page1['soil_moisture'] = st.session_state.soil_moisture_input_value

    def submit_light_intensity():
        st.session_state.page1['light_intensity'] = st.session_state.light_intensity_input_value

    st.title("Tham số đầu vào")
    temperature_input = st.number_input("**Nhiệt độ (°C):**", min_value=-20.0, max_value=50.0, step=0.1, value=st.session_state.page1['temperature'], key='temperature_input_value', on_change=submit_temperature)
    soil_moisture_input = st.number_input("**Độ ẩm đất (%)**", min_value=0.0, max_value=100.0, step=0.1, value=st.session_state.page1['soil_moisture'], key='soil_moisture_input_value', on_change=submit_soil_moisture)
    light_intensity_input = st.number_input("**Cường độ ánh sáng PAR (µmol/m²/s)**", min_value=0.0, max_value=1000.0, step=0.1, value=st.session_state.page1['light_intensity'], key='light_intensity_input_value', on_change=submit_light_intensity)

    col1, col2, col3 = st.columns([1, 0.5, 0.477])
    with col1:
        if st.button("Nộp"):
            st.session_state.page1['is_first_load'] = False
            submitted = True
    with col3:
        if st.button("Reset"):
            st.session_state.page1['is_first_load'] = True

if submitted == False and st.session_state.page1['is_first_load'] == True:
    st.subheader("Vui lòng nhập các thông số:")
    st.markdown(
    """
    <ul style="padding-left: 2rem">
    <li>Nhiệt độ (°C)</li>
    <li>Độ ẩm đất (%)</li>
    <li>Cường độ ánh sáng PAR (µmol/m²/s)</li>
    </ul>
    """, unsafe_allow_html=True)

if submitted == True or st.session_state.page1['is_first_load'] == False:
    st.header("1. Mờ hoá")
    fz = FuzzyLogic()

    st.subheader("a. Nhiệt độ")
    st.markdown(f"<p class='text'>Từ giá trị đầu vào {temperature_input}°C, bằng các hàm thành viên đã được định nghĩa, tính được các giá trị mờ như sau:</p>", unsafe_allow_html=True)
    fz.do_fuzzification_of_temperature(temperature_input)
    st.table(pd.DataFrame(np.array([[i for i in fz.membership_values_of_temperature]]), columns = ("Rất lạnh", "Lạnh", "Ấm", "Nóng")))
    st.markdown("<p class='text'>Đồ thị minh hoạ:</p>", unsafe_allow_html=True)
    fig1, ax1 = TemperatureVisualizer(fz.membership_values_of_temperature, temperature_input).plot()
    st.write(fig1)

    st.subheader("b. Độ ẩm đất")
    st.markdown(f"<p class='text'>Từ giá trị đầu vào {soil_moisture_input}%, bằng các hàm thành viên đã được định nghĩa, tính được các giá trị mờ như sau:</p>", unsafe_allow_html=True)
    fz.do_fuzzification_of_soil_moisture(soil_moisture_input)
    st.table(pd.DataFrame(np.array([[i for i in fz.membership_values_of_soil_moisture]]), columns = ("Rất khô", "Khô", "Ẩm", "Rất ẩm")))
    st.markdown("<p class='text'>Đồ thị minh hoạ:</p>", unsafe_allow_html=True)
    fig2, ax2 = SoilMoistureVisualizer(fz.membership_values_of_soil_moisture, soil_moisture_input).plot()
    st.write(fig2)

    st.subheader("c. Cường độ ánh sáng PAR")
    st.markdown(f"<p class='text'>Từ giá trị đầu vào {light_intensity_input} µmol/m²/s, bằng các hàm thành viên đã được định nghĩa, tính được các giá trị mờ như sau:</p>", unsafe_allow_html=True)
    fz.do_fuzzification_of_light_intensity(light_intensity_input)
    st.table(pd.DataFrame(np.array([[i for i in fz.membership_values_of_light_intensity]]), columns = ("Yếu", "Trung bình", "Mạnh")))
    st.markdown("<p class='text'>Đồ thị minh hoạ:</p>", unsafe_allow_html=True)
    fig3, ax3 = LightIntensityVisualizer(fz.membership_values_of_light_intensity, light_intensity_input).plot()
    st.write(fig3)

    st.header("2. Suy diễn mờ")
    ok = fz.do_fuzzy_inference()
    if ok == False:
        st.markdown(f"<p class='text'>Từ các giá trị mờ tính được ở trên, vận dụng các tập luật đã được định nghĩa, kết luận:</p>", unsafe_allow_html=True)
        st.markdown("<p class='text center'><b>Không nên tưới cây trong điều kiện này</b></p>", unsafe_allow_html=True)

    else:
        st.markdown(f"<p class='text'>Từ các giá trị mờ tính được ở trên, vận dụng các tập luật đã được định nghĩa, tính được các giá trị mờ cho đầu ra tốc độ tưới nước như sau:</p>", unsafe_allow_html=True)
        st.table(pd.DataFrame(np.array([[i for i in fz.membership_values_of_watering_speed]]), columns = ("Rất chậm", "Chậm", "Nhanh", "Rất nhanh")))

        st.header("3. Giải mờ")
        st.markdown(f"<p class='text'>Chiếu các giá trị tính toán được từ suy diễn mờ vào hàm thành viên của tốc độ nước tưới, ta có:</p>", unsafe_allow_html=True)
        fz.do_defuzzification_of_watering_speed()
        fig4, ax4 = WateringSpeedVisualizer(fz.membership_values_of_watering_speed, fz.crisp_value).plot()
        st.write(fig4)
        st.markdown(f"<p class='text'>Xác định được 2 cực đại đầu và cuối là: {fz.max1} và {fz.max2}</p>", unsafe_allow_html=True)
        st.markdown("<p class='text'>Sử dụng phương pháp cực đại trung bình, xác định được giá trị đầu ra là:</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='text center'>({fz.max1} + {fz.max2}) / 2 =  {fz.crisp_value} lít/phút ~ <b>{'{:.10f}'.format(fz.output)} m3/s</b></p>", unsafe_allow_html=True)

   
        