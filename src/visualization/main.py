"""
Main Streamlit dashboard for ESG Data Tracker.
Provides interactive visualization of ESG data for public companies.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import altair as alt
from typing import List, Dict, Any, Optional
import sys
import os

# Add the parent directory to the path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db_manager
from mock_data import SAMPLE_COMPANIES

# Page configuration
st.set_page_config(
    page_title="ESG Data Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .positive-sentiment {
        color: #28a745;
        font-weight: bold;
    }
    .negative-sentiment {
        color: #dc3545;
        font-weight: bold;
    }
    .neutral-sentiment {
        color: #6c757d;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


class ESGDashboard:
    """Main dashboard class for ESG data visualization."""
    
    def __init__(self):
        self.db_manager = get_db_manager()
        self.companies = SAMPLE_COMPANIES
    
    def get_company_options(self) -> List[Dict[str, str]]:
        """Get list of companies for dropdown."""
        return [{"label": f"{c['ticker']} - {c['name']}", "value": c['ticker']} 
                for c in self.companies]
    
    def get_esg_data(self, ticker: str, days: int = 30) -> pd.DataFrame:
        """Get ESG scores data for a company."""
        try:
            company = self.db_manager.get_company_by_ticker(ticker)
            if not company:
                return pd.DataFrame()
            
            scores = self.db_manager.get_esg_scores_history(company['id'], days)
            if not scores:
                return pd.DataFrame()
            
            df = pd.DataFrame(scores)
            df['date'] = pd.to_datetime(df['date'])
            return df.sort_values('date')
            
        except Exception as e:
            st.error(f"Error fetching ESG data: {e}")
            return pd.DataFrame()
    
    def get_news_data(self, ticker: str, limit: int = 10) -> pd.DataFrame:
        """Get news data for a company."""
        try:
            company = self.db_manager.get_company_by_ticker(ticker)
            if not company:
                return pd.DataFrame()
            
            news = self.db_manager.get_latest_news(company['id'], limit)
            if not news:
                return pd.DataFrame()
            
            df = pd.DataFrame(news)
            df['date'] = pd.to_datetime(df['date'])
            return df.sort_values('date', ascending=False)
            
        except Exception as e:
            st.error(f"Error fetching news data: {e}")
            return pd.DataFrame()
    
    def plot_esg_trends(self, df: pd.DataFrame, ticker: str):
        """Create ESG trends line chart."""
        if df.empty:
            st.warning("No ESG data available for this company.")
            return
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Environmental Score', 'Social Score', 
                          'Governance Score', 'Overall ESG Score'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Environmental Score
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['environmental_score'], 
                      mode='lines+markers', name='Environmental',
                      line=dict(color='#2E8B57', width=3)),
            row=1, col=1
        )
        
        # Social Score
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['social_score'], 
                      mode='lines+markers', name='Social',
                      line=dict(color='#4169E1', width=3)),
            row=1, col=2
        )
        
        # Governance Score
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['governance_score'], 
                      mode='lines+markers', name='Governance',
                      line=dict(color='#8B4513', width=3)),
            row=2, col=1
        )
        
        # Overall Score
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['overall_score'], 
                      mode='lines+markers', name='Overall',
                      line=dict(color='#FF4500', width=3)),
            row=2, col=2
        )
        
        fig.update_layout(
            title=f"ESG Score Trends for {ticker}",
            height=600,
            showlegend=False,
            template="plotly_white"
        )
        
        # Update y-axis ranges
        for i in range(1, 3):
            for j in range(1, 3):
                fig.update_yaxes(range=[0, 100], row=i, col=j)
        
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_esg_comparison(self, selected_companies: List[str]):
        """Create ESG comparison bar chart."""
        if not selected_companies:
            return
        
        comparison_data = []
        
        for ticker in selected_companies:
            company = self.db_manager.get_company_by_ticker(ticker)
            if company:
                scores = self.db_manager.get_esg_scores_history(company['id'], 1)
                if scores:
                    latest = scores[0]
                    comparison_data.append({
                        'Company': ticker,
                        'Environmental': latest['environmental_score'],
                        'Social': latest['social_score'],
                        'Governance': latest['governance_score'],
                        'Overall': latest['overall_score']
                    })
        
        if not comparison_data:
            st.warning("No data available for comparison.")
            return
        
        df = pd.DataFrame(comparison_data)
        
        # Create comparison chart
        fig = go.Figure()
        
        categories = ['Environmental', 'Social', 'Governance', 'Overall']
        colors = ['#2E8B57', '#4169E1', '#8B4513', '#FF4500']
        
        for i, category in enumerate(categories):
            fig.add_trace(go.Bar(
                name=category,
                x=df['Company'],
                y=df[category],
                marker_color=colors[i]
            ))
        
        fig.update_layout(
            title="ESG Score Comparison",
            barmode='group',
            height=500,
            template="plotly_white",
            xaxis_title="Company",
            yaxis_title="Score",
            yaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def display_news_sentiment(self, df: pd.DataFrame):
        """Display news articles with sentiment analysis."""
        if df.empty:
            st.warning("No news data available.")
            return
        
        st.subheader("📰 Latest ESG News & Sentiment Analysis")
        
        for _, article in df.iterrows():
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**{article['headline']}**")
                    st.caption(f"Source: {article['source']} | Date: {article['date'].strftime('%Y-%m-%d')}")
                    if pd.notna(article['content']):
                        st.write(article['content'][:200] + "...")
                
                with col2:
                    sentiment_score = article['sentiment_score']
                    sentiment_label = article['sentiment_label']
                    
                    # Color code sentiment
                    if sentiment_label == 'positive':
                        sentiment_class = 'positive-sentiment'
                    elif sentiment_label == 'negative':
                        sentiment_class = 'negative-sentiment'
                    else:
                        sentiment_class = 'neutral-sentiment'
                    
                    st.markdown(f"""
                    <div class="metric-card">
                        <p><strong>Sentiment:</strong></p>
                        <p class="{sentiment_class}">{sentiment_label.title()}</p>
                        <p><strong>Score:</strong> {sentiment_score:.3f}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.divider()
    
    def display_company_metrics(self, ticker: str):
        """Display key company metrics."""
        company = self.db_manager.get_company_by_ticker(ticker)
        if not company:
            return
        
        st.subheader(f"📈 Company Overview: {company['name']} ({ticker})")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Sector", company.get('sector', 'N/A'))
        
        with col2:
            st.metric("Industry", company.get('industry', 'N/A'))
        
        with col3:
            market_cap = company.get('market_cap', 0)
            if market_cap > 0:
                market_cap_billions = market_cap / 1e9
                st.metric("Market Cap", f"${market_cap_billions:.1f}B")
            else:
                st.metric("Market Cap", "N/A")
        
        with col4:
            st.metric("Country", company.get('country', 'N/A'))
    
    def export_data(self, df: pd.DataFrame, ticker: str, data_type: str):
        """Export data to CSV."""
        if df.empty:
            st.warning("No data to export.")
            return
        
        csv = df.to_csv(index=False)
        st.download_button(
            label=f"Download {data_type} Data (CSV)",
            data=csv,
            file_name=f"{ticker}_{data_type}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    def run_dashboard(self):
        """Run the main dashboard."""
        # Header
        st.markdown('<h1 class="main-header">📊 ESG Data Tracker</h1>', unsafe_allow_html=True)
        st.markdown("### Professional ESG Monitoring & Analysis Platform")
        
        # Sidebar
        st.sidebar.header("🎯 Dashboard Controls")
        
        # Company selection
        company_options = self.get_company_options()
        selected_ticker = st.sidebar.selectbox(
            "Select Company",
            options=[c['value'] for c in company_options],
            format_func=lambda x: next(c['label'] for c in company_options if c['value'] == x)
        )
        
        # Date range
        days_back = st.sidebar.slider("Days of Historical Data", 7, 90, 30)
        
        # Multi-company comparison
        st.sidebar.header("📊 Comparison")
        comparison_companies = st.sidebar.multiselect(
            "Select Companies for Comparison",
            options=[c['ticker'] for c in self.companies],
            default=[selected_ticker] if selected_ticker else []
        )
        
        # Main content
        if selected_ticker:
            # Company overview
            self.display_company_metrics(selected_ticker)
            
            # ESG Trends
            st.subheader("📈 ESG Score Trends")
            esg_df = self.get_esg_data(selected_ticker, days_back)
            self.plot_esg_trends(esg_df, selected_ticker)
            
            # Export ESG data
            if not esg_df.empty:
                self.export_data(esg_df, selected_ticker, "ESG_Scores")
            
            # News and sentiment
            news_df = self.get_news_data(selected_ticker, 10)
            self.display_news_sentiment(news_df)
            
            # Export news data
            if not news_df.empty:
                self.export_data(news_df, selected_ticker, "News")
        
        # Company comparison
        if len(comparison_companies) > 1:
            st.subheader("🏆 ESG Score Comparison")
            self.plot_esg_comparison(comparison_companies)
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>Built with ❤️ for ESG transparency and sustainable investing</p>
            <p>Data sources: Mock data for demonstration | Real APIs in production</p>
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main function to run the dashboard."""
    try:
        dashboard = ESGDashboard()
        dashboard.run_dashboard()
    except Exception as e:
        st.error(f"Error running dashboard: {e}")
        st.exception(e)


if __name__ == "__main__":
    main() 