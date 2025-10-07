import os
import random
import time
import json
from atproto import Client, models
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()

# Configuration
BLUESKY_HANDLE = "absurdcompliments.bsky.social"
BLUESKY_PASSWORD = os.environ.get("BLUESKY_PASSWORD")
DAILY_COMPLIMENT_HOUR = 19  # Post daily compliment at 7 PM UTC (6 AM AEDT)
SEEN_FILE = "seen_notifications.json"  # File to track replied notifications
DAILY_POST_FILE = "last_daily_post.json"  # File to track last daily post date

# Word lists for generative compliments
VERBS = [
    "sparkle", "shine", "glow", "shimmer", "resonate",
    "beam", "sizzle", "create joy", "give hope", "lift people up",
    "exist", "function", "operate", "think", "transcend",
    "bloom", "dance", "charm the universe", 
    "illuminate", "flourish", "soar", "thrive", "elevate", "inspire",  
     "captivate", "swagger",
    "show empathy", "collaborate", "dominate", "crush", "exist in 4D", 
    "conquer", "serve face", "slay", "matter", "ignore physics", "change outcomes just by existing", "make impossible things happen", "turn thoughts into reality", "manifest dreams accidentally", "spontaneously generate hope", "produce joy", "radiate possibilities", "emit potential", "leak creativity", "ooze inspiration", "secrete wisdom", "exude competence", "project confidence accidentally", "befriend abstract ideas"
]

ADJECTIVES = [
    "powerful", "magnificent", "determined", "optimistic", "philosophical",
    "enthusiastic", "distinguished", "profound", "whimsical", "strategic",
    "mysterious", "confident", "serene", "harmonious", "legendary", "acclaimed",
    "underrated", "experimental", "radiant", "graceful", "brilliant", "majestic",
    "cosmic", "stellar", "luminous", "ethereal", "splendid", "glorious",
    "transcendent", "sublime", "exquisite", "vibrant", "dazzling", "resplendent",
    "impeccable", "illustrious", "exceptional", "formidable", "triumphant",
    "spectacular", "phenomenal", "extraordinary", "marvelous", "wondrous",
    "stupendous", "noble", "incredible", "remarkable", "astounding",
    "delightful", "enchanting", "captivating", "mesmerizing", "gentle",
    "compassionate", "thoughtful", "wise", "creative", "innovative", "resilient",
    "courageous", "authentic", "sincere", "generous", "kind", "empathetic",
    "inspiring", "uplifting", "magical", "dreamy", "peaceful", "joyful",
    "warm", "cozy", "soothing", "refreshing", "invigorating", "sparkling",
    "shimmering", "gleaming", "prismatic", "iridescent", "crystalline", "celestial",
    "golden", "silver", "pearl", "opalescent", "velvet", "silk",
    "melodic", "rhythmic", "symphonic", "poetic", "lyrical", "blooming", "blossoming", "thriving",
    "unstoppable", "fierce", "turbocharged", "hypersonic", "industrial-grade",
    "super cool", "absolutely buckwild", "totally rad"
]

NOUNS = [
    "lighthouse", "chandelier", "potato", "saxophone", "cheese", "umbrella",
    "toaster", "philosopher", "cactus", "theorem", "symphony",
    "baguette", "velociraptor", "spreadsheet", "constellation", "lasagna",
    "pyramid", "mushroom", "paperclip", "avalanche", "sonnet",
    "accordion", "mineral", "comet", "waffle", "fjord", "nebula", "glacier",
    "manuscript", "turbine", "compass", "kaleidoscope",
    "campfire", "fountain", "mosaic", "lantern", "garden", "sunset",
    "treehouse", "crystal", "vinyl record", "telescope", "windmill", "coffee mug",
    "blanket", "carousel", "harmonica", "pottery", "pillow fort", "waterfall",
    "hammock", "quilt", "honeycomb", "terrarium", "music box", "snow globe",
    "cake", "puzzle", "hot air balloon", "candle", "butterfly", "lullaby", "cryptid", "menace", "legend", "icon", "wizard", "oracle", "sage", "champion", "hero", "warrior", "knight", "dragon", "phoenix", "unicorn", "pegasus", "griffin", "sphinx", "kraken", "leviathan", "titan", "colossus", "behemoth", "chimera", "hydra", "mongoose", "capybara", "otter", "raccoon", "crow", "raven", "owl", "hawk", "falcon", "eagle", "wolf", "fox", "bear", "lion", "tiger", "panther", "leopard", "jaguar", "lynx", "bobcat", "cheetah", "puma", "octopus", "jellyfish", "mantis shrimp", "axolotl", "tardigrade", "platypus", "narwhal", "dolphin", "whale", "shark", "seal", "walrus", "penguin", "flamingo", "peacock", "swan", "hummingbird", "kingfisher", "tortoise", "gecko", "chameleon", "iguana", "komodo dragon", "crocodile", "alligator", "salamander", "newt", "frog", "toad", "bee", "butterfly", "moth", "dragonfly", "firefly", "ladybug", "beetle", "ant", "termite", "spider", "scorpion", "crab", "lobster", "shrimp", "squid", "cuttlefish", "nautilus", "snail", "slug", "worm", "caterpillar", "chrysalis", "cocoon", "puppy", "kitten", "bunny", "duckling", "cup of tea", "Saturday morning cartoon"
]

CATEGORIES = [
    "the galaxy", "gettin' it done", "being alive", "existing beautifully",
    "making things happen", "the universe", "personal growth", "vibing",
    "absolutely crushing it", "reality", "consciousness", "the cosmos",
    "human achievement", "living your truth", "the food chain", "evolution",
    "making an impact", "the animal kingdom", "creative expression",
    "problem solving", "social situations", "keeping it together",
    "emotional intelligence", "the whole vibe", "succeeding at life",
    "meaningful connections", "quiet moments", "big dreams", "small joys",
    "rainy afternoons", "sunrise energy", "late night thoughts",
    "adventure", "friendship", "hope", "wonder", "peace",
    "gentle chaos", "organized fun", "cozy season", "fresh starts",
    "second chances", "self-discovery", "healing",
    "beautiful mistakes", "life lessons", "happy accidents",
    "absolute chaos", "professional mischief", "necessary chaos", "keeping it real"
]

BODY_PARTS_TRAITS = [
    "elbows", "aura", "sense of timing", "bone structure", "neural pathways",
    "pinky finger", "posture", "metabolic efficiency", "spatial awareness",
    "eyebrows", "voice", "shadow", "wavelength", "essence",
    "vibes", "energy signature", "presence", "stride", "handwriting",
    "laugh", "conscience", "instincts", "decision-making process", "temporal flux",
    "inner monologue", "dreams", "capacity for joy", "sense of wonder",
    "ability to hope", "right elbow", "thoughtfulness", "creativity",
    "kindness", "resilience", "authenticity", "empathy",
    "curiosity", "patience", "courage", "integrity", "spontaneity",
    "wisdom", "imagination", "intuition", "spirit", "heart", "soul",
    "smile", "energy", "perspective", "outlook", "approach to life",
    "resting face", "sense of humour",
    "energy", "unfiltered thoughts", "spite reserves", "audacity", "willpower", "determination", "unique skills"
]

ABSURD_ACHIEVEMENTS = [
    "negotiate peace treaties", "confuse a calendar", "win an argument with a mirror",
    "make bread nervous", "intimidate a mountain", "teach philosophy to plants",
    "reorganize the solar system", "convince ghosts to be productive",
    "mediate disputes between colors", "inspire profound thoughts in furniture",
    "solve equations that don't exist yet", "make time feel self-conscious",
    "persuade clouds to form better shapes", "run a successful campaign for mayor of the ocean",
    "write a bestseller in a language nobody speaks", "make mathematics question itself",
    "convince the moon to change its schedule", "win a debate against a very confident rock",
    "teach fish about aerodynamics", "make parallel lines meet out of respect",
    "convince shadows to unionize", "negotiate with forgotten Tuesdays",
     "teach patience to lightning",
    "convince gravity to take a day off", "make soup feel seen", "help clocks understand infinity",
    "teach mountains about humility", "make silence feel heard", "convince rainbows to be bolder",
    "mediate between sunrise and sunset", "teach clouds about retirement planning",
    "convince stars to shine a little brighter", "help the wind find its purpose",
    "make thunder feel understood", "teach rivers about going with the flow",
    "convince the ocean to share its secrets", "help trees understand their own wisdom",
    "make butterflies feel accomplished", "teach snow about letting go",
    "convince rain to dance more freely", "help flowers understand their own beauty",
    "make bees feel appreciated for their work", 
    "help sunsets feel proud of themselves",
    "make dewdrops feel significant", "convince spring to take its time", "help winter understand warmth",
    "make summer nights last longer", "teach comets about commitment",
    "intimidate the sun into setting earlier", "bully physics into submission",
    "gaslight reality into doubting itself", "convince the void to reconsider",
    "strong-arm fate into giving you a better deal", "threaten the concept of time",
    "absolutely devastate the space-time continuum", "dropkick existential dread into the sun",
    "wrestle probability into giving better odds", 
    "powerbomb insecurity through a table"
]

def load_seen_notifications():
    """Load the set of notifications we've already replied to."""
    try:
        if os.path.exists(SEEN_FILE):
            with open(SEEN_FILE, 'r') as f:
                return set(json.load(f))
    except Exception as e:
        print(f"Error loading seen notifications: {e}")
    return set()

def save_seen_notifications(seen_notifications):
    """Save the set of notifications we've replied to."""
    try:
        with open(SEEN_FILE, 'w') as f:
            json.dump(list(seen_notifications), f)
    except Exception as e:
        print(f"Error saving seen notifications: {e}")

def load_last_posted_date():
    """Load the date when we last posted a daily compliment."""
    try:
        if os.path.exists(DAILY_POST_FILE):
            with open(DAILY_POST_FILE, 'r') as f:
                date_str = json.load(f)
                return datetime.fromisoformat(date_str).date()
    except Exception as e:
        print(f"Error loading last posted date: {e}")
    return None

def save_last_posted_date(posted_date):
    """Save the date when we posted a daily compliment."""
    try:
        with open(DAILY_POST_FILE, 'w') as f:
            json.dump(posted_date.isoformat(), f)
    except Exception as e:
        print(f"Error saving last posted date: {e}")

def generate_compliment():
    """Generate a random absurd compliment using one of three formats."""
    format_choice = random.randint(1, 3)
    
    if format_choice == 1:
        # Action format: "You [verb] like [a/an] [adjective] [noun]"
        verb = random.choice(VERBS)
        adjective = random.choice(ADJECTIVES)
        noun = random.choice(NOUNS)
        
        # Use "an" if adjective starts with a vowel sound
        article = "an" if adjective[0].lower() in ['a', 'e', 'i', 'o', 'u'] else "a"
        
        return f"You {verb} like {article} {adjective} {noun}"
    
    elif format_choice == 2:
        # Identity format: "You're the [adjective] [noun] of [category]"
        adjective = random.choice(ADJECTIVES)
        noun = random.choice(NOUNS)
        category = random.choice(CATEGORIES)
        return f"You're the {adjective} {noun} of {category}"
    
    else:
        # Capability format: "Your [adjective] [body part/trait] could [absurd achievement]"
        adjective = random.choice(ADJECTIVES)
        trait = random.choice(BODY_PARTS_TRAITS)
        achievement = random.choice(ABSURD_ACHIEVEMENTS)
        return f"Your {adjective} {trait} could {achievement}"

def check_for_mentions(client, seen_notifications):
    """Check for new mentions and reply with compliments."""
    try:
        # Get notifications
        notifications = client.app.bsky.notification.list_notifications(params={'limit': 50})
        
        replied_to = []
        
        for notification in notifications.notifications:
            # Skip if we've already replied to this notification
            notification_uri = notification.uri
            if notification_uri in seen_notifications:
                continue
            
            # Process both mentions and quote posts that mention the bot
            is_mention = notification.reason == "mention"
            is_quote_with_mention = (
                notification.reason == "quote" and 
                hasattr(notification.record, 'text') and 
                BLUESKY_HANDLE in notification.record.text
            )
            
            if is_mention or is_quote_with_mention:
                # Don't reply to our own posts
                if notification.author.handle == BLUESKY_HANDLE:
                    continue
                    
                # Generate a compliment
                compliment = generate_compliment()
                
                # Create reply reference with proper threading
                # Check if the mention is itself a reply to preserve thread structure
                if hasattr(notification.record, 'reply') and notification.record.reply:
                    root = notification.record.reply.root
                else:
                    root = models.create_strong_ref(notification)
                
                reply_ref = models.AppBskyFeedPost.ReplyRef(
                    parent=models.create_strong_ref(notification),
                    root=root
                )
                
                # Post the reply
                client.send_post(
                    text=compliment,
                    reply_to=reply_ref
                )
                
                print(f"[{datetime.now()}] Replied to @{notification.author.handle} with: {compliment}")
                replied_to.append(notification.author.handle)
                seen_notifications.add(notification_uri)
                
                # Be nice to the API - small delay between replies
                time.sleep(2)
        
        if replied_to:
            print(f"Replied to {len(replied_to)} mention(s)")
            # Save after replying to preserve state
            save_seen_notifications(seen_notifications)
            
    except Exception as e:
        print(f"Error checking mentions: {e}")

def post_daily_compliment(client, last_posted_date):
    """Post a daily compliment if it's time."""
    try:
        now = datetime.now(timezone.utc)
        current_date = now.date()
        current_hour = now.hour
        
        # Check if we should post (right hour and haven't posted today)
        if current_hour == DAILY_COMPLIMENT_HOUR and current_date != last_posted_date:
            compliment = generate_compliment()
            
            # Post the daily compliment
            client.send_post(
                text=compliment
            )
            
            print(f"[{datetime.now()}] Posted daily compliment: {compliment}")
            save_last_posted_date(current_date)
            return current_date
        
        return last_posted_date
            
    except Exception as e:
        print(f"Error posting daily compliment: {e}")
        return last_posted_date

def main():
    """Main bot loop."""
    # Check for password
    if not BLUESKY_PASSWORD:
        print("Error: BLUESKY_PASSWORD environment variable not set!")
        print("Set it with: export BLUESKY_PASSWORD='your_password'")
        return
    
    # Login to Bluesky
    print(f"Logging in as {BLUESKY_HANDLE}...")
    client = Client()
    
    try:
        client.login(BLUESKY_HANDLE, BLUESKY_PASSWORD)
        print("Successfully logged in!")
    except Exception as e:
        print(f"Failed to login: {e}")
        return
    
    # Show some example compliments
    print("\nExample compliments this bot will generate:")
    for _ in range(5):
        print(f"  - {generate_compliment()}")
    print()
    
    # Load previously seen notifications
    seen_notifications = load_seen_notifications()
    print(f"Loaded {len(seen_notifications)} previously seen notifications")
    
    # Load last posted date
    last_posted_date = load_last_posted_date()
    if last_posted_date:
        print(f"Last daily compliment was posted on {last_posted_date}")
    else:
        print("No previous daily compliment found - will post at next opportunity")
    
    print("Bot is now running. Press Ctrl+C to stop.")
    print(f"Checking for mentions every 30 seconds...")
    print(f"Daily compliment will post at {DAILY_COMPLIMENT_HOUR}:00 UTC")
    
    # Main loop
    try:
        while True:
            check_for_mentions(client, seen_notifications)
            last_posted_date = post_daily_compliment(client, last_posted_date)
            time.sleep(30)  # Check every 30 seconds
            
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
