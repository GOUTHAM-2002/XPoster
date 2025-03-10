from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import tweepy
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Twitter API credentials
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
CALLBACK_URL = os.getenv("CALLBACK_URL")

# Store tokens temporarily (in production, use a proper database)
user_tokens = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login/twitter")
async def twitter_login():
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET, CALLBACK_URL)
    try:
        redirect_url = auth.get_authorization_url()
        return RedirectResponse(url=redirect_url)
    except tweepy.TweepError:
        return {"error": "Error getting Twitter authorization URL"}

@app.get("/callback")
async def callback(oauth_token: str, oauth_verifier: str):
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.request_token = {'oauth_token': oauth_token,
                         'oauth_token_secret': oauth_verifier}
    
    try:
        auth.get_access_token(oauth_verifier)
        user_tokens['access_token'] = auth.access_token
        user_tokens['access_token_secret'] = auth.access_token_secret
        
        print(f"Access Token: {auth.access_token}")
        print(f"Access Token Secret: {auth.access_token_secret}")
        
        return RedirectResponse(url="/upload")
    except Exception as e:
        return {"error": str(e)}

@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/post_tweet")
async def post_tweet(tweet_text: str = Form(...)):
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(user_tokens['access_token'], user_tokens['access_token_secret'])
    api = tweepy.API(auth)
    
    try:
        api.update_status(tweet_text)
        return {"message": "Tweet posted successfully!"}
    except Exception as e:
        return {"error": str(e)}

from fastapi import File, UploadFile
import aiofiles
import os

@app.post("/post_video")
async def post_video(
    video: UploadFile = File(...),
    caption: str = Form(None)
):
    # Create a temporary file to store the upload
    temp_file = f"temp_video_{video.filename}"
    
    try:
        # Save uploaded file temporarily
        async with aiofiles.open(temp_file, 'wb') as out_file:
            content = await video.read()
            await out_file.write(content)

        # Initialize Twitter auth
        auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
        auth.set_access_token(user_tokens['access_token'], user_tokens['access_token_secret'])
        api = tweepy.API(auth)
        
        # Upload the video
        media = api.media_upload(temp_file)
        api.update_status(status=caption or "", media_ids=[media.media_id])
        
        # Clean up the temporary file
        os.remove(temp_file)
        
        return {"message": "Video posted successfully!"}
    except Exception as e:
        # Clean up the temporary file if it exists
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return {"error": str(e)}