import discord
import time
import threading
import requests

# Discordbotvariables
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Scriptvariables
Abort = False
max_wait_time = 1800  # How long will the bot wait to send the request in seconds? 1800 = 30 minutes

# request URL
urlServer = "https://www.servercontrolpanel.de:443/SCP/WSEndUser"
urlNotification = "<YourWebhookURL>"

# Payload for Server
payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:end="http://enduser.service.web.vcp.netcup.de/">
   <soapenv:Header/>
   <soapenv:Body>
      <end:stopVServer>
         <loginName>#YourLoginName#</loginName>
         <password>#YourPassword#</password>
         <vserverName>#YourServerName#</vserverName>
      </end:stopVServer>
   </soapenv:Body>
</soapenv:Envelope>"""

# headers for Server
headers = {
    'Content-Type': 'text/xml; charset=utf-8'
}

# print a message when we log in the bot
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(<YourChannelID>)
    #send a message to YourChannel to warn users
    await channel.send('Stopping Server in 30 Minutes, write "abort" to abort.')
    
@client.event
async def on_message(message):
    global Abort  # Use the global variable
    if message.author == client.user:
        return

    # if any message starts with abort
    if message.content.startswith('abort'):
        # writes something in chat
        await message.channel.send('Serverstop aborted, cya!')
        Abort = True
        # Disconnects the Bot if someone says abort
        await client.close()

# Main function
def main():
    global max_wait_time

    # Start a timer
    start_time = time.time()

    #loop
    while True:
        elapsed_time = time.time() - start_time

        if elapsed_time >= max_wait_time:
            print("Maximum wait time exceeded. Starting server and finishing the program.")
            # start server
            response = requests.request("POST", urlServer, headers=headers, data=payload)
            
            #Data for Discordnotification
            data = {
                "content" : "Starting Server. Server response HTTP Code: "+ str(response.status_code),
                "username" : "Lucky's Bot"
                }

            # Send Discord message via Webhook
            result = requests.post(urlNotification, json = data)

            # Errorhandling
            try:
                result.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)
            else:
                print("Discord Payload delivered successfully, code {}.".format(result.status_code))
                        
            # Disconnects the Bot
            client.loop.create_task(client.close())  
            #todo: Disconnect server
            break

        #If someone writes abort and the boolean is set to True, nothing happens and the bot will disconnect, see line 50
        if Abort:
            print("Abort detected, cya")
            break

        time.sleep(1)

if __name__ == "__main__":
    # Create a seperate thread for the bot
    bot_thread = threading.Thread(target=client.run, args=('YourBotToken',))
    bot_thread.start()

    # Start the main function in the main thread
    main()
