import streamlit as st
import matplotlib.pyplot as plt

# Business Old Tax Regime
@st.cache_data
def old_tax_regime_business(taxable_income, age):
    if age < 60:
        slabs = [0, 250000, 500000, 1000000]
        rates = [0.00, 0.05, 0.20, 0.30]
    elif age < 80:
        slabs = [0, 300000, 500000, 1000000]
        rates = [0.00, 0.05, 0.20, 0.30]
    else:
        slabs = [0, 500000, 1000000]
        rates = [0.00, 0.20, 0.30]
    
    slabs.append(float('inf'))  # Adding an upper bound to the slabs
    tax = 0
    for i in range(1, len(slabs)):
        slab_diff = min(taxable_income, slabs[i]) - slabs[i - 1]
        tax += slab_diff * rates[min(i - 1, len(rates) - 1)] # Using min to avoid index out of range
        if taxable_income <= slabs[i]:
            break
    return tax

# Business New Tax Regime
@st.cache_data
def new_tax_regime_business(taxable_income, age):
    slabs = [0, 250000, 500000, 750000, 1000000, 1500000]
    rates = [0.00, 0.05, 0.10, 0.15, 0.20, 0.30] if age < 60 else [0.00, 0.05, 0.10, 0.15, 0.30, 0.30]

    slabs.append(float('inf'))  # Adding an upper bound to the slabs
    tax = 0
    for i in range(1, len(slabs)):
        slab_diff = min(taxable_income, slabs[i]) - slabs[i - 1]
        tax += slab_diff * rates[min(i - 1, len(rates) - 1)] # Using min to avoid index out of range
        if taxable_income <= slabs[i]:
            break
    return tax

@st.cache_data
def calculate_tax(age, tax_regime, business_income, house_property_income, capital_gains, other_income, deduction_80c, deduction_80d, deduction_80g, tds, advance_tax):

    # Validate Inputs (e.g., non-negative numbers)
    inputs = [age, business_income, house_property_income, capital_gains, other_income, deduction_80c, deduction_80d, deduction_80g, tds, advance_tax]
    if any(val < 0 for val in inputs):
        raise ValueError('All values must be non-negative.')

    # Calculate Total Income
    total_income = business_income + house_property_income + capital_gains + other_income

    # Apply Deductions
    total_deductions = deduction_80c + deduction_80d + deduction_80g
    taxable_income = total_income - total_deductions

    # Handling Negative Taxable Income
    if taxable_income < 0:
        raise ValueError('Taxable income is negative after deductions.')
    
    # Apply Tax Slabs
    if tax_regime == 'New Tax Regime':
        tax = new_tax_regime_business(taxable_income, age)
    else:
        tax = old_tax_regime_business(taxable_income, age)

    # Add Cess (Health and Education Cess, 4% on income tax)
    tax += tax * 0.04

    # Subtract TDS and Advance Tax
    net_tax_payable = tax - tds - advance_tax

    return net_tax_payable, total_income, total_deductions, taxable_income

def show():
    business_profession()

def business_profession():
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
    st.title('Tax Analysis App for Business')
    st.header('Personal Information')
    __name__ = st.text_input('Full Name')
    age = st.number_input('Age', value=30)
    tax_regime = st.selectbox('Choose Tax Regime', ['Old Tax Regime', 'New Tax Regime'])

    # Income Details Section
    st.header('Income Details')
    business_income = st.number_input('Business Income', value=500000)
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
    st.header('Results')
    if st.button('Calculate Tax'):
        try:
            # Apply Tax Slabs
            net_tax_payable, total_income, total_deductions, taxable_income = calculate_tax(age, tax_regime, business_income, house_property_income, capital_gains, other_income, deduction_80c, deduction_80d, deduction_80g, tds, advance_tax)

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
    st.markdown("# Tax Insight App Tutorial for Business")
    st.markdown("Welcome to the **Tax Insight Tutorial for Business**. This tutorial will guide you through using the app to understand how your tax is calculated, considering various factors such as business income, deductions, and tax payments.")

    with st.expander("Overview and Key Concepts"):
        st.markdown("- Applicable tax rates and rules for businesses and professionals.")
        st.markdown("- Deductions, TDS, and advance tax payments are incorporated into the calculations.")
        st.markdown("- The app considers different sources of income, including business income, property income, capital gains, and others.")

    steps = [
        ("Step 1: Personal Information", "Provide basic personal details like Full Name, Age, and Tax Regime selection.", "Example:\n- If you are under the New Tax Regime, different tax slabs may apply."),
        ("Step 2: Income Details", "Enter various sources of income such as Business Income, House Property Income, Capital Gains, and Other Income.", "For instance:\n- If your Business Income is ₹500,000, it becomes part of your total income."),
        ("Step 3: Deductions", "Deductions like Section 80C, 80D, and 80G can be entered to lower taxable income.", "For example:\n- If you have a Section 80D deduction of ₹25,000 for Health Insurance, it's subtracted from total income."),
        ("Step 4: Tax Paid", "Enter taxes paid via TDS or Advance Tax. This considers taxes paid before calculating final tax liability.", "For example:\n- If you've paid ₹20,000 as TDS and ₹10,000 as Advance Tax, these are subtracted."),
        ("Step 5: Results", "Click 'Calculate Tax' to simulate the tax calculation process using your data.", "Example:\n- The app will calculate the total tax liability, considering all inputs, and display a summary and breakdown of income and taxes.")
    ]

    for step, explanation, example in steps:
        with st.expander(step):
            st.write(explanation)
            st.markdown("#### Example:")
            st.write(example)
    
    st.markdown("## Tax Slabs and Calculations")

    st.markdown("### Business Tax Slabs (Old Regime)")
    st.table({
        "Range": ["₹0 to ₹250,000", "₹250,001 to ₹500,000", "₹500,001 to ₹1,000,000", "Above ₹1,000,000"],
        "Rate": ["0%", "5%", "20%", "30%"]
    })
    st.write("Example Calculation for Taxable Income of ₹485,000:")
    st.write("- ₹250,000 at 0% = ₹0\n- ₹235,000 at 5% = ₹11,750\n- Total Tax (Old Regime): ₹11,750")

    st.markdown("### Business Tax Slabs (New Regime)")
    st.table({
        "Range": ["₹0 to ₹250,000", "₹250,001 to ₹500,000", "₹500,001 to ₹750,000", "₹750,001 to ₹1,000,000", "₹1,000,001 to ₹1,500,000"],
        "Rate": ["0%", "5%", "10%", "15%", "30%"]
    })
    st.write("Example Calculation for Taxable Income of ₹485,000:")
    st.write("- ₹250,000 at 0% = ₹0\n- ₹235,000 at 5% = ₹11,750\n- Total Tax (New Regime): ₹11,750")

    st.markdown("### Health and Education Cess")
    st.write("A 4% cess is added to the calculated tax.")
    st.write("Example:")
    st.write("- Total Tax (Old Regime): ₹11,750\n- Health and Education Cess: ₹470 (4% of ₹11,750)\n- Total Tax after Cess: ₹12,220")