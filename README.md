# telegram_AC_bot
This Telegram bot was made independently by me to log questions for AstroChallenge 2025. It's an imperfect bot. What it does is --> once the script is started, there is an inbuilt logic that allows it to detect questions, and categorize them according to the needs of AstroChallenge and its specific rounds for the Finals. 

## How did I step aside the issue of paying for to launch it forever on a server? 
I realised that QMs will not be continuously posting questions, so it would be very expensive for us as an organization to launch it on a server, and pay for that. Instead, this bot 'logs' messages from the last time that it was started manually by me, and only pushes the relevant ones to the linked Google sheet. 

## The privacy aspect
The common APIs to connect the scope to the script are given inside the script, but the private API key and the email-ids are secret and are unique to each other/each API service that you create on Google Cloud. You can abuse the Telegram token, but you can't do much with it without the private APIs, which for obvious reasons I have not uploaded on this repo. 
 
## Usefulness
This has made life easier for me and all the QMs who are supposed to make questions for the finals. Now they can send in questions, without having to worry about them getting lost in the spam/chat! 