# Tokyo GitHub Follower Scraper
This project utilizes the GitHub API to gather data on GitHub users located in Tokyo with more than 200 followers. Additionally, it collects data on the repositories associated with each of these users.

## Project Description

The primary goals of this project are to:
1. Identify all GitHub users based in Tokyo who have over 200 followers.
2. Retrieve and compile a list of repositories for each of these users.

The data collected can be useful for analysis of popular GitHub profiles in Tokyo, including insights on their repositories.

## Repository Structure

- **Bhavika.ipynb**: Jupyter notebook used for testing, developing, and visualizing the data scraping process.
- **data_Scraper.py**: The main Python script that connects to the GitHub API, performs the search for users and repositories, and saves the data.
- **users.csv**: Contains details on each user with over 200 followers, such as username, follower count, and location.
- **repositories.csv**: Stores information about the repositories of the identified users, including repo names, stars, forks, and other relevant metadata.
