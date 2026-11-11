def sanitize_meter_id(meter_id):
    meter_id = meter_id.strip()
    for ch in ['!', '@', '#', '$', '%']:
        meter_id = meter_id.replace(ch, '')
    return meter_id.upper()

def parse_consumption_readings(readings_csv):
    readings = readings_csv.split(',')
    return [int(r) for r in readings]

def format_billing_summary(account_record):
    parts = account_record.split(':')
    customer_name = parts[0].strip()
    units = int(parts[1])
    zone = parts[2].strip()
    return f"Customer {customer_name} billed {units * 2} USD in {zone}"

def main():
    print("==== Running sanitize_meter_id ====")
    raw_id = input("Enter a meter ID with prefixes (!,@,#,$,%): ")
    clean_id = sanitize_meter_id(raw_id)
    print("Sanitized Meter ID:", clean_id)

    print("\n==== Running parse_consumption_readings ====")
    csv_input = input("Enter consumption readings (e.g. 10,25,30): ")
    readings_list = parse_consumption_readings(csv_input)
    print("Parsed Readings:", readings_list)

    print("\n==== Running format_billing_summary ====")
    summary_input = input("Enter account record (Name:Usage:Zone): ")
    summary = format_billing_summary(summary_input)
    print("Billing Summary:", summary)

if __name__ == "__main__":
    main()