import streamlit as st
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import matplotlib.pyplot as plt
from skfuzzy.control.visualization import FuzzyVariableVisualizer

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

    col1, col2, col3 = st.columns([1, 0.5, 0.85])
    with col1:
        if st.button("Nộp"):
            st.session_state.page1['is_first_load'] = False
            submitted = True
    with col3:
        if st.button("Reset"):
            st.session_state.page1['is_first_load'] = True
            

def get_fig(self, sim):
    fig, ax = FuzzyVariableVisualizer(self).view(sim)
    return fig

ctrl.Consequent.get_fig = get_fig

temperature = ctrl.Antecedent(np.arange(-20, 50.01, 0.01), 'Nhiệt độ')
soil_moisture = ctrl.Antecedent(np.arange(0, 100.01, 0.01), 'Độ ẩm đất')
light_intensity = ctrl.Antecedent(np.arange(0, 1000.01, 0.01), 'Cường độ ánh sáng')
watering_speed = ctrl.Consequent(np.arange(0, 12.01, 0.01), 'Tốc độ tưới', defuzzify_method='centroid')


temperature['rất lạnh'] = fuzz.trapmf(temperature.universe, [-20, -20, 5, 10])
temperature['lạnh'] = fuzz.trapmf(temperature.universe, [5, 10, 15, 20])
temperature['ấm'] = fuzz.trapmf(temperature.universe, [15, 20, 25, 30])
temperature['nóng'] = fuzz.trapmf(temperature.universe, [25, 30, 51, 51])
# temperature.view()

soil_moisture['rất khô'] = fuzz.trapmf(soil_moisture.universe, [0, 0, 25, 35])
soil_moisture['khô'] = fuzz.trapmf(soil_moisture.universe, [25, 35, 45, 55])
soil_moisture['ẩm'] = fuzz.trapmf(soil_moisture.universe, [45, 55, 65, 75])
soil_moisture['rất ẩm'] = fuzz.trapmf(soil_moisture.universe, [65, 75, 101, 101])
# soil_moisture.view()

light_intensity['yếu'] = fuzz.trapmf(light_intensity.universe, [0, 0, 300, 400])
light_intensity['trung bình'] = fuzz.trapmf(light_intensity.universe, [300, 400, 700, 800])
light_intensity['mạnh'] = fuzz.trapmf(light_intensity.universe, [700, 800, 1001, 1001])
# light_intensity.view()

watering_speed['rất chậm'] = fuzz.trapmf(watering_speed.universe, [0, 0, 2, 3])
watering_speed['chậm'] = fuzz.trapmf(watering_speed.universe, [2, 3, 5, 6])
watering_speed['nhanh'] = fuzz.trapmf(watering_speed.universe, [5, 6, 8, 9])
watering_speed['rất nhanh'] = fuzz.trapmf(watering_speed.universe, [8, 9, 12, 12])
# watering_speed.view()

rule1 = ctrl.Rule(temperature['rất lạnh'] & soil_moisture['rất khô'] & light_intensity['mạnh'], watering_speed['rất chậm'])
rule2 = ctrl.Rule(temperature['lạnh'] & soil_moisture['rất khô'] & light_intensity['yếu'], watering_speed['nhanh'])
rule3 = ctrl.Rule(temperature['lạnh'] & soil_moisture['rất khô'] & light_intensity['trung bình'], watering_speed['nhanh'])
rule4 = ctrl.Rule(temperature['lạnh'] & soil_moisture['rất khô'] & light_intensity['mạnh'], watering_speed['rất nhanh'])
rule5 = ctrl.Rule(temperature['lạnh'] & soil_moisture['khô'] & light_intensity['yếu'], watering_speed['chậm'])
rule6 = ctrl.Rule(temperature['lạnh'] & soil_moisture['khô'] & light_intensity['trung bình'], watering_speed['chậm'])
rule7 = ctrl.Rule(temperature['lạnh'] & soil_moisture['khô'] & light_intensity['mạnh'], watering_speed['nhanh'])
rule8 = ctrl.Rule(temperature['lạnh'] & soil_moisture['ẩm'] & light_intensity['trung bình'], watering_speed['rất chậm'])
rule9 = ctrl.Rule(temperature['lạnh'] & soil_moisture['ẩm'] & light_intensity['mạnh'], watering_speed['chậm'])
rule10 = ctrl.Rule(temperature['ấm'] & soil_moisture['rất khô'] & light_intensity['yếu'], watering_speed['rất nhanh'])
rule11 = ctrl.Rule(temperature['ấm'] & soil_moisture['rất khô'] & light_intensity['trung bình'], watering_speed['rất nhanh'])
rule12 = ctrl.Rule(temperature['ấm'] & soil_moisture['rất khô'] & light_intensity['mạnh'], watering_speed['rất nhanh'])
rule13 = ctrl.Rule(temperature['ấm'] & soil_moisture['khô'] & light_intensity['yếu'], watering_speed['nhanh'])
rule14 = ctrl.Rule(temperature['ấm'] & soil_moisture['khô'] & light_intensity['trung bình'], watering_speed['nhanh'])
rule15 = ctrl.Rule(temperature['ấm'] & soil_moisture['khô'] & light_intensity['mạnh'], watering_speed['rất nhanh'])
rule16 = ctrl.Rule(temperature['ấm'] & soil_moisture['ẩm'] & light_intensity['yếu'], watering_speed['chậm'])
rule17 = ctrl.Rule(temperature['ấm'] & soil_moisture['ẩm'] & light_intensity['trung bình'], watering_speed['chậm'])
rule18 = ctrl.Rule(temperature['ấm'] & soil_moisture['ẩm'] & light_intensity['mạnh'], watering_speed['nhanh'])
rule19 = ctrl.Rule(temperature['nóng'] & soil_moisture['rất khô'] & light_intensity['yếu'], watering_speed['rất nhanh'])
rule20 = ctrl.Rule(temperature['nóng'] & soil_moisture['rất khô'] & light_intensity['trung bình'], watering_speed['rất nhanh'])
rule21 = ctrl.Rule(temperature['nóng'] & soil_moisture['rất khô'] & light_intensity['mạnh'], watering_speed['rất nhanh'])
rule22 = ctrl.Rule(temperature['nóng'] & soil_moisture['khô'] & light_intensity['yếu'], watering_speed['nhanh'])
rule23 = ctrl.Rule(temperature['nóng'] & soil_moisture['khô'] & light_intensity['trung bình'], watering_speed['nhanh'])
rule24 = ctrl.Rule(temperature['nóng'] & soil_moisture['khô'] & light_intensity['mạnh'], watering_speed['rất nhanh'])
rule25 = ctrl.Rule(temperature['nóng'] & soil_moisture['ẩm'] & light_intensity['yếu'], watering_speed['chậm'])
rule26 = ctrl.Rule(temperature['nóng'] & soil_moisture['ẩm'] & light_intensity['trung bình'], watering_speed['nhanh'])
rule27 = ctrl.Rule(temperature['nóng'] & soil_moisture['ẩm'] & light_intensity['mạnh'], watering_speed['nhanh'])

watering_system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10,
                                     rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20,
                                     rule21, rule22, rule23, rule24, rule25, rule26, rule27])
watering = ctrl.ControlSystemSimulation(watering_system)

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
    watering.input['Nhiệt độ'] = temperature_input
    watering.input['Độ ẩm đất'] = soil_moisture_input
    watering.input['Cường độ ánh sáng'] = light_intensity_input

    st.subheader("Kết quả tính toán sử dụng thư viện skfuzzy:")
    print("skfuzzy:")

    try:
        watering.compute()

        watering_speed.defuzzify_method = 'mom'
        watering = ctrl.ControlSystemSimulation(watering_system)
        watering.input['Nhiệt độ'] = temperature_input
        watering.input['Độ ẩm đất'] = soil_moisture_input
        watering.input['Cường độ ánh sáng'] = light_intensity_input
        watering.compute()
        print(f"Cực đại trung bình ({watering_speed.defuzzify_method})", end = ": ")
        print(round(watering.output['Tốc độ tưới'], 2))
        st.markdown("<p class='text'>Sử dụng phương pháp cực đại trung bình, xác định được giá trị đầu ra là:</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='text center'>{'{:.2f}'.format(round(watering.output['Tốc độ tưới'], 2))} lít/phút ~ <b>{'{:.10f}'.format(round(watering.output['Tốc độ tưới'], 2) / 60000)} m3/s</b></p>", unsafe_allow_html=True)
        fig1 = watering_speed.get_fig(sim=watering)
        st.write(fig1)

        watering_speed.defuzzify_method = 'centroid'
        watering = ctrl.ControlSystemSimulation(watering_system)
        watering.input['Nhiệt độ'] = temperature_input
        watering.input['Độ ẩm đất'] = soil_moisture_input
        watering.input['Cường độ ánh sáng'] = light_intensity_input
        watering.compute()
        print(f"Trọng tâm ({watering_speed.defuzzify_method})", end = ": ")
        print(round(watering.output['Tốc độ tưới'], 2))
        st.markdown("<p class='text'>Sử dụng phương pháp trọng tâm, xác định được giá trị đầu ra là:</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='text center'>{'{:.2f}'.format(round(watering.output['Tốc độ tưới'], 2))} lít/phút ~ <b>{'{:.10f}'.format(round(watering.output['Tốc độ tưới'], 2) / 60000)} m3/s</b></p>", unsafe_allow_html=True)
        fig2 = watering_speed.get_fig(sim=watering)
        st.write(fig2)
      
    except ValueError:
        st.markdown(f"<p class='text'>Từ các giá trị mờ tính được, vận dụng các tập luật đã được định nghĩa, kết luận:</p>", unsafe_allow_html=True)
        st.markdown("<p class='text center'><b>Không nên tưới cây trong điều kiện này</b></p>", unsafe_allow_html=True)
        print("Crisp output cannot be calculated!")
    submitted = False
    print("___________________________________________")