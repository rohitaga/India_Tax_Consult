import streamlit as st
import matplotlib.pyplot as plt

def show():
    senior_citizens()

def senior_citizens():
    # Personal Information Section
    st.title('Tax Analysis App for Senior Citizens (60 years or more)')
    st.header('Personal Information')
    name = st.text_input('Full Name')
    age = st.number_input('Age', value=60, min_value=60)
    tax_regime = st.selectbox('Choose Tax Regime', ['Old Tax Regime', 'New Tax Regime'])

    # Income Details Section
    st.header('Income Details')
    pension_income = st.number_input('Pension Income', value=500000)
    house_property_income = st.number_input('House Property Income', value=0)
    capital_gains = st.number_input('Capital Gains', value=0)
    other_income = st.number_input('Other Income', value=0)

    # Deductions Section
    st.header('Deductions')
    if tax_regime == 'Old Tax Regime':
        deduction_80c = st.number_input('Section 80C (e.g., EPF, PPF)', value=0, max_value=150000)
        deduction_80d = st.number_input('Section 80D (Health Insurance)', value=0, max_value=25000)
        deduction_80g = st.number_input('Section 80G (Donations)', value=0)
        total_deductions = deduction_80c + deduction_80d + deduction_80g
    else:
        total_deductions = 0

    # Tax Paid Section
    st.header('Tax Paid')
    tds = st.number_input('TDS (Tax Deducted at Source)', value=0)
    advance_tax = st.number_input('Advance Tax', value=0)

    # Results Section
    st.header('Results')
    if st.button('Calculate Tax'):
        try:
            # Validate Inputs
            inputs = [pension_income, house_property_income, capital_gains, other_income, total_deductions, tds, advance_tax]
            if any(val < 0 for val in inputs):
                raise ValueError('All values must be non-negative.')

            # Calculate Total Income
            total_income = pension_income + house_property_income + capital_gains + other_income

            # Apply Deductions
            taxable_income = total_income - total_deductions

            # Handling Negative Taxable Income
            if taxable_income < 0:
                raise ValueError('Taxable income is negative after deductions.')

            # Apply Tax Slabs
            tax = 0
            if tax_regime == 'Old Tax Regime':
                if age < 80:
                    slab_amounts = [300000, 500000, 1000000]
                    tax_rates = [0.05, 0.20, 0.30]
                else:
                    slab_amounts = [500000, 1000000]
                    tax_rates = [0.20, 0.30]
                for slab, rate in zip(slab_amounts, tax_rates):
                    tax += max(min(taxable_income, slab) - max(slab - slab_amounts[0], 0), 0) * rate
            else: # New Tax Regime
                slab_amounts = [250000, 500000, 750000, 1000000, 1250000, 1500000]
                tax_rates = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
                for slab, rate in zip(slab_amounts, tax_rates):
                    tax += max(min(taxable_income, slab) - max(slab - 250000, 0), 0) * rate

            # Add Cess
            tax += tax * 0.04

            # Subtract TDS and Advance Tax
            net_tax_payable = tax - tds - advance_tax

            # Display the Result
            st.subheader('Tax Liability Summary')
            st.write(f'Total Tax Payable: ₹{net_tax_payable}')

            # Income Breakdown Visualization
            st.subheader('Income Breakdown')
            income_labels = ['Pension', 'House Property', 'Capital Gains', 'Other']
            income_values = [pension_income, house_property_income, capital_gains, other_income]
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            wedges, texts, autotexts = ax1.pie(income_values, autopct='%1.1f%%', startangle=140)
            ax1.axis('equal')
            ax1.legend(wedges, income_labels, title="Income Types", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            st.pyplot(fig1)

            # Tax Breakdown Visualization
            st.subheader('Tax Breakdown')
            tax_labels = ['Total Income', 'Deductions', 'Taxable Income', 'Tax Payable']
            tax_values = [total_income, total_deductions, taxable_income, net_tax_payable]
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            ax2.bar(tax_labels, tax_values)
            plt.ylabel('Amount (₹)')
            plt.title('Tax Breakdown')
            plt.xticks(rotation=45)
            st.pyplot(fig2)

        except ValueError as e:
            st.error(f'Error: {str(e)}')
        except Exception as e:
            st.error('An unexpected error occurred. Please try again or contact support.')