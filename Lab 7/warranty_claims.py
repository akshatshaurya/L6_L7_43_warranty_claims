def parse_claim(text):
    plan, months = text.split(':')
    return plan.strip().title(), float(months)

def age_average(ages_csv):
    values = [int(r) for r in ages_csv.split(',')]
    return sum(values) // len(values)

def payable_charge(text):
    charge, discount = text.split('|')
    total = float(charge) * 1.18 - float(discount)
    return max(total, 0)

def main():
    print("==== Running parse_claim ====")
    user_input = input("Enter plan:age in months (e.g. standard:30): ")
    result = parse_claim(user_input)
    print("Plan and Age:", result)

    print("\n==== Running age_average ====")
    user_input = input("Enter product ages as CSV (e.g. 12,24,36): ")
    result = age_average(user_input)
    print("Average Age:", result)

    print("\n==== Running payable_charge ====")
    user_input = input("Enter charge|discount (e.g. 1500|200): ")
    result = payable_charge(user_input)
    print("Payable Charge:", result)

if __name__ == "__main__":
    main()
