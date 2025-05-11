import requests
import time
import scratchattach as sa
import os
from pypresence import Presence
import os

print("Automating scratch accounts is technically against the TOS. Use at your own risk.")

# config
BOT_USERNAME = "YOUR_BOT_USERNAME"
BOT_PASSWORD = "YOUR_BOT_PASSWORD"
DOWNLOAD_DIR = os.path.join(os.getcwd(), "projects")
MOTD = """Scratch has fallen. Billions must archive."""
CONTACT_USERNAME = "@chuden"
VERSION = "0.1.0" + ".ARCHIVER"
LATEST_VERSION = VERSION # yea i know that this is pointless but i'm too tired to implement the internet check yet,, its cause there arent any new versions out yet.

# state tracking
amount_archived = 0
requests_made = 0



# does download dir exist????
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# DRP setup
discord_client_id = "DISCORD CLIENT ID"  # REPLACE WITH YOUR BOT'S CLIENT ID!!!!!! yeah
rpc = Presence(discord_client_id)
rpc.connect()

# start the bot

def initialize_bot():
    """Log in and set up bot profile"""
    global amount_archived, requests_made
    
    session = sa.login(BOT_USERNAME, BOT_PASSWORD)
    if session.banned:
        print("Your bot's account has been banned! New archival bot is needed... This is probably our fault, We might've made it too spammy.")
        exit()

    user = session.connect_user(session.username)
    user.update()
    
    # set bot to christmas islands in hopes that setting accounts to be christmas islands so in the future its a dogwhistle for bot accounts 
    if user.country != "Christmas Island":
        session.set_country("Christmas Island")
    
    # set bot status in WIWO
    status = f"Running Chudbot V{VERSION}" + (
        "" if VERSION == LATEST_VERSION 
        else f" (update to {LATEST_VERSION} available)"
    )
    user.set_wiwo(status)
    
    # update the bio
    update_bio(user)
    
    return session, user

def update_bio(user):
    """Update the bot's profile bio with current stats"""
    bio = f"""{MOTD}

a bot intended to archive scratch projects in case they ever get deleted or if scratch gets shut down.
based off of a close sourced version of chudbot on github. this is a fork only accessible to me since if 8 billion people spam the scratch servers with downloads they will crash and i dont want that
by @chuden, bot hosted by {CONTACT_USERNAME}

{amount_archived} archived projects this session
"""
    user.set_bio(bio)

def update_discord_presence():
    """Update Discord Rich Presence with current status"""
    rpc.update(
        state=f"Archiving projects: {amount_archived} archived",
        details=f"Chudbot V{VERSION}",
        large_image="chud1.jpeg",
        small_image="chud2.png",
        start=time.time()
    )

def archive_projects(session, user):
    """Main archiving loop"""
    global amount_archived, requests_made

    # scan projects from a range
    # IMPORTANT, this range is a little weird.
    # don't start from where this script starts, otherwise you'll be archiving the same projects as everyone else with the script.
    # start from somewhere, poke about, see how often you archive, update the end of the range to the most recent project, etc.
    for project_id in range(100_000_102, 117_294_5218):
        try:
            time.sleep(10)  # dont get rate limited lol
            requests_made += 1
            
            # does ts exist icl???
            response = requests.get(f'https://api.scratch.mit.edu/projects/{project_id}')
            if response.status_code != 200:
                print(f"Project {project_id} does not exist! Rahhh")
                continue
                
            # get the project details rq
            project = session.connect_project(project_id)

            # Lost scratch media.. More like.. Archive today...
            project.favorite() # favourite incase commenting fails
            print(f"Favorited project: {project.title}")
            print(f"Share date: {project.share_date}")
            project.download(filename=f"{project.title}.sb3", dir=DOWNLOAD_DIR) # HOLY FUCK THE SCRIPT DID THE THING
            amount_archived += 1
            
            # update profile & comment
            update_bio(user)
            user.post_comment(
                f"Archived project {project_id} ({project.title})"
            )
            
            print(f"Successfully archived {project_id}")
            update_discord_presence()  # update da rich presence

        except Exception as e:
            print(f"Error processing {project_id}: {str(e)}")
            
        # update bio every now and then
        if requests_made % 5 == 0:
            update_bio(user)
            update_discord_presence()  # Update Discord presence every 10 requests

if __name__ == "__main__":
    session, user = initialize_bot()
    archive_projects(session, user)
