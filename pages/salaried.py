import streamlit as st
import matplotlib.pyplot as plt

# Old Tax Regime (Salaried Individuals)
@st.cache_data
def old_tax_regime_salaried(taxable_income, age):
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

# New Tax Regime (Salaried Individuals)
@st.cache_data
def new_tax_regime_salaried(taxable_income):
    slabs = [0, 250000, 500000, 750000, 1000000, 1250000, 1500000]
    rates = [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]

    slabs.append(float('inf'))  # Adding an upper bound to the slabs
    tax = 0
    for i in range(1, len(slabs)):
        slab_diff = min(taxable_income, slabs[i]) - slabs[i - 1]
        tax += slab_diff * rates[min(i - 1, len(rates) - 1)] # Using min to avoid index out of range
        if taxable_income <= slabs[i]:
            break
    return tax

# Old Tax Regime (NRI)
@st.cache_data
def old_tax_regime_nri(taxable_income):
    slabs = [0, 250000, 500000, 1000000]
    rates = [0.00, 0.05, 0.20, 0.30]

    slabs.append(float('inf'))  # Adding an upper bound to the slabs
    tax = 0
    for i in range(1, len(slabs)):
        slab_diff = min(taxable_income, slabs[i]) - slabs[i - 1]
        tax += slab_diff * rates[min(i - 1, len(rates) - 1)] # Using min to avoid index out of range
        if taxable_income <= slabs[i]:
            break
    return tax

# New Tax Regime (NRI)
@st.cache_data
def new_tax_regime_nri(taxable_income):
    slabs = [0, 250000, 500000, 750000, 1000000, 1500000]
    rates = [0.00, 0.05, 0.10, 0.15, 0.30, 0.30]

    slabs.append(float('inf'))  # Adding an upper bound to the slabs
    tax = 0
    for i in range(1, len(slabs)):
        slab_diff = min(taxable_income, slabs[i]) - slabs[i - 1]
        tax += slab_diff * rates[min(i - 1, len(rates) - 1)] # Using min to avoid index out of range
        if taxable_income <= slabs[i]:
            break
    return tax

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
    if residential_status == 'Resident':
        if tax_regime == 'New Tax Regime':
            tax = new_tax_regime_salaried(taxable_income)
        else:
            tax = old_tax_regime_salaried(taxable_income, age)
    else:
        if tax_regime == 'New Tax Regime':
            tax = new_tax_regime_nri(taxable_income)
        else:
            tax = old_tax_regime_nri(taxable_income)

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
    residential_status = st.selectbox('Residential Status', ['Resident', 'Non-Resident'])
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
            st.write(f'Total Tax Payable with 4% cess: ₹{net_tax_payable}')
            
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
        ("Step 2: Income Details", "Enter various sources of income. Each source contributes to your total income and affects tax calculations based on distinct rates.", "Example:\n- Salary: ₹400,000\n- House Property Income: ₹50,000\n- Capital Gains: ₹30,000\n- Other Income: ₹5,000\n- Total Income: ₹485,000"),
        ("Step 3: Deductions", "Deductions lower taxable income. They decrease the portion subject to taxation, providing a more accurate tax estimation.", "Example:\n- Section 80C: ₹20,000\n- Section 80D: ₹5,000\n- Total Deductions: ₹25,000\n- Taxable Income after Deductions: ₹460,000"),
        ("Step 4: Tax Paid", "Enter taxes paid via TDS or Advance Tax. This considers taxes paid before calculating final tax liability.", "Example:\n- Total Tax after Cess: ₹12,220\n- TDS: ₹2,000\n- Advance Tax: ₹1,000\n- Net Tax Payable: ₹9,220"),
        ("Step 5: Results", "Click 'Calculate Tax' to simulate the process using your data.", "Example:\n- Based on your inputs, the app will calculate the total tax liability, including any applicable cess or surcharge.")
    ]

    for step, explanation, example in steps:
        with st.expander(step):
            st.write(explanation)
            st.markdown("#### Example:")
            st.write(example)

    st.markdown("## Tax Slabs and Calculations")
    st.markdown("### Resident Tax Slabs (Old Regime)")
    st.table({
        "Range": ["₹0 to ₹250,000", "₹250,001 to ₹500,000", "₹500,001 to ₹1,000,000", "Above ₹1,000,000"],
        "Rate": ["0%", "5%", "20%", "30%"]
    })
    st.write("Example Calculation for Taxable Income of ₹485,000:")
    st.write("- ₹250,000 at 0% = ₹0\n- ₹235,000 at 5% = ₹11,750\n- Total Tax (Old Regime): ₹11,750")

    st.markdown("### Resident Tax Slabs (New Regime)")
    st.table({
        "Range": ["₹0 to ₹250,000", "₹250,001 to ₹500,000", "₹500,001 to ₹750,000", "₹750,001 to ₹1,000,000", "₹1,000,001 to ₹1,500,000"],
        "Rate": ["0%", "5%", "10%", "15%", "30%"]
    })
    st.write("Example Calculation for Taxable Income of ₹485,000:")
    st.write("- ₹250,000 at 0% = ₹0\n- ₹235,000 at 5% = ₹11,750\n- Total Tax (New Regime): ₹11,750")

    st.markdown("### Non-Resident Tax Slabs (Old Regime)")
    st.table({
        "Range": ["₹0 to ₹250,000", "₹250,001 to ₹500,000", "₹500,001 to ₹1,000,000", "Above ₹1,000,000"],
        "Rate": ["0%", "5%", "20%", "30%"]
    })
    st.write("Example Calculation for Taxable Income of ₹700,000:")
    st.write("- ₹250,000 at 0% = ₹0\n- ₹250,000 at 5% = ₹12,500\n- ₹200,000 at 20% = ₹40,000\n- Total Tax (Old Regime): ₹52,500")

    st.markdown("### Non-Resident Tax Slabs (New Regime)")
    st.table({
        "Range": ["₹0 to ₹250,000", "₹250,001 to ₹500,000", "₹500,001 to ₹750,000", "₹750,001 to ₹1,000,000", "₹1,000,001 to ₹1,500,000"],
        "Rate": ["0%", "5%", "10%", "15%", "30%"]
    })
    st.write("Example Calculation for Taxable Income of ₹700,000:")
    st.write("- ₹250,000 at 0% = ₹0\n- ₹250,000 at 5% = ₹12,500\n- ₹200,000 at 10% = ₹20,000\n- Total Tax (New Regime): ₹32,500")

    st.markdown("### Health and Education Cess")
    st.write("A 4% cess is added to the calculated tax.")
    st.write("Example:")
    st.write("- Total Tax (Old Regime): ₹11,750\n- Health and Education Cess: ₹470 (4% of ₹11,750)\n- Total Tax after Cess: ₹12,220")

    # with st.expander("Resident Tax Slabs (Old Regime)"):
    #     st.markdown("- ₹0 to ₹250,000: 0%\n- ₹250,001 to ₹500,000: 5%\n- ₹500,001 to ₹1,000,000: 20%\n- Above ₹1,000,000: 30%")
    #     st.write("Example Calculation for Taxable Income of ₹485,000:")
    #     st.write("- ₹250,000 at 0% = ₹0\n- ₹235,000 at 5% = ₹11,750\n- Total Tax (Old Regime): ₹11,750")

    # with st.expander("Resident Tax Slabs (New Regime)"):
    #     st.markdown("- ₹0 to ₹250,000: 0%\n- ₹250,001 to ₹500,000: 5%\n- ₹500,001 to ₹750,000: 10%\n- ... and so on.")
    #     st.write("Example Calculation for Taxable Income of ₹485,000:")
    #     st.write("- ₹250,000 at 0% = ₹0\n- ₹235,000 at 5% = ₹11,750\n- Total Tax (New Regime): ₹11,750")

    # with st.expander("Non-Resident Tax Slabs (Old Regime)"):
    #     st.markdown("- ₹0 to ₹250,000: 0%\n- ₹250,001 to ₹500,000: 5%\n- ₹500,001 to ₹1,000,000: 20%\n- Above ₹1,000,000: 30%")
    #     st.write("Example Calculation for Taxable Income of ₹700,000:")
    #     st.write("- ₹250,000 at 0% = ₹0\n- ₹250,000 at 5% = ₹12,500\n- ₹200,000 at 20% = ₹40,000\n- Total Tax (Old Regime): ₹52,500")

    # with st.expander("Non-Resident Tax Slabs (New Regime)"):
    #     st.markdown("- ₹0 to ₹250,000: 0%\n- ₹250,001 to ₹500,000: 5%\n- ₹500,001 to ₹750,000: 10%\n- ₹750,001 to ₹1,000,000: 15%\n- ₹1,000,001 to ₹1,500,000: 30%")
    #     st.write("Example Calculation for Taxable Income of ₹700,000:")
    #     st.write("- ₹250,000 at 0% = ₹0\n- ₹250,000 at 5% = ₹12,500\n- ₹200,000 at 10% = ₹20,000\n- Total Tax (New Regime): ₹32,500")

    # with st.expander("Health and Education Cess"):
    #     st.markdown("A 4% cess is added to the calculated tax.")
    #     st.write("Example:")
    #     st.write("- Total Tax (Old Regime): ₹11,750\n- Health and Education Cess: ₹470 (4% of ₹11,750)\n- Total Tax after Cess: ₹12,220")
