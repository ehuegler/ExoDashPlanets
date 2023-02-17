# ExoDashPlanets

A dashboard for looking at exoplanet stuff from NASA's huge database.

The dashboard itself can be found at [exo-dash-planets.vercel.app](https://exo-dash-planets-0.vercel.app).

## Architecture
```mermaid
flowchart LR
    A[Client] -- Web Request --> B[Flask Server]
    B -- Web Response --> A
    B -- Data Query --> C[Database]
    C -- Query Response --> B
    D[Other server or python script or whatever \n that does the data scrapping and wrangling ] --> C
    %%{init: {'theme':'neutral'}}%%
 ```


## Development and Running Locally

### Git Workflow
The web app is hosted as a Vercel project. [Vercel](https://vercel.com/) is a cloud hosting platform that handles the web server side of things for us. It is set to track the `main` branch, so any commits to `main` will update the web app in production. Hence it is generally a bad idea to push commits to main directly. The primary branch for development use is `dev`. Ideally we should only commit to `main` by merging `dev` into it through a pull request.

### Python Virtual Environment

This project is setup to use a python virtual environment. 
To setup a virtual environment, navigate to the root of this project in your terminal, and run the command
```
python3 -m venv venv
```
This will create a `venv/` folder in the project directory which will store the correct versions of all the packages used in this project (`venv` is already ignored by `.gitignore`). 
You will only need to run this command once, on your initial setup.

Once you have created a virtual environment, you need to activate it with
```
. venv/bin/activate
```
You must activate the virtual environment every time you work on the project.

The next step is to install the projects dependencies. All of the required packages to run this project are stored in `requirements.txt` with the necessary version numbers.
To install all required dependancies, use the command
```
pip install -r requirements
```

To add a new package to the project, add a new line to `requirements.txt` with the package name and version number. Then run `pip install -r requirements` again. You will need to run that command every time deppendencies are changed or added.

### Running the Flask App Locally
You can run the web app locally to see changes to the dashboard as you make them.

From the root of the project with the virtual environment active and requirements installed, run
```
flask run
```
