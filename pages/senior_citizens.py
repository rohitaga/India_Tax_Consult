import streamlit as st
import matplotlib.pyplot as plt

# senior_citizen_old_tax_regime
@st.cache_data
def senior_citizen_old_tax_regime(taxable_income, age):
    slabs = [0, 300000, 500000, 1000000, float('inf')]
    rates = [0.00, 0.05, 0.20, 0.30]
    fixed_amounts = [0, 0, 10000, 110000]

    tax = 0
    for i in range(1, len(slabs)):
        slab_diff = min(taxable_income, slabs[i]) - slabs[i - 1]
        tax += fixed_amounts[i - 1] + slab_diff * rates[i - 1]
        if taxable_income <= slabs[i]:
            break
    return tax

# senior_citizen_new_tax_regime
@st.cache_data
def senior_citizen_new_tax_regime(taxable_income, age):
    slabs = [0, 250000, 500000, 750000, 1000000, 1250000, 1500000, float('inf')]
    rates = [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    fixed_amounts = [0, 0, 12500, 37500, 75000, 125000, 187500]

    tax = 0
    for i in range(1, len(slabs)):
        slab_diff = min(taxable_income, slabs[i]) - slabs[i - 1]
        tax += fixed_amounts[i - 1] + slab_diff * rates[i - 1]
        if taxable_income <= slabs[i]:
            break
    return tax

# super_senior_citizen_old_tax_regime
@st.cache_data
def super_senior_citizen_old_tax_regime(taxable_income, age):
    slabs = [0, 500000, 1000000, float('inf')]
    rates = [0.00, 0.20, 0.30]
    fixed_amounts = [0, 0, 100000]

    tax = 0
    for i in range(1, len(slabs)):
        slab_diff = min(taxable_income, slabs[i]) - slabs[i - 1]
        tax += fixed_amounts[i - 1] + slab_diff * rates[i - 1]
        if taxable_income <= slabs[i]:
            break
    return tax

# super_senior_citizen_new_tax_regime
@st.cache_data
def super_senior_citizen_new_tax_regime(taxable_income, age):
    slabs = [0, 250000, 500000, 750000, 1000000, 1250000, 1500000, float('inf')]
    rates = [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    fixed_amounts = [0, 0, 12500, 37500, 75000, 125000, 187500]

    tax = 0
    for i in range(1, len(slabs)):
        slab_diff = min(taxable_income, slabs[i]) - slabs[i - 1]
        tax += fixed_amounts[i - 1] + slab_diff * rates[i - 1]
        if taxable_income <= slabs[i]:
            break
    return tax  

@st.cache_data
def calculate_tax(age, tax_regime, pension_income, house_property_income, capital_gains, other_income, total_deductions, tds, advance_tax):

    # Validate Inputs
    inputs = [age, pension_income, house_property_income, capital_gains, other_income, total_deductions, tds, advance_tax]
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
    if age < 80:
        if tax_regime == 'New Tax Regime':
            tax = senior_citizen_new_tax_regime(taxable_income, age)
        else:
            tax = senior_citizen_old_tax_regime(taxable_income, age)
    else:
        if tax_regime == 'New Tax Regime':
            tax = super_senior_citizen_new_tax_regime(taxable_income, age)
        else:
            tax = super_senior_citizen_old_tax_regime(taxable_income, age)

    # Add Cess
    tax += tax * 0.04

    # Subtract TDS and Advance Tax
    net_tax_payable = tax - tds - advance_tax

    return net_tax_payable, total_income, total_deductions, taxable_income

def show():
    senior_citizens()

def senior_citizens():
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
    st.title('Tax Analysis App for Senior Citizens (60 years or more)')
    st.header('Personal Information')
    __name__ = st.text_input('Full Name')
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
            net_tax_payable, total_income, total_deductions, taxable_income = calculate_tax(age, tax_regime, pension_income, house_property_income, capital_gains, other_income, total_deductions, tds, advance_tax)
            
            # Display the Result
            st.subheader('Tax Liability Summary')
            st.write(f'Total Tax Payable with 4% cess: ₹{net_tax_payable}')

            # Income Breakdown Visualization
            st.subheader('Income Breakdown')
            income_labels = ['Pension', 'House Property', 'Capital Gains', 'Other']
            income_values = [pension_income, house_property_income, capital_gains, other_income]
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            wedges, texts, autotexts = ax1.pie(income_values, autopct='', startangle=140)
            ax1.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
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
    st.markdown("# Tax Insight App Tutorial for Senior Citizens")
    st.markdown("Welcome to the **Tax Insight Tutorial** specifically designed for senior citizens. This tutorial will guide you through using the app and understanding how your tax is calculated. Different rules and benefits are considered for individuals aged 60 years or more.")

    with st.expander("Overview and Key Concepts"):
        st.markdown("- Tax benefits are applicable for senior citizens.")
        st.markdown("- The app considers age-specific tax rules, deductions, and other factors to estimate potential tax liability.")
        st.markdown("- The calculation involves segmenting your income, applying rates to each segment, considering deductions, and incorporating Health and Education Cess.")

    steps = [
        ("Step 1: Personal Information", "Provide basic personal details like Full Name and Age (60 years or more). Age is considered to apply specific tax benefits for senior citizens.", "Example:\n- If you are 80 years or more, different tax slabs may apply."),
        ("Step 2: Income Details", "Enter various sources of income like Pension Income, House Property Income, Capital Gains, and Other Income.", "For instance:\n- If your Pension Income is ₹500,000, it becomes part of your total income."),
        ("Step 3: Deductions", "Deductions lower taxable income. They are applicable in the Old Tax Regime only. Deductions decrease the portion subject to taxation.", "For example:\n- If you have a Section 80C deduction of ₹150,000, it's subtracted from total income."),
        ("Step 4: Tax Paid", "Enter taxes paid via TDS or Advance Tax. This considers taxes paid before calculating final tax liability.", "For example:\n- If you've paid ₹20,000 as TDS and ₹10,000 as Advance Tax, these are subtracted."),
        ("Step 5: Results", "Click 'Calculate Tax' to simulate the process using your data.", "Example:\n- Based on your inputs, the app will calculate the total tax liability, including any applicable cess or surcharge.")
    ]

    for step, explanation, example in steps:
        with st.expander(step):
            st.write(explanation)
            st.markdown("#### Example:")
            st.write(example)

    st.markdown("## Senior Citizen Tax Slabs and Calculations (60 years or more but less than 80 years)")

    st.markdown("### Senior Citizen Tax Slabs (Old Regime)")
    st.table({
        "Range": ["₹0 to ₹300,000", "₹300,001 to ₹500,000", "₹500,001 to ₹1,000,000", "Above ₹1,000,000"],
        "Rate": ["0%", "5%", "20%", "30%"]
    })
    st.write("Example Calculation for Taxable Income of ₹3,000,000:")
    st.write("- ₹300,000 at 0% = ₹0\n- ₹200,000 at 5% = ₹10,000\n- ₹500,000 at 20% = ₹100,000\n- ₹2,000,000 at 30% = ₹600,000\n- Total Tax (Old Regime): ₹710,000")

    st.markdown("### Senior Citizen Tax Slabs (New Regime)")
    st.table({
        "Range": ["₹0 to ₹250,000", "₹250,001 to ₹500,000", "₹500,001 to ₹750,000", "₹750,001 to ₹1,000,000", "₹1,000,001 to ₹1,250,000", "₹1,250,001 to ₹1,500,000", "Above ₹1,500,000"],
        "Rate": ["0%", "5%", "10%", "15%", "20%", "25%", "30%"]
    })
    st.write("Example Calculation for Taxable Income of ₹3,000,000:")
    st.write("- ₹250,000 at 0% = ₹0\n- ₹250,000 at 5% = ₹12,500\n- ₹250,000 at 10% = ₹25,000\n- ₹250,000 at 15% = ₹37,500\n- ₹250,000 at 20% = ₹50,000\n- ₹250,000 at 25% = ₹62,500\n- ₹1,500,000 at 30% = ₹450,000\n- Total Tax (New Regime): ₹837,500")

    st.markdown("## Super Senior Citizen Tax Slabs and Calculations (80 years or more)")

    st.markdown("### Super Senior Citizen Tax Slabs (Old Regime)")
    st.table({
        "Range": ["₹0 to ₹500,000", "₹500,001 to ₹1,000,000", "Above ₹1,000,000"],
        "Rate": ["0%", "20%", "30%"]
    })
    st.write("Example Calculation for Taxable Income of ₹3,000,000:")
    st.write("- ₹500,000 at 0% = ₹0\n- ₹500,000 at 20% = ₹100,000\n- ₹2,000,000 at 30% = ₹600,000\n- Total Tax (Old Regime): ₹700,000")

    st.markdown("### Super Senior Citizen Tax Slabs (New Regime)")
    st.table({
        "Range": ["₹0 to ₹250,000", "₹250,001 to ₹500,000", "₹500,001 to ₹750,000", "₹750,001 to ₹1,000,000", "₹1,000,001 to ₹1,250,000", "₹1,250,001 to ₹1,500,000", "Above ₹1,500,000"],
        "Rate": ["0%", "5%", "10%", "15%", "20%", "25%", "30%"]
    })
    st.write("Example Calculation for Taxable Income of ₹3,000,000:")
    st.write("- ₹250,000 at 0% = ₹0\n- ₹250,000 at 5% = ₹12,500\n- ₹250,000 at 10% = ₹25,000\n- ₹250,000 at 15% = ₹37,500\n- ₹250,000 at 20% = ₹50,000\n- ₹250,000 at 25% = ₹62,500\n- ₹1,500,000 at 30% = ₹450,000\n- Total Tax (New Regime): ₹837,500")

    st.markdown("### Health and Education Cess")
    st.write("A 4% cess is added to the calculated tax.")
    st.write("Example:")
    st.write("- Total Tax (Old Regime): ₹11,750\n- Health and Education Cess: ₹470 (4% of ₹11,750)\n- Total Tax after Cess: ₹12,220")