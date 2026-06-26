class RuleBasedRiskEngine:
    @staticmethod
    def evaluate(app_data: dict, features: dict) -> tuple[float, list[str]]:
        score = 100.0
        deductions = []
        
        if features['dti'] > 0.45:
            score -= 25
            deductions.append("High Debt-to-Income ratio (>45%): -25 pts")
        if features['emi_burden'] > 0.50:
            score -= 20
            deductions.append("Critical Monthly EMI Burden (>50% income): -20 pts")
        if app_data['credit_score'] < 600:
            score -= 30
            deductions.append("Poor Credit Score (<600): -30 pts")
        elif app_data['credit_score'] > 750:
            score += 10
            deductions.append("Excellent Credit Score Reward (>750): +10 pts")
            
        if features['emp_stability'] < 40:
            score -= 15
            deductions.append("Unstable Employment history: -15 pts")
        if app_data['existing_loans'] > 3:
            score -= 10
            deductions.append("Multiple active lines of credit (>3 loans): -10 pts")
            
        return max(0.0, min(100.0, score)), deductions