# Social Analytics Module for Artist Portal

This module allows artists to connect their Facebook Page and Instagram Business accounts to track key metrics like followers and reach via official Meta APIs.

## Features
- **Meta OAuth 2.0 Login**: Secure connection flow.
- **Account Linking**: Automatically detect IG Business accounts linked to FB Pages.
- **Daily Metrics Ingestion**: Time-series storage for Followers and Reach.
- **Interactive Dashboard**: Modern UI with Chart.js visualization.

## Setup Instructions

### 1. Meta App Configuration
1. Go to [Meta for Developers](https://developers.facebook.com/).
2. Create a new App (Type: "Business").
3. Add **Facebook Login for Business** and **Instagram Graph API** products.
4. Set the Redirect URI to: `http://localhost:5000/social/callback` (or your production URL).
5. In App Settings -> Basic, get your **App ID** and **App Secret**.

### 2. Environment Setup
Update `config.py` in your Flask project with your credentials:
```python
FB_APP_ID = "your_app_id"
FB_APP_SECRET = "your_app_secret"
FB_VERSION = "v21.0"
```

### 3. Database Migration
Run the provided SQL script to create the necessary tables:
```bash
# Using SQL Server Management Studio or any SQL client
run social_schema.sql
```

### 4. Required Python Packages
Ensure `requests` is installed:
```bash
pip install requests
```

### 5. Permissions (Scopes)
The app requests the following permissions during the OAuth flow:
- `pages_read_engagement`
- `pages_show_list`
- `instagram_basic`
- `instagram_manage_insights`
- `public_profile`

## How to Test Locally
1. Start your Flask app: `python app.py`.
2. Log in to the Artist Portal as an artist.
3. Navigate to `/social/dashboard`.
4. Click **Connect Meta**.
5. Follow the Facebook popup to select your Page and IG account.
6. Once redirected back, select the account from the list.
7. Click **Sync Now** to fetch initial data.
8. View the charts and cards!

## Security Notes
- Access tokens are stored server-side in the `SocialAccounts` table.
- A dummy encryption placeholder is recommended for `AccessToken` in production.
- CSRF protection is handled by Flask (if enabled) or can be added to the forms.
