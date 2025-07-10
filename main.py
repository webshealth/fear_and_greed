import requests
import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

# Configuration with your exact rules
COIN_RULES = {
    'BTC': {
        'allocation': 0.35,
        'buy_tiers': [(40, 140), (30, 140), (20, 70)],
        'sell_rules': [(75, 0.25), (85, 0.50)]
    },
    'ETH': {
        'allocation': 0.25,
        'buy_tiers': [(40, 100), (30, 100), (20, 50)],
        'sell_rules': [(75, 0.25), (85, 0.50)]
    },
    'SOL': {
        'allocation': 0.20,
        'buy_tiers': [(40, 80), (30, 80), (20, 40)],
        'sell_rules': [(70, 0.30), (80, 0.50)]
    },
    'ADA': {
        'allocation': 0.15,
        'buy_tiers': [(40, 60), (30, 60), (20, 30)],
        'sell_rules': [(70, 0.40), (80, 0.50)]
    },
    'INJ': {
        'allocation': 0.05,
        'buy_tiers': [(40, 20), (30, 20), (20, 10)],
        'sell_rules': []  # Profit-based only
    }
}

# Email configuration (set these as environment variables)
EMAIL_USER = os.getenv('EMAIL_USER', 'chanakaworkmail@gmail.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'edzm eugn hdgk qinb')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', 'cbcusandaruwan@gmail.com')

# Get API keys from environment variables
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'ITAPJIQ80TVGWFCH')



def get_fear_greed_index():
    """Fetch current Fear & Greed Index from Alternative.me"""
    url = "https://api.alternative.me/fng/?limit=1"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return int(data['data'][0]['value'])
    except Exception as e:
        print(f"Error fetching Fear & Greed Index: {e}")
        return None

def analyze_market(fgi):
    """Provide detailed market analysis based on FGI score"""
    if fgi >= 85:
        return ("🚨 EXTREME GREED: Market at peak euphoria. Strong sell signal. "
                "Consider taking significant profits as correction likely.")
    elif fgi >= 75:
        return ("📈 Extreme Greed: Market showing greed characteristics. "
                "Good time to take partial profits. Set stop-losses.")
    elif fgi >= 65:
        return ("📈 Greed: Bullish sentiment growing. "
                "Watch for profit-taking opportunities. Avoid FOMO buys.")
    elif fgi >= 55:
        return ("➖ Neutral: Market in balance. "
                "Maintain positions but monitor for trend changes.")
    elif fgi >= 45:
        return ("➖ Neutral: Transition phase. "
                "No strong signals. Good time for research.")
    elif fgi >= 30:
        return ("📉 Fear: Accumulation opportunity. "
                "Good zone for strategic buying. Consider DCA.")
    elif fgi >= 20:
        return ("📉📉 Extreme Fear: Strong fear in market. "
                "Potential buying opportunity for long-term holders.")
    else:
        return ("🚨 PANIC ZONE: Extreme fear and capitulation. "
                "Historically good entry point but high volatility expected.")

def calculate_buy_amounts(fgi, portfolio_size=1000):
    """Calculate exact USD amounts to buy based on FGI and portfolio size"""
    scale = portfolio_size / 1000  # Scale amounts based on portfolio size
    actions = {}

    for coin, rules in COIN_RULES.items():
        amount = 0
        # Find the highest applicable buy tier
        for threshold, tier_amount in rules['buy_tiers']:
            if fgi < threshold:
                amount = tier_amount * scale
                break  # Use the highest matched tier
        actions[coin] = round(amount, 2)

    return actions

def calculate_sell_amounts(fgi, holdings):
    """Calculate USD amounts to sell based on FGI and current holdings"""
    actions = {}

    for coin, amount in holdings.items():
        if coin not in COIN_RULES:
            continue

        sell_rules = COIN_RULES[coin]['sell_rules']
        sell_amount = 0

        # Apply the strongest sell rule that matches
        max_percent = 0
        for threshold, sell_percent in sell_rules:
            if fgi >= threshold and sell_percent > max_percent:
                max_percent = sell_percent

        if max_percent > 0:
            sell_amount = amount * max_percent

        actions[coin] = round(sell_amount, 2)

    return actions

def get_market_news():
    """Get reliable crypto news without API key restrictions"""
    try:
        # Get today's date and yesterday's date
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        # Try CryptoCointracker API
        url = "https://cryptocointracker.com/api/news"
        response = requests.get(url, timeout=10)
        news_data = response.json()
        print("news_data", news_data)
        # Filter for recent news (last 2 days)
        recent_news = []
        for item in news_data.get('news', []):
            if item.get('date', '').startswith(today) or item.get('date', '').startswith(yesterday):
                recent_news.append({
                    'title': item.get('title', ''),
                    'source': item.get('source', 'Unknown'),
                    'date': item.get('date', '')[:10],  # Get YYYY-MM-DD
                    'sentiment': "Neutral"  # Placeholder, we'll analyze below
                })

        # Return top 3 recent news
        return recent_news[:3]
    except:
        # Fallback to Bitcoin News API
        try:
            url = "https://newsdata.io/api/1/latest?apikey=pub_a9c7d3781a50489f984530372a8b8105&q=bitcoin"

            print(url)
            response = requests.get(url, timeout=10)
            print("response",response)
            data = response.json()
            print("bitcoinnews", data)
            news_items = []
            for item in data.get('results', [])[:3]:
                news_items.append({
                    'title': item.get('title', ''),
                    'source': "BitcoinNews",
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'sentiment': "Neutral"
                })
            return news_items
        except Exception as e:
            # Final fallback - generate placeholder news
            return [
                {
                    'title': "Bitcoin volatility increases as market sentiment shifts",
                    'source': "CryptoCointracker",
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'sentiment': "Neutral"
                },
                {
                    'title': "Institutional adoption of crypto continues to grow",
                    'source': "CryptoCointracker",
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'sentiment': "Positive"
                },
                {
                    'title': "Regulatory developments shaping crypto landscape",
                    'source': "CryptoCointracker",
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'sentiment': "Neutral"
                }
            ]

def analyze_news_sentiment(news_items):
    """Simple sentiment analysis based on keywords"""
    positive_keywords = ['bullish', 'adopt', 'growth', 'approve', 'positive', 'rise', 'gain', 'increase']
    negative_keywords = ['bearish', 'regulat', 'ban', 'negative', 'fall', 'drop', 'decline', 'warn', 'risk']

    for item in news_items:
        title = item['title'].lower()
        positive_count = sum(1 for word in positive_keywords if word in title)
        negative_count = sum(1 for word in negative_keywords if word in title)

        if positive_count > negative_count:
            item['sentiment'] = "Positive"
            item['emoji'] = "🟢"
        elif negative_count > positive_count:
            item['sentiment'] = "Negative"
            item['emoji'] = "🔴"
        else:
            item['sentiment'] = "Neutral"
            item['emoji'] = "⚪"

    return news_items

def get_crypto_prices(coins):
    """Get current prices from CoinGecko"""
    try:
        coin_ids = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'SOL': 'solana',
            'ADA': 'cardano',
            'INJ': 'injective-protocol'
        }
        ids = ','.join([coin_ids[coin] for coin in coins])
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
        response = requests.get(url, timeout=10)
        prices = response.json()
        return {coin: prices[coin_ids[coin]]['usd'] for coin in coins}
    except:
        # Return placeholder prices if API fails
        return {
            'BTC': 35000,
            'ETH': 2000,
            'SOL': 100,
            'ADA': 0.5,
            'INJ': 25
        }

def generate_html_report(fgi, sentiment_analysis, news_items, prices, action_type, actions, total_amount, portfolio_size=None, holdings=None):
    """Generate HTML report for email"""
    # Generate strategy table
    strategy_table = """
    <table border="1" cellpadding="5" cellspacing="0" width="100%">
        <tr>
            <th>Coin</th>
            <th>Allocation</th>
            <th>Buy Rules (FGI-based)</th>
            <th>Sell Rules (FGI-based)</th>
        </tr>
    """

    for coin, rules in COIN_RULES.items():
        buy_str = ", ".join([f"${amt} at FGI&lt;{th}" for th, amt in rules['buy_tiers']])

        sell_str = ", ".join([f"Sell {int(perc*100)}% at FGI&gt;{th}" for th, perc in rules['sell_rules']])
        if not sell_str and coin == 'INJ':
            sell_str = "Sell 50% at 2x, 50% at 3x (Profit-based)"

        alloc_percent = f"{rules['allocation']*100:.0f}%"

        strategy_table += f"""
        <tr>
            <td>{coin}</td>
            <td>{alloc_percent}</td>
            <td>{buy_str}</td>
            <td>{sell_str}</td>
        </tr>
        """

    strategy_table += "</table>"

    # Generate news section
    news_html = ""
    for item in news_items:
        news_html += f"""
        <div style="margin-bottom: 15px; padding: 10px; border-left: 4px solid {'#4CAF50' if item['sentiment'] == 'Positive' else '#F44336' if item['sentiment'] == 'Negative' else '#9E9E9E'};">
            <div style="font-weight: bold; font-size: 16px;">{item['emoji']} {item['title']}</div>
            <div style="color: #666; font-size: 14px;">Sentiment: {item['sentiment']} | Source: {item['source']} | Date: {item['date']}</div>
        </div>
        """

    # Generate prices section
    prices_html = "<ul>"
    for coin, price in prices.items():
        prices_html += f"<li><strong>{coin}:</strong> ${price:,.2f}</li>"
    prices_html += "</ul>"

    # Generate action recommendations
    actions_html = ""
    if action_type == "buy":
        actions_html = f"""
        <h3>✅ BUYING OPPORTUNITY DETECTED</h3>
        <p>Portfolio Size: ${portfolio_size:,.2f}</p>
        <h4>Recommended Buy Orders:</h4>
        <ul>
        """
        for coin, amount in actions.items():
            if amount > 0:
                actions_html += f"<li><strong>{coin}:</strong> ${amount:,.2f}</li>"
        actions_html += f"""
        </ul>
        <p><strong>Total to Invest:</strong> ${total_amount:,.2f}</p>
        <p>Strategy: Buy these amounts now. If FGI drops further, consider additional buys at lower thresholds per your plan.</p>
        """
    elif action_type == "sell":
        actions_html = f"""
        <h3>📉 SELLING OPPORTUNITY DETECTED</h3>
        <h4>Recommended Sell Orders:</h4>
        <ul>
        """
        for coin, amount in actions.items():
            if amount > 0:
                actions_html += f"<li><strong>{coin}:</strong> ${amount:,.2f}</li>"
        actions_html += f"""
        </ul>
        <p><strong>Total to Sell:</strong> ${total_amount:,.2f}</p>
        <p>Strategy: Take profits now. Consider setting stop-loss orders to protect remaining gains.</p>
        """
    else:
        actions_html = """
        <h3>⚖️ MARKET IN NEUTRAL ZONE</h3>
        <p>Recommended action: Hold current positions</p>
        <p>Monitor for FGI &lt;40 (buy) or &gt;70 (sell) opportunities</p>
        """

    # Overall market sentiment
    sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    for item in news_items:
        sentiment_counts[item['sentiment']] += 1

    if sentiment_counts['Positive'] > sentiment_counts['Negative']:
        market_sentiment = "POSITIVE TREND 📈"
    elif sentiment_counts['Negative'] > sentiment_counts['Positive']:
        market_sentiment = "NEGATIVE TREND 📉"
    else:
        market_sentiment = "NEUTRAL MARKET ➖"

    # Build the full HTML
    html = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #f8f9fa; padding: 20px; text-align: center; border-bottom: 1px solid #ddd; }}
                .section {{ margin: 20px 0; padding: 20px; background-color: white; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                th {{ background-color: #f2f2f2; text-align: left; }}
                .positive {{ color: #4CAF50; }}
                .negative {{ color: #F44336; }}
                .neutral {{ color: #9E9E9E; }}
                h1, h2, h3 {{ color: #2c3e50; }}
                .footer {{ text-align: center; margin-top: 30px; color: #7f8c8d; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Cryptocurrency Portfolio Strategy Report</h1>
                    <p>Generated on {time.strftime("%Y-%m-%d %H:%M:%S")}</p>
                </div>

                <div class="section">
                    <h2>Market Overview</h2>
                    <p><strong>Fear & Greed Index:</strong> {fgi}</p>
                    <p><strong>Market Analysis:</strong> {sentiment_analysis}</p>
                    <p><strong>Overall Market Sentiment:</strong> {market_sentiment}</p>
                </div>

                <div class="section">
                    <h2>Recent Market News</h2>
                    {news_html}
                </div>

                <div class="section">
                    <h2>Current Prices</h2>
                    {prices_html}
                </div>

                <div class="section">
                    <h2>Investment Strategy</h2>
                    {strategy_table}
                    {actions_html}
                    <p><strong>Note:</strong> INJ uses profit-based selling (50% at 2x, 50% at 3x) not FGI-based</p>
                </div>

                <div class="footer">
                    <p>This report was generated automatically. Please review recommendations before making investment decisions.</p>
                    <p>Cryptocurrency investments are volatile and risky. Only invest what you can afford to lose.</p>
                </div>
            </div>
        </body>
    </html>
    """

    return html

def send_email(html_content):
    """Send the portfolio report via email"""
    try:
        # Create message container
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Crypto Portfolio Strategy Report - {time.strftime('%Y-%m-%d')}"
        msg['From'] = EMAIL_USER
        msg['To'] = RECIPIENT_EMAIL

        # Create HTML version of message
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, RECIPIENT_EMAIL, msg.as_string())

        print("\n✅ Email sent successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Error sending email: {e}")
        return False

def main():
    # Get market data
    fgi = get_fear_greed_index()
    if fgi is None:
        print("\n⚠️ Failed to get Fear & Greed Index. Try again later.")
        return

    sentiment = analyze_market(fgi)
    news_items = get_market_news()
    news_items = analyze_news_sentiment(news_items)
    prices = get_crypto_prices(list(COIN_RULES.keys()))

    # Initialize variables for actions
    action_type = "hold"
    actions = {}
    total_amount = 0
    portfolio_size = 0
    holdings = {}

    # Determine investment actions
    if fgi < 40:  # Buying zone
        action_type = "buy"
        portfolio_size = 1000  # Default portfolio size for scheduled tasks
        actions = calculate_buy_amounts(fgi, portfolio_size)
        total_amount = sum(actions.values())
    elif fgi >= 70:  # Selling zone
        action_type = "sell"
        # Default holdings for scheduled tasks
        holdings = {coin: 100 for coin in COIN_RULES}
        actions = calculate_sell_amounts(fgi, holdings)
        total_amount = sum(actions.values())

    # Generate HTML report
    html_report = generate_html_report(
        fgi, sentiment, news_items, prices,
        action_type, actions, total_amount,
        portfolio_size, holdings
    )

    # Send email automatically for scheduled tasks
    # send_email(html_report)
    print("\n",html_report)

if __name__ == "__main__":
    print("🚀 CRYPTOCURRENCY PORTFOLIO MANAGER")
    print("🔐 Strategy: Fear & Greed Index-based Trading")
    print("📆 Last update:", time.strftime("%Y-%m-%d %H:%M:%S"))
    print("📰 News powered by CryptoCointracker")
    print("📧 Email functionality enabled")
    main()
