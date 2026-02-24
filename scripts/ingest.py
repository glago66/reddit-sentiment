import praw
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

# Connect to Reddit API
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# Subreddits to pull from
SUBREDDITS = [
    "WeAreTheMusicMakers",
    "makinghiphop",
    "edmproduction",
    "Music",
    "soundcloud"
]

# Keywords to search for
KEYWORDS = [
    "soundcloud",
    "streaming platform",
    "music distribution",
    "artist payout",
    "playlist",
    "music upload"
]

def scrape_subreddit(subreddit_name, limit=100):
    """Pull top posts and comments from a subreddit."""
    print(f"Scraping r/{subreddit_name}...")
    posts = []

    subreddit = reddit.subreddit(subreddit_name)

    for post in subreddit.hot(limit=limit):
        post_data = {
            "id": post.id,
            "subreddit": subreddit_name,
            "title": post.title,
            "selftext": post.selftext,
            "score": post.score,
            "num_comments": post.num_comments,
            "created_utc": datetime.utcfromtimestamp(post.created_utc).isoformat(),
            "url": post.url,
            "comments": []
        }

        # Pull top comments for each post
        post.comments.replace_more(limit=0)
        for comment in post.comments.list()[:20]:
            post_data["comments"].append({
                "id": comment.id,
                "body": comment.body,
                "score": comment.score,
                "created_utc": datetime.utcfromtimestamp(comment.created_utc).isoformat()
            })

        posts.append(post_data)

    return posts

def save_raw_data(data, subreddit_name):
    """Save raw data to data/raw/ folder."""
    os.makedirs("data/raw", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/raw/{subreddit_name}_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(data)} posts to {filename}")

def main():
    all_data = []

    for subreddit in SUBREDDITS:
        try:
            posts = scrape_subreddit(subreddit, limit=100)
            save_raw_data(posts, subreddit)
            all_data.extend(posts)
        except Exception as e:
            print(f"Error scraping r/{subreddit}: {e}")

    print(f"\nDone! Total posts collected: {len(all_data)}")

if __name__ == "__main__":
    main()