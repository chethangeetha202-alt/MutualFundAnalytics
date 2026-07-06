"""
Fund Recommender System
Purpose: Generate intelligent fund recommendations based on risk appetite
Author: Advanced Analytics Pipeline
"""

import pandas as pd
import numpy as np

class FundRecommender:
    """
    Recommends funds based on investor risk profile and fund performance metrics.

    Risk Categories:
    - Low: Conservative, stable funds with lower volatility
    - Moderate: Balanced approach with moderate growth potential
    - High: Aggressive funds with high growth potential
    """

    def __init__(self, scheme_data_path='data/processed/scheme_performance_clean.csv'):
        """Initialize recommender with scheme data."""
        self.scheme_df = pd.read_csv(scheme_data_path)
        self.valid_risk_levels = {'Low': 'Low', 'Moderate': 'Moderate', 'High': 'High'}

    def get_recommendations(self, risk_appetite, num_recommendations=3):
        """
        Generate fund recommendations for given risk appetite.

        Parameters:
        -----------
        risk_appetite : str
            'Low', 'Moderate', or 'High'
        num_recommendations : int
            Number of funds to recommend (default: 3)

        Returns:
        --------
        pd.DataFrame
            Top funds ranked by Sharpe ratio with full metrics
        """
        if risk_appetite not in self.valid_risk_levels:
            raise ValueError(f"Invalid risk appetite. Choose from: {list(self.valid_risk_levels.keys())}")

        # Filter by risk grade
        filtered_funds = self.scheme_df[
            self.scheme_df['risk_grade'] == self.valid_risk_levels[risk_appetite]
        ]

        if len(filtered_funds) == 0:
            raise ValueError(f"No funds found for risk grade: {risk_appetite}")

        # Rank by Sharpe ratio
        recommended = filtered_funds.nlargest(
            num_recommendations, 
            'sharpe_ratio'
        )[['scheme_name', 'fund_house', 'category', 'sharpe_ratio', 
           'alpha', 'beta', 'std_dev_ann_pct', 'return_3yr_pct']]

        return recommended.reset_index(drop=True)

    def get_portfolio_allocation(self, risk_appetite):
        """
        Suggest portfolio allocation weights for risk appetite.

        Parameters:
        -----------
        risk_appetite : str
            'Low', 'Moderate', or 'High'

        Returns:
        --------
        dict
            Allocation strategy with fund weights
        """
        allocations = {
            'Low': {
                'description': 'Conservative Portfolio - Stability Focus',
                'strategy': '60% Low Risk + 40% Moderate Risk',
                'weight': 0.6
            },
            'Moderate': {
                'description': 'Balanced Portfolio - Growth & Stability',
                'strategy': '50% Moderate Risk + 50% High Risk',
                'weight': 0.5
            },
            'High': {
                'description': 'Aggressive Portfolio - Maximum Growth',
                'strategy': '80% High Risk + 20% Moderate Risk',
                'weight': 0.8
            }
        }
        return allocations.get(risk_appetite, None)

    def analyze_fund_performance(self, scheme_name):
        """
        Provide detailed analysis for a specific fund.

        Parameters:
        -----------
        scheme_name : str
            Name of the fund to analyze

        Returns:
        --------
        pd.Series
            Complete fund metrics and analysis
        """
        fund = self.scheme_df[self.scheme_df['scheme_name'] == scheme_name]
        if len(fund) == 0:
            raise ValueError(f"Fund not found: {scheme_name}")
        return fund.iloc[0]


# Example Usage:
if __name__ == "__main__":
    recommender = FundRecommender()

    # Get recommendations for each risk profile
    for risk in ['Low', 'Moderate', 'High']:
        print(f"\n{risk} Risk Appetite:")
        print("-" * 80)
        recommendations = recommender.get_recommendations(risk, num_recommendations=3)
        print(recommendations.to_string(index=False))

        allocation = recommender.get_portfolio_allocation(risk)
        print(f"\nAllocation: {allocation['strategy']}")
