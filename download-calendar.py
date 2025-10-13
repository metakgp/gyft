from utils.academic_calander_handler import get_latest_calendar
import time

MAX_RETRIES = 10
WAIT_TIME = 2

def main():
	for attempt in range(1, MAX_RETRIES + 1):
		print(f"Attempt {attempt} to download academic calendar...")
		success = get_latest_calendar()
		if success:
			print("Academic calendar downloaded successfully.")
			return
		else:
			print(f"Download failed. Retrying in {WAIT_TIME} seconds...")
			time.sleep(WAIT_TIME)
	print("Failed to download academic calendar after multiple attempts.")

if __name__ == "__main__":
	main()

