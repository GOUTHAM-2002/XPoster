# Twitter API Integration

A FastAPI application that allows users to post tweets and videos to Twitter using OAuth authentication.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd XApi
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

### 3. Twitter API Configuration
- Go to the [Twitter Developer Portal](https://developer.twitter.com/)
- Create a new app or select an existing app
- Get your API credentials
- Enable OAuth 1.0a
- Request Elevated access for posting capabilities

### 4. Environment Variables
Create a `.env` file in the root directory with the following:
```plaintext
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
CALLBACK_URL=your_ngrok_url/callback
```

### 5. Setup ngrok
- Download and install [ngrok](https://ngrok.com/)
- Start ngrok:
```bash
ngrok http 8000
```
- Copy the HTTPS URL from ngrok (e.g., `https://xxxx-xx-xx-xxx-xx.ngrok-free.app`)
- Update your `.env` file with the new callback URL
- Update your Twitter App settings with the same callback URL

### 6. Run the Application
```bash
uvicorn main:app --reload
```

## Features
- OAuth authentication with Twitter
- Post text tweets
- Upload and post videos (MP4 format)

## Limitations
- Video files must be in MP4 format
- Maximum video file size: 512MB
- Maximum video length: 2 minutes and 20 seconds
- Twitter API rate limits apply

## Important Notes
- **Never commit your `.env` file**
- Update the callback URL in both `.env` and Twitter Developer Portal when the ngrok URL changes
- Ensure you have **Elevated API access** for posting capabilities
