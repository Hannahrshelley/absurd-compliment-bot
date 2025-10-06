# Absurd Compliments Bot

A Bluesky bot that generates wonderfully weird compliments using random word combinations.

🤖 **Live bot:** [@absurdcompliments.bsky.social](https://bsky.app/profile/absurdcompliments.bsky.social)

## What it does

- Monitors mentions and replies with randomly generated absurd compliments
- Posts one daily compliment at 19:00 UTC (6 AM AEDT)
- Tracks replied mentions to avoid double-posting
- Catches up on missed mentions when restarted
- Uses proper grammar (a/an) based on adjective

## Example compliments

- "You sparkle like a cosmic potato"
- "You're the magnificent velociraptor of absolutely crushing it"
- "Your stellar empathy could convince shadows to unionize"
- "You exist in 4D like an ethereal capybara"
- "Your sense of wonder could teach philosophy to plants"

## How it works

The bot generates compliments using three templates:

1. **Action format:** "You [verb] like a/an [adjective] [noun]"
2. **Identity format:** "You're the [adjective] [noun] of [category]"
3. **Capability format:** "Your [adjective] [trait] could [absurd achievement]"
