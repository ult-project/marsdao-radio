#!/usr/local/bin/liquidsoap
# Liquid Soap 2.1.4

# Configuration
%include "radio.conf"

# Standard settings
log.file.set(true)
log.file.path.set("/radio/logs/liquidsoap.log")
log.level.set(4)
settings.server.telnet.set(true)
settings.server.telnet.bind_addr.set("0.0.0.0")
settings.harbor.bind_addrs.set(["0.0.0.0"])

# Endpoint playlists
playlist_live = playlist(mode = "randomize", reload = 600, reload_mode = "live", playlist_live_path)
playlist_rock = playlist(mode = "randomize", reload = 600, reload_mode = "live", playlist_rock_path)

# Crossfade for the tracks
playlist_live = crossfade(smart = true, fade_in = 2.00, fade_out = 2.00, playlist_live)
playlist_rock = crossfade(smart = true, fade_in = 2.00, fade_out = 2.00, playlist_rock)

# OnAir endpoint input settings (allows to intercept the live stream)
onair_input = input.harbor(
  "live",
  port                 = onair_port,
  user                 = onair_user,
  password             = onair_password,
  icy                  = true,
  icy_metadata_charset = "UTF-8",
  metadata_charset     = "UTF-8",
  buffer               = 5.00,
  max                  = 10.00
)

# Make the output for the live stream
live_output = fallback(replay_metadata = true, track_sensitive = false, [onair_input, playlist_live])

# Live endpoint output settings
live = output.icecast(
  %mp3(bitrate = 192, id3v2 = true),
  host         = icecast_host,
  port         = icecast_port,
  mount        = "live",
  user         = icecast_user,
  password     = icecast_password,
  name         = icecast_name,
  description  = icecast_description,
  genre        = "Music",
  url          = icecast_url,
  encoding     = "UTF-8",
  icy_metadata = "true",
  fallible     = true,
  live_output
)

# Rock endpoint output settings
rock = output.icecast(
  %mp3(bitrate = 192, id3v2 = true),
  host         = icecast_host,
  port         = icecast_port,
  mount        = "rock",
  user         = icecast_user,
  password     = icecast_password,
  name         = icecast_name,
  description  = icecast_description,
  genre        = "Rock",
  url          = icecast_url,
  encoding     = "UTF-8",
  icy_metadata = "true",
  fallible     = true,
  playlist_rock
)
