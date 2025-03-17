# Emerging Artist Discovery Tool - A&R Dashboard Demo for Concord Music Group

A data-driven dashboard for A&R teams to discover and evaluate emerging music artists showing early signs of breakout success.

## Features

- **Data-Driven Discovery**: Identify emerging artists based on streaming growth, social engagement, and playlist additions
- **Comprehensive Analysis**: Evaluate artists across multiple metrics and platforms
- **Actionable Insights**: Understand why an artist is trending and their growth potential
- **Detailed Analytics**: View streaming trends, social engagement, and momentum metrics for each artist

## Deployment

### Local Development

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```
   streamlit run app/dashboard/streamlit_app.py
   ```

### Deploying to Streamlit Cloud

1. Create a free account on [Streamlit Cloud](https://streamlit.io/cloud)
2. Connect your GitHub account
3. Create a new app and select this repository
4. Set the main file path to: `app/dashboard/streamlit_app.py`
5. Deploy!

## How It Works

The dashboard uses simulated data to demonstrate how the tool would work with real data from Spotify and social platforms. In a production environment, it would connect to:

- Spotify API for streaming data, playlist additions, and artist information
- Social media APIs for engagement metrics

## License

© 2025 Kiriti Vundavilli for Concord Music Group | Emerging Artist Discovery Tool 
