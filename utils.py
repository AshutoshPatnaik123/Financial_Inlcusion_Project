def calculate_expenses(
        rent,
        loan,
        insurance,
        groceries,
        transport,
        eating_out,
        entertainment,
        utilities,
        healthcare,
        education,
        miscellaneous):

    return (
        rent +
        loan +
        insurance +
        groceries +
        transport +
        eating_out +
        entertainment +
        utilities +
        healthcare +
        education +
        miscellaneous
    )


def calculate_credit_score(income,expenses,loan,savings):
    if income == 0:
        return 0

    savings_rate = savings / income

    expense_ratio = expenses / income

    debt_ratio = loan / income

    score = (
        savings_rate * 40 +
        (1 - expense_ratio) * 35 +
        (1 - debt_ratio) * 25
    )
    
    score = max(0,min(100, int(score)))
    return score


def risk_level(score):

    if score >= 70:
        return "Low Risk"

    elif score >= 40:
        return "Moderate Risk"

    else:
        return "High Risk"