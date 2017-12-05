# gyft

Get Your Freaking Timetable

## About

Gets your timetable from ERP and adds it to your **Google Calendar** or gives
you an **ICS file** which you can add in any common calendar application.

**Note:** Please use this utility with `python3`.

![instructions](https://cloud.githubusercontent.com/assets/9252491/17613570/7af6ae98-607c-11e6-8597-e720c3475c24.gif)

## How to use the program?

- **Step 1:** Get your timetable from ERP:

  ```sh
  $ python3 gyft.py --user <ROLL_NUMBER>
  ```

  Enter your password & security answer when prompted.

  Your timetable will be saved in `data.txt`. Make any changes required appropriately in `data.txt`.

- **Step 2:** Decide whether you want to add the events to Google Calendar or
    generate an ICS file from the data.

    Adding to Google Calendar requires an Internet connection

    ICS files are compatible with almost all Calendar applications (including
    the iOS calendar application, Sunrise etc)

- **Step 2(a):** If you decide on adding your events to your Google Calendar:

    - **Step (i):** Get your `client_secret.json` and save it to the current directory by
                    following the Step 1 from
                    [here](https://developers.google.com/google-apps/calendar/quickstart/python#step_1_turn_on_the_api_name).

    - **Step (ii):** Now, run:

        ```sh
        $ python add_events.py
        ```

    - **MISC:** To delete all the recurring events (It deletes all the events having summary: `Class Of *`):

        ```sh
        $ python del_events.py
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

## License

GPLv3.
