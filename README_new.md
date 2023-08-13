<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links-->
<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

</div>

<!-- PROJECT LOGO -->
<br />
<!-- UPDATE -->
<div align="center">
  <a href="https://github.com/metakgp/gyft">
    <img width="140" alt="image" src="https://user-images.githubusercontent.com/86282911/206632284-cb260f57-c612-4ab5-b92b-2172c341ab23.png">
  </a>

  <h3 align="center">GYFT</h3>

  <p align="center">
  <!-- UPDATE -->
    <i>Get Your Freaking Timetable</i>
    <!-- <br /> -->
    <!-- <a href="https://github.com/proffapt/PROJECT_NAME"><strong>Explore the docs »</strong></a> -->
    <!-- <br /> -->
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
  - [Supports](#supports)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Development Notes](#development-notes)
<!-- - [Contact](#contact) -->
<!-- - [Acknowledgements](#acknowledgments) -->
<!-- - [Additional documentation](#additional-documentation) -->

</details>


<!-- ABOUT THE PROJECT -->
## About The Project
<!-- UPDATE -->
<!-- <div align="center">
  <a href="https://github.com/proffapt/PROJECT_NAME">
    <img width="80%" alt="image" src="https://user-images.githubusercontent.com/86282911/206632547-a3b34b47-e7ae-4186-a1e6-ecda7ddb38e6.png">
  </a>
</div> -->

_Gets your timetable from ERP and adds it to your Google Calendar or gives you an ICS file which you can add in any common calendar application._

> **Note** All updates to this repo should reflect, with appropriate refactorisation, in [gyft-serve](https://github.com/metakgp/gyft-serve/)

<p align="right">(<a href="#top">back to top</a>)</p>

<div id="supports"></div>

### Supports:
1. Shells
    * `bash`
    * `fish`
    * `zsh`
2. OS(s)
    * `MacOS`[`BSD` based]
    * any `*nix`[`GNU+Linux` and `Unix`]
    * `Windows`

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To set up a local instance of the application, follow the steps below.

### Prerequisites
<!-- UPDATE -->
The following dependencies are required to be installed for the project to function properly:
* Python 3
* IIT-KGP Student [ERP](https://erp.iitkgp.ac.in) Account

<p align="right">(<a href="#top">back to top</a>)</p>

### Installation

_Now that the environment has been set up and configured to properly compile and run the project, the next step is to install and configure the project locally on your system._
<!-- UPDATE -->
1. Clone the repository
   ```sh
   git clone https://github.com/metakgp/gyft
   ```
2. Change current directory to the project directory
   ```sh
   cd gyft
   ```
3. Install the dependencies
   ```sh
   pip install requirements.txt
   ```
4. Run the script
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

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage
<!-- UPDATE -->
Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space.

<div align="center">
  <a href="https://github.com/proffapt/PROJECT_NAME">
    <img width="80%" alt="image" src="https://user-images.githubusercontent.com/86282911/206632640-40dc440e-5ef3-4893-be48-618f2bd85f37.png">
  </a>
</div>

<p align="right">(<a href="#top">back to top</a>)</p>

## Development Notes 
This project utilizes the [iitkgp-erp-login](https://github.com/proffapt/iitkgp-erp-login-pypi/) package to handle ERP login functionality.

<p align="right">(<a href="#top">back to top</a>)</p>

## Contributing

Please read [CONTRIBUTING.md](https://github.com/metakgp/gyft/blob/master/CONTRIBUTING.md) guide to know more.

### Updates To Be Made Each Sem
The following procedure is to be followed each new semester by the maintainer for updating GYFT to work properly.

- Download the academic calendar for the particular year.
- New semester dates need to be updated in dates.py
- The format for the date-time is `(YYYY, MM, DD, HH, MM)`.
- Raise a pull request once the dates are updated.


<!-- CONTACT -->
<!-- ## Contact -->

<!-- <p> -->
<!-- 📫 Arpit Bhardwaj ( aka proffapt ) - -->
<!-- <a href="https://twitter.com/proffapt">
  <img align="center" alt="proffapt's Twitter " width="22px" src="https://raw.githubusercontent.com/edent/SuperTinyIcons/master/images/svg/twitter.svg" />
</a>
<a href="https://t.me/proffapt">
  <img align="center" alt="proffapt's Telegram" width="22px" src="https://raw.githubusercontent.com/edent/SuperTinyIcons/master/images/svg/telegram.svg" />
</a>
<a href="https://www.linkedin.com/in/proffapt/">
  <img align="center" alt="proffapt's LinkedIn" width="22px" src="https://raw.githubusercontent.com/edent/SuperTinyIcons/master/images/svg/linkedin.svg" />
</a>
<a href="mailto:proffapt@pm.me">
  <img align="center" alt="proffapt's mail" width="22px" src="https://raw.githubusercontent.com/edent/SuperTinyIcons/master/images/svg/mail.svg" />
</a>
<a href="https://cybernity.group">
  <img align="center" alt="proffapt's forum for cybernity" width="22px" src="https://cybernity.group/uploads/default/original/1X/a8338f86bbbedd39701c85d5f32cf3d817c04c27.png" />
</a>
</p>

<p align="right">(<a href="#top">back to top</a>)</p> -->


<!-- ACKNOWLEDGMENTS -->
<!-- ## Acknowledgments

* [Choose an Open Source License](https://choosealicense.com)
* [Img Shields](https://shields.io)
<!-- UPDATE -->
<!-- 
<p align="right">(<a href="#top">back to top</a>)</p> --> -->

<!-- ## Additional documentation

  - [Changelogs](/.github/CHANGELOG.md)
  - [License](/LICENSE.txt)
  - [Security Policy](/.github/SECURITY.md)
  - [Code of Conduct](/.github/CODE_OF_CONDUCT.md)
  - [Contribution Guidelines](/.github/CONTRIBUTING.md)

<p align="right">(<a href="#top">back to top</a>)</p> -->

<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/metakgp/gyft.svg?style=flat
[contributors-url]: https://github.com/metakgp/gyft/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/metakgp/gyft.svg?style=flat
[forks-url]: https://github.com/metakgp/gyft/network/members
[stars-shield]: https://img.shields.io/github/stars/metakgp/gyft.svg?style=flat
[stars-url]: https://github.com/metakgp/gyft/stargazers
[issues-shield]: https://img.shields.io/github/issues/metakgp/gyft.svg?style=flat
[issues-url]: https://github.com/metakgp/gyft/issues
[license-shield]: https://img.shields.io/github/license/metakgp/gyft.svg?style=flat
[license-url]: https://github.com/metakgp/gyft/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/proffapt
