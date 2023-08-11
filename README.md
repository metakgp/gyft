# gyft

Get Your Freaking Timetable

NOTE: All updates to this repo should reflect, with appropriate refactorisation, in [gyft-serve](https://github.com/metakgp/gyft-serve/)

## About

Gets your timetable from ERP and adds it to your **Google Calendar** or gives
you an **ICS file** which you can add in any common calendar application.

![instructions](https://cloud.githubusercontent.com/assets/9252491/17613570/7af6ae98-607c-11e6-8597-e720c3475c24.gif)

## Updates To Be Made Each Sem

The following procedure is to be followed each new semester by the maintainer for updating GYFT to work properly.

- Download the academic calendar for the particular year.
- New semester dates need to be updated in dates.py
- The format for the date-time is `(YYYY, MM, DD, HH, MM)`.
- Raise a pull request once the dates are updated.

## How to use the program?

- **Step 1:** Get your timetable from ERP:

  **Run the Gyft script locally (using Python)**
  
  Clone this repository and run the following command:
   ```sh
  $ pip install -r requirements.txt
  ```

  ```sh
  $ python3 gyft.py --user <ROLL_NUMBER> --sem <CURRENT_SEM_NUMBER>
  ```

  Enter your password and security answer when prompted.

  Your timetable will be saved in `data.txt`. Make any changes required in `data.txt`. Then, proceed to Step 2.
  
  **Use the web application on any browser**

  - Go to the [GYFT WebApp](https://gyftkgp.herokuapp.com/).
  - Enter your roll number and get the security question.
  - Once the security question is fetched, enter your credentials and save the ICS file.
  - Move to step 2(b)(ii).
  
  Source at [metakgp/gyft-serve](https://github.com/metakgp/gyft-serve).

- **Step 2:** Decide whether you want to add the events to Google Calendar or
    generate an ICS file from the data.

    Adding to Google Calendar requires an Internet connection

    ICS files are compatible with almost all Calendar applications (including
    the iOS calendar application, Sunrise etc)

- **Step 2(a):** If you decide on adding your events to your Google Calendar:

    - **Step (i):** Get your `credentials.json` and save it as `client_secret.json` to the current directory by
                    following the Step 1 from
                    [here](https://developers.google.com/google-apps/calendar/quickstart/python#step_1_turn_on_the_api_name).

    - **Step (ii):** Now, run:

        ```sh
        $ python3 add_events.py
        ```

    - **MISC:** To delete all the recurring events added by the CLI or GYFT Web Application (uses property of recurrence to identify events to delete):

        ```sh
        $ python3 del_events.py
        ```

- **Step 2(b):** If you decide on generating an ICS file:

    - **Step (i):** Run the command:

        ```sh
        $ python3 generate_ics.py
        ```

        ```sh
        # you can provide input and output file path to this python script
        $ python3 generate_ics.py --input d.txt --output t.ics
        ```

    - **Step (ii):** Open your calendar application and import this ICS file
        into it.

        For google calendar, follow the instructions given [here](https://support.google.com/calendar/answer/37118?hl=en).


## Development Notes 
This project utilizes the [iitkgp-erp-login](https://github.com/proffapt/iitkgp-erp-login-pypi/) package to handle ERP login functionality.

## License

GPLv3.

## Contributing

Please read CONTRIBUTING.md guide to know more.
