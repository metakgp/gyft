# Frontend

## Get Your Freaking Timetable

GYFT allows you to download an ICS file from your timetable which can be imported into calendar apps.

### Running locally

First install [nodejs](https://nodejs.org/en/download/package-manager). Then install `pnpm` by running `npm install -g pnpm`. 

Then follow the given steps to launch the frontend:

1. Clone the repository
   ```sh
   git clone https://github.com/metakgp/gyft.git
   ```
2. Install dependencies
   ```sh
   cd gyft/frontend
   pnpm install
   ```
3. Start the server
   ```sh
   pnpm dev
   ```

This setup will launch the frontend. To start backend server also, please follow the instructions [here](https://github.com/metakgp/gyft/blob/main/README.md)