# Netcup-Server-Scheduler
A Script to start or stop a vServer hotsted Netcup - interurptable via Discord. 

Netcup allows to schedule server stats and shutdowns via SOAP.
To save on money we can schedule this script on a server or Lambda to shutdown or start the server during a time of our choosing.
E.g. you have a gameserver you want to shut down during 00:00 - 12:00 ? Run a scheduled task and the script will give a 30 minute warning on a discord channel of your chosing.
If any User writes "abort" the start / shutdown will be stopped. Handy if youre gaming late at night and you forgot the server will shut down.


Change following variables:

YourWebhookURL = your Webhook for the Discord channel you want the 30 minute warning to be sent to 
YourLoginName = your netcup login id (customer id)
YourPassword = your webservice password (has to be activated seperately !NOT YOUR LOGIN PASSWORD FOR NETCUP!)
YourServerName = the vSever ID 
YourChannelID = the channel the bot will confirm the shutdown to
YourBotToken = your Token ID to your Discord bot that will read messages in your server of chosing

<end:stopVServer> or <end:startVServer> in payload = to stop or start the vServer
