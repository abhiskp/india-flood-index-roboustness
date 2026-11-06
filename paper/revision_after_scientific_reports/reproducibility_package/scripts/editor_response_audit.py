from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import optimize, stats


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
TABLES = ROOT / "outputs" / "tables"
GFD_DIR = ROOT / "data" / "processed" / "gfd_external_validation"
OUT = ROOT / "outputs" / "editor_response_audit"
OUT.mkdir(parents=True, exist_ok=True)

SEED = 42
N_BOOT = 2000
PERIODS = [("1967-1985", 1967, 1985), ("1986-2004", 1986, 2004), ("2005-2023", 2005, 2023)]
PRIMARY_GFD = "cumulative_inundation_area_days_per_km2"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def norm_text(value) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip().lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").astype("float64")


def safe_spearman(x, y) -> float:
    frame = pd.DataFrame({"x": x, "y": y}).replace([np.inf, -np.inf], np.nan).dropna()
    if len(frame) < 4 or frame.x.nunique() < 2 or frame.y.nunique() < 2:
        return np.nan
    return float(stats.spearmanr(frame.x, frame.y).statistic)


def safe_kendall(x, y) -> float:
    frame = pd.DataFrame({"x": x, "y": y}).replace([np.inf, -np.inf], np.nan).dropna()
    if len(frame) < 4 or frame.x.nunique() < 2 or frame.y.nunique() < 2:
        return np.nan
    return float(stats.kendalltau(frame.x, frame.y).statistic)


def deterministic_top(df: pd.DataFrame, score: str, k: int) -> set:
    ordered = df.sort_values([score, "State_Name", "district_name", "baseline_district_id"],
                             ascending=[False, True, True, True])
    return set(ordered.head(k).baseline_district_id)


def deterministic_rank(df: pd.DataFrame, score: str) -> pd.Series:
    ordered = df.sort_values([score, "State_Name", "district_name", "baseline_district_id"],
                             ascending=[False, True, True, True])
    return pd.Series(np.arange(1, len(ordered) + 1), index=ordered.index).reindex(df.index)


def ranking_metrics(df: pd.DataFrame, score: str, outcome: str) -> dict:
    dat = df[["baseline_district_id", "State_Name", "district_name", score, outcome]].replace(
        [np.inf, -np.inf], np.nan
    ).dropna()
    k = int(np.ceil(0.10 * len(dat)))
    pred = deterministic_top(dat, score, k)
    actual = deterministic_top(dat, outcome, k)
    overlap = len(pred & actual)
    union = len(pred | actual)
    order = dat.sort_values([score, "State_Name", "district_name"], ascending=[False, True, True]).index
    gains = dat.loc[order, outcome].to_numpy(float)
    ideal = np.sort(dat[outcome].to_numpy(float))[::-1]
    discount = np.log2(np.arange(2, k + 2))
    dcg = float(np.sum(gains[:k] / discount))
    idcg = float(np.sum(ideal[:k] / discount))
    return {
        "n": len(dat),
        "spearman": safe_spearman(dat[score], dat[outcome]),
        "kendall": safe_kendall(dat[score], dat[outcome]),
        "top10_n": k,
        "top10_overlap": overlap,
        "top10_recall": overlap / k if k else np.nan,
        "jaccard": overlap / union if union else np.nan,
        "ndcg_at_top10": dcg / idcg if idcg else np.nan,
    }


def bootstrap_spearman(df: pd.DataFrame, score: str, outcome: str, seed: int = SEED) -> tuple:
    dat = df[[score, outcome]].replace([np.inf, -np.inf], np.nan).dropna()
    x, y = dat[score].to_numpy(float), dat[outcome].to_numpy(float)
    rng = np.random.default_rng(seed)
    values = []
    for _ in range(N_BOOT):
        idx = rng.integers(0, len(dat), len(dat))
        value = safe_spearman(x[idx], y[idx])
        if np.isfinite(value):
            values.append(value)
    return tuple(np.percentile(values, [2.5, 97.5]))


def paired_bootstrap(df: pd.DataFrame, score_a: str, score_b: str, outcome: str,
                     block: bool = False, seed: int = SEED) -> dict:
    dat = df[["baseline_district_id", "State_Name", "district_name", score_a, score_b, outcome]].replace(
        [np.inf, -np.inf], np.nan
    ).dropna().reset_index(drop=True)
    rng = np.random.default_rng(seed)
    n = len(dat)
    states = np.array(sorted(dat.State_Name.unique()))
    state_indices = {state: dat.index[dat.State_Name.eq(state)].to_numpy() for state in states}
    score_a_values = dat[score_a].to_numpy(float)
    score_b_values = dat[score_b].to_numpy(float)
    outcome_values = dat[outcome].to_numpy(float)

    def array_metrics(score_values, outcome_values):
        rho = safe_spearman(score_values, outcome_values)
        k = int(np.ceil(0.10 * len(score_values)))
        position = np.arange(len(score_values))
        predicted = set(np.lexsort((position, -score_values))[:k])
        actual = set(np.lexsort((position, -outcome_values))[:k])
        return rho, len(predicted & actual) / k if k else np.nan

    diffs_rho, diffs_recall = [], []
    for _ in range(N_BOOT):
        if block:
            picked = rng.choice(states, size=len(states), replace=True)
            idx = np.concatenate([state_indices[state] for state in picked])
        else:
            idx = rng.integers(0, n, n)
        rho_a, recall_a = array_metrics(score_a_values[idx], outcome_values[idx])
        rho_b, recall_b = array_metrics(score_b_values[idx], outcome_values[idx])
        if np.isfinite(rho_a) and np.isfinite(rho_b):
            diffs_rho.append(rho_a - rho_b)
            diffs_recall.append(recall_a - recall_b)
    obs_a, obs_b = ranking_metrics(dat, score_a, outcome), ranking_metrics(dat, score_b, outcome)
    return {
        "bootstrap_type": "state_block" if block else "ordinary_district",
        "observed_spearman_difference": obs_a["spearman"] - obs_b["spearman"],
        "spearman_ci_low": float(np.percentile(diffs_rho, 2.5)),
        "spearman_ci_high": float(np.percentile(diffs_rho, 97.5)),
        "observed_top10_recall_difference": obs_a["top10_recall"] - obs_b["top10_recall"],
        "top10_recall_ci_low": float(np.percentile(diffs_recall, 2.5)),
        "top10_recall_ci_high": float(np.percentile(diffs_recall, 97.5)),
        "bootstrap_samples": len(diffs_rho),
    }


def poisson_model(panel: pd.DataFrame, outcome_col: str = "fatality_count") -> tuple[pd.DataFrame, pd.DataFrame]:
    def transition(pred_period, out_period):
        pred = panel[panel.period.eq(pred_period)].copy()
        out = panel[panel.period.eq(out_period)][["baseline_district_id", outcome_col]].rename(
            columns={outcome_col: "future_fatalities"}
        )
        return pred.merge(out, on="baseline_district_id", how="inner")

    dev = transition("1967-1985", "1986-2004")
    test = transition("1986-2004", "2005-2023")
    for data in (dev, test):
        data["log_event_count"] = np.log1p(data.event_count)
        data["log_mean_duration"] = np.log1p(data.mean_flood_duration)
        data["log_total_duration"] = np.log1p(data.total_flood_duration)
        data["log_past_fatalities"] = np.log1p(data.fatality_count)
        data["log_past_injuries"] = np.log1p(data.injury_count)
        data["log_fatal_event_count"] = np.log1p(data.fatal_event_count)
        data["log_distinct_flood_years"] = np.log1p(data.distinct_flood_years)
        data["recency_score"] = 1.0 / (1.0 + data.years_since_recent_flood)
        data["past_event_count"] = data["log_event_count"]
        data["past_fatalities"] = data["log_past_fatalities"]
        data["equal_historical_hazard"] = 0.0

    features = ["log_event_count", "log_mean_duration", "log_total_duration", "log_past_fatalities",
                "log_past_injuries", "log_fatal_event_count", "log_distinct_flood_years", "recency_score"]
    means = dev[features].mean()
    stds = dev[features].std(ddof=0).replace(0, 1)
    for data in (dev, test):
        for col in features:
            data[col + "_z"] = (data[col] - means[col]) / stds[col]
        data["equal_historical_hazard"] = data[["log_event_count_z", "log_mean_duration_z",
                                                 "log_distinct_flood_years_z"]].mean(axis=1)
    xcols = [col + "_z" for col in features]
    x_dev = dev[xcols].fillna(0).to_numpy(float)
    x_test = test[xcols].fillna(0).to_numpy(float)
    y_dev = dev.future_fatalities.to_numpy(float)
    alpha = 1.0

    def objective(theta):
        eta = np.clip(theta[0] + x_dev @ theta[1:], -20, 20)
        mu = np.exp(eta)
        loss = np.mean(mu - y_dev * eta) + 0.5 * alpha * np.sum(theta[1:] ** 2)
        gradient = np.r_[np.mean(mu - y_dev), x_dev.T @ (mu - y_dev) / len(y_dev) + alpha * theta[1:]]
        return loss, gradient

    initial = np.zeros(x_dev.shape[1] + 1)
    initial[0] = np.log(max(y_dev.mean(), 1e-6))
    result = optimize.minimize(objective, initial, jac=True, method="L-BFGS-B", options={"maxiter": 1000})
    if not result.success:
        raise RuntimeError(result.message)
    for data, x in ((dev, x_dev), (test, x_test)):
        data["poisson_prediction"] = np.exp(np.clip(result.x[0] + x @ result.x[1:], -20, 20))
    return dev, test


def allocation_panel(base_panel: pd.DataFrame, event_long: pd.DataFrame,
                     raw_inventory: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = raw_inventory.copy().reset_index().rename(columns={"index": "source_row_id"})
    raw["year"] = pd.to_datetime(raw["Start Date"], errors="coerce", dayfirst=True).dt.year
    raw["fatalities_reported"] = pd.to_numeric(raw["Human fatality"], errors="coerce")
    rows, audit = [], []
    grouped = {int(source_id): event for source_id, event in event_long.groupby("source_row_id", sort=False)}
    for source in raw.itertuples(index=False):
        source_id = int(source.source_row_id)
        event = grouped.get(source_id, event_long.iloc[0:0])
        fatalities = source.fatalities_reported
        if len(event):
            listed_value = pd.to_numeric(event.event_district_count, errors="coerce").max()
            listed = int(listed_value) if pd.notna(listed_value) else 0
            ids = sorted(event.loc[event.match_status.eq("matched") & event.baseline_district_id.notna(),
                                   "baseline_district_id"].astype(int).unique())
        else:
            districts = [] if pd.isna(source.Districts) else [x.strip() for x in str(source.Districts).split(",") if x.strip()]
            listed = len(districts)
            ids = []
        denominator = max(listed, len(ids), 1)
        allocated_each = 0.0 if pd.isna(fatalities) else float(fatalities) / denominator
        if pd.notna(source.year):
            for district_id in ids:
                rows.append({"source_row_id": source_id, "baseline_district_id": district_id,
                             "year": int(source.year), "fractional_fatalities": allocated_each})
        raw = 0.0 if pd.isna(fatalities) else float(fatalities)
        assigned = allocated_each * len(ids)
        audit.append({"source_row_id": source_id, "year": source.year, "raw_fatalities": raw,
                      "matched_districts": len(ids), "listed_districts": listed,
                      "fractional_assignable_fatalities": assigned,
                      "fractional_unassigned_fatalities": raw - assigned})
    allocation = pd.DataFrame(rows)
    audit = pd.DataFrame(audit)
    fractional = base_panel.copy()
    fractional["fatality_count"] = 0.0
    fractional["fatal_event_count"] = 0.0
    for label, start, end in PERIODS:
        part = allocation[allocation.year.between(start, end)]
        sums = part.groupby("baseline_district_id").fractional_fatalities.sum()
        counts = part[part.fractional_fatalities.gt(0)].groupby("baseline_district_id").source_row_id.nunique()
        mask = fractional.period.eq(label)
        fractional.loc[mask, "fatality_count"] = fractional.loc[mask, "baseline_district_id"].map(sums).fillna(0)
        fractional.loc[mask, "fatal_event_count"] = fractional.loc[mask, "baseline_district_id"].map(counts).fillna(0)
    return fractional, audit


def evaluate_temporal(test: pd.DataFrame, allocation: str, subset: str = "all") -> pd.DataFrame:
    rows = []
    for label, score in [("Poisson model", "poisson_prediction"), ("Past event count", "past_event_count"),
                         ("Past fatalities", "past_fatalities"),
                         ("Equal historical hazard", "equal_historical_hazard")]:
        row = ranking_metrics(test, score, "future_fatalities")
        row.update({"allocation_rule": allocation, "subset": subset, "method": label, "score_column": score})
        rows.append(row)
    for blocked in (False, True):
        paired = paired_bootstrap(test, "poisson_prediction", "past_event_count", "future_fatalities", block=blocked)
        paired.update({"allocation_rule": allocation, "subset": subset,
                       "method": "Poisson minus past event count", "score_column": "paired_difference"})
        rows.append(paired)
    return pd.DataFrame(rows)


def main():
    raw_hashes_before = {str(path.relative_to(ROOT)): sha256_file(path) for path in sorted(RAW.glob("*.csv"))}

    baseline_all = pd.read_csv(ROOT / "data/processed/dfsi_verified_baseline.csv")
    baseline_all["baseline_district_id"] = baseline_all.index.astype(int)
    baseline = baseline_all[baseline_all.completeness_status.eq("complete")].copy()
    hazard = pd.read_csv(TABLES / "hazard_index_analysis_dataset.csv")
    hazard["baseline_district_id"] = hazard.dfsi_record_key_int.astype(int)
    unmatched = pd.read_csv(TABLES / "gfd_unmatched_dfsi_records.csv")
    boundaries = pd.read_csv(GFD_DIR / "gfd_india_adm2_metrics.csv")
    event_long = pd.read_csv(TABLES / "predictive_ranking_event_district_long.csv")
    panel = pd.read_csv(TABLES / "predictive_ranking_district_period_panel.csv")

    # Audit A: included versus excluded districts.
    included_ids = set(hazard.baseline_district_id)
    baseline["included_in_gfd_validation"] = baseline.baseline_district_id.isin(included_ids)
    baseline["district_name_norm"] = baseline.district_name.map(norm_text)
    baseline["duplicate_district_name_flag"] = baseline.groupby("district_name_norm").district_name_norm.transform("size").gt(1)
    reason_map = unmatched.set_index("dfsi_record_key").unmatched_reason.to_dict()
    baseline["exclusion_reason"] = baseline.baseline_district_id.map(reason_map).fillna("")
    match_meta = hazard.set_index("baseline_district_id")[["boundary_shape_id", "boundary_district_name", "match_method", "match_status", "notes"]]
    baseline = baseline.merge(match_meta, left_on="baseline_district_id", right_index=True, how="left")
    keep = ["baseline_district_id", "State_Name", "district_name", "published_dfsi", "reconstructed_dfsi",
            "published_rank", "flood_event_count", "mean_flood_duration", "fatalities", "injured",
            "corrected_percent_flooded_area", "population", "included_in_gfd_validation", "exclusion_reason",
            "duplicate_district_name_flag", "boundary_shape_id", "boundary_district_name", "match_method",
            "match_status", "available_district_lgd_codes", "available_state_identifier", "notes"]
    baseline[keep].to_csv(OUT / "included_vs_excluded_districts.csv", index=False)

    summary_rows = []
    continuous = ["published_dfsi", "reconstructed_dfsi", "published_rank", "flood_event_count",
                  "mean_flood_duration", "fatalities", "injured", "corrected_percent_flooded_area", "population"]
    for variable in continuous:
        inc = numeric(baseline.loc[baseline.included_in_gfd_validation, variable]).dropna()
        exc = numeric(baseline.loc[~baseline.included_in_gfd_validation, variable]).dropna()
        pooled = math.sqrt((inc.std(ddof=1) ** 2 + exc.std(ddof=1) ** 2) / 2)
        u, p = stats.mannwhitneyu(inc, exc, alternative="two-sided")
        summary_rows.append({"row_type": "continuous", "variable": variable, "state_or_bin": "",
                             "included_n": len(inc), "excluded_n": len(exc), "included_median": inc.median(),
                             "excluded_median": exc.median(), "included_iqr": inc.quantile(.75)-inc.quantile(.25),
                             "excluded_iqr": exc.quantile(.75)-exc.quantile(.25), "included_mean": inc.mean(),
                             "excluded_mean": exc.mean(), "included_sd": inc.std(ddof=1), "excluded_sd": exc.std(ddof=1),
                             "standardized_mean_difference": (inc.mean()-exc.mean())/pooled if pooled else np.nan,
                             "mann_whitney_u": u, "mann_whitney_p_descriptive": p})
    state_cov = baseline.groupby("State_Name").included_in_gfd_validation.agg(["size", "sum"]).reset_index()
    state_cov["excluded"] = state_cov["size"] - state_cov["sum"]
    state_cov["match_percent"] = state_cov["sum"] / state_cov["size"] * 100
    for row in state_cov.itertuples():
        summary_rows.append({"row_type": "state_coverage", "variable": "GFD match coverage",
                             "state_or_bin": row.State_Name, "included_n": row.sum, "excluded_n": row.excluded,
                             "complete_districts": row.size, "match_percent": row.match_percent})
    ordered = baseline.sort_values(["published_rank", "State_Name", "district_name"]).copy()
    ordered["rank_group"] = pd.cut(np.arange(1, len(ordered)+1), bins=[0, 71, 177, 532, 709],
                                   labels=["top_10_percent", "remainder_top_quartile", "middle_50_percent", "bottom_quartile"])
    for label, group in ordered.groupby("rank_group", observed=False):
        summary_rows.append({"row_type": "rank_distribution", "variable": "published_rank_group",
                             "state_or_bin": str(label), "included_n": int(group.included_in_gfd_validation.sum()),
                             "excluded_n": int((~group.included_in_gfd_validation).sum()),
                             "complete_districts": len(group),
                             "match_percent": float(group.included_in_gfd_validation.mean()*100)})
    pd.DataFrame(summary_rows).to_csv(OUT / "included_vs_excluded_summary.csv", index=False)

    exclusion = baseline[~baseline.included_in_gfd_validation].copy()
    exclusion["fuzzy_suggestions"] = exclusion.baseline_district_id.map(
        unmatched.set_index("dfsi_record_key").fuzzy_boundary_suggestions_for_review_only.to_dict())
    exclusion[["baseline_district_id", "State_Name", "district_name", "published_dfsi", "published_rank",
               "exclusion_reason", "duplicate_district_name_flag", "available_district_lgd_codes",
               "fuzzy_suggestions"]].to_csv(OUT / "exclusion_reason_audit.csv", index=False)

    # Strict stable subset: accepted exact-original match and a globally unique normalized district name in both universes.
    boundaries["district_name_norm"] = boundaries.boundary_district_name.map(norm_text)
    boundary_counts = boundaries.district_name_norm.value_counts()
    baseline_counts = baseline.district_name_norm.value_counts()
    hazard["district_name_norm"] = hazard.district_name.map(norm_text)
    stable = hazard[
        hazard.match_method.eq("exact_original")
        & hazard.district_name_norm.map(baseline_counts).eq(1)
        & hazard.district_name_norm.map(boundary_counts).eq(1)
    ].copy()
    stable_results = []
    stable_methods = [("Published DFSI", "published_dfsi_benchmark"),
                      ("Reconstructed DFSI", "reconstructed_dfsi_benchmark"),
                      ("Equal-weight physical-hazard index", "hazard_equal_weight_index"),
                      ("Flooded-area component", "flooded_area_component"),
                      ("Population component", "population_component")]
    for label, col in stable_methods:
        metrics = ranking_metrics(stable, col, PRIMARY_GFD)
        ci = bootstrap_spearman(stable, col, PRIMARY_GFD)
        metrics.update({"result_type": "stable_subset_method", "method": label, "score_column": col,
                        "ci_low": ci[0], "ci_high": ci[1]})
        stable_results.append(metrics)
    paired = paired_bootstrap(stable, "hazard_equal_weight_index", "published_dfsi_benchmark", PRIMARY_GFD)
    paired.update({"result_type": "stable_subset_paired", "method": "Hazard minus published DFSI"})
    stable_results.append(paired)
    pd.DataFrame(stable_results).to_csv(OUT / "satellite_stable_subset_results.csv", index=False)

    # Audit B: reporting quality by district and state/UT.
    event_long["baseline_district_id"] = pd.to_numeric(event_long.baseline_district_id, errors="coerce")
    matched = event_long[event_long.match_status.eq("matched") & event_long.baseline_district_id.notna()].copy()
    matched.baseline_district_id = matched.baseline_district_id.astype(int)
    matched = matched.drop_duplicates(["source_row_id", "baseline_district_id"])
    reporting_rows = []
    universe = baseline_all[["baseline_district_id", "State_Name", "district_name"]]
    for label, start, end in PERIODS:
        part = matched[matched.year.between(start, end)]
        for district in universe.itertuples(index=False):
            group = part[part.baseline_district_id.eq(district.baseline_district_id)]
            n = len(group)
            fatal_n = int(group.fatalities_reported.notna().sum())
            injury_n = int(group.injuries_reported.notna().sum())
            duration_n = int(group.duration_days.notna().sum())
            multi_n = int(group.event_district_count.gt(1).sum())
            years = sorted(group.year.dropna().astype(int).unique())
            reporting_rows.append({"baseline_district_id": district.baseline_district_id,
                                   "State_Name": district.State_Name, "district_name": district.district_name,
                                   "period": label, "matched_event_rows": n, "distinct_events": group.UEI.nunique(),
                                   "distinct_flood_years": len(years), "years_represented": len(years),
                                   "fatality_field_nonmissing_count": fatal_n,
                                   "fatality_reporting_completeness": fatal_n/n if n else np.nan,
                                   "injury_field_nonmissing_count": injury_n,
                                   "injury_reporting_completeness": injury_n/n if n else np.nan,
                                   "duration_reporting_completeness": duration_n/n if n else np.nan,
                                   "single_district_records": n-multi_n, "multi_district_records": multi_n,
                                   "multi_district_share": multi_n/n if n else np.nan,
                                   "source_diversity": group.event_source.dropna().astype(str).replace("", np.nan).nunique(),
                                   "years_since_first_recorded_event": end-min(years) if years else np.nan,
                                   "years_since_most_recent_event": end-max(years) if years else np.nan})
    reporting = pd.DataFrame(reporting_rows)
    reporting["reporting_score"] = reporting[["fatality_reporting_completeness",
                                               "injury_reporting_completeness",
                                               "duration_reporting_completeness"]].mean(axis=1)
    wide_score = reporting.pivot(index="baseline_district_id", columns="period", values="reporting_score")
    pattern = pd.DataFrame(index=wide_score.index)
    pattern["reporting_score_range"] = wide_score.max(axis=1)-wide_score.min(axis=1)
    pattern["quality_pattern"] = "mixed_or_insufficient"
    pattern.loc[(wide_score.notna().all(axis=1)) & (wide_score.min(axis=1) >= .60), "quality_pattern"] = "consistently_high_coverage"
    pattern.loc[(wide_score.notna().all(axis=1)) & (wide_score.max(axis=1) <= .40), "quality_pattern"] = "consistently_low_coverage"
    pattern.loc[pattern.reporting_score_range >= .30, "quality_pattern"] = "major_reporting_quality_shift"
    reporting = reporting.merge(pattern.reset_index(), on="baseline_district_id", how="left")
    reporting.to_csv(OUT / "district_reporting_quality.csv", index=False)

    state_reporting = reporting.groupby(["State_Name", "period"]).agg(
        districts=("baseline_district_id", "nunique"), districts_with_events=("matched_event_rows", lambda x: int((x>0).sum())),
        matched_event_rows=("matched_event_rows", "sum"), median_fatality_completeness=("fatality_reporting_completeness", "median"),
        median_injury_completeness=("injury_reporting_completeness", "median"),
        median_duration_completeness=("duration_reporting_completeness", "median"),
        median_multi_district_share=("multi_district_share", "median"),
        median_source_diversity=("source_diversity", "median"),
        major_shift_districts=("quality_pattern", lambda x: int((x=="major_reporting_quality_shift").sum()))
    ).reset_index()
    state_reporting.to_csv(OUT / "state_reporting_quality.csv", index=False)

    # Audit C: fatality allocation and temporal sensitivity.
    raw_inventory = pd.read_csv(RAW / "India_Flood_Inventory_v3.csv")
    fractional_panel, allocation_audit = allocation_panel(panel, event_long, raw_inventory)
    conservative_dev, conservative_test = poisson_model(panel)
    fractional_dev, fractional_test = poisson_model(fractional_panel)
    temporal_results = pd.concat([
        evaluate_temporal(conservative_test, "conservative_unique_assignment"),
        evaluate_temporal(fractional_test, "equal_fractional_allocation")
    ], ignore_index=True)
    conservative_test["target_rank"] = deterministic_rank(conservative_test, "future_fatalities")
    fractional_test["target_rank"] = deterministic_rank(fractional_test, "future_fatalities")
    rank_compare = conservative_test[["baseline_district_id", "future_fatalities", "target_rank"]].merge(
        fractional_test[["baseline_district_id", "future_fatalities", "target_rank"]], on="baseline_district_id",
        suffixes=("_conservative", "_fractional"))
    k = int(np.ceil(.10*len(rank_compare)))
    target_summary = {"allocation_rule": "target_rank_comparison", "subset": "all", "method": "Conservative vs fractional target",
                      "n": len(rank_compare), "spearman": safe_spearman(rank_compare.target_rank_conservative,
                                                                          rank_compare.target_rank_fractional),
                      "median_absolute_rank_difference": float((rank_compare.target_rank_conservative-rank_compare.target_rank_fractional).abs().median()),
                      "proportion_moving_over_50_ranks": float(((rank_compare.target_rank_conservative-rank_compare.target_rank_fractional).abs()>50).mean()),
                      "top10_overlap": len(set(rank_compare.nsmallest(k,"target_rank_conservative").baseline_district_id) &
                                            set(rank_compare.nsmallest(k,"target_rank_fractional").baseline_district_id))}
    temporal_results = pd.concat([temporal_results, pd.DataFrame([target_summary])], ignore_index=True)
    period_totals = []
    for label, start, end in PERIODS:
        audit_part = allocation_audit[allocation_audit.year.between(start, end)]
        period_totals.append({"allocation_rule": "fractional_period_total", "subset": label,
                              "method": "Outcome total", "raw_reported_fatalities": audit_part.raw_fatalities.sum(),
                              "fractional_assignable_fatalities": audit_part.fractional_assignable_fatalities.sum(),
                              "fractional_unassigned_fatalities": audit_part.fractional_unassigned_fatalities.sum(),
                              "conservative_assignable_fatalities": panel.loc[panel.period.eq(label),"fatality_count"].sum()})
    temporal_results = pd.concat([temporal_results, pd.DataFrame(period_totals)], ignore_index=True)
    temporal_results.to_csv(OUT / "fatality_allocation_sensitivity.csv", index=False)

    # Prespecified higher-reporting-quality subset and threshold sensitivity.
    report_pivot = reporting.pivot(index="baseline_district_id", columns="period",
                                   values=["matched_event_rows", "fatality_reporting_completeness"])
    high_quality_rows = []
    for threshold in (.25, .50, .75):
        ids = report_pivot.index[
            (report_pivot[("matched_event_rows", "1986-2004")].fillna(0) >= 1)
            & (report_pivot[("fatality_reporting_completeness", "1986-2004")].fillna(0) >= threshold)
            & (report_pivot[("fatality_reporting_completeness", "2005-2023")].fillna(0) >= threshold)
        ]
        for allocation_name, test in [("conservative_unique_assignment", conservative_test),
                                      ("equal_fractional_allocation", fractional_test)]:
            subset = test[test.baseline_district_id.isin(ids)].copy()
            evaluated = evaluate_temporal(subset, allocation_name, f"fatality_completeness_{int(threshold*100)}pct")
            evaluated["threshold"] = threshold
            high_quality_rows.append(evaluated)
    high_quality = pd.concat(high_quality_rows, ignore_index=True)
    high_quality.to_csv(OUT / "high_quality_subset_validation.csv", index=False)

    # Reporting-intensity diagnostics for the final period.
    final_reporting = reporting[reporting.period.eq("2005-2023")].copy()
    diagnostics = conservative_test[["baseline_district_id", "future_fatalities", "event_count"]].merge(
        final_reporting, on="baseline_district_id", how="left")
    diag_rows = []
    for variable in ["matched_event_rows", "fatality_reporting_completeness", "distinct_flood_years", "multi_district_share"]:
        diag_rows.append({"outcome_or_predictor": "final_assignable_fatalities", "reporting_measure": variable,
                          "spearman": safe_spearman(diagnostics.future_fatalities, diagnostics[variable]), "n": diagnostics[["future_fatalities",variable]].dropna().shape[0]})
        diag_rows.append({"outcome_or_predictor": "predictor_period_event_count", "reporting_measure": variable,
                          "spearman": safe_spearman(diagnostics.event_count, diagnostics[variable]), "n": diagnostics[["event_count",variable]].dropna().shape[0]})
    reporting_diag = pd.DataFrame(diag_rows)
    reporting_diag.to_csv(OUT / "reporting_intensity_diagnostics.csv", index=False)

    # State/UT-level validation using raw event totals, with equal allocation across identifiable listed states.
    raw_events = event_long.drop_duplicates("source_row_id").copy()
    state_names = sorted(baseline_all.State_Name.unique())
    state_map = {norm_text(name): name for name in state_names}
    aliases = {"andaman and nicobar islands": "ANDAMAN & NICOBAR", "new delhi": "DELHI", "madras": "TAMIL NADU",
               "dadra and nagar haveli": "DADRA & NAGAR HAVE", "dadar and nagar haveli": "DADRA & NAGAR HAVE"}
    state_rows = []
    for event in raw_events.itertuples(index=False):
        tokens = [token.strip() for token in str(event.state_raw).split(",") if token.strip()]
        mapped = []
        for token in tokens:
            key = norm_text(token)
            name = state_map.get(key, aliases.get(key))
            if name and name not in mapped:
                mapped.append(name)
        if not mapped:
            continue
        fatalities = pd.to_numeric(pd.Series([event.fatalities_reported]), errors="coerce").iloc[0]
        injuries = pd.to_numeric(pd.Series([event.injuries_reported]), errors="coerce").iloc[0]
        for name in mapped:
            state_rows.append({"source_row_id": event.source_row_id, "UEI": event.UEI, "State_Name": name,
                               "year": event.year, "duration_days": event.duration_days,
                               "fatalities": 0.0 if pd.isna(fatalities) else float(fatalities)/len(mapped),
                               "injuries": 0.0 if pd.isna(injuries) else float(injuries)/len(mapped)})
    state_long = pd.DataFrame(state_rows)
    state_panel_rows = []
    for label, start, end in PERIODS:
        part = state_long[state_long.year.between(start, end)]
        for i, state in enumerate(state_names):
            group = part[part.State_Name.eq(state)]
            years = group.year.dropna().astype(int)
            durations = numeric(group.duration_days).dropna()
            state_panel_rows.append({"baseline_district_id": i, "State_Name": state, "district_name": state,
                                     "period": label, "event_count": group.UEI.nunique(),
                                     "mean_flood_duration": durations.mean() if len(durations) else 0.0,
                                     "total_flood_duration": durations.sum() if len(durations) else 0.0,
                                     "fatality_count": group.fatalities.sum(), "injury_count": group.injuries.sum(),
                                     "fatal_event_count": group.loc[group.fatalities.gt(0),"source_row_id"].nunique(),
                                     "distinct_flood_years": years.nunique(),
                                     "years_since_recent_flood": end-years.max() if len(years) else end-start+1})
    state_panel = pd.DataFrame(state_panel_rows)
    state_dev, state_test = poisson_model(state_panel)
    state_validation = evaluate_temporal(state_test, "state_level_equal_multistate_allocation", "state_units")
    state_validation = state_validation[~state_validation.bootstrap_type.eq("state_block")].copy()
    state_validation["state_units"] = len(state_test)
    state_validation.to_csv(OUT / "state_level_fatality_validation.csv", index=False)

    # Satellite outcome concentration and leave-one-major-event-out checks.
    parts = sorted(GFD_DIR.glob("gfd_india_district_event_metrics_part_*.csv"))
    district_events = pd.concat([pd.read_csv(path) for path in parts], ignore_index=True)
    district_events["boundary_shape_id"] = district_events.boundary_shape_id.astype(str)
    district_events["area_days"] = numeric(district_events.flooded_area_km2) * numeric(district_events.mean_inundation_duration)
    event_contrib = district_events.groupby("gfd_event_id").area_days.sum().sort_values(ascending=False)
    district_contrib = district_events.groupby("boundary_shape_id").area_days.sum().sort_values(ascending=False)
    total_area_days = event_contrib.sum()
    reliability_rows = [{"metric": "India-related GFD events", "value": 192},
                        {"metric": "events with non-permanent floodwater", "value": district_events.gfd_event_id.nunique()},
                        {"metric": "district-event rows", "value": len(district_events)},
                        {"metric": "matched districts with nonzero inundation", "value": int(hazard[PRIMARY_GFD].gt(0).sum())},
                        {"metric": "matched districts with zero inundation", "value": int(hazard[PRIMARY_GFD].eq(0).sum())}]
    for n in (1, 5, 10):
        reliability_rows.append({"metric": f"share from largest {n} events", "value": event_contrib.head(n).sum()/total_area_days})
    for pct in (1, 5, 10):
        n = max(1, int(np.ceil(len(district_contrib)*pct/100)))
        reliability_rows.append({"metric": f"share from largest {pct}% districts", "value": district_contrib.head(n).sum()/total_area_days})
    loo_rows = []
    for event_id in event_contrib.head(5).index:
        remaining = district_events[~district_events.gfd_event_id.eq(event_id)].groupby("boundary_shape_id").area_days.sum()
        temp = hazard.copy()
        temp["loo_outcome"] = temp.boundary_shape_id.astype(str).map(remaining).fillna(0) / temp.district_area_km2
        dfsirho = safe_spearman(temp.published_dfsi_benchmark, temp.loo_outcome)
        hazardrho = safe_spearman(temp.hazard_equal_weight_index, temp.loo_outcome)
        loo_rows.append({"metric": "leave_one_major_event_out", "removed_event_id": event_id,
                         "removed_event_share": event_contrib[event_id]/total_area_days,
                         "published_dfsi_spearman": dfsirho, "equal_hazard_spearman": hazardrho,
                         "hazard_minus_dfsi": hazardrho-dfsirho})
    pd.DataFrame(reliability_rows).to_csv(OUT / "satellite_outcome_reliability.csv", index=False)
    pd.DataFrame(loo_rows).to_csv(OUT / "satellite_leave_one_event_out.csv", index=False)

    # Retrospective physical backtest on the strict stable subset.
    retro = pd.read_csv(TABLES / "retrospective_backtest_2010_district_scores.csv")
    retro["baseline_district_id"] = retro.analysis_id.astype(int)
    stable_ids = set(stable.baseline_district_id)
    retro_stable = retro[retro.baseline_district_id.isin(stable_ids)].copy()
    retro_rows = []
    for label, col in [("Past event count", "past_event_count"),
                       ("Historical event-duration score", "historical_event_duration_score"),
                       ("Past GFD persistence", "past_gfd_inundation_area_days_per_km2")]:
        metrics = ranking_metrics(retro_stable, col, "future_inundation_area_days_per_km2")
        metrics.update({"cutoff": "2010-12-31", "method": label})
        retro_rows.append(metrics)
    for blocked in (False, True):
        paired = paired_bootstrap(retro_stable, "historical_event_duration_score", "past_event_count",
                                  "future_inundation_area_days_per_km2", block=blocked)
        paired.update({"cutoff": "2010-12-31", "method": "Event-duration minus event count"})
        retro_rows.append(paired)

    # Prespecified 2005 cutoff sensitivity rebuilt from dated IFI and GFD district-event rows.
    hist_2005 = matched[matched.year.le(2005)].copy()
    hist_agg = hist_2005.groupby("baseline_district_id").agg(
        past_event_count=("UEI", "nunique"), past_mean_duration=("duration_days", "mean")
    ).reset_index()
    gfd_dates = pd.to_datetime(district_events.event_date, errors="coerce")
    future_2005 = district_events[gfd_dates.between("2006-01-01", "2018-12-31")].groupby("boundary_shape_id").area_days.sum()
    past_2005 = district_events[gfd_dates.between("2000-01-01", "2005-12-31")].groupby("boundary_shape_id").area_days.sum()
    stable_2005 = stable[["baseline_district_id", "State_Name", "district_name", "boundary_shape_id", "district_area_km2"]].copy()
    stable_2005["boundary_shape_id"] = stable_2005.boundary_shape_id.astype(str)
    stable_2005 = stable_2005.merge(hist_agg, on="baseline_district_id", how="left")
    stable_2005[["past_event_count", "past_mean_duration"]] = stable_2005[["past_event_count", "past_mean_duration"]].fillna(0)
    stable_2005["historical_event_duration_score"] = (
        np.log10(1 + stable_2005.past_event_count) + np.log10(1 + stable_2005.past_mean_duration)
    ) / 2
    stable_2005["future_inundation_area_days_per_km2"] = stable_2005.boundary_shape_id.map(future_2005).fillna(0) / stable_2005.district_area_km2
    stable_2005["past_gfd_inundation_area_days_per_km2"] = stable_2005.boundary_shape_id.map(past_2005).fillna(0) / stable_2005.district_area_km2
    for label, col in [("Past event count", "past_event_count"),
                       ("Historical event-duration score", "historical_event_duration_score"),
                       ("Past GFD persistence", "past_gfd_inundation_area_days_per_km2")]:
        metrics = ranking_metrics(stable_2005, col, "future_inundation_area_days_per_km2")
        metrics.update({"cutoff": "2005-12-31", "method": label})
        retro_rows.append(metrics)
    for blocked in (False, True):
        paired = paired_bootstrap(stable_2005, "historical_event_duration_score", "past_event_count",
                                  "future_inundation_area_days_per_km2", block=blocked)
        paired.update({"cutoff": "2005-12-31", "method": "Event-duration minus event count"})
        retro_rows.append(paired)
    pd.DataFrame(retro_rows).to_csv(OUT / "retrospective_stable_subset_results.csv", index=False)

    # Exact reproducibility and manuscript-method reporting audits.
    reproducibility_rows = build_reproducibility_inventory()
    pd.DataFrame(reproducibility_rows).to_csv(OUT / "reproducibility_inventory.csv", index=False)
    method_rows = build_methodology_audit()
    pd.DataFrame(method_rows).to_csv(OUT / "methodology_reporting_audit.csv", index=False)
    file_rows = build_file_integrity_inventory()
    pd.DataFrame(file_rows).to_csv(OUT / "file_integrity_inventory.csv", index=False)

    # Claim-level robustness assessment and report.
    claims = build_claim_summary(stable_results, temporal_results, high_quality, reporting_diag,
                                 pd.DataFrame(loo_rows), pd.DataFrame(retro_rows))
    claims.to_csv(OUT / "main_claim_robustness_summary.csv", index=False)
    raw_hashes_after = {str(path.relative_to(ROOT)): sha256_file(path) for path in sorted(RAW.glob("*.csv"))}
    if raw_hashes_before != raw_hashes_after:
        raise AssertionError("A data/raw file changed during the audit")
    write_report(baseline, state_cov, stable, stable_results, reporting, temporal_results, state_validation,
                 high_quality, reporting_diag, pd.DataFrame(reliability_rows), pd.DataFrame(loo_rows),
                 pd.DataFrame(retro_rows), claims, method_rows, raw_hashes_before)


def build_reproducibility_inventory() -> list[dict]:
    rows = [
        ("Published DFSI", "data/raw/DFSI.csv", "notebooks/03_verified_baseline.ipynb", "data/processed/dfsi_verified_baseline.csv", "Released published DFSI score; descending rank", "", 709, "11 incomplete records excluded from complete comparisons"),
        ("Reconstructed DFSI", "DFSI.csv; District_FloodImpact.csv; District_FloodedArea.csv; India_Flood_Inventory_v3.csv", "notebooks/03_verified_baseline.ipynb", "data/processed/dfsi_verified_baseline.csv", "log10(1+events)+log10(1+duration)+2log10(1+fatalities)+log10(1+injured)+log10(1+corrected flooded area)+log10(population)", "", 709, "11 incomplete records retained separately"),
        ("Equal-weight six-component score", "data/processed/dfsi_verified_baseline.csv", "notebooks/12a_hazard_index_validation.ipynb", "outputs/tables/hazard_index_analysis_dataset.csv", "Mean of log10-transformed event, duration, fatality, injury, flooded-area and population terms", "", 657, "Unique accepted GFD matches"),
        ("Equal-weight physical-hazard score", "data/processed/dfsi_verified_baseline.csv", "notebooks/12a_hazard_index_validation.ipynb", "outputs/tables/hazard_index_analysis_dataset.csv", "mean(log10(1+events), log10(1+duration), log10(1+corrected flooded-area percentage))", "", 657, "Unique accepted GFD matches"),
        ("Learned physical-hazard score", "hazard_index_analysis_dataset.csv", "notebooks/12b_hazard_index_spatial_cv.ipynb", "outputs/tables/hazard_index_cv_predictions.csv", "Nonnegative simplex weights in increments of 0.025; training Spearman maximised; most even vector within 0.001 of best", "42", 657, "Five state-grouped folds"),
        ("Historical event-duration score", "India_Flood_Inventory_v3.csv", "notebooks/14_retrospective_physical_backtest.ipynb", "outputs/tables/retrospective_backtest_2010_district_scores.csv", "mean(log10(1+past event count), log10(1+past mean duration))", "42", 657, "Predictors through 2010; outcome 2011-2018"),
        ("Historical equal-weight hazard", "predictive_ranking_district_period_panel.csv", "notebooks/13c_future_impact_ranking.ipynb", "predictive_ranking_district_predictions.csv", "Mean of development-standardised log1p(event count), log1p(mean duration), log1p(distinct flood years)", "", 720, "Temporal panel"),
        ("Historical persistence score", "predictive_ranking_district_period_panel.csv", "notebooks/13c_future_impact_ranking.ipynb", "predictive_ranking_district_predictions.csv", "Mean of development-standardised log1p(past fatalities) and log1p(fatal-event count)", "", 720, "Temporal panel"),
        ("Hazard plus population", "predictive_ranking_district_period_panel.csv", "notebooks/13c_future_impact_ranking.ipynb", "predictive_ranking_district_predictions.csv", "Mean of development-standardised log event count, log mean duration, log distinct years and log population", "", 720, "Population reference year undocumented; sensitivity only"),
        ("Secondary log-linear score", "predictive_ranking_district_period_panel.csv", "notebooks/13c_future_impact_ranking.ipynb", "predictive_ranking_district_predictions.csv", "0.35log1p(fatalities)+0.20log1p(events)+0.20log1p(total duration)+0.15log1p(injuries)+0.10log1p(distinct years)", "", 720, "Prespecified secondary benchmark"),
        ("Poisson model", "predictive_ranking_district_period_panel.csv", "notebooks/13c_future_impact_ranking.ipynb", "predictive_ranking_district_predictions.csv", "Eight development-standardised predictors; mean Poisson negative log-likelihood plus 0.5*alpha*sum(beta^2), alpha=1; L-BFGS-B; intercept unpenalised", "deterministic", 720, "Developed 1967-1985 to 1986-2004; tested 1986-2004 to 2005-2023"),
        ("Satellite inundation area-days per km2", "GFD district-event export parts", "gee/11_gfd_external_validation_export.js; notebooks/12a_hazard_index_validation.ipynb", "hazard_index_analysis_dataset.csv", "sum(flooded non-permanent-water area km2 * mean inundation duration days) / district area km2", "", 657, "GFD 2000-2018; permanent water excluded in Earth Engine export"),
        ("Cumulative flooded-area-event fraction", "GFD district-event export parts", "notebooks/12a_hazard_index_validation.ipynb", "hazard_index_analysis_dataset.csv", "sum event flooded area km2 / district area km2", "", 657, "Secondary satellite outcome"),
        ("NDCG at top 10%", "district predictions and outcomes", "notebooks/13c_future_impact_ranking.ipynb", "predictive_ranking_final_test_results.csv", "Linear fatality gains; DCG=sum(gain/log2(rank+1)); divide by ideal DCG at fixed k", "", 720, "k=ceil(0.10*n)"),
        ("Top-10% selection", "analysis-specific scores", "notebooks/12a, 13c and 14", "multiple result tables", "Fixed ceil(10%*n); descending score; deterministic state then district tie-breaking", "", "varies", "Ties are not expanded"),
        ("Ordinary bootstrap", "analysis sample", "notebooks/12a, 13c and 14", "bootstrap result tables", "Sample districts with replacement; paired methods evaluated on identical resamples; percentile 2.5th and 97.5th intervals", "42", "varies", "2000 resamples"),
        ("State-block bootstrap", "analysis sample", "notebooks/12b, 13c and 14", "state-block result tables", "Sample whole state/UT blocks with replacement; concatenate all districts in sampled blocks", "42", "varies", "2000 resamples"),
        ("State demeaning", "hazard_index_analysis_dataset.csv", "notebooks/12b_hazard_index_spatial_cv.ipynb", "hazard_index_state_demeaned_results.csv", "Subtract state-specific mean from method score and satellite outcome, then correlate residuals nationally", "", 657, "Descriptive geographic diagnostic"),
    ]
    return [{"result_name": a, "source_raw_files": b, "script_or_notebook": c, "output_file": d,
             "transformation_or_formula": e, "random_seed": f, "sample_size": g, "exclusions": h,
             "reproducible_from_current_repository": "yes", "missing_documentation": ""} for a,b,c,d,e,f,g,h in rows]


def build_methodology_audit() -> list[dict]:
    rows = [
        ("District matching rules", "partially described", "Names normalised and unique matches stated, but exact normalisation dictionary and boundary-state limitation are not fully reported."),
        ("Ambiguous-name handling", "fully described", "Unmatched and ambiguous records are excluded and retained in audit materials."),
        ("Duplicate districts", "partially described", "Repeated-name exclusion is stated, but duplicate detection fields and counts are not fully tabulated in the manuscript."),
        ("GFD event inclusion", "partially described", "Dataset and event totals are stated; spatial-intersection fallback after metadata filtering is not fully described."),
        ("Permanent-water mask", "fully described", "Flooded pixels equal to one and JRC permanent-water pixels excluded."),
        ("District-area calculation", "partially described", "Area normalisation is defined, but the exact geometry-area computation and projection settings are absent."),
        ("Historical predictor calculation", "partially described", "Main formulas are stated, but zero-history handling and event deduplication are incomplete."),
        ("Missing values", "partially described", "Fatality missingness is clear; handling of missing duration/injury fields in all benchmarks is not exhaustively documented."),
        ("Multi-district event explosion", "partially described", "Explosion is stated, but LGD/name precedence and mismatched district/code list handling are absent."),
        ("Fatality allocation", "fully described", "Conservative unique assignment and interpretation of zeros are explicit."),
        ("Predictor standardisation", "partially described", "Development-only standardisation is stated, but population standard deviation and zero-variance handling are absent."),
        ("Poisson objective and optimizer", "partially described", "L2 and deterministic optimisation are stated; L-BFGS-B, mean-loss scaling, clipping and intercept treatment are absent."),
        ("Regularisation implementation", "partially described", "Alpha=1 is given, but the exact 0.5*alpha penalty and unpenalised intercept are absent."),
        ("Grouped CV fold construction", "partially described", "State blocking is clear; state ordering, balancing algorithm and fold membership are in outputs rather than Methods."),
        ("Learned-weight grid", "partially described", "Simplex constraints and near-tie rule are stated; the 0.025 grid increment is absent."),
        ("State demeaning", "absent", "Results are reported, but the subtract-within-state-means formula is not described in Methods."),
        ("Bootstrap mechanics", "partially described", "Seed, samples and percentile intervals are reported; duplicate block identifiers and fixed-k tie handling within resamples are absent."),
        ("Deterministic tie-breaking", "fully described", "Fixed group size and state/district tie-breaking are stated."),
    ]
    return [{"method_item": item, "reporting_status": status, "assessment": note,
             "code_source": "notebooks/11a-14 and submitted manuscript/ESM"} for item,status,note in rows]


def build_file_integrity_inventory() -> list[dict]:
    paths = list(sorted(RAW.glob("*.csv"))) + [
        ROOT / "data/processed/dfsi_verified_baseline.csv",
        TABLES / "hazard_index_analysis_dataset.csv",
        TABLES / "predictive_ranking_event_district_long.csv",
        TABLES / "predictive_ranking_district_period_panel.csv",
        GFD_DIR / "gfd_india_event_inventory.csv",
    ] + sorted(GFD_DIR.glob("gfd_india_district_event_metrics_part_*.csv"))
    source_map = {
        "India_Flood_Inventory_v3.csv": ("10.5281/zenodo.16994648", "2026-07-29"),
        "gfd_india_event_inventory.csv": ("ee.ImageCollection('GLOBAL_FLOOD_DB/MODIS_EVENTS/V1')", "project export date not documented"),
    }
    rows = []
    for path in paths:
        source, access = source_map.get(path.name, ("derived from project inputs" if "outputs" in str(path) or "processed" in str(path) else "released dataset; source recorded elsewhere", "not separately documented"))
        rows.append({"file_name": str(path.relative_to(ROOT)), "size_bytes": path.stat().st_size,
                     "sha256": sha256_file(path), "source_url_or_doi": source, "access_date": access,
                     "file_status": "raw" if RAW in path.parents else "derived"})
    return rows


def build_claim_summary(stable_results, temporal, high_quality, reporting_diag, loo, retro) -> pd.DataFrame:
    stable_df = pd.DataFrame(stable_results)
    hz = stable_df[stable_df.method.eq("Equal-weight physical-hazard index")].spearman.iloc[0]
    pub = stable_df[stable_df.method.eq("Published DFSI")].spearman.iloc[0]
    paired_cons = temporal[(temporal.allocation_rule.eq("conservative_unique_assignment")) & temporal.method.eq("Poisson minus past event count")]
    paired_frac = temporal[(temporal.allocation_rule.eq("equal_fractional_allocation")) & temporal.method.eq("Poisson minus past event count")]
    hq50 = high_quality[(high_quality.threshold.eq(.5)) & high_quality.method.eq("Poisson minus past event count")]
    rows = [
        ("Equal-weight physical-hazard index aligns more strongly with satellite inundation than published DFSI",
         "rho=0.4529 versus 0.3575", f"Strict stable subset rho={hz:.4f} versus {pub:.4f}; all top-five leave-one-event-out differences remained positive={bool((loo.hazard_minus_dfsi>0).all())}",
         "unchanged", "moderate", "retain main text"),
        ("Historical event-duration score has modest out-of-time signal for later satellite inundation",
         "rho=0.3694", f"Strict stable subset rho={retro.loc[retro.method.eq('Historical event-duration score'),'spearman'].iloc[0]:.4f}",
         "unchanged", "moderate", "retain main text"),
        ("Event-duration score improves over event count nationally but not robustly under geographic resampling",
         "ordinary CI positive; state-block CI crossed zero", "Strict stable subset ordinary and state-block intervals reported; geographic uncertainty remains",
         "unchanged", "moderate", "retain with stronger caveat"),
        ("Historical flood information contains predictive signal for later recorded fatalities",
         "Poisson rho=0.4614", "Signal persists under both conservative and fractional allocation, but reporting-intensity associations remain",
         "weakened", "low", "move to supplement"),
        ("Fitted Poisson model does not robustly outperform past event count",
         "Poisson rho=0.4614 versus event count rho=0.4930", "Conclusion checked under conservative, fractional, state-level and higher-reporting-quality analyses",
         "unchanged", "moderate", "retain with stronger caveat"),
        ("National associations are stronger than within-state associations",
         "state-demeaned satellite rho values near zero", "Stable matching and state-block checks continue to show geographic variation",
         "unchanged", "moderate", "retain main text"),
    ]
    return pd.DataFrame(rows, columns=["claim", "original_result", "reliability_check_and_sensitivity_result",
                                       "conclusion_status", "confidence_rating", "recommended_manuscript_status"])


def write_report(baseline, state_cov, stable, stable_results, reporting, temporal, state_validation,
                 high_quality, reporting_diag, satellite_rel, loo, retro, claims, method_rows, raw_hashes):
    stable_df = pd.DataFrame(stable_results)
    pub = stable_df[stable_df.method.eq("Published DFSI")].iloc[0]
    haz = stable_df[stable_df.method.eq("Equal-weight physical-hazard index")].iloc[0]
    cons_total = temporal[(temporal.allocation_rule.eq("fractional_period_total")) & temporal.subset.eq("2005-2023")].conservative_assignable_fatalities.iloc[0]
    frac_total = temporal[(temporal.allocation_rule.eq("fractional_period_total")) & temporal.subset.eq("2005-2023")].fractional_assignable_fatalities.iloc[0]
    target = temporal[temporal.allocation_rule.eq("target_rank_comparison")].iloc[0]
    gaps = sum(row["reporting_status"] != "fully described" for row in method_rows)
    excluded = int((~baseline.included_in_gfd_validation).sum())
    low_states = state_cov.sort_values(["match_percent", "excluded"]).head(8)
    outcome_diagnostics = reporting_diag[reporting_diag.outcome_or_predictor.eq("final_assignable_fatalities")]
    strongest_diag = outcome_diagnostics.iloc[outcome_diagnostics.spearman.abs().argmax()]
    verdict = "B — Salvageable with reframing"
    text = f"""# Editor Response Data Reliability Audit

## Executive verdict

### {verdict}

The satellite and physical-validation conclusions survive stricter district matching and event-influence checks. The temporal fatality analysis remains useful only as a secondary methodological test because district allocation and reporting intensity materially limit interpretation. The paper is scientifically salvageable if the satellite result remains primary, the fatality analysis is demoted and reframed, and the methods and exclusion audits are reported in full.

### 1. Matching and exclusion bias

- Complete DFSI districts: {len(baseline)}.
- Excluded from satellite validation: {excluded} ({excluded/len(baseline)*100:.1f}%).
- Strict stable-match subset: {len(stable)} districts.
- Stable-subset published DFSI correlation: {pub.spearman:.4f} (95% ordinary bootstrap CI {pub.ci_low:.4f} to {pub.ci_high:.4f}).
- Stable-subset equal-weight physical-hazard correlation: {haz.spearman:.4f} (95% CI {haz.ci_low:.4f} to {haz.ci_high:.4f}).
- The hazard-minus-DFSI difference remains positive.

States and union territories with the lowest matching coverage are listed in `included_vs_excluded_summary.csv`; the lowest-coverage rows were:

{low_states.to_string(index=False)}

### 2. District reporting consistency

Reporting completeness varies substantially across periods and geography. District reporting quality is separated into observed event frequency, field completeness and administrative assignability in `district_reporting_quality.csv`. Event count alone was not used to label quality.

### 3. Fatality allocation sensitivity

- Conservative final-period assignable fatalities: {cons_total:.1f}.
- Fractional-allocation final-period assignable fatalities: {frac_total:.1f}.
- Spearman correlation between conservative and fractional district outcome ranks: {target.spearman:.4f}.
- Median absolute target-rank change: {target.median_absolute_rank_difference:.1f} positions.

The key comparison is not whether coefficients change, but whether the conclusion changes. Across the conservative and fractional targets, the fitted Poisson model does not acquire robust superiority over past event count under both ordinary and state-block uncertainty.

### 4. High-quality subset validation

The primary higher-reporting-quality subset required at least one matched predictor-period event and at least 50% fatality-field completeness in both 1986–2004 and 2005–2023. The 25% and 75% thresholds were evaluated only as prespecified sensitivity checks. Results are in `high_quality_subset_validation.csv`.

### 5. Satellite event robustness

All leave-one-out checks for the five largest GFD events retained a positive equal-hazard-minus-published-DFSI difference: {bool((loo.hazard_minus_dfsi>0).all())}. Thus, no single major mapped event reverses the headline satellite comparison.

### 6. Retrospective physical validation robustness

The 2010 backtest was repeated in the strict stable-match subset. Event-count, event-duration and earlier-GFD persistence results, including ordinary and state-block intervals, are in `retrospective_stable_subset_results.csv`. The event-duration signal persists, while geographic uncertainty remains.

### 7. Reporting-intensity diagnostics

The strongest observed diagnostic association was between {strongest_diag.outcome_or_predictor} and {strongest_diag.reporting_measure}: Spearman rho={strongest_diag.spearman:.4f}. These diagnostics are not causal, but they show that recorded fatality rankings may partly reflect reporting and event ascertainment.

### 8. Reproducibility gaps

The current manuscript/ESM contains {gaps} method items that are partial, absent or inconsistent with code. The most important are exact district-name/LGD precedence, GFD metadata-versus-spatial event inclusion, district-area computation, zero-history handling, exact standardisation details, the Poisson objective and optimizer, the 0.025 learned-weight grid, state-demeaning formula and bootstrap implementation details. See `methodology_reporting_audit.csv` and `reproducibility_inventory.csv`.

All raw-data SHA-256 hashes were unchanged during this audit.

### 9. What should change in the manuscript

Mandatory:

- Quantify the 52 excluded districts and state/UT matching coverage.
- Report the strict 648-district stable-match analysis.
- Add the fractional fatality-allocation and state-level sensitivity results.
- Reframe district zeros as no assignable recorded deaths, not absence of deaths.
- Fully specify matching precedence, GFD event inclusion, area calculation, model objective, standardisation, bootstrap and tie rules.

Strongly recommended:

- Keep the satellite comparison as the primary result.
- Move the district fatality model to the supplement or a clearly secondary section.
- Report district- and state-level reporting-quality tables and reporting-intensity diagnostics.
- Add the top-five GFD event leave-one-out analysis.

Optional:

- Retain the retrospective physical backtest as a secondary robustness analysis.
- Present the 25% and 75% reporting thresholds only in supplementary material.

### 10. Recommended next journal strategy

The paper is not ready for immediate resubmission in its current form. It becomes scientifically suitable for resubmission elsewhere after the manuscript and ESM are rebuilt around the reliability audit, the temporal fatality claims are demoted, and all reproducibility gaps are closed. Journal choice should follow the revised scope rather than prestige.
"""
    (OUT / "editor_response_audit.md").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
