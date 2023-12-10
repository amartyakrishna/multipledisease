import streamlit as st
import streamlit_authenticator as stauth
import yaml
import pickle
from streamlit_option_menu import option_menu
from yaml.loader import SafeLoader
import pdfkit
from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("invoice_template.html")


# button_style = """
#         <style>
#         .stButton > button {
#             color: white;
#             background: purple;
#             border-radius: 15px;
#         }
#         </style>
#         """
# loading the saved models

diabetes_model = pickle.load(open('saved models/diabetes_model.sav', 'rb'))

heart_disease_model = pickle.load(open('saved models/heart_disease_model.sav','rb'))

parkinsons_model = pickle.load(open('saved models/parkinsons_model.sav', 'rb'))

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    hashed_passwords = stauth.Hasher(['abc', 'def']).generate()


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


authenticator.login('Login', 'main')
if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome *{st.session_state["name"]}*')
# sidebar for navigation
    with st.sidebar:
        selected = option_menu('Multiple Disease Prediction System',
                          ['Diabetes Prediction',
                           'Heart Disease Prediction',
                           'Parkinsons Prediction'],
                          icons=['activity','heart','person'],
                          default_index=0)
# Diabetes Prediction Page
    if (selected == 'Diabetes Prediction'):

# page title
        st.title('Diabetes Prediction using ML')

        flag=True
    # getting the input data from the user
        col1, col2, col3 = st.columns(3)

    
        with col1:
            Pregnancies = st.number_input('Number of Pregnancies',value=0,min_value=0,max_value=15)
        
        with col2:
            Glucose = st.number_input('Glucose Level',min_value=50,max_value=500,value=None)
    
        with col3:
            BloodPressure = st.number_input('Blood Pressure value',value=None,min_value=30,max_value=400)
    
        with col1:
            SkinThickness = st.number_input('Skin Thickness value',value=None,min_value=10,max_value=100)
    
        with col2:
            Insulin = st.number_input('Insulin Level',value=None,min_value=10,max_value=850)
    
        with col3:
            BMI = st.number_input('BMI value',value=None,min_value=10.0,max_value=70.0)
    
        with col1:
            DiabetesPedigreeFunction = st.number_input('Diabetes Pedigree Function value',value=0.0,min_value=0.0,max_value=2.5)
    
        with col2:
            Age = st.number_input('Age of the Person',value=15,min_value=15,max_value=125)
        with col1:
            pat_name=st.text_input('Enter Patient Name')
        with col2:
            pat_add=st.text_input('Enter Patient Address')
        with col3:
            pat_num=st.text_input('Enter Patient Phone')
        
        if pat_name and pat_add and pat_num and BloodPressure!=None and Glucose!=None and BMI!=None and Insulin!=None and SkinThickness!=None:
            flag=False
    
    # code for Prediction
        diab_diagnosis = ''
        
    
    # creating a button for Prediction
    
        if st.button('Diabetes Test Result',disabled=flag):
            diab_prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
        
            if (diab_prediction[0] == 1):
                diab_diagnosis = 'The person is diabetic'
            else:
                diab_diagnosis = 'The person is not diabetic'
        
            st.success(diab_diagnosis)
            html = template.render(
             pat_name=pat_name ,
             pat_add=pat_add ,
             pat_num=pat_num ,
             age =Age , 
             test_res=diab_diagnosis,    
                )

            pdf = pdfkit.from_string(html, False)
            st.download_button(
        "⬇️ Download Report",
        data=pdf,
        file_name="report.pdf",
        mime="application/octet-stream",
    )
        # st.download_button(label="download report",data=diab_diagnosis,file_name="report.txt")




# Heart Disease Prediction Page
    if (selected == 'Heart Disease Prediction'):
    
    # page title
        st.title('Heart Disease Prediction using ML')
        flag=True
    
        col1, col2, col3 = st.columns(3)
        
        with col1:
            age = st.number_input('Age',value=0,min_value=0,max_value=125)
            
        with col2:
            sex = st.number_input('Sex (1 = male; 0 = female)',value=0,min_value=0,max_value=1)
            
        with col3:
            cp = st.number_input('Chest Pain types',value=0,min_value=0,max_value=4)
            
        with col1:
            trestbps = st.number_input('Resting Blood Pressure',min_value=15,max_value=200)
            
        with col2:
            chol = st.number_input('Serum Cholestoral in mg/dl',value=100,min_value=100,max_value=600)
            
        with col3:
            fbs = st.number_input('Fasting Blood Sugar > 120 mg/dl (1 = true; 0 = false)',value=0,min_value=0,max_value=1)
            
        with col1:
            restecg = st.number_input('Resting Electrocardiographic results',value=0,min_value=0,max_value=1)
            
        with col2:
            thalach = st.number_input('Maximum Heart Rate achieved',value=50,min_value=50,max_value=250)
            
        with col3:
            exang = st.number_input('Exercise Induced Angina (1 = yes; 0 = no)',value=0,min_value=0,max_value=1)
            
        with col1:
            oldpeak = st.number_input('ST depression induced by exercise',value=0.0,min_value=0.0,max_value=6.2)
            
        with col2:
            slope = st.number_input('Slope of the peak exercise ST segment',value=0,min_value=0,max_value=2)
            
        with col3:
            ca = st.number_input('Major vessels colored by flourosopy (0-3)',value=0,min_value=0,max_value=3)
            
        with col1:
            thal = st.number_input('thal: 1 = normal; 2= fixed defect; 3 = reversable defect',value=1,min_value=1,max_value=3)
        
        with col1:
            pat_name=st.text_input('Enter Patient Name')
        with col2:
            pat_add=st.text_input('Enter Patient Address')
        with col3:
            pat_num=st.text_input('Enter Patient Phone')
        if pat_name and pat_add and pat_num:
            flag=False
            
            
        
        
        # code for Prediction
        heart_diagnosis = ''
        
        # creating a button for Prediction
        
        if st.button('Heart Disease Test Result',disabled=flag):
            heart_prediction = heart_disease_model.predict([[age, sex, cp, trestbps, chol, fbs, restecg,thalach,exang,oldpeak,slope,ca,thal]])                          
            
            if (heart_prediction[0] == 1):
                heart_diagnosis = 'The person is having heart disease'
            else:
                heart_diagnosis = 'The person does not have any heart disease'
            
            st.success(heart_diagnosis)
            html = template.render(
        pat_name=pat_name ,
        pat_add=pat_add ,
        pat_num=pat_num ,
        age =age , 
        test_res=heart_diagnosis,

        
    )

            pdf = pdfkit.from_string(html, False)
            st.download_button(
        "⬇️ Download Report",
        data=pdf,
        file_name="report.pdf",
        mime="application/octet-stream",
    )
        
        



    # Parkinson's Prediction Page
    if (selected == "Parkinsons Prediction"):
        
        # page title
            st.title("Parkinson's Disease Prediction using ML")
            flag=True
        
            col1, col2, col3, col4, col5 = st.columns(5)  
            
            with col1:
                fo = st.number_input('MDVP : Fo(Hz)')
                
            with col2:
                fhi = st.number_input('MDVP : Fhi(Hz)')
                
            with col3:
                flo = st.number_input('MDVP : Flo(Hz)')
                
            with col4:
                Jitter_percent = st.number_input('MDVP : Jitter(%)')
                
            with col5:
                Jitter_Abs = st.number_input('MDVP : Jitter(Abs)')
                
            with col1:
                RAP = st.number_input('MDVP: RAP')
                
            with col2:
                PPQ = st.number_input('MDVP: PPQ')
                
            with col3:
                DDP = st.number_input('Jitter: DDP')
                
            with col4:
                Shimmer = st.number_input('MDVP: Shimmer')
                
            with col5:
                Shimmer_dB = st.number_input('MDVP: Shimmer(dB)')
                
            with col1:
                APQ3 = st.number_input('Shimmer: APQ3')
                
            with col2:
                APQ5 = st.number_input('Shimmer: APQ5')
                
            with col3:
                APQ = st.number_input('MDVP: APQ')
                
            with col4:
                DDA = st.number_input('Shimmer: DDA')
                
            with col5:
                NHR = st.number_input('NHR')
                
            with col1:
                HNR = st.number_input('HNR')
                
            with col2:
                RPDE = st.number_input('RPDE')
                
            with col3:
                DFA = st.number_input('DFA')
                
            with col4:
                spread1 = st.number_input('spread1')
                
            with col5:
                spread2 = st.number_input('spread2')
                
            with col1:
                D2 = st.number_input('D2')
                
            with col2:
                PPE = st.number_input('PPE')
            with col3:
                pat_name=st.text_input('Enter Patient Name')
            with col4:
                pat_add=st.text_input('Enter Patient Address')
            with col5:
                pat_num=st.text_input('Enter Patient Phone')
            with col1:
                age=st.number_input('Age',value=0,min_value=0,max_value=125)
            if pat_name and pat_add and pat_num:
                flag=False
                
            
            
            # code for Prediction
            parkinsons_diagnosis = ''
            
            # creating a button for Prediction    
            if st.button("Parkinson's Test Result",disabled=flag):
                parkinsons_prediction = parkinsons_model.predict([[fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ,DDP,Shimmer,Shimmer_dB,APQ3,APQ5,APQ,DDA,NHR,HNR,RPDE,DFA,spread1,spread2,D2,PPE]])                          
                
                if (parkinsons_prediction[0] == 1):
                    parkinsons_diagnosis = "The person has Parkinson's disease"
                else:
                    parkinsons_diagnosis = "The person does not have Parkinson's disease"
                
                st.success(parkinsons_diagnosis)
                html = template.render(
        pat_name=pat_name ,
        pat_add=pat_add ,
        pat_num=pat_num ,
        age =age , 
        test_res=parkinsons_diagnosis,

        
    )

                pdf = pdfkit.from_string(html, False)
                st.download_button(
        "⬇️ Download Report",
        data=pdf,
        file_name="report.pdf",
        mime="application/octet-stream",
    )



elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
    with st.expander("Register New User"):
        try:
            if authenticator.register_user("Register user", preauthorization=False):
                st.success("User registered successfully")
        except Exception as e:
            st.error(e)

        with open("config.yaml", "w") as file:
            yaml.dump(config, file, default_flow_style=False)

  

elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
    st.markdown("  <br>",unsafe_allow_html=True)
    st.markdown('<div style="text-align: center;">Or </div>', unsafe_allow_html=True)
    st.markdown("  <br>",unsafe_allow_html=True)
    with st.expander("Register New User"):
        try:
            if authenticator.register_user("Register user", preauthorization=False):
                st.success("User registered successfully")
        except Exception as e:
            st.error(e)

        with open("config.yaml", "w") as file:
            yaml.dump(config, file, default_flow_style=False)

   
   
   
   
   
    # res=st.selectbox("Choose Option : ",["Register new User","Forgot Password"])
    # if res=="Register new User":
    #     try:
    #         if authenticator.register_user("Register user", preauthorization=False):
    #                 st.success("User registered successfully")
    #     except Exception as e:
    #         st.error(e)
    #     with open("config.yaml", "w") as file:
    #         yaml.dump(config, file, default_flow_style=False)
    # if res=="Forgot Password":
    #     try:
    #         username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password('Forgot password')
    #         if username_of_forgotten_password:
    #             st.success('New password is:')
    #             st.success(new_random_password )
    #             with open('../config.yaml', 'w') as file:
    #                     yaml.dump(config, file, default_flow_style=False)
    #             try:
    #                 if authenticator.reset_password(st.session_state["username"], 'Reset password'):
    #                         st.success('Password modified successfully')
    #             except Exception as e:
    #                  st.error(e)
    #             with open('../config.yaml', 'w') as file:
    #                 yaml.dump(config, file, default_flow_style=False)
    #     # Random password should be transferred to user securely
    #         else:
    #             st.error('Username not found')
    #     except Exception as e:
    #         st.error(e)

        







# https://www.kaggle.com/datasets/mathchi/diabetes-data-set/data
# https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset
# https://www.kaggle.com/datasets/vikasukani/parkinsons-disease-data-set
   







