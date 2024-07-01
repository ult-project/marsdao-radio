# Introduction
[![MarsDAO Radio](https://img.shields.io/badge/MarsDAO-Radio-blue.svg)](https://radio.daomars.net)
[![GitHub release](https://img.shields.io/badge/release-v1.3.0-blue.svg)](https://github.com/profinch/telegram-bot-icecast-radio/releases/tag/v1.3.0)

Telegram bot designed to interact with an Icecast2 server to stream the live mount endpoint to the Telegram group live
video chat and manage the radio station infrastructure.

[update] We found some issues with logs - fixing...

# Features
Streaming from the Icecast2 server **live** mount endpoint to the Telegram live video chat.

# Commands
`/start` - start the Telegram bot

`/play` - start radio stream in Telegram live video chat

`/stop` - stop radio stream in Telegram live video chat

`/restart` - restart radio stream in Telegram live video chat

`/status` - radio stream status in Telegram live video chat

`/scheduler` - show current week events from the Google Calendar

`/song` - get the name of current track in the stream

`/report` - send a message to the support team

`/help` - show the help page


# Configurations
### Telegram bot
- `TELEGRAM_TOKEN` - Telegram bot API token ([how to create](https://core.telegram.org/bots/tutorial))
- `TELEGRAM_VOICE_CHAT_LINK` - Telegram real-time messaging protocol server URL (Settings => Server URL)
- `TELEGRAM_VOICE_CHAT_KEY` - particular Telegram live video chat key (Settings => Stream Key)
- `STREAM_URL` - Icecast2 server mount endpoint URL
- `STREAM_STATUS` - Icecast2 server mount endpoint JSON file with the stream parameters  
- `GOOGLE_CALENDAR_ID` - Google Calendar ID (Calendar settings => Integrate calendar => Calendar ID)
- `ADMINS` - space-separated list of Telegram user IDs with administrator permissions
- `SUPPORT` - space-separated list of Telegram user IDs who receive report messages

    ℹ️ Telegram user [@profinch](https://t.me/profinch) automatically added to `ADMINS` and `SUPPORT` lists.  

### Google Calendar credentials
1. Configure [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent).

2. Create OAuth 2.0 Client ID [credentials](https://console.cloud.google.com/apis/credentials)
      (Create credentials => OAuth Client ID).
   
      **Application type**: Web application

      **Name**: Google Calendar

      **Authorized redirect URIs**: https://developers.google.com/oauthplayground

      ℹ️ Download JSON file with credentials.
   
3. Make sure there is no [third-party connection](https://myaccount.google.com/connections?filters=3,4&hl=en)
      in your Google managed account for the calendar.
   
      Open the developers OAuth 2.0 playground.

      **Step 1. Select & authorize APIs** - select Google Calendar API v3 (https://www.googleapis.com/auth/calendar) service. 

      Click on the gear (OAuth 2.0 Configuration) => enable checkbox "Use your own OAuth credentials"

      Add your **OAuth Client ID** and **OAuth Client** secret credentials

      Click "Authorize APIs" button and allow connection.
   
      **Step 2. Exchange authorization code for tokens** - click "Exchange authorization code for tokens" button and get
      **Refresh token** value.

5. Rename **google_calendar.json.dist** file to **google_calendar.json** and update with secrets.

You can read the full article (russian) related to setting up the **Google Calendar credentials** in my blog:
https://profinch.ru/google-cloud-platform/google-calendar-api-oauth
