from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

ROOT = Path(__file__).resolve().parent

# Load data
nav_path = ROOT / "data/processed/nav_history_clean.csv"
perf_path = ROOT / "data/processed/scheme_performance_clean.csv"
if not nav_path.exists():
    nav_path = ROOT / "data/raw/02_nav_history.csv"
if not perf_path.exists():
    perf_path = ROOT / "data/raw/07_scheme_performance.csv"

nav = pd.read_csv(nav_path)
perf = pd.read_csv(perf_path)
bench = pd.read_csv(ROOT / "data/raw/10_benchmark_indices.csv")

nav["date"] = pd.to_datetime(nav["date"])
nav = nav.sort_values(["amfi_code", "date"])
nav = nav.drop_duplicates(subset=["amfi_code", "date"])
nav = nav[nav["nav"] > 0]

perf["amfi_code"] = perf["amfi_code"].astype(int)
perf = perf.drop_duplicates(subset=["amfi_code"])

bench["date"] = pd.to_datetime(bench["date"])
bench = bench.sort_values(["index_name", "date"])

# Pivot NAV history to wide format
nav_pivot = nav.pivot_table(index="date", columns="amfi_code", values="nav").sort_index()

# Daily returns for all funds
fund_daily_returns = nav_pivot.pct_change().dropna()

# Validate distribution roughly
summary = (
    fund_daily_returns.agg(["mean", "std", "min", "max", "median"])
    .T.rename(columns={"mean": "mean_return", "std": "std_return", "min": "min_return", "max": "max_return", "median": "median_return"})
)
summary = summary.sort_values("mean_return", ascending=False)

# CAGR calculations
latest_date = fund_daily_returns.index.max()

cagr_rows = []
for amfi_code in fund_daily_returns.columns:
    fund_nav = nav_pivot[amfi_code].dropna().sort_index()
    if fund_nav.empty:
        continue

    end_nav = fund_nav.iloc[-1]
    for years in [1, 3, 5]:
        start_date = latest_date - pd.DateOffset(years=years)
        prior_nav = fund_nav.loc[fund_nav.index <= start_date]
        if prior_nav.empty:
            start_nav = np.nan
            n_years = np.nan
        else:
            start_nav = prior_nav.iloc[-1]
            n_years = (latest_date - prior_nav.index[-1]).days / 365.0
        if pd.notna(start_nav) and pd.notna(end_nav) and start_nav > 0 and n_years > 0:
            cagr = (end_nav / start_nav) ** (1 / n_years) - 1
        else:
            cagr = np.nan
        cagr_rows.append((int(amfi_code), years, cagr))

cagr_df = pd.DataFrame(cagr_rows, columns=["amfi_code", "period_years", "cagr"])
cagr_wide = cagr_df.pivot(index="amfi_code", columns="period_years", values="cagr").rename(columns={1: "cagr_1yr", 3: "cagr_3yr", 5: "cagr_5yr"})

# Risk metrics
rf_daily = 0.065 / 252
risk_rows = []

for amfi_code in fund_daily_returns.columns:
    returns = fund_daily_returns[amfi_code]
    mean_return = returns.mean()
    std_return = returns.std(ddof=0)
    downside = returns[returns < 0]
    downside_std = downside.std(ddof=0) if not downside.empty else np.nan

    sharpe = ((mean_return - rf_daily) / std_return) * np.sqrt(252) if pd.notna(std_return) and std_return > 0 else np.nan
    sortino = ((mean_return - rf_daily) / downside_std) * np.sqrt(252) if pd.notna(downside_std) and downside_std > 0 else np.nan

    # Alpha and beta versus NIFTY100
    bench_pivot = bench.pivot_table(index="date", columns="index_name", values="close_value").sort_index()
    bench_returns = bench_pivot["NIFTY100"].pct_change().dropna()
    aligned = pd.concat([returns, bench_returns], axis=1).dropna()
    aligned.columns = ["fund_return", "benchmark_return"]
    slope, intercept, r_value, p_value, std_err = linregress(aligned["benchmark_return"], aligned["fund_return"])
    alpha = intercept * 252
    beta = slope

    # Max drawdown
    fund_nav = nav_pivot[amfi_code].dropna().sort_index()
    running_max = fund_nav.cummax()
    drawdown = fund_nav / running_max - 1
    worst_idx = drawdown.idxmin()
    peak_idx = running_max.loc[:worst_idx].idxmax()
    max_dd = drawdown.loc[worst_idx]

    # Tracking error vs benchmark
    te_nifty100 = (aligned["fund_return"] - aligned["benchmark_return"]).std(ddof=0) * np.sqrt(252)

    risk_rows.append({
        "amfi_code": int(amfi_code),
        "daily_return_mean": mean_return,
        "daily_return_std": std_return,
        "sharpe_ratio": sharpe,
        "sortino_ratio": sortino,
        "alpha": alpha,
        "beta": beta,
        "max_drawdown": max_dd,
        "max_drawdown_start_date": peak_idx,
        "max_drawdown_end_date": worst_idx,
        "tracking_error_nifty100": te_nifty100,
    })

risk_df = pd.DataFrame(risk_rows)
metrics = perf[["amfi_code", "scheme_name", "fund_house", "category", "plan", "expense_ratio_pct", "return_1yr_pct", "return_3yr_pct", "return_5yr_pct"]].merge(cagr_wide.reset_index(), on="amfi_code", how="left")
metrics = metrics.merge(risk_df, on="amfi_code", how="left")
metrics = metrics.merge(summary[["mean_return", "std_return", "min_return", "max_return", "median_return"]], left_on="amfi_code", right_index=True, how="left")
metrics = metrics.rename(columns={"mean_return": "daily_return_mean_from_summary", "std_return": "daily_return_std_from_summary"})

# Use daily metrics from risk_df and align with summary
metrics["daily_return_mean"] = metrics["amfi_code"].map(risk_df.set_index("amfi_code")["daily_return_mean"])
metrics["daily_return_std"] = metrics["amfi_code"].map(risk_df.set_index("amfi_code")["daily_return_std"])
metrics["sharpe_ratio"] = metrics["amfi_code"].map(risk_df.set_index("amfi_code")["sharpe_ratio"])
metrics["sortino_ratio"] = metrics["amfi_code"].map(risk_df.set_index("amfi_code")["sortino_ratio"])
metrics["alpha"] = metrics["amfi_code"].map(risk_df.set_index("amfi_code")["alpha"])
metrics["beta"] = metrics["amfi_code"].map(risk_df.set_index("amfi_code")["beta"])
metrics["max_drawdown"] = metrics["amfi_code"].map(risk_df.set_index("amfi_code")["max_drawdown"])
metrics["max_drawdown_start_date"] = metrics["amfi_code"].map(risk_df.set_index("amfi_code")["max_drawdown_start_date"])
metrics["max_drawdown_end_date"] = metrics["amfi_code"].map(risk_df.set_index("amfi_code")["max_drawdown_end_date"])
metrics["tracking_error_nifty100"] = metrics["amfi_code"].map(risk_df.set_index("amfi_code")["tracking_error_nifty100"])

# Rank-based scorecard
scorecard = metrics.copy()
scorecard["return_3yr_rank"] = scorecard["cagr_3yr"].rank(method="average", ascending=False)
scorecard["sharpe_rank"] = scorecard["sharpe_ratio"].rank(method="average", ascending=False)
scorecard["alpha_rank"] = scorecard["alpha"].rank(method="average", ascending=False)
scorecard["expense_ratio_rank"] = scorecard["expense_ratio_pct"].rank(method="average", ascending=True)
scorecard["max_drawdown_rank"] = (-scorecard["max_drawdown"]).rank(method="average", ascending=False)
scorecard["composite_rank_score"] = (
    0.30 * scorecard["return_3yr_rank"]
    + 0.25 * scorecard["sharpe_rank"]
    + 0.20 * scorecard["alpha_rank"]
    + 0.15 * scorecard["expense_ratio_rank"]
    + 0.10 * scorecard["max_drawdown_rank"]
)
scorecard["fund_score"] = 100 * (1 - (scorecard["composite_rank_score"] - 1) / (len(scorecard) - 1))
scorecard = scorecard.sort_values("fund_score", ascending=False).reset_index(drop=True)

# Alpha and beta output
alpha_beta = scorecard[["amfi_code", "scheme_name", "alpha", "beta", "tracking_error_nifty100"]].copy()
alpha_beta = alpha_beta.sort_values("alpha", ascending=False).reset_index(drop=True)

# Advanced risk analytics: VaR, CVaR, rolling Sharpe

def compute_var_cvar(returns, confidence=0.95):
    if len(returns) == 0:
        return np.nan, np.nan
    sorted_returns = np.sort(returns.dropna().values)
    alpha = 1 - confidence
    idx = int(np.floor(alpha * len(sorted_returns)))
    idx = max(0, min(idx, len(sorted_returns) - 1))
    var_value = sorted_returns[idx]
    cvar_value = sorted_returns[sorted_returns <= var_value].mean() if (sorted_returns <= var_value).any() else var_value
    return var_value * 100, cvar_value * 100

risk_var_rows = []
rolling_sharpe_map = {}
for amfi_code in fund_daily_returns.columns:
    returns = fund_daily_returns[amfi_code].dropna()
    var_95, cvar_95 = compute_var_cvar(returns, confidence=0.95)
    var_99, cvar_99 = compute_var_cvar(returns, confidence=0.99)
    rolling_sharpe = (
        (returns.rolling(90).mean() - rf_daily)
        / returns.rolling(90).std(ddof=0)
        * np.sqrt(252)
    )
    rolling_sharpe_map[int(amfi_code)] = rolling_sharpe.iloc[-1] if len(rolling_sharpe.dropna()) else np.nan
    risk_var_rows.append({
        "amfi_code": int(amfi_code),
        "var_95_pct": var_95,
        "cvar_95_pct": cvar_95,
        "var_99_pct": var_99,
        "cvar_99_pct": cvar_99,
        "rolling_sharpe_90d": rolling_sharpe.iloc[-1] if len(rolling_sharpe.dropna()) else np.nan,
    })
risk_var_df = pd.DataFrame(risk_var_rows)

fund_risk_profile = scorecard.merge(risk_var_df, on="amfi_code", how="left")
fund_risk_profile.to_csv(ROOT / "fund_risk_profile.csv", index=False)

# Sector concentration and portfolio holdings analytics
holdings_path = ROOT / "data/raw/09_portfolio_holdings.csv"
holdings = pd.read_csv(holdings_path)
holdings["weight_pct"] = pd.to_numeric(holdings["weight_pct"], errors="coerce").fillna(0)

sector_stats = (
    holdings.groupby(["amfi_code", "sector"])["weight_pct"].sum().reset_index()
)
def sector_concentration_metrics(group):
    weights = group["weight_pct"].values
    hhi = np.sum((weights / 100) ** 2)
    top_sector = group.loc[group["weight_pct"].idxmax(), "sector"]
    top_sector_share = group["weight_pct"].max()
    top3_share = group["weight_pct"].nlargest(3).sum()
    return pd.Series({
        "sector_hhi": hhi,
        "top_sector": top_sector,
        "top_sector_share_pct": top_sector_share,
        "top_3_sector_share_pct": top3_share,
        "number_of_sectors": len(group),
    })

sector_concentration = sector_stats.groupby("amfi_code").apply(sector_concentration_metrics).reset_index()
sector_concentration = sector_concentration.merge(perf[["amfi_code", "scheme_name", "fund_house", "category", "plan"]], on="amfi_code", how="left")
sector_concentration.to_csv(ROOT / "sector_concentration.csv", index=False)

sector_plot = sector_concentration.sort_values("sector_hhi", ascending=False).head(10)
fig, ax = plt.subplots(figsize=(12, 7))
ax.barh(sector_plot["scheme_name"].astype(str), sector_plot["sector_hhi"], color="#3f51b5")
ax.set_xlabel("Herfindahl-Hirschman Index (HHI)")
ax.set_title("Top 10 Funds by Sector Concentration")
ax.invert_yaxis()
fig.tight_layout()
fig.savefig(ROOT / "sector_concentration.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# SIP cohort and continuity analysis
transactions_path = ROOT / "data/processed/investor_transactions_clean.csv"
transactions = pd.read_csv(transactions_path)
transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"], errors="coerce")
transactions = transactions.dropna(subset=["transaction_date"])
transactions["month"] = transactions["transaction_date"].dt.to_period("M").dt.to_timestamp()

sip_transactions = transactions[transactions["transaction_type"] == "SIP"].copy()
if not sip_transactions.empty:
    sip_transactions["first_month"] = sip_transactions.groupby("investor_id")["month"].transform("min")
    cohort_counts = (
        sip_transactions.groupby(["first_month", "month"])["investor_id"]
        .nunique()
        .reset_index(name="active_investors")
    )
    cohort_sizes = (
        sip_transactions.groupby("first_month")["investor_id"]
        .nunique()
        .reset_index(name="cohort_size")
    )
    cohort_retention = cohort_counts.merge(cohort_sizes, on="first_month", how="left")
    cohort_retention["months_since_cohort"] = (
        (cohort_retention["month"].dt.year - cohort_retention["first_month"].dt.year) * 12
        + (cohort_retention["month"].dt.month - cohort_retention["first_month"].dt.month)
    )
    cohort_retention["retention_rate"] = (
        cohort_retention["active_investors"] / cohort_retention["cohort_size"]
    )
    cohort_retention.to_csv(ROOT / "sip_cohort_retention.csv", index=False)

    cohort_plot_data = cohort_retention[cohort_retention["first_month"] >= (cohort_retention["first_month"].max() - pd.DateOffset(months=12))]
    cohort_pivot = cohort_plot_data.pivot(index="months_since_cohort", columns="first_month", values="retention_rate")
    fig, ax = plt.subplots(figsize=(14, 8))
    cohort_pivot.plot(ax=ax, marker="o")
    ax.set_title("SIP Cohort Retention (Recent 12 Cohorts)")
    ax.set_xlabel("Months Since First SIP")
    ax.set_ylabel("Retention Rate")
    ax.legend(title="Cohort Start Month", bbox_to_anchor=(1.05, 1), loc="upper left")
    fig.tight_layout()
    fig.savefig(ROOT / "sip_cohort_retention.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    sip_monthly = sip_transactions[["investor_id", "month"]].drop_duplicates()
    participation = (
        sip_monthly.assign(value=1)
        .pivot(index="investor_id", columns="month", values="value")
        .fillna(0)
    )
    sorted_months = sorted(participation.columns)
    participation = participation[sorted_months]
    continuity_3m = participation.T.rolling(window=3).sum().T == 3
    continuity_6m = participation.T.rolling(window=6).sum().T == 6
    monthly_active = participation.sum(axis=0)
    continuity_summary = pd.DataFrame({
        "month": monthly_active.index,
        "active_investors": monthly_active.values,
        "continuity_3m_rate": (continuity_3m.sum(axis=0) / monthly_active).fillna(0).values,
        "continuity_6m_rate": (continuity_6m.sum(axis=0) / monthly_active).fillna(0).values,
    })
    continuity_summary["month"] = pd.to_datetime(continuity_summary["month"])
    continuity_summary.to_csv(ROOT / "sip_continuity.csv", index=False)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(continuity_summary["month"], continuity_summary["continuity_3m_rate"], label="3-month continuity", marker="o")
    ax.plot(continuity_summary["month"], continuity_summary["continuity_6m_rate"], label="6-month continuity", marker="o")
    ax.set_title("SIP Investor Continuity")
    ax.set_xlabel("Month")
    ax.set_ylabel("Continuity Rate")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0%}"))
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(ROOT / "sip_continuity.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

# Fund recommendation engine by risk appetite
recommendations = []
conservative = scorecard[
    (scorecard["max_drawdown"] >= -0.20)
    & (scorecard["sharpe_ratio"] >= 0.70)
    & (scorecard["beta"] <= 1.05)
].sort_values(["sharpe_ratio", "fund_score"], ascending=[False, False]).head(10)
for _, row in conservative.iterrows():
    recommendations.append({
        "risk_profile": "Conservative",
        "amfi_code": row["amfi_code"],
        "scheme_name": row["scheme_name"],
        "fund_house": row["fund_house"],
        "category": row["category"],
        "plan": row["plan"],
        "fund_score": row["fund_score"],
        "sharpe_ratio": row["sharpe_ratio"],
        "max_drawdown": row["max_drawdown"],
        "beta": row["beta"],
        "alpha": row["alpha"],
    })
balanced = scorecard.sort_values("fund_score", ascending=False).head(10)
for _, row in balanced.iterrows():
    recommendations.append({
        "risk_profile": "Balanced",
        "amfi_code": row["amfi_code"],
        "scheme_name": row["scheme_name"],
        "fund_house": row["fund_house"],
        "category": row["category"],
        "plan": row["plan"],
        "fund_score": row["fund_score"],
        "sharpe_ratio": row["sharpe_ratio"],
        "max_drawdown": row["max_drawdown"],
        "beta": row["beta"],
        "alpha": row["alpha"],
    })
aggressive = scorecard[
    (scorecard["alpha"] >= 0)
    & (scorecard["beta"] >= 0.90)
].sort_values(["alpha", "cagr_3yr"], ascending=[False, False]).head(10)
for _, row in aggressive.iterrows():
    recommendations.append({
        "risk_profile": "Aggressive",
        "amfi_code": row["amfi_code"],
        "scheme_name": row["scheme_name"],
        "fund_house": row["fund_house"],
        "category": row["category"],
        "plan": row["plan"],
        "fund_score": row["fund_score"],
        "sharpe_ratio": row["sharpe_ratio"],
        "max_drawdown": row["max_drawdown"],
        "beta": row["beta"],
        "alpha": row["alpha"],
    })
recommendations_df = pd.DataFrame(recommendations)
recommendations_df.to_csv(ROOT / "fund_recommendations.csv", index=False)

# Save outputs
scorecard.to_csv(ROOT / "fund_scorecard.csv", index=False)
alpha_beta.to_csv(ROOT / "alpha_beta.csv", index=False)

# Benchmark comparison chart for top 5 funds over 3 years
start_date = pd.Timestamp("2023-01-01")
bench_series = bench.pivot_table(index="date", columns="index_name", values="close_value").sort_index()
bench_series = bench_series[["NIFTY50", "NIFTY100"]].loc[start_date:]
bench_series = bench_series / bench_series.iloc[0] * 100

# Use top 5 funds by score
selected_funds = scorecard.head(5)["amfi_code"].tolist()
fig, ax = plt.subplots(figsize=(12, 7))
for amfi_code in selected_funds:
    fund_series = nav_pivot[amfi_code].dropna().sort_index()
    fund_series = fund_series.loc[start_date:]
    if fund_series.empty:
        continue
    fund_series = fund_series / fund_series.iloc[0] * 100
    ax.plot(fund_series.index, fund_series.values, label=perf.loc[perf["amfi_code"] == amfi_code, "scheme_name"].iloc[0])

ax.plot(bench_series.index, bench_series["NIFTY50"].values, label="NIFTY 50", linestyle="--", linewidth=1.8)
ax.plot(bench_series.index, bench_series["NIFTY100"].values, label="NIFTY 100", linestyle=":", linewidth=1.8)
ax.set_title("Top 5 Funds vs NIFTY 50/100 (3-year view)")
ax.set_xlabel("Date")
ax.set_ylabel("Normalized NAV / Index")
ax.legend(loc="best")
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(ROOT / "benchmark_comparison.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# Write a quick summary
print("Daily return summary rows:", len(summary))
print("Scorecard rows:", len(scorecard))
print("Alpha-beta rows:", len(alpha_beta))
print("Fund risk profile rows:", len(fund_risk_profile))
print("Sector concentration rows:", len(sector_concentration))
print("Fund recommendation rows:", len(recommendations_df))
print("Top 5 funds:")
print(scorecard[["scheme_name", "fund_score"]].head().to_string(index=False))
print("Benchmark chart saved to:", ROOT / "benchmark_comparison.png")
