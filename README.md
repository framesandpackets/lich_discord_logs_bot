# Discord Bot for Warcraft Logs Integration

## Overview

This Python script serves as a Discord bot designed to streamline the process of retrieving raid logs from users via [warcraftlogs.com](https://www.warcraftlogs.com/) and storing them in a PostgreSQL database. The bot ensures seamless integration with Discord, creates a PostgreSQL database, and allows users to upload raid logs, which are stored with timestamps for easy retrieval and searchability.

## Features

- **Warcraft Logs Integration:**
  - Fetches raid logs from [warcraftlogs.com](https://www.warcraftlogs.com/) for specified users through async calls.
  
- **PostgreSQL Database Management:**
  - Establishes a connection to a PostgreSQL database.
  - Creates tables to store raid logs, including timestamps for ingestion.

- **Discord Integration:**
  - Listens for user commands on Discord to initiate the log retrieval and storage process.

- **Asynchronous Database Queries:**
  - Uses asynchronous calls to interact with the PostgreSQL database, ensuring efficiency and responsiveness.

- **Timestamped Log Storage:**
  - Logs are stored in the database with corresponding timestamps for easy tracking and organization.

- **Searchable Logs:**
  - Enables users to search logs by date, providing a convenient way to retrieve specific records.


## Screenshot

![Bot Screenshot](https://i.ibb.co/0VnHYyr/bot-screenshot.jpg)


## Requirements

- Python 3.x
- [Discord.py](https://discordpy.readthedocs.io/en/latest/) library
- [Asyncpg](https://magicstack.github.io/asyncpg/) library


