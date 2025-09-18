import json, os
import pandas as pd

# All JSON files expected at project root (same level as main.py)
DATA_FOLDER = "ERROR"

FILES = {
    "invoices": "invoices_data.json",
    "jobs": "jobs_data.json",
    "customers": "customers_data.json",
    "estimates": "estimates_data.json",
}

def _safe_load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def load_data():
    invoices = _safe_load(os.path.join(DATA_FOLDER, FILES["invoices"]))
    jobs = _safe_load(os.path.join(DATA_FOLDER, FILES["jobs"]))
    customers = _safe_load(os.path.join(DATA_FOLDER, FILES["customers"]))
    estimates = _safe_load(os.path.join(DATA_FOLDER, FILES["estimates"]))
    return invoices, jobs, customers, estimates

def get_kpis(invoices, jobs, customers, estimates):
    df_inv = pd.DataFrame(invoices)
    revenue = float(df_inv.get("amount", pd.Series(dtype=float)).fillna(0).sum()) if not df_inv.empty else 0.0
    outstanding = float(df_inv.get("due_amount", pd.Series(dtype=float)).fillna(0).sum()) if not df_inv.empty else 0.0
    jobs_booked = len(jobs)
    leads_count = len(customers)
    return {
        "revenue": revenue,
        "outstanding_balance": outstanding,
        "jobs_booked": jobs_booked,
        "leads_count": leads_count,
    }

def _to_naive(ts):
    """Convert to pandas Timestamp (tz-naive). Returns pd.NaT on failure."""
    try:
        t = pd.to_datetime(ts, errors="coerce")
        if pd.isna(t):
            return pd.NaT
        # If a DatetimeIndex/Timestamp with tz, strip it
        try:
            return t.tz_localize(None)
        except Exception:
            # Already tz-naive
            return t
    except Exception:
        return pd.NaT

def apply_filters(invoices, jobs, customers, estimates, filters):
    # Normalize the sidebar date inputs (which may be date objects) to tz-naive Timestamps
    date_from = _to_naive(filters.get("date_from")) if filters else None
    date_to = _to_naive(filters.get("date_to")) if filters else None
    search = (filters.get("search") or "").strip().lower() if filters else ""
    lead_sources = set(filters.get("lead_sources") or []) if filters else set()
    job_statuses = set(filters.get("job_statuses") or []) if filters else set()

    # Invoices by date & search
    if invoices:
        for inv in invoices:
            inv["_dt"] = _to_naive(inv.get("invoice_date"))
        if date_from is not None or date_to is not None:
            invoices = [
                i for i in invoices
                if (not pd.isna(i.get("_dt")))
                and (date_from is None or i["_dt"] >= date_from)
                and (date_to is None or i["_dt"] <= date_to)
            ]
        if search:
            invoices = [i for i in invoices if search in json.dumps(i).lower()]

    # Jobs by status & search & created_at
    if jobs:
        for j in jobs:
            j["_dt"] = _to_naive(j.get("created_at"))
        if job_statuses:
            jobs = [j for j in jobs if (j.get("work_status") or "Unknown") in job_statuses]
        if date_from is not None or date_to is not None:
            jobs = [
                j for j in jobs
                if (not pd.isna(j.get("_dt")))
                and (date_from is None or j["_dt"] >= date_from)
                and (date_to is None or j["_dt"] <= date_to)
            ]
        if search:
            jobs = [j for j in jobs if search in json.dumps(j).lower()]

    # Customers by lead source & search & created_at
    if customers:
        for c in customers:
            c["_dt"] = _to_naive(c.get("created_at"))
        if lead_sources:
            customers = [c for c in customers if (c.get("lead_source") or "Unknown") in lead_sources]
        if date_from is not None or date_to is not None:
            customers = [
                c for c in customers
                if (not pd.isna(c.get("_dt")))
                and (date_from is None or c["_dt"] >= date_from)
                and (date_to is None or c["_dt"] <= date_to)
            ]
        if search:
            customers = [c for c in customers if search in json.dumps(c).lower()]

    return invoices, jobs, customers, estimates

def get_unique_options(jobs, customers):
    """Return sorted unique job statuses and lead sources for populating filters."""
    js = sorted(list({(j.get("work_status") or "Unknown") for j in (jobs or [])}))
    ls = sorted(list({(c.get("lead_source") or "Unknown") for c in (customers or [])}))
    return js, ls

def get_charts_data(invoices, jobs, customers, estimates, chart):
    import pandas as pd
    if chart == "revenue_by_job":
        df_jobs = pd.DataFrame(jobs)
        if not df_jobs.empty and "description" in df_jobs.columns:
            df_jobs["revenue"] = pd.to_numeric(df_jobs.get("total_amount", 0)).fillna(0)
            return df_jobs.groupby("description", as_index=False)["revenue"].sum().rename(columns={"description":"job"}).sort_values("revenue", ascending=False)
        return pd.DataFrame()
    elif chart == "revenue_by_source":
        rows = []
        for job in jobs:
            rows.append({"source": job.get("customer",{}).get("lead_source") or "Unknown", "revenue": job.get("total_amount") or 0})
        df = pd.DataFrame(rows)
        if df.empty: return df
        return df.groupby("source", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    elif chart == "revenue_trend":
        df = pd.DataFrame(invoices)
        if df.empty or "invoice_date" not in df: return pd.DataFrame()
        df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce").dt.tz_localize(None)
        df["amount"] = pd.to_numeric(df.get("amount", 0)).fillna(0)
        trend = df.groupby(df["invoice_date"].dt.date)["amount"].sum().reset_index()
        trend.columns = ["date", "revenue"]
        return trend.sort_values("date")
    elif chart == "jobs_status":
        df = pd.DataFrame(jobs)
        if df.empty or "work_status" not in df: return pd.DataFrame()
        out = df["work_status"].fillna("Unknown").value_counts().reset_index()
        out.columns = ["status", "count"]
        return out
    elif chart == "leads_by_source":
        df = pd.DataFrame(customers)
        if df.empty: return pd.DataFrame()
        out = df.get("lead_source", pd.Series(dtype=str)).fillna("Unknown").value_counts().reset_index()
        out.columns = ["source", "count"]
        return out
    elif chart == "leads_trend":
        df = pd.DataFrame(customers)
        if df.empty or "created_at" not in df: return pd.DataFrame()
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce").dt.tz_localize(None)
        out = df.groupby(df["created_at"].dt.date).size().reset_index(name="leads")
        out.columns = ["date", "leads"]
        return out.sort_values("date")
    return pd.DataFrame()
