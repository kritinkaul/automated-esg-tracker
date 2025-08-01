"""
Example: Integrating PostgreSQL database with Streamlit Dashboard
Shows how to load real data from database instead of APIs
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from src.database import DatabaseManager
from datetime import datetime, timedelta

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_companies_from_db():
    """Load all companies from the database."""
    try:
        db = DatabaseManager()
        
        if db.SessionLocal:  # Development mode with SQLAlchemy
            session = db.get_session()
            from src.database import Company
            
            companies = session.query(Company).all()
            company_data = []
            
            for company in companies:
                company_data.append({
                    'ticker': company.ticker,
                    'name': company.name,
                    'sector': company.sector,
                    'industry': company.industry,
                    'market_cap': company.market_cap,
                    'country': company.country
                })
            
            session.close()
            return pd.DataFrame(company_data)
        
        else:  # Production mode with Supabase
            result = db.supabase.table("companies").select("*").execute()
            return pd.DataFrame(result.data)
            
    except Exception as e:
        st.error(f"Error loading companies: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_esg_scores_from_db(ticker=None):
    """Load ESG scores from database."""
    try:
        db = DatabaseManager()
        
        if db.SessionLocal:  # Development mode
            session = db.get_session()
            from src.database import Company, ESGScores
            
            query = session.query(ESGScores, Company.ticker).join(
                Company, ESGScores.company_id == Company.id
            )
            
            if ticker:
                query = query.filter(Company.ticker == ticker)
            
            results = query.all()
            
            esg_data = []
            for esg, company_ticker in results:
                esg_data.append({
                    'ticker': company_ticker,
                    'environmental_score': esg.environmental_score,
                    'social_score': esg.social_score,
                    'governance_score': esg.governance_score,
                    'overall_score': esg.overall_score,
                    'data_source': esg.data_source,
                    'created_at': esg.created_at
                })
            
            session.close()
            return pd.DataFrame(esg_data)
            
        else:  # Production mode with Supabase
            query = db.supabase.table("esg_scores").select(
                "*, companies(ticker)"
            )
            
            if ticker:
                # Get company ID first
                company_result = db.supabase.table("companies").select("id").eq("ticker", ticker).execute()
                if company_result.data:
                    company_id = company_result.data[0]['id']
                    query = query.eq("company_id", company_id)
            
            result = query.execute()
            return pd.DataFrame(result.data)
            
    except Exception as e:
        st.error(f"Error loading ESG scores: {e}")
        return pd.DataFrame()

def display_company_overview_from_db():
    """Display company overview using database data."""
    st.header("🏢 Companies in Database")
    
    companies_df = load_companies_from_db()
    
    if not companies_df.empty:
        # Company selector
        selected_ticker = st.selectbox(
            "Select Company",
            companies_df['ticker'].tolist()
        )
        
        # Display selected company info
        company_info = companies_df[companies_df['ticker'] == selected_ticker].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Company", company_info['name'])
            st.metric("Sector", company_info['sector'])
        
        with col2:
            st.metric("Industry", company_info['industry'])
            st.metric("Country", company_info['country'])
        
        with col3:
            if company_info['market_cap']:
                market_cap_b = company_info['market_cap'] / 1e9
                st.metric("Market Cap", f"${market_cap_b:.1f}B")
        
        return selected_ticker
    else:
        st.info("No companies found in database. Please run data collection first.")
        return None

def display_esg_dashboard_from_db(ticker):
    """Display ESG dashboard using database data."""
    st.header(f"📊 ESG Data for {ticker}")
    
    esg_df = load_esg_scores_from_db(ticker)
    
    if not esg_df.empty:
        # Get latest scores
        latest_scores = esg_df.iloc[-1]
        
        # Display current ESG scores
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Environmental", 
                f"{latest_scores['environmental_score']:.1f}",
                help="Environmental impact score"
            )
        
        with col2:
            st.metric(
                "Social", 
                f"{latest_scores['social_score']:.1f}",
                help="Social responsibility score"
            )
        
        with col3:
            st.metric(
                "Governance", 
                f"{latest_scores['governance_score']:.1f}",
                help="Corporate governance score"
            )
        
        with col4:
            st.metric(
                "Overall ESG", 
                f"{latest_scores['overall_score']:.1f}",
                help="Combined ESG score"
            )
        
        # ESG Score Chart
        if len(esg_df) > 1:
            st.subheader("📈 ESG Score Trends")
            
            # Prepare data for plotting
            chart_data = esg_df[['created_at', 'environmental_score', 'social_score', 'governance_score', 'overall_score']]
            chart_data['created_at'] = pd.to_datetime(chart_data['created_at'])
            
            fig = px.line(
                chart_data,
                x='created_at',
                y=['environmental_score', 'social_score', 'governance_score', 'overall_score'],
                title=f"ESG Score Trends for {ticker}",
                labels={'value': 'Score', 'created_at': 'Date'}
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # ESG Breakdown
        st.subheader("🔍 Current ESG Breakdown")
        
        breakdown_data = {
            'Category': ['Environmental', 'Social', 'Governance'],
            'Score': [
                latest_scores['environmental_score'],
                latest_scores['social_score'],
                latest_scores['governance_score']
            ]
        }
        
        fig_bar = px.bar(
            breakdown_data,
            x='Category',
            y='Score',
            title=f"ESG Score Breakdown for {ticker}",
            color='Score',
            color_continuous_scale='viridis'
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
        
    else:
        st.info(f"No ESG data found for {ticker}. Please collect data first.")

def display_sector_analysis_from_db():
    """Display sector-wide ESG analysis."""
    st.header("🏭 Sector ESG Analysis")
    
    companies_df = load_companies_from_db()
    esg_df = load_esg_scores_from_db()
    
    if not companies_df.empty and not esg_df.empty:
        # Merge company and ESG data
        merged_df = pd.merge(
            esg_df.groupby('ticker').last().reset_index(),
            companies_df[['ticker', 'sector']],
            on='ticker'
        )
        
        # Sector averages
        sector_avg = merged_df.groupby('sector')[
            ['environmental_score', 'social_score', 'governance_score', 'overall_score']
        ].mean().reset_index()
        
        # Display sector comparison
        fig_sector = px.bar(
            sector_avg,
            x='sector',
            y='overall_score',
            title="Average ESG Scores by Sector",
            color='overall_score',
            color_continuous_scale='viridis'
        )
        
        st.plotly_chart(fig_sector, use_container_width=True)
        
        # Detailed sector table
        st.subheader("📊 Detailed Sector Breakdown")
        st.dataframe(
            sector_avg.round(2),
            use_container_width=True
        )

def main_dashboard_with_db():
    """Main dashboard function using database data."""
    st.set_page_config(
        page_title="ESG Tracker - Database Version",
        page_icon="🌱",
        layout="wide"
    )
    
    st.title("🌱 ESG Data Tracker - Database Integration")
    st.markdown("---")
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Navigate",
        ["Company Overview", "ESG Dashboard", "Sector Analysis", "Data Management"]
    )
    
    if page == "Company Overview":
        selected_ticker = display_company_overview_from_db()
        
        if selected_ticker:
            st.markdown("---")
            display_esg_dashboard_from_db(selected_ticker)
    
    elif page == "ESG Dashboard":
        companies_df = load_companies_from_db()
        if not companies_df.empty:
            ticker = st.selectbox("Select Company", companies_df['ticker'].tolist())
            display_esg_dashboard_from_db(ticker)
        else:
            st.info("No companies available. Please add companies to the database.")
    
    elif page == "Sector Analysis":
        display_sector_analysis_from_db()
    
    elif page == "Data Management":
        st.header("🗄️ Database Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Database Statistics")
            companies_df = load_companies_from_db()
            esg_df = load_esg_scores_from_db()
            
            st.metric("Total Companies", len(companies_df))
            st.metric("Total ESG Records", len(esg_df))
            
            if not companies_df.empty:
                st.metric("Sectors Covered", companies_df['sector'].nunique())
        
        with col2:
            st.subheader("🔄 Data Operations")
            
            if st.button("🔄 Refresh Cache"):
                st.cache_data.clear()
                st.success("Cache cleared! Data will be refreshed on next load.")
            
            if st.button("📥 Run Data Collection"):
                st.info("This would trigger the data collection process...")
                # You can integrate this with your data collection scripts

if __name__ == "__main__":
    main_dashboard_with_db() 