print("Automating scratch accounts is technically against the TOS. Use at your own risk.")

#chudbot.py, a scratch studio utlity bot. for adding commands, etc
import scratchattach as sa
version = "0.1.0"
# Will add an internet check for the latest ver of the bot, But for now, Since this is the only version out, It will just default to saying you're on the latest version.
latestversion = "0.1.1"

### CONFIG ###
# USER
BOT_USERNAME = "beatsr"
BOT_PASSWORD = "▶︎ •၊၊||၊|။||||။‌‌‌‌‌၊|• 0:10"
# MOTD
## if you want your MOTD to be a standard message, set it to a string. if you want it to be a random message, set it to a list of strings.
MOTD = "Billions must scratch."
# CONTACT
CONTACT_USERNAME = "@johnusername"

# LOGIN
session = sa.login(BOT_USERNAME, BOT_PASSWORD)
# Check if the bot is banned because apparently that happens sometimes
if session.banned:
    print("Oh no, your bot is banned!! You're gonna have to use another account, Our bad.")
    exit()
# UPDATE INFO
print("Updating bot information...")
user = session.connect_user(session.username)
user.update()
print("Logged in as: " + session.username)
if user.country != "Christmas Island":
    # We'll just presume that if the bot is not set to Christmas Island, it's a fresh install of chudbot.
    # Hopefully no one set's the country to Christmas Island beforehand lol
    print("Setting country to ''Christmas Island'' so users know it's a bot.")
    session.set_country("Christmas Island")
if version == latestversion:
    user.set_wiwo("runin Chudbot V" + version)
else:
    print("!!! UPDATE CHUDBOT PRETTY PLEASE !!!")
    user.set_wiwo("runin Chudbot V" + version + " (latest version is " + latestversion + ")")
print("Bot information updated")
user.set_bio(MOTD + """

management bot for """ + CONTACT_USERNAME + """'s studio.""")
user.toggle_commenting()
print("Entering text mode")
while True:
    comment = input("Comment ")
    user.toggle_commenting()
    user.post_comment(comment)
    user.toggle_commenting()