from django.http.response import (JsonResponse)
from rest_framework.views import APIView
import json
import pandas as pd
import numpy as np
import pickle
import ipdb


class PatientReadmission(APIView):
    trained_columns = ['age', 'num_procedures', 'num_medications',
                       'num_diagnoses', 'admission_source_id_7', 'admission_source_id_1',
                       'admission_source_id_17', 'admission_source_id_4',
                       'admission_source_id_6', 'admission_source_id_2',
                       'admission_source_id_5', 'admission_source_id_9',
                       'admission_source_id_3', 'admission_type_id_1', 'admission_type_id_3',
                       'admission_type_id_2', 'admission_type_id_6', 'admission_type_id_5',
                       'race_type3', 'race_type1', 'race_type4', 'race_type5',
                       'days_in_hospital', 'gender_Male', 'max_glu_serum_>300',
                       'max_glu_serum_None', 'max_glu_serum_Norm', 'A1Cresult_>8',
                       'A1Cresult_None', 'A1Cresult_Norm', 'metformin_No', 'metformin_Steady',
                       'metformin_Up', 'repaglinide_No', 'repaglinide_Steady',
                       'repaglinide_Up', 'glimepiride_No', 'glimepiride_Steady',
                       'glimepiride_Up', 'glipizide_No', 'glipizide_Steady', 'glipizide_Up',
                       'glyburide_No', 'glyburide_Steady', 'glyburide_Up', 'pioglitazone_No',
                       'pioglitazone_Steady', 'pioglitazone_Up', 'rosiglitazone_No',
                       'rosiglitazone_Steady', 'rosiglitazone_Up', 'acarbose_Steady',
                       'acarbose_Up', 'tolazamide_Steady', 'insulin_No', 'insulin_Steady',
                       'insulin_Up', 'glyburide.metformin_Steady', 'glyburide.metformin_Up',
                       'change_No', 'diabetesMed_Yes']
    drop_columns = ['patientID', 'AdmissionID',
                    'weight', 'payer_code', 'medical_specialty',
                    'nateglinide', 'chlorpropamide', 'tolbutamide', 'acetohexamide',
                    'miglitol', 'troglitazone', 'glipizide.metformin', 'metformin.rosiglitazone',
                    'metformin.pioglitazone', 'Target', 'istrain']

    def post(self, request):
        request = json.dumps(request.data)
        data = pd.DataFrame(json.loads(request))
        data = self.preprocess(data)
        model = pickle.load(open(r"E:\Data Science\Ggk assignments\patient_readmission_model", 'rb'))
        predicted = model.predict_proba(data)
        return JsonResponse(status=200, data={'classes': model.classes_.tolist(),
                                              'predictions': predicted.tolist()})

    def preprocess(self, data):
        # Creating days_in_hospital column
        data['days_in_hospital'] = (pd.to_datetime(data.Discharge_date) - pd.to_datetime(
            data.Admission_date)) / np.timedelta64(1, 'D')
        data.drop(['Admission_date', 'Discharge_date'], axis=1, inplace=True)
        # Creating age column
        age = data.age.str.split("-", expand=True)
        data.age = (pd.to_numeric(age[0].str.replace("[", "")) + pd.to_numeric(age[1].str.replace(")", ""))) / 2
        # pre-processing production data as done to training data
        data.drop(self.drop_columns, axis=1, inplace=True)
        categorical_columns = data.select_dtypes(['object']).columns
        data = pd.get_dummies(data, columns=categorical_columns[categorical_columns != 'Target'],
                              prefix=categorical_columns[categorical_columns != 'Target'])
        for col in self.trained_columns:
            if col not in data.columns:
                data[col] = 0
        data = data[self.trained_columns]
        return data
