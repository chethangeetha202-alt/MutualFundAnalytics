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
print("Top 5 funds:")
print(scorecard[["scheme_name", "fund_score"]].head().to_string(index=False))
print("Benchmark chart saved to:", ROOT / "benchmark_comparison.png")
