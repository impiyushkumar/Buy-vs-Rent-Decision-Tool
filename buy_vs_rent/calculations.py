import pandas as pd



def calculate_emi(loan_amount, annual_rate, tenure_years):
    monthly_rate = annual_rate / (12 * 100)
    months = tenure_years * 12
    emi = loan_amount * monthly_rate * (1 + monthly_rate) ** months / (
        (1 + monthly_rate) ** months - 1
    )
    return emi



def calculate_sip(monthly_investment, annual_return, years):
    monthly_rate = annual_return / (12 * 100)
    months = years * 12
    fv = monthly_investment * ((1 + monthly_rate) ** months - 1) / monthly_rate
    return fv



def remaining_loan_balance(loan_amount, annual_rate, tenure_years, months_paid):
    monthly_rate = annual_rate / (12 * 100)
    emi = calculate_emi(loan_amount, annual_rate, tenure_years)

    balance = loan_amount

    for _ in range(months_paid):
        interest = balance * monthly_rate
        principal = emi - interest
        balance -= principal

        if balance < 0:
            balance = 0
            break

    return balance


def build_wealth_table(
    property_price,
    down_payment,
    loan_rate,
    tenure,
    rent,
    rent_growth,
    sip_return,
    property_growth,
    years=20
):
    loan_amount = property_price - down_payment
    emi = calculate_emi(loan_amount, loan_rate, tenure)

    
    total_emi_paid = emi * 12 * tenure

    total_rent_paid = 0
    break_even_year = None
    data = []

    for year in range(1, years + 1):

        
        yearly_rent = rent * 12 * ((1 + rent_growth / 100) ** (year - 1))
        total_rent_paid += yearly_rent

        
        monthly_sip = max(0, emi - rent)
        sip_value = calculate_sip(monthly_sip, sip_return, year)

        
        property_value = property_price * ((1 + property_growth / 100) ** year)

        
        months_paid = year * 12
        remaining_loan = remaining_loan_balance(
            loan_amount,
            loan_rate,
            tenure,
            months_paid
        )

        
        buy_net_worth = property_value - remaining_loan
        rent_net_worth = sip_value

        
        if break_even_year is None and rent_net_worth >= buy_net_worth:
            break_even_year = year

        data.append({
            "Year": year,
            "Rent Net Worth (₹)": round(rent_net_worth, 0),
            "Buy Net Worth (₹)": round(buy_net_worth, 0)
        })

    df = pd.DataFrame(data)

    summary = {
        "emi": round(emi, 0),
        "total_emi_paid": round(total_emi_paid, 0),
        "total_rent_paid": round(total_rent_paid, 0),
        "final_rent_net_worth": round(df.iloc[-1]["Rent Net Worth (₹)"], 0),
        "final_buy_net_worth": round(df.iloc[-1]["Buy Net Worth (₹)"], 0),
        "break_even_year": break_even_year
    }

    return df, summary
