## Blitzcrank Bot

Blitzcrank Bot is a Discord bot in its second iteration that retrieves useful information about League of Legends players.

Invite link: **Still in production :)**

### Commands

Command | Usage | Description
--------|-------|------------
b!search|b!search Riviere| Retrieves ranked statistics for a given user
b!mastery|b!mastery Riviere Sivir| Retrieves champion mastery information for a given user
b!region view||Retrieves a server's default region
b!region set|b!region set OCE|Sets a server's default region
b!region update|b!region update OCE|Updates a server's default region
b!region remove||Removes a server's default region
b!region list||Lists all valid regions
b!invite||Retrieves Blitzcrank Bot's invite link
b!support||Retreives link to Blitzcrank Bot's support server

## Future Commands

Command | Usage | Description
--------|-------|------------
b!top|b!top Sivir|Retrieves the top 10 users on the server by mastery points
b!ingame|b!game Riviere|Retrieves information about the user's current game

## FAQ

### What are the region commands?
The region commands (b!region set, etc) are part of Blitzcrank Bot's ability to set a default region per server. This means that you don't have to add the region as an argument to every command!

### But what if my account is on a different region to the default?
You can specify which region Blitzcrank Bot should use at the end of the usual command! For example, if the default region of your server was NA, but your account was on EUW, you can use `b!search [User] EUW`.

## Troubleshooting
**99% of issues with the bot can be solved by enclosing Summoner and Champion names in quotation marks (i.e "Lee Sin")**
### The bot tells me some part of my name isn't a valid region
Unfortunately, if your Summoner name contains a space (i.e Super Frosty), you must enclose the name in quotation marks like so: "Super Frosty".

### "[Champion] is not a valid region!"
Same as above, either your summoner name has a space, the champion name has a space, or both. They need to be in quotation marks if this is the case.

### The bot doesn't respond at all!
This happens when your name has a space _and_ you specified a region, or _both_ your summoner name and champion name have a space. See above, enclose name in quotation marks.

### The bot complains about permissions!
Blitzcrank Bot needs the 'embed links' permission, either at the role or channel level, since it sends messages using rich embeds.

### "Something unexpected went wrong!"
I've done my best to catch all exceptions and display proper error messages, but some slip through. This is that message. Join the support server or dm me with details and I'll try to help.

## Enquiries
Questions, enquiries, etc. can be directed towards Frosty ☃#5263 on Discord or, by email: apal0934@uni.sydney.edu.au
