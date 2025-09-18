# C:\Users\ancheta\Desktop\RosCross\THATS_CRAZYYYYY\graphics\metrics.py
from __future__ import annotations
from typing import Any, Dict, List

PAID_STATUSES = {"paid", "complete", "completed", "closed", "settled"}
CANCELLED_STATUSES = {"cancelled", "canceled", "void"}

def _lower(x: Any) -> str:
    return str(x).strip().lower() if x is not None else ""

def _num(v: Any) -> float:
    try:
        return float(v)
    except Exception:
        return 0.0

def _invoice_status(inv: Dict[str, Any]) -> str:
    # tolerate many possible keys
    for k in ("status", "invoice_status", "payment_status"):
        if k in inv:
            return _lower(inv.get(k))
    return ""

def _amount_due(inv: Dict[str, Any]) -> float:
    # best-effort due/balance detection
    for k in ("due_amount", "balance", "amount_due"):
        if k in inv:
            return _num(inv.get(k))
    # fallback: total - amount_paid (if both present)
    total = 0.0
    for k in ("grand_total", "total", "amount"):
        if k in inv:
            total = _num(inv.get(k))
            break
    paid = 0.0
    for k in ("amount_paid", "paid_amount"):
        if k in inv:
            paid = _num(inv.get(k))
            break
    due = total - paid
    return due if due > 0 else 0.0

def _amount_paid(inv: Dict[str, Any]) -> float:
    # paid if explicit field exists
    for k in ("amount_paid", "paid_amount"):
        if k in inv:
            return _num(inv.get(k))
    # else, if invoice is marked paid, use total
    status = _invoice_status(inv)
    if status in PAID_STATUSES:
        for k in ("grand_total", "total", "amount"):
            if k in inv:
                return _num(inv.get(k))
    return 0.0

def get_kpis(
    invoices: List[Dict[str, Any]],
    jobs: List[Dict[str, Any]],
    customers: List[Dict[str, Any]],
    estimates: List[Dict[str, Any]],
) -> Dict[str, Any]:
    # Revenue = sum of paid amounts (robust across schemas)
    revenue = sum(_amount_paid(inv) for inv in (invoices or []))

    # Outstanding = sum of due/balance (robust across schemas)
    outstanding = sum(_amount_due(inv) for inv in (invoices or []))

    # Jobs booked = exclude cancelled if a status exists; else count all
    jobs_booked = 0
    for j in (jobs or []):
        status = _lower(j.get("status") or j.get("job_status"))
        if status and status in CANCELLED_STATUSES:
            continue
        jobs_booked += 1

    # Leads count = prefer estimates length; else customers with a lead_source; else 0
    if estimates:
        leads_count = len(estimates)
    else:
        leads_count = sum(1 for c in (customers or []) if c.get("lead_source") or c.get("leadSource"))

    return {
        # names your kpi_section can read (it’s tolerant, but we provide the common ones)
        "revenue": revenue,
        "outstanding_balance": outstanding,
        "jobs_booked": jobs_booked,
        "leads_count": leads_count,
        # optional alternates some code might look for
        "total_revenue": revenue,
        "total_jobs": jobs_booked,
        "new_customers": leads_count,
        "outstanding": outstanding,
    }

def get_charts_data(
    invoices: List[Dict[str, Any]],
    jobs: List[Dict[str, Any]],
    customers: List[Dict[str, Any]],
) -> Dict[str, Any]:
    # Minimal, safe payload for downstream charts
    return {
        "invoices_count": len(invoices or []),
        "jobs_count": len(jobs or []),
        "customers_count": len(customers or []),
    }
