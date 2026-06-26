class FeatureEngine:
    @staticmethod
    def compute_all(data: dict) -> dict:
        annual_income = float(data.get('annual_income', 1.0))
        monthly_income = float(data.get('monthly_income', annual_income / 12.0))
        loan_amount = float(data.get('loan_amount', 0.0))
        loan_tenure = float(data.get('loan_tenure', 1.0))
        existing_emis = float(data.get('existing_emis', 0.0))
        years_of_emp = float(data.get('years_of_employment', 0.0))
        
        new_emi = loan_amount / loan_tenure
        total_future_emi = existing_emis + new_emi
        
        return {
            "dti": round((total_future_emi * 12) / max(annual_income, 1.0), 3),
            "lti": round(loan_amount / max(annual_income, 1.0), 3),
            "emi_burden": round(total_future_emi / max(monthly_income, 1.0), 3),
            "disposable_income": round(monthly_income - total_future_emi - (float(data.get('dependents', 0)) * 200), 2),
            "emp_stability": round(min((years_of_emp / 4.0) * 100, 100.0), 2)
        }