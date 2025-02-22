import datetime

# File to store journal entries
JOURNAL_FILE = "journal.txt"

def write_entry():
    """Take user input and save it with a timestamp."""
    entry = input("Write your journal entry: ")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_entry = f"{timestamp} - {entry}\n"

    # Save to file
    with open(JOURNAL_FILE, "a") as file:
        file.write(formatted_entry)

    print("Entry saved successfully!")

if __name__ == "__main__":
    write_entry()
