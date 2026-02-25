from flask import Blueprint, request, redirect, url_for, session, jsonify, render_template, current_app, flash
import requests
from ..extensions import db
from ..models import SocialAccount, SocialMetric, SocialSyncLog, Artist
from flask_login import login_required, current_user
from datetime import datetime, timedelta
import secrets

social_bp = Blueprint('social', __name__)

def get_fb_config():
    return {
        'app_id': current_app.config.get('FB_APP_ID'),
        'app_secret': current_app.config.get('FB_APP_SECRET'),
        'version': current_app.config.get('FB_VERSION', 'v21.0'),
        'redirect_uri': url_for('social.callback', _external=True)
    }

@social_bp.route("/social/connect")
@login_required
def connect():
    config = get_fb_config()
    # Permissions: business_management, pages_read_engagement, pages_show_list, instagram_basic, instagram_manage_insights
    scope = "pages_read_engagement,pages_show_list,instagram_basic,instagram_manage_insights,public_profile"
    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state
    
    auth_url = (
        f"https://www.facebook.com/{config['version']}/dialog/oauth?"
        f"client_id={config['app_id']}&"
        f"redirect_uri={config['redirect_uri']}&"
        f"state={state}&"
        f"scope={scope}"
    )
    return redirect(auth_url)

@social_bp.route("/social/callback")
@login_required
def callback():
    state = request.args.get('state')
    if state != session.get('oauth_state'):
        return "Invalid state parameter", 401
    
    code = request.args.get('code')
    if not code:
        return "No code provided", 400
    
    config = get_fb_config()
    fb_base_url = f"https://graph.facebook.com/{config['version']}"
    
    # 1. Exchange code for access token
    token_url = f"{fb_base_url}/oauth/access_token"
    params = {
        'client_id': config['app_id'],
        'client_secret': config['app_secret'],
        'redirect_uri': config['redirect_uri'],
        'code': code
    }
    
    r = requests.get(token_url, params=params)
    data = r.json()
    if 'error' in data:
        return jsonify(data), 400
    
    short_token = data['access_token']
    
    # 2. Exchange for long-lived token (approx 60 days)
    long_token_url = f"{fb_base_url}/oauth/access_token"
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': config['app_id'],
        'client_secret': config['app_secret'],
        'fb_exchange_token': short_token
    }
    
    lr = requests.get(long_token_url, params=params)
    ldata = lr.json()
    long_token = ldata.get('access_token', short_token)
    
    session['fb_temp_token'] = long_token
    return redirect(url_for('social.select_page'))

@social_bp.route("/social/select-page")
@login_required
def select_page():
    token = session.get('fb_temp_token')
    if not token:
        return redirect(url_for('social.connect'))
    
    config = get_fb_config()
    fb_base_url = f"https://graph.facebook.com/{config['version']}"
    
    # Fetch user's pages
    r = requests.get(f"{fb_base_url}/me/accounts", params={
        'access_token': token,
        'fields': 'id,name,access_token'
    })
    pages = r.json().get('data', [])
    
    available_accounts = []
    for page in pages:
        page_id = page['id']
        page_token = page['access_token']
        
        # Check IG account
        ir = requests.get(f"{fb_base_url}/{page_id}", params={
            'access_token': page_token,
            'fields': 'instagram_business_account'
        })
        ig_data = ir.json()
        ig_id = ig_data.get('instagram_business_account', {}).get('id')
        
        ig_name = None
        if ig_id:
             hr = requests.get(f"{fb_base_url}/{ig_id}", params={
                 'access_token': page_token,
                 'fields': 'username'
             })
             ig_name = hr.json().get('username')
        
        available_accounts.append({
            'page_id': page_id,
            'page_name': page['name'],
            'page_token': page_token,
            'ig_id': ig_id,
            'ig_name': ig_name
        })
    
    return render_template("social/select_page.html", accounts=available_accounts)

@social_bp.route("/social/link-account", methods=['POST'])
@login_required
def link_account():
    artist_id = current_user.ArtistId
    if not artist_id:
        return "No artist ID found for your account", 400
        
    page_id = request.form.get('page_id')
    ig_id = request.form.get('ig_id')
    page_token = request.form.get('page_token')
    page_name = request.form.get('page_name')
    ig_name = request.form.get('ig_name')

    # Remove existing
    SocialAccount.query.filter_by(ArtistId=artist_id).delete()
    
    new_acc = SocialAccount(
        ArtistId=artist_id,
        Platform='meta',
        PageId=page_id,
        IgBusinessId=ig_id,
        AccessToken=page_token,
        PageName=page_name,
        IgHandle=ig_name
    )
    db.session.add(new_acc)
    db.session.commit()
    
    flash("Connected Meta accounts successfully!", "success")
    return redirect(url_for('social.dashboard'))

@social_bp.route("/social/dashboard")
@login_required
def dashboard():
    artist_id = current_user.ArtistId
    account = SocialAccount.query.filter_by(ArtistId=artist_id).first()
    
    if not account:
        return render_template("social/dashboard.html", connected=False)

    # Get latest metrics for cards
    today = datetime.utcnow().date()
    metrics = SocialMetric.query.filter_by(ArtistId=artist_id).order_by(SocialMetric.MetricDate.desc()).limit(20).all()
    
    return render_template("social/dashboard.html", connected=True, account=account, metrics=metrics)

@social_bp.route("/social/api/data")
@login_required
def chart_data():
    artist_id = current_user.ArtistId
    metrics = SocialMetric.query.filter_by(ArtistId=artist_id).order_by(SocialMetric.MetricDate.asc()).all()
    
    # Organize data for Chart.js
    data = {}
    for m in metrics:
        key = f"{m.Platform}_{m.MetricName}"
        if key not in data:
            data[key] = {"labels": [], "values": []}
        data[key]["labels"].append(m.MetricDate.strftime("%Y-%m-%d"))
        data[key]["values"].append(float(m.Value))
        
    return jsonify(data)

@social_bp.route("/social/sync", methods=['POST'])
@login_required
def sync_data():
    artist_id = current_user.ArtistId
    success, message = run_sync_for_artist(artist_id)
    if success:
        return jsonify({"status": "success", "message": message})
    return jsonify({"status": "error", "message": message}), 500

@social_bp.route("/social/disconnect", methods=['POST'])
@login_required
def disconnect():
    artist_id = current_user.ArtistId
    SocialAccount.query.filter_by(ArtistId=artist_id).delete()
    SocialMetric.query.filter_by(ArtistId=artist_id).delete()
    db.session.commit()
    flash("Disconnected social accounts.", "success")
    return redirect(url_for('social.dashboard'))

def run_sync_for_artist(artist_id):
    account = SocialAccount.query.filter_by(ArtistId=artist_id).first()
    if not account:
        return False, "Not connected"
    
    v = current_app.config.get('FB_VERSION', 'v21.0')
    fb_url = f"https://graph.facebook.com/{v}"
    token = account.AccessToken
    
    try:
        # 1. FB Page Metrics
        if account.PageId:
            # Followers
            pr = requests.get(f"{fb_url}/{account.PageId}", params={
                'fields': 'fan_count,name',
                'access_token': token
            })
            pdata = pr.json()
            if 'fan_count' in pdata:
                save_metric(artist_id, 'facebook', 'followers', pdata['fan_count'])
            
            # Impressions (Reach)
            ir = requests.get(f"{fb_url}/{account.PageId}/insights", params={
                'metric': 'page_impressions_unique',
                'period': 'day',
                'access_token': token
            })
            idata = ir.json()
            if 'data' in idata and idata['data']:
                val = idata['data'][0]['values'][-1]['value']
                save_metric(artist_id, 'facebook', 'reach', val)

        # 2. IG Business Metrics
        if account.IgBusinessId:
            # Followers
            igr = requests.get(f"{fb_url}/{account.IgBusinessId}", params={
                'fields': 'followers_count',
                'access_token': token
            })
            igdata = igr.json()
            if 'followers_count' in igdata:
                save_metric(artist_id, 'instagram', 'followers', igdata['followers_count'])
            
            # Insights
            insr = requests.get(f"{fb_url}/{account.IgBusinessId}/insights", params={
                'metric': 'impressions,reach',
                'period': 'day',
                'access_token': token
            })
            insdata = insr.json()
            if 'data' in insdata:
                for metric in insdata['data']:
                    name = metric['name']
                    val = metric['values'][-1]['value']
                    save_metric(artist_id, 'instagram', name, val)

        account.LastSync = datetime.utcnow()
        db.session.add(SocialSyncLog(ArtistId=artist_id, Platform='meta', Status='SUCCESS', Message='Manual sync completed'))
        db.session.commit()
        return True, "Sync completed"
        
    except Exception as e:
        db.session.add(SocialSyncLog(ArtistId=artist_id, Platform='meta', Status='ERROR', Message=str(e)))
        db.session.commit()
        return False, str(e)

def save_metric(artist_id, platform, name, value):
    today = datetime.utcnow().date()
    # Upsert logic: search for today's entry
    existing = SocialMetric.query.filter_by(
        ArtistId=artist_id, 
        Platform=platform, 
        MetricName=name, 
        MetricDate=today
    ).first()
    
    if existing:
        existing.Value = value
    else:
        new_m = SocialMetric(
            ArtistId=artist_id,
            Platform=platform,
            MetricName=name,
            MetricDate=today,
            Value=value
        )
        db.session.add(new_m)
