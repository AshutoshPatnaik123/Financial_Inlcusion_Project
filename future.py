def loan_repayment_probability(
    income,
    expenses,
    loan,
    savings,
    occupation
    ):
    
    occupation_weights = {
        "Government": 20,
        "Private": 15,
        "Self-Employed": 10,
        "Freelancer": 5,
        "Student": 2
    }

    if income <= 0:
        return 0

    savings_rate = savings / income
    expense_ratio = expenses / income
    debt_ratio = loan / income

    occ_bonus = occupation_weights.get(occupation, 5)

    probability = (
        savings_rate * 40 +
        (1 - expense_ratio) * 30 +
        (1 - debt_ratio) * 20 +
        occ_bonus
    )

    probability = max(0, min(100, round(probability)))

    return probability

def calculate_resilience_score(income, expenses, loan, savings):
    if income<=0:
        return 0
    
    savings_rate = savings/income
    expense_ratio = expenses/income
    debt_ratio = loan/income
    estimated_emergency_funds = savings*6
    months = estimated_emergency_funds/expenses
    
    score = (savings_rate*50 + (1-expense_ratio)*30 + (1-debt_ratio)*20)
    
    score = max(0,min(100, int(score)))
    
    return score, round(months, 2)