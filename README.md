<div id="top"></div>

<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![Wiki][wiki-shield]][wiki-url]

</div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <!-- <a href="https://github.com/metakgp/gyft">
    <img width="140" alt="image" src="https://user-images.githubusercontent.com/86282911/206632284-cb260f57-c612-4ab5-b92b-2172c341ab23.png">
  </a> -->

  <h1 align="center">GYFT</h1>

  <p align="center">
    <i>Get Your Freaking Timetable</i>
    <br />
    <a href="https://github.com/metakgp/gyft/issues">Report Bug</a>
    ·
    <a href="https://github.com/metakgp/gyft/issues">Request Feature</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
<summary>Table of Contents</summary>

- [About The Project](#about-the-project)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Development Notes](#development-notes)
- [Contributing](#contributing)
- [Maintainer(s)](#maintainers)

</details>


<!-- ABOUT THE PROJECT -->
## About The Project

Gets your timetable from ERP and adds it to your Google Calendar or gives you an ICS file which you can add in any common calendar application.

> **Note** All updates to this repo should reflect, with appropriate refactorisation, in [gyft-serve](https://github.com/metakgp/gyft-serve/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To set up a local instance of the application, follow the steps below.

### Prerequisites
The following prerequisites are required to be installed for the project to function properly:
* Python 3
* IIT-KGP Student [ERP](https://erp.iitkgp.ac.in) Account

<p align="right">(<a href="#top">back to top</a>)</p>

### Installation

_Now that the environment has been set up and configured to properly compile and run the project, the next step is to install and configure the project locally on your system._
1. Clone the repository
   ```sh
   git clone --depth 1 https://github.com/metakgp/gyft
   ```
2. Change current directory to the project directory
   ```sh
   cd gyft
   ```
3. Install the dependencies
   ```sh
   pip install requirements.txt
   ```

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

1. Run the script
   ```sh
   python3 gyft.py
   ```
2. Enter your roll number, password, security answer and OTP (if required) when prompted
3. Now you can choose between 2 options, which will be prompted to you:
   - #### Add to Google Calendar:
     - For this, you have to get your `credentials.json` and save it as `client_secret.json` to the current directory by following the Step 1 from [here](https://developers.google.com/google-apps/calendar/quickstart/python#step_1_turn_on_the_api_name)
     - Also note that adding to Google Calendar requires an Internet connection
  
   - #### Generate ICS file:
     - This will generate an ICS file which you can import into any calendar application.
     - For importing to Google Calendar, follow the instructions given [here](https://support.google.com/calendar/answer/37118?hl=en).

<br />

- Optional flags: 
  - To delete all the recurring events added by the CLI or GYFT Web Application (uses property of recurrence to identify events to delete), you can run `gyft.py` with the `--del-events` flag:
    ```sh
    python3 gyft.py --del-events
    ```
  - To specifiy the output file (`.ics`) to which the ICS file will be written, use the `--output` flag.
    ```sh
    python3 gyft.py --output autumn_2023.ics
    ```

<p align="right">(<a href="#top">back to top</a>)</p>

## Development Notes 
This project utilizes the [iitkgp-erp-login](https://github.com/proffapt/iitkgp-erp-login-pypi/) package to handle ERP login functionality.

### Updates To Be Made Each Sem
The following procedure is to be followed each new semester by the maintainer for updating GYFT to work properly.

- Download the academic calendar for the particular year.
- New semester dates need to be updated in utils/dates.py
- The format for the date-time is `(YYYY, MM, DD, HH, MM)`.
- Raise a pull request once the dates are updated.

<p align="right">(<a href="#top">back to top</a>)</p>

## Contributing

Please read [CONTRIBUTING.md](https://github.com/metakgp/gyft/blob/master/CONTRIBUTING.md) guide to know more.

## Maintainer(s)

- [Ashwin Prasanth](https://github.com/ashwinpra)

<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/metakgp/gyft.svg?style=for-the-badge
[contributors-url]: https://github.com/metakgp/gyft/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/metakgp/gyft.svg?style=for-the-badge
[forks-url]: https://github.com/metakgp/gyft/network/members
[stars-shield]: https://img.shields.io/github/stars/metakgp/gyft.svg?style=for-the-badge
[stars-url]: https://github.com/metakgp/gyft/stargazers
[issues-shield]: https://img.shields.io/github/issues/metakgp/gyft.svg?style=for-the-badge
[issues-url]: https://github.com/metakgp/gyft/issues
[license-shield]: https://img.shields.io/github/license/metakgp/gyft.svg?style=for-the-badge
[license-url]: https://github.com/metakgp/gyft/blob/master/LICENSE.txt
[wiki-shield]: https://custom-icon-badges.demolab.com/badge/metakgp_wiki-grey?logo=metakgp_logo&logoColor=white&style=for-the-badge
[wiki-url]: https://wiki.metakgp.org
