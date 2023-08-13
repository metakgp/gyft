# GYFT - Get Your Freaking Timetable

Gets your timetable from ERP and adds it to your **Google Calendar** or gives you an **ICS file** which you can add in any common calendar application.

> **Note** All updates to this repo should reflect, with appropriate refactorisation, in [gyft-serve](https://github.com/metakgp/gyft-serve/)


## Updates To Be Made Each Sem

The following procedure is to be followed each new semester by the maintainer for updating GYFT to work properly.

- Download the academic calendar for the particular year.
- New semester dates need to be updated in dates.py
- The format for the date-time is `(YYYY, MM, DD, HH, MM)`.
- Raise a pull request once the dates are updated.

## Getting Started

1. Clone this repository 
2. Install the dependencies by running:
    ```sh
    pip install -r requirements.txt
    ```
3. Run the gyft script:
    ```sh
    python3 gyft.py
    ```
    - Optional flags: 
    	- `--input` or `i`: Input file (`.txt`) containing the timetable data/to which timetable data will be saved. **Default:** `data.txt` 
    	- `--output` or `o`: Output file (`.ics`) to which the ICS file will be written. **Default:** `timetable.ics`
    	- `--del-events`: To delete events automatically added by the script before adding new events (explained later) **Default:** `False`

4. Enter your roll number, password, security answer and OTP (if required) when prompted
5. Your timetable will be saved in the file specified by the `--input` flag (**default:** `data.txt`)
6. Now you can choose between 2 options, which will be prompted to you:
   - #### Add to Google Calendar:
     - For this, you have to get your `credentials.json` and save it as `client_secret.json` to the current directory by following the Step 1 from [here](https://developers.google.com/google-apps/calendar/quickstart/python#step_1_turn_on_the_api_name)
     - Also note that adding to Google Calendar requires an Internet connection
  
   - #### Generate ICS file:
     - This will generate an ICS file which you can import into any calendar application.
     - For importing to Google Calendar, follow the instructions given [here](https://support.google.com/calendar/answer/37118?hl=en).
  
> **Note** 
> - You can also use the web application to get your ICS file
> - Go to the [GYFT WebApp](https://gyft.metakgp.org/)
> - Enter your roll number and get the security question
> - Once the security question is fetched, enter your credentials and save the ICS file
> - Source at [metakgp/gyft-serve](https://github.com/metakgp/gyft-serve)

#### Miscellaneous 
To delete all the recurring events added by the CLI or GYFT Web Application (uses property of recurrence to identify events to delete), you can run `gyft.py` with the `--del-events` flag:
```sh
python3 gyft.py --del-events
```

## Development Notes 
This project utilizes the [iitkgp-erp-login](https://github.com/proffapt/iitkgp-erp-login-pypi/) package to handle ERP login functionality.

## Contributing

Please read CONTRIBUTING.md guide to know more.
