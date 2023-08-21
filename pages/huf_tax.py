import streamlit as st
import matplotlib.pyplot as plt

@st.cache_data
def calculate_tax(tax_regime, business_income, house_property_income, capital_gains, other_income, total_deductions, tds, advance_tax):

    # Validate Inputs
    inputs = [business_income, house_property_income, capital_gains, other_income, total_deductions, tds, advance_tax]
    if any(val < 0 for val in inputs):
        raise ValueError('All values must be non-negative.')

    # Calculate Total Income
    total_income = business_income + house_property_income + capital_gains + other_income

    # Apply Deductions
    taxable_income = total_income - total_deductions

    # Handling Negative Taxable Income
    if taxable_income < 0:
        raise ValueError('Taxable income is negative after deductions.')

    # Apply Tax Slabs
    tax = 0
    if tax_regime == 'Old Tax Regime':
        slab_amounts = [250000, 500000, 1000000]
        tax_rates = [0.05, 0.20, 0.30]
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

    return net_tax_payable, total_income, total_deductions, taxable_income

def show():
    hindu_undivided_family()

def hindu_undivided_family():
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
    st.title('Tax Analysis App for Hindu Undivided Family')
    st.header('Personal Information')
    __name__ = st.text_input('Full Name')
    tax_regime = st.selectbox('Choose Tax Regime', ['Old Tax Regime', 'New Tax Regime'])

    # Income Details Section
    st.header('Income Details')
    business_income = st.number_input('Business Income', value=500000)
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
            # Apply Tax slab
            net_tax_payable, total_income, total_deductions, taxable_income = calculate_tax(tax_regime, business_income, house_property_income, capital_gains, other_income, total_deductions, tds, advance_tax)
            
            # Display the Result
            st.subheader('Tax Liability Summary')
            st.write(f'Total Tax Payable with 4% cess: ₹{net_tax_payable}')

            # Income Breakdown Visualization
            st.subheader('Income Breakdown')
            income_labels = ['Business', 'House Property', 'Capital Gains', 'Other']
            income_values = [business_income, house_property_income, capital_gains, other_income]
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
            plt.xticks(rotation=45)
            st.pyplot(fig2)

        except ValueError as e:
            st.error(f'Error: {str(e)}')
        except Exception as e:
            st.error('An unexpected error occurred. Please try again or contact support.')

def description():
    st.markdown("# Tax Insight App Tutorial for Hindu Undivided Family")
    st.markdown("Welcome to the **Tax Insight Tutorial** for Hindu Undivided Families (HUF). This tutorial will guide you through using the app and understanding how your HUF's tax is calculated.")

    with st.expander("Overview and Key Concepts"):
        st.markdown("- Special tax provisions apply for Hindu Undivided Families.")
        st.markdown("- The app considers tax rules, deductions, and other factors specific to HUF to estimate potential tax liability.")
        st.markdown("- The calculation involves segmenting your income, applying rates to each segment, considering deductions, and incorporating Health and Education Cess.")

    steps = [
        ("Step 1: Tax Regime Selection", "Choose between the Old and New Tax Regime. Different deductions are applicable depending on the chosen regime.", "Example:\n- The Old Tax Regime allows certain deductions under Section 80C, 80D, and 80G."),
        ("Step 2: Income Details", "Enter various sources of income like Business Income, House Property Income, Capital Gains, and Other Income.", "For instance:\n- If your Business Income is ₹500,000, it becomes part of your total income."),
        ("Step 3: Deductions", "Deductions lower taxable income. They are applicable in the Old Tax Regime only. Deductions decrease the portion subject to taxation.", "For example:\n- If you have a Section 80C deduction of ₹150,000, it's subtracted from total income."),
        ("Step 4: Tax Paid", "Enter taxes paid via TDS or Advance Tax. This considers taxes paid before calculating final tax liability.", "For example:\n- If you've paid ₹20,000 as TDS and ₹10,000 as Advance Tax, these are subtracted."),
        ("Step 5: Results", "Click 'Calculate Tax' to simulate the process using your data.", "Example:\n- Based on your inputs, the app will calculate the total tax liability, including any applicable cess or surcharge.")
    ]

    for step, explanation, example in steps:
        with st.expander(step):
            st.write(explanation)
            st.markdown("#### Example:")
            st.write(example)