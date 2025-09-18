# graphics/kpi_section.py
from __future__ import annotations

from typing import Any, Mapping
import streamlit as st


def _inject_kpi_css_once() -> None:
    """Inject KPI pill styles once per session."""
    if st.session_state.get("_kpi_css_injected"):
        return
    st.session_state["_kpi_css_injected"] = True

    st.markdown(
        """
        <style>
          .kpi {
            background: var(--slate-50, #f8fafc);
            border: 1px solid var(--slate-200, #e2e8f0);
            border-radius: 18px;
            box-shadow: 0 8px 24px rgba(0,0,0,.06);
            padding: 12px 14px;
          }
          .kpi-title {
            font-size: 12px;
            font-weight: 700;
            color: var(--emerald, #008060);
            letter-spacing: .2px;
          }
          .kpi-value {
            font-size: 28px;
            font-weight: 800;
            margin-top: 4px;
            line-height: 1.05;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _pick(d: Mapping[str, Any], *keys: str, default: Any = 0) -> Any:
    """Return the first non-None value for any key in `keys`; else `default`."""
    for k in keys:
        if k in d and d[k] is not None:
            return d[k]
    return default


def _fmt_money(x: Any) -> str:
    try:
        return f"${float(x):,.0f}"
    except Exception:
        return "$0"


def kpi_pill(title: str, value: str, icon: str = "") -> str:
    return f"""
    <div class='kpi'>
        <div class='kpi-title'>{icon} {title}</div>
        <div class='kpi-value'>{value}</div>
    </div>
    """


def kpi_section(kpis: Mapping[str, Any], **_ignored: Any) -> None:
    """
    Render 4 KPI pills.

    Accepts extra keyword args (e.g., invoices, jobs, customers, get_charts_data)
    for backward compatibility; they are ignored.
    """
    _inject_kpi_css_once()

    revenue     = _pick(kpis, "revenue", "total_revenue", "grand_total", default=0)
    outstanding = _pick(kpis, "outstanding_balance", "outstanding", "unpaid_total", "due_total", default=0)
    jobs        = _pick(kpis, "jobs_booked", "total_jobs", "jobs_count", default=0)
    leads       = _pick(kpis, "leads_count", "new_customers", "leads", default=0)

    c1, c2, c3, c4 = st.columns(4, gap="small")
    c1.markdown(kpi_pill("Total Revenue", _fmt_money(revenue), "💰"), unsafe_allow_html=True)
    c2.markdown(kpi_pill("Outstanding",  _fmt_money(outstanding), "🧾"), unsafe_allow_html=True)
    c3.markdown(kpi_pill("Jobs",         f"{int(float(jobs)):,}", "📋"), unsafe_allow_html=True)
    c4.markdown(kpi_pill("Leads",        f"{int(float(leads)):,}", "👥"), unsafe_allow_html=True)
