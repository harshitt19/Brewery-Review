# Brewery Review

Welcome to Brewery Review! This is a Flask application where users can review different breweries and their beers.

## Table of Contents
- [About](#about)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## About

Brewery Review is a web application built using Flask, HTML, CSS, and JavaScript. It allows users to create accounts, add reviews for breweries and beers, and explore the reviews submitted by others.

## Features

- User authentication: Users can sign up for accounts and log in securely.
- Brewery and beer reviews: Users can submit reviews for breweries and their beers.
- Rating system: Users can rate breweries and beers based on their experience.
- Search functionality: Users can search for specific breweries or beers.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your machine. You can download it from [python.org](https://www.python.org/).
- pip (Python package installer) installed. It typically comes with Python, but you can install it manually if needed.
- Git installed to clone the repository.

## Installation

1. **Clone the Repository**

   ```sh
   git clone https://github.com/harshitt19/Brewery-Review-.git
   cd Brewery-Review-
2. **Install Dependencies**

   ```sh
   pip install -r requirements.txt

## Running the Application
1. Initialize the Database

Initialize the database and create the necessary tables:

    ```sh
    flask db init
    flask db migrate
    flask db upgrade

2. Run the Flask Application

    ```sh
    flask run

By default, the application will run on http://127.0.0.1:5000/.
