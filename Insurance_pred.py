import streamlit as st # type: ignore
import pandas as pd # type: ignore
import os
print(os.getcwd())
import pickle

# load the model from disk.
with open("Insurance_PremiumPrice.pkl", 'rb') as f:
    model = pickle.load(f)

cars_df = pd.read_csv("./insurance.csv")

#st.title("Insurance PremiumPrice Prediction")
st.header("Insurance PremiumPrice Prediction", divider=True)

st.image("https://media.istockphoto.com/id/1792643153/vector/life-and-health-insurance-set-tiny-doctors-check-insurance-form-and-medical-care-card.jpg?s=612x612&w=0&k=20&c=npu88u7cPTIpU65CU_bvTFzHHreFt0l4fmRnZDHf5a0=")

st.markdown(''':blue-background[Accurate Insurance Premium Prediction Using Advanced Analytics and Machine Learning]''')
#st.caption("Accurate Insurance Premium Prediction Using Advanced Analytics and Machine Learning")

#st.dataframe(cars_df.head())

col1, col2, col3 = st.columns(3)

with col1:
    age = st.slider("How old are you?", 18, 80, 25)
    st.write(age, "years old")

with col2:
    weight = st.slider("Select your weight", 30, 130, 25)
    st.write("Weight : ", weight)

with col3:
    height = st.slider("Select your Height", 30, 200, 25)
    st.write("Height : ", height)


col1, col2, col3 = st.columns(3)

# Diabetes_status = col1.selectbox("Select Diabetes status",
#                            ["Yes","No"])

# BloodPressure_status = col1.selectbox("Select BloodPressureProblem status",
#                            ["Yes","No"])


ChronicDisease_status = col1.selectbox("Select ChronicDisease status",
                                   ["Have","Have'nt"])

NumberOfMajorSurgeries = col1.selectbox("Enter NumberOfMajorSurgeries",
                       [0,1,2,3,4])

AnyTransplants_status = col1.selectbox("Select AnyTransplants status",
                           ["Yes","No"])

# KnownAllergies_status = col3.selectbox("Select KnownAllergies status",
#                            ["Yes","No"])

HistoryOfCancerInFamily_status = col2.selectbox("Select HistoryOfCancerInFamily status",
                           ["Yes","No"])

#encode data
encode_dict = {
    # "Diabetes_status": {'Yes': 1, 'No': 0},
    # "BloodPressure_status": {'Yes': 1, 'No': 0},
    "ChronicDisease_status": {'Have': 1, "Have'nt": 0},
    "AnyTransplants_status": {'Yes': 1, "No": 0},
    # "KnownAllergies_status": {'Yes': 1, 'No': 0},
    "HistoryOfCancerInFamily_status": {'Yes': 1, 'No': 0}
}

if st.button("Get PremiumPrice"):

    # encode_Diabetes_status = encode_dict['Diabetes_status'][Diabetes_status]
    # encode_BloodPressure_status = encode_dict['BloodPressure_status'][BloodPressure_status]
    encode_ChronicDisease_status = encode_dict['ChronicDisease_status'][ChronicDisease_status]
    encode_AnyTransplants_status = encode_dict['AnyTransplants_status'][AnyTransplants_status] 
    # encode_KnownAllergies_status = encode_dict['KnownAllergies_status'][KnownAllergies_status] 
    encode_HistoryOfCancerInFamily_status = encode_dict['HistoryOfCancerInFamily_status'][HistoryOfCancerInFamily_status] 

    input_data = [age,weight,height,encode_ChronicDisease_status,encode_AnyTransplants_status,
                  encode_HistoryOfCancerInFamily_status,NumberOfMajorSurgeries]
    pred = model.predict([input_data])[0]

    st.write(round(pred,2))
