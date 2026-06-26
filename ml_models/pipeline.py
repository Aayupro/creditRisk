import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class MLModelPipeline:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.features_list = ['age', 'annual_income', 'loan_amount', 'loan_tenure', 'credit_score', 'dti', 'lti', 'emi_burden', 'disposable_income', 'emp_stability']
        self._bootstrap_synthetic_train()

    def _bootstrap_synthetic_train(self):
        np.random.seed(42)
        n = 1000
        age = np.random.randint(21, 65, n)
        income = np.random.randint(25000, 150000, n)
        amt = np.random.randint(5000, 80000, n)
        tenure = np.random.choice([12, 24, 36, 48, 60], n)
        scr = np.random.randint(500, 850, n)
        
        dti = (amt / tenure * 12) / income
        lti = amt / income
        emi_b = (amt / tenure) / (income / 12)
        disp = (income / 12) - (amt / tenure)
        stb = np.random.randint(0, 100, n)
        
        y = [1 if (s < 600 or d > 0.45 or eb > 0.5) else 0 for s, d, eb in zip(scr, dti, emi_b)]
        
        df = pd.DataFrame(list(zip(age, income, amt, tenure, scr, dti, lti, emi_b, disp, stb)), columns=self.features_list)
        X_scaled = self.scaler.fit_transform(df)
        self.model.fit(X_scaled, y)

    def predict_risk(self, vector: list) -> float:
        scaled = self.scaler.transform([vector])
        return float(self.model.predict_proba(scaled)[0][1])

ml_pipeline = MLModelPipeline()