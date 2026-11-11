
def sanitize_meter_id(meter_id):
    """Remove specified prefixes and normalize the meter ID."""
    if not isinstance(meter_id, str):
        return ""

    meter_id = meter_id.strip()

    for ch in ['!', '@', '#', '$', '%']:
        meter_id = meter_id.replace(ch, '')

    return meter_id.upper()


def parse_consumption_readings(readings_csv):
    """Safely parse comma-separated consumption readings."""
    if not isinstance(readings_csv, str):
        return []

    if not readings_csv.strip():
        return []

    readings = readings_csv.split(',')
    parsed_readings = []

    try:
        for reading in readings:
            reading = reading.strip()

            if not reading:
                return []

            parsed_readings.append(int(reading))

        return parsed_readings

    except (ValueError, TypeError):
        return []


def format_billing_summary(account_record):
    """Safely format a customer's billing summary."""
    if not isinstance(account_record, str):
        return "Invalid account record"

    parts = account_record.split(':')

    if len(parts) != 3:
        return "Invalid account record"

    customer_name = parts[0].strip()
    zone = parts[2].strip()

    if not customer_name or not zone:
        return "Invalid account record"

    try:
        units = int(parts[1].strip())

        if units < 0:
            return "Invalid account record"

    except (ValueError, TypeError):
        return "Invalid account record"

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
