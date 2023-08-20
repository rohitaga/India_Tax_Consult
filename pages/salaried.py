import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def calculate_tax(residential_status, tax_regime, age, salary, house_property_income, capital_gains, other_income, deduction_80c, deduction_80d, deduction_80g, tds, advance_tax):
    # Validate Inputs (e.g., non-negative numbers)
    inputs = [age, salary, house_property_income, capital_gains, other_income, deduction_80c, deduction_80d, deduction_80g, tds, advance_tax]
    if any(val < 0 for val in inputs):
        raise ValueError('All values must be non-negative.')

    # Calculate Total Income
    total_income = salary + house_property_income + capital_gains + other_income

    # Apply Deductions
    total_deductions = deduction_80c + deduction_80d + deduction_80g
    taxable_income = total_income - total_deductions

    # Handling Negative Taxable Income
    if taxable_income < 0:
        raise ValueError('Taxable income is negative after deductions.')

    # Apply Tax Slabs
    tax = 0
    if residential_status == 'Resident':
        if tax_regime == 'New Tax Regime':
            # New Tax Regime for Residents
            slab_amounts = [300000, 600000, 900000, 1200000, 1500000]
            tax_rates = [0.05, 0.10, 0.15, 0.20, 0.25]
            for slab, rate in zip(slab_amounts, tax_rates):
                tax += max(min(taxable_income, slab) - max(slab - 300000, 0), 0) * rate
            tax -= 15000  # Adjustment for the initial slab
        else:
            # Old Tax Regime for Residents (considering age)
            slab_amounts = [250000, 500000, 1000000]
            tax_rates = [0.05, 0.20, 0.30]
            if age < 60:
                slab_amounts[0] = 250000
            elif age < 80:
                slab_amounts[0] = 300000
            else:
                slab_amounts[0] = 500000
            for slab, rate in zip(slab_amounts, tax_rates):
                tax += max(min(taxable_income, slab) - max(slab - 250000, 0), 0) * rate
    else:
        # Tax Slabs for Non-Residents (New Tax Regime is applied)
        slab_amounts = [300000, 600000, 900000, 1200000, 1500000]
        tax_rates = [0.05, 0.10, 0.15, 0.20, 0.25]
        for slab, rate in zip(slab_amounts, tax_rates):
            tax += max(min(taxable_income, slab) - max(slab - 300000, 0), 0) * rate
        tax -= 15000  # Adjustment for the initial slab

    # Add Cess (Health and Education Cess, 4% on income tax)
    tax += tax * 0.04

    # Subtract TDS and Advance Tax
    net_tax_payable = tax - tds - advance_tax

    return net_tax_payable, total_income, total_deductions, taxable_income

def show():
    salaried_non_resident()

def salaried_non_resident():
    # Customizing the sidebar appearance
    st.sidebar.title("Navigation")

    navigation = st.sidebar.selectbox("Select an Option", ["Tax Calculator", "Learning Manual"])

    if navigation == "Tax Calculator":
        main_app()
    elif navigation == "Learning Manual":
        description()
        
def main_app():
    # Personal Information Section
    st.info('Note: Default values have been provided for all fields. Please update them according to your financial details.')
    st.title('Tax Analysis App for Salaried Employees and Non-Residents')
    st.header('Personal Information')
    name = st.text_input('Full Name')
    age = st.number_input('Age', value=30)
    residential_status = st.selectbox('Residential Status', ['Resident', 'Non-Resident', 'Not Ordinarily Resident'])
    tax_regime = st.selectbox('Choose Tax Regime', ['Old Tax Regime', 'New Tax Regime'])

    # Income Details Section
    st.header('Income Details')
    salary = st.number_input('Salary Income', value=500000)
    house_property_income = st.number_input('House Property Income', value=0)
    capital_gains = st.number_input('Capital Gains', value=0)
    other_income = st.number_input('Other Income', value=0)

    # Deductions Section
    st.header('Deductions')
    deduction_80c = st.number_input('Section 80C (e.g., EPF, PPF)', value=0, max_value=150000)
    deduction_80d = st.number_input('Section 80D (Health Insurance)', value=0, max_value=25000)
    deduction_80g = st.number_input('Section 80G (Donations)', value=0)

    # Tax Paid Section
    st.header('Tax Paid')
    tds = st.number_input('TDS (Tax Deducted at Source)', value=0)
    advance_tax = st.number_input('Advance Tax', value=0)

    # Results Section
    if st.button('Calculate Tax'):
        try:
            net_tax_payable, total_income, total_deductions, taxable_income = calculate_tax(residential_status, tax_regime, age, salary, house_property_income, capital_gains, other_income, deduction_80c, deduction_80d, deduction_80g, tds, advance_tax)
            st.subheader('Tax Liability Summary')
            st.write(f'Total Tax Payable: ₹{net_tax_payable}')
            
            # Income Breakdown Visualization
            st.subheader('Income Breakdown')
            income_labels = ['Salary', 'House Property', 'Capital Gains', 'Other']
            income_values = [salary, house_property_income, capital_gains, other_income]
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            wedges, texts, autotexts = ax1.pie(income_values, autopct='', startangle=140)
            ax1.axis('equal')
            percentages = [f'{value/sum(income_values)*100:.1f}%' for value in income_values]
            legend_labels = [f'{label}: {pct}' for label, pct in zip(income_labels, percentages)]
            ax1.legend(wedges, legend_labels, title="Income Types", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            st.pyplot(fig1)

            # Tax Breakdown Visualization
            st.subheader('Tax Breakdown')
            tax_labels = ['Total Income', 'Deductions', 'Taxable Income', 'Tax Payable']
            tax_values = [total_income, total_deductions, taxable_income, net_tax_payable]
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            ax2.bar(tax_labels, tax_values)
            plt.ylabel('Amount (₹)')
            plt.title('Tax Breakdown')
            plt.xticks(rotation=45)  # Rotate x-axis labels
            st.pyplot(fig2)

        except ValueError as e:
            st.error(f'Error: {str(e)}')
        except Exception as e:
            st.error('An unexpected error occurred. Please try again or contact support.')

def description():
    st.markdown("# Tax Insight App Tutorial")
    st.markdown("Welcome to the **Tax Insight Tutorial**. This tutorial will guide you through using the app and understanding how your tax is calculated. Behind the scenes, the app utilizes tax rules and the data you've provided to perform tax calculations.")

    with st.expander("Overview and Key Concepts"):
        st.markdown("- Different tax rates apply for non-residents.")
        st.markdown("- The app considers tax rules, deductions, and other factors to estimate potential tax liability.")
        st.markdown("- The calculation involves segmenting your income, applying rates to each segment, considering deductions, and incorporating Health and Education Cess.")

    steps = [
        ("Step 1: Personal Information", "Provide basic personal details like Full Name, Age, and Residential Status. These details are used to customize tax calculations based on age and residency rules.", "Example:\n- If you are a senior citizen, different tax slabs may apply."),
        ("Step 2: Income Details", "Enter various sources of income. Each source contributes to your total income and affects tax calculations based on distinct rates.", "For instance:\n- If your Salary Income is ₹500,000, it becomes part of your total income.\n- Tax slabs vary by income ranges."),
        ("Step 3: Deductions", "Deductions lower taxable income. They decrease the portion subject to taxation, providing a more accurate tax estimation.", "For example:\n- If you have a Section 80C deduction of ₹150,000, it's subtracted from total income before tax rates are applied."),
        ("Step 4: Tax Paid", "Enter taxes paid via TDS or Advance Tax. This considers taxes paid before calculating final tax liability.", "For example:\n- If you've paid ₹20,000 as TDS and ₹10,000 as Advance Tax, these are subtracted."),
        ("Step 5: Results", "Click 'Calculate Tax' to simulate the process using your data.", "Example:\n- Based on your inputs, the app will calculate the total tax liability, including any applicable cess or surcharge.")
    ]

    for step, explanation, example in steps:
        with st.expander(step):
            st.write(explanation)
            st.markdown("#### Example:")
            st.write(example)