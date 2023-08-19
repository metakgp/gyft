import argparse
from timetable import scrape_timetable, delete_calendar, create_calendar, generate_ICS
from utils import ERPSession


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output",
                        help="Output file containing timetable in .ics format")
    parser.add_argument("-d", "--del-events", action="store_true",
                        help="Delete events automatically added by the script before adding new events")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    if args.del_events:
        delete_calendar()
        if input("\nWould you like to generate a new timetable? (y/n): ").lower() == 'n':
            return

    output_filename = args.output if args.output else "timetable.ics"
    erp_session = ERPSession.login()
    timetable_dict = scrape_timetable(erp_session)

    print(f"Timetable fetched.\n")

    print("What would you like to do now?")
    print("1. Add timetable directly to Google Calendar (requires client_secret.json)")
    print("2. Generate an ICS file")
    print("3. Exit")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        create_calendar(timetable_dict)
    elif choice == 2:
        generate_ICS(timetable_dict, output_filename)
    else:
        exit()


if __name__ == "__main__":
    main()
