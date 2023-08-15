import streamlit as st
import matplotlib.pyplot as plt

# Personal Information Section
st.title('Tax Analysis App')
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

# Note for Users
st.info('Note: Default values have been provided for all fields. Please update them according to your financial details.')

# Results Section
st.header('Results')
if st.button('Calculate Tax'):
    try:
        # Validate Inputs (e.g., non-negative numbers)
        inputs = [salary, house_property_income, capital_gains, other_income, deduction_80c, deduction_80d, deduction_80g, tds, advance_tax]
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

        # Display the Result
        st.subheader('Tax Liability Summary')
        st.write(f'Total Tax Payable: ₹{net_tax_payable}')

        # Income Breakdown Visualization
        st.subheader('Income Breakdown')
        income_labels = ['Salary', 'House Property', 'Capital Gains', 'Other']
        income_values = [salary, house_property_income, capital_gains, other_income]
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        wedges, texts, autotexts = ax1.pie(income_values, autopct='', startangle=140)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
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

# Warning for Tax Law Updates
st.warning('Please note that this app is based on tax laws as of the 2023 fiscal year. Always consult with a tax professional to ensure compliance with the latest regulations.')