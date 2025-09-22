import argparse
import pandas as pd
import numpy as np

### TAKES COMMAND LINE ARGUMENTS <----

def calculate_dcf(cash_flows, discount_rate, terminal_growth_rate, terminal_year):
    years = np.arange(1, len(cash_flows) + 1)
    discounted_cfs = cash_flows / ((1 + discount_rate) ** years)
    terminal_value = (cash_flows[-1] * (1 + terminal_growth_rate)) / (discount_rate - terminal_growth_rate)
    discounted_terminal = terminal_value / ((1 + discount_rate) ** terminal_year)
    dcf_value = np.sum(discounted_cfs) + discounted_terminal
    return dcf_value, discounted_cfs, discounted_terminal

def main():
    parser = argparse.ArgumentParser(description="Automated DCF Valuation Calculator")
    parser.add_argument('--cash_flows', nargs='+', type=float, required=True, help='Projected free cash flows (space-separated list)')
    parser.add_argument('--discount_rate', type=float, required=True, help='Discount rate as decimal (e.g., 0.10 for 10%)')
    parser.add_argument('--terminal_growth', type=float, required=True, help='Terminal growth rate as decimal (e.g., 0.03 for 3%)')
    args = parser.parse_args()
    
    cash_flows = np.array(args.cash_flows)
    discount_rate = args.discount_rate
    terminal_growth_rate = args.terminal_growth
    terminal_year = len(cash_flows)
    
    dcf_value, discounted_cfs, discounted_terminal = calculate_dcf(cash_flows, discount_rate, terminal_growth_rate, terminal_year)
    
    df = pd.DataFrame({
        'Year': np.arange(1, len(cash_flows)+1),
        'Projected FCF': cash_flows,
        'Discounted FCF': discounted_cfs
    })
    print(df.to_string(index=False))
    print(f"\nDiscounted Terminal Value: ${discounted_terminal:,.2f}")
    print(f"Total DCF Value: ${dcf_value:,.2f}")

if __name__ == "__main__":
    main()
