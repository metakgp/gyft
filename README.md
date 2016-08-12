# gyft

Get Your Freaking Timetable

## About

Gets your timetable from ERP and adds it to your **Google Calendar**.
![instructions](https://cloud.githubusercontent.com/assets/9252491/17613570/7af6ae98-607c-11e6-8597-e720c3475c24.gif)

## How to use and flow of the program

- To get your timetable from ERP:
```
  python gyft.py -user <USERNAME> -pwd <PASSWORD>
```
  Answer your security question when prompted.
<br>
  Your timetable will be saved in `data.txt`.
  <br>
  Get your `client_secret.json` and save it to the current directory by following the Step 1 from [here](https://developers.google.com/google-apps/calendar/quickstart/python#step_1_turn_on_the_api_name).

- To add events to your calendar (Needs internet connection):
```
  python add_events.py
```

- To delete all the recurring events (It deletes all the events having summary: `Class Of *`):
```
  python del_events.py
```

## License

GPLv3.
