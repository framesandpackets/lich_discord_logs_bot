import discord
import asyncpg
from dotenv import load_dotenv
import os
import random



#### LOADING OF ENVIRONMENT VARIABLE ####
load_dotenv()
postgres_user = os.getenv('POSTGRES_USER')
postgres_pass = os.getenv('POSTGRES_PASS')
postgres_server = os.getenv('POSTGRES_SERVER')
db_name = os.getenv('DB_NAME')
discord_token = os.getenv('DISCORD_TOKEN')
#########################################



#### POSTGRES SERVER LOCATION/LOGIN CREDENTIALS ####
DATABASE_URL = f"postgresql://{postgres_user}:{postgres_pass}@{postgres_server}/{db_name}"
##########################################



# listen and have access to all available events and data
client = discord.Client(intents=discord.Intents.all())


#function to create log_bot table if it doesn't alrady exist in the db
async def create_table():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''CREATE TABLE IF NOT EXISTS log_bot (
    id serial PRIMARY KEY,
    date date,
    time time with time zone,
    link text,
    raid text
    );
''')

#function to format SQL query data.

def format_query(data):
        query_data = {}

        for row in data:
            query_data.update({"id": f"{row['id']}"})
            time = str(row['time'])
            query_data.update({"time": f"{time[0:5]}"})
            query_data.update({"date": f"{row['date']}"})
            query_data.update({"link": f"{row['link']}"})
            query_data.update({"raid": f"{row['raid']}"})

        lich_speaking = ['Behold, mortal, your requested item has been resurrected from the depths of oblivion and now rests in my bony grasp, ready for delivery unto thee.','From the crypts of eternal darkness, I summon forth the coveted relic you seek, its spectral aura now bound to my undead essence, awaiting your presence to claim it.', 'Through the necromantic currents of the afterlife, I have unearthed the artifact you desired, its ethereal glow pulsating with the echoes of the undead, awaiting your command', 'In the necrotic embrace of eternity, your wish resonates; I shall be the harbinger of your request.']

        num = random.randint(0,len(lich_speaking) - 1)

        formatted_message = f"{lich_speaking[num]}\n\nDate: {query_data['date']}\nTime: {query_data['time']}\nLog Link: {query_data['link']}\nRaid: {query_data['raid']} "

        return formatted_message




@client.event
async def on_ready():
    print(f"Logged in with user {client.user}")

    # conn = to_regclass function is used to check if a table exists in the db.
    table_check = "SELECT to_regclass('log_bot');"


    print(f"\nDEBUGGING: CONNECTING TO DATABASE!")
    conn = await asyncpg.connect(DATABASE_URL)
    print(f"\nDEBUGGING: CONNECTED TO DATABASE!")


    print(f"\nDEBUGGING: QUERY DATABASE!")
    result = await conn.fetchrow(table_check)


    if result[0] is not None:
        print("DEBUGGING: 'log_bot' already exists.")
    #calling create_table() to create log_bot table if it already doesn't
    else:
        await create_table()
        print("DEBUGGING: 'log_bot' created")






@client.event
async def on_message(message):


    if '!lich_log upload' in message.content:

        mess = message.content

        print(f"--------{mess}-------")

        print(f"\nDEBUGGING: GETTING LINK TO LOGS!")
        user_input = message.content[len('!lich_log upload'):].strip()
        print(f"\nDEBUGGING: INPUT FORMATED!")


        print(f"\nDEBUGGING: TRYING TO CONNECT TO POSQL SERVER!")
        conn = await asyncpg.connect(DATABASE_URL)
        print(f"\nDEBUGGING: CONNECTED!")


        print(f"\nDEBUGGING: UPDATING DATABASE!")
        rows = await conn.fetch(f"INSERT INTO log_bot (date, time,link,raid) values (NOW()::DATE, CURRENT_TIME, '{user_input}', 'Blackfathom Deeps');")
        print(f"\nDEBUGGING: DATABASE SUCESSFULLY UPDATED!")



    elif '!lich_log latest logs' in message.content:


        print(f"\nDEBUGGING: TRYING TO CONNECT TO POSQL SERVER!")
        conn = await asyncpg.connect(DATABASE_URL)
        print(f"\nDEBUGGING: CONNECTED!")


        print(f"\nDEBUGGING: ATTEMPTING TO QUERY DB!")
        rows = await conn.fetch('SELECT * FROM log_bot WHERE id = (SELECT MAX(id) FROM log_bot);')
        print(f"\nDEBUGGING: SUCESSFULL QUERY!")

        print(f"\nDEBUGGING: formatting db query!")
        formatted_message = format_query(rows)
        print(f"\nDEBUGGING: printing return to user!")
        await message.channel.send(formatted_message)





    elif '!lich_log get ' in message.content:

        print(f"\nDEBUGGING: Formatting user input to get date")
        user_input = message.content[len('!lich_log get'):].strip()

        print(f"\nDEBUGGING: Connecting to DB!")
        conn = await asyncpg.connect(DATABASE_URL)
        print(f"\nDEBUGGING: Connected to DB!")

        print(f"\nDEBUGGING: querying DB for certain date of logs")
        rows = await conn.fetch(f"SELECT * FROM log_bot WHERE date = '{user_input}';")

        print(f"\nDEBUGGING: formatting db query!")
        formatted_message = format_query(rows)

        print(f"\nDEBUGGING: printing return to user!")
        await message.channel.send(formatted_message)

client.run(discord_token)
