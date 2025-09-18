# graphics/details_charts.py
from __future__ import annotations

import streamlit as st
import pandas as pd
import plotly.express as px

# Theme (with safe fallbacks so a missing token won't crash the page)
try:
    from graphics.theme import EMERALD, GOLD, WHITE, CARD_BG
except Exception:  # fallback colors
    EMERALD = "#008060"
    GOLD    = "#d4af37"
    WHITE   = "#ffffff"
    CARD_BG = "#121a17"

__all__ = ["details_tables", "details_charts"]


# ---------- helpers ----------
def _to_df(data) -> pd.DataFrame:
    if not data:
        return pd.DataFrame()
    try:
        return pd.json_normalize(list(data), sep=".")
    except Exception:
        return pd.DataFrame(list(data))

def _search(df: pd.DataFrame, query: str) -> pd.DataFrame:
    if df.empty or not query:
        return df
    mask = df.apply(lambda r: r.astype(str).str.contains(query, case=False, na=False).any(), axis=1)
    return df[mask]

def _naive(series: pd.Series) -> pd.Series:
    """Make any timestamp-like series tz-naive to avoid tz-aware/naive errors."""
    ts = pd.to_datetime(series, errors="coerce", utc=True)
    return ts.dt.tz_convert(None)

def _pick_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    return next((c for c in candidates if c in df.columns), None)

def _card_start(title: str) -> None:
    st.markdown(f"<div class='card'><div class='card-header'>{title}</div>", unsafe_allow_html=True)

def _card_end() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


# ---------- public API ----------
def details_tables(invoices=None, jobs=None, customers=None, estimates=None) -> None:
    """
    Uses your real schema:

    invoices: status, amount, due_amount, invoice_date, due_at, paid_at, ...
    jobs: work_status, schedule.scheduled_start, created_at, ...
    customers: created_at, updated_at
    estimates: work_status, options[].status, created_at, ...

    Renders:
      • 4 quick charts (Invoices + Jobs)
      • Searchable tables for all datasets + CSV download
    """
    dfi = _to_df(invoices)
    dfj = _to_df(jobs)
    dfc = _to_df(customers)
    dfe = _to_df(estimates)

    # -----------------------------
    # Row: Invoice charts
    # -----------------------------
    c1, c2 = st.columns(2, gap="small")

    with c1:
        _card_start("📑 Invoices by Status (Count)")
        if dfi.empty:
            st.info("No invoice data available.")
        else:
            status_col = _pick_col(dfi, ["status"])
            if status_col:
                counts = (
                    dfi[status_col]
                    .fillna("Unknown")
                    .value_counts()
                    .rename_axis("status")
                    .reset_index(name="count")
                    .sort_values("count", ascending=False)
                )
                fig = px.bar(
                    counts, x="status", y="count", text_auto=True,
                    color_discrete_sequence=[EMERALD], template="plotly_dark"
                )
                fig.update_layout(
                    height=190, margin=dict(l=0, r=0, t=0, b=0),
                    paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG, showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No status field found in invoices.")
        _card_end()

    with c2:
        _card_start("💵 Paid vs Outstanding")
        if dfi.empty:
            st.info("No invoice amount data available.")
        else:
            amt_col = _pick_col(dfi, ["amount", "totals.total"])
            due_col = _pick_col(dfi, ["due_amount", "totals.balance_due", "balance_due"])
            if amt_col and due_col:
                total_paid = float(dfi[amt_col].fillna(0).sum() - dfi[due_col].fillna(0).sum())
                total_outstanding = float(dfi[due_col].fillna(0).sum())
                pie = pd.DataFrame({"type": ["Paid", "Outstanding"], "value": [total_paid, total_outstanding]})
                fig2 = px.pie(
                    pie, names="type", values="value", hole=0.45, color="type",
                    color_discrete_map={"Paid": EMERALD, "Outstanding": GOLD},
                    template="plotly_dark"
                )
                fig2.update_traces(textposition="inside", textinfo="label+percent")
                fig2.update_layout(
                    height=190, margin=dict(l=0, r=0, t=0, b=0),
                    paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG, showlegend=False
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("Fields `amount` and/or `due_amount` not found.")
        _card_end()

    # -----------------------------
    # Row: Jobs charts
    # -----------------------------
    c3, c4 = st.columns(2, gap="small")

    with c3:
        _card_start("🧾 Jobs by Status")
        if dfj.empty:
            st.info("No job data available.")
        else:
            status_col = _pick_col(dfj, ["work_status", "status", "job.status", "state"])
            if status_col:
                counts = (
                    dfj[status_col]
                    .fillna("Unknown")
                    .value_counts()
                    .rename_axis("work_status")
                    .reset_index(name="count")
                    .sort_values("count", ascending=False)
                )
                fig = px.bar(
                    counts, x="work_status", y="count", text_auto=True,
                    color_discrete_sequence=[WHITE], template="plotly_dark"
                )
                fig.update_layout(
                    height=190, margin=dict(l=0, r=0, t=0, b=0),
                    paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG, showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No status field found in jobs.")
        _card_end()

    with c4:
        _card_start("📅 Jobs Created (Last 30 Days)")
        if dfj.empty:
            st.info("No job data available.")
        else:
            # Prefer top-level created_at; fall back to schedule.scheduled_start
            time_col = _pick_col(dfj, ["created_at", "schedule.scheduled_start", "updated_at"])
            if time_col:
                ts = _naive(dfj[time_col])
                now = pd.Timestamp.utcnow().tz_localize(None)
                mask = ts >= (now - pd.Timedelta(days=30))
                if mask.any():
                    daily = ts[mask].dt.date.value_counts().sort_index()
                    line = pd.DataFrame({"created_at": list(daily.index), "count": list(daily.values)})
                    fig = px.line(line, x="created_at", y="count", markers=True,
                                  color_discrete_sequence=[GOLD], template="plotly_dark")
                    fig.update_layout(
                        height=190, margin=dict(l=0, r=0, t=0, b=0),
                        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG, showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No jobs created in the last 30 days.")
            else:
                st.info("No timestamp field found in jobs.")
        _card_end()

    # -----------------------------
    # Details tabs + CSV
    # -----------------------------
    st.subheader("Details")
    tabs = st.tabs([
        f"Invoices ({len(dfi)})",
        f"Jobs ({len(dfj)})",
        f"Customers ({len(dfc)})",
        f"Estimates ({len(dfe)})",
    ])

    def _table(df: pd.DataFrame, name: str, key_suffix: str) -> None:
        if df.empty:
            st.info(f"No {name.lower()} to show.")
            return
        q = st.text_input(f"Search {name}", key=f"search_{key_suffix}")
        view = _search(df, q)
        st.dataframe(view, hide_index=True, use_container_width=True)
        st.download_button(
            f"Download {name} CSV",
            data=view.to_csv(index=False).encode("utf-8"),
            file_name=f"{name.lower()}_details.csv",
            mime="text/csv",
            use_container_width=True,
            key=f"dl_{key_suffix}",
        )

    with tabs[0]:
        _table(dfi, "Invoices", "invoices")
    with tabs[1]:
        _table(dfj, "Jobs", "jobs")
    with tabs[2]:
        _table(dfc, "Customers", "customers")
    with tabs[3]:
        # Helpful extra: show both top-level estimate fields and option statuses if present
        if not dfe.empty and "options" in dfe.columns:
            # Keep options as-is in the table; charting options would require exploding.
            pass
        _table(dfe, "Estimates", "estimates")


def details_charts(invoices=None, jobs=None, customers=None, estimates=None) -> None:
    """Back-compat wrapper if some pages still call details_charts(...)."""
    return details_tables(invoices=invoices, jobs=jobs, customers=customers, estimates=estimates)
