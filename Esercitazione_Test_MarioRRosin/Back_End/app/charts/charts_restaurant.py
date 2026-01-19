import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text


DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "restaurant")

# Set this to True if you want to include cancelled bookings in charts
INCLUDE_CANCELLED = False

# If my months are: December (previous year), January (current year), February (current year)
# Example: 2025-12, 2026-01, 2026-02
TARGET_MONTHS = [
    ("December", 12, 2025),
    ("January", 1, 2026),
    ("February", 2, 2026),
]

# Time slots for "fascia oraria" (customize as you like)
TIME_SLOTS = [
    ("Lunch (12:00-14:59)", "12:00:00", "14:59:59"),
    ("Afternoon (15:00-18:59)", "15:00:00", "18:59:59"),
    ("Dinner (19:00-22:59)", "19:00:00", "22:59:59"),
    ("Late (23:00-23:59)", "23:00:00", "23:59:59"),
]


def make_engine():
    url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url, pool_pre_ping=True)


def fetch_bookings(engine) -> pd.DataFrame:
    status_filter = "" if INCLUDE_CANCELLED else "AND b.status <> 'cancelled'"

    sql = text(f"""
        SELECT
            b.id,
            b.table_id,
            b.reservation_date,
            b.day_of_week,
            b.reservation_time,
            b.guest_count,
            b.status,
            t.max_capacity
        FROM bookings b
        JOIN `tables` t ON t.id = b.table_id
        WHERE 1=1
        {status_filter}
    """)

    with engine.connect() as conn:
        df = pd.read_sql(sql, conn)

    # Ensure proper dtypes
    df["reservation_date"] = pd.to_datetime(df["reservation_date"])
    # reservation_time can arrive as timedelta or time; normalize to time safely
    if pd.api.types.is_timedelta64_dtype(df["reservation_time"]):
        df["reservation_time"] = (pd.to_datetime("1970-01-01") + df["reservation_time"]).dt.time
    else:
        df["reservation_time"] = pd.to_datetime(df["reservation_time"].astype(str)).dt.time

    return df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    # Hour extracted from reservation_time
    df = df.copy()
    df["hour"] = df["reservation_time"].apply(lambda t: t.hour)
    # occupancy ratio: guests / capacity (cap at 1.0 just in case)
    df["occupancy_ratio"] = (df["guest_count"] / df["max_capacity"]).clip(lower=0, upper=1)
    # month key
    df["month_key"] = df["reservation_date"].dt.to_period("M").astype(str)
    return df


def plot_avg_occupancy_by_time_slot(df: pd.DataFrame):
    # Build slot label for each booking
    def slot_for_time(t):
        hhmmss = f"{t.hour:02d}:{t.minute:02d}:{t.second:02d}"
        for label, start, end in TIME_SLOTS:
            if start <= hhmmss <= end:
                return label
        return "Other"

    tmp = df.copy()
    tmp["time_slot"] = tmp["reservation_time"].apply(slot_for_time)

    agg = (
        tmp.groupby("time_slot", as_index=False)["occupancy_ratio"]
        .mean()
        .sort_values("occupancy_ratio", ascending=False)
    )

    plt.figure()
    plt.bar(agg["time_slot"], agg["occupancy_ratio"])
    plt.title("Average Table Occupancy by Time Slot")
    plt.ylabel("Average Occupancy (guests / capacity)")
    plt.xticks(rotation=25, ha="right")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.show()


def plot_bookings_by_day_of_week(df: pd.DataFrame):
    # Your DB stores day_of_week as ENUM('Monday',...,'Sunday')
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    counts = df["day_of_week"].value_counts().reindex(day_order).fillna(0).astype(int)

    plt.figure()
    plt.bar(counts.index, counts.values)
    plt.title("Bookings by Day of Week")
    plt.ylabel("Number of Bookings")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.show()


def plot_booking_trends_last_3_months(df: pd.DataFrame):
    # Filter to the requested months (Dec, Jan, Feb with explicit years)
    month_keys = []
    pretty_labels = []
    for name, month_num, year in TARGET_MONTHS:
        month_keys.append(f"{year:04d}-{month_num:02d}")
        pretty_labels.append(f"{name} {year}")

    tmp = df[df["month_key"].isin(month_keys)].copy()

    # Daily trend within those months
    daily = (
        tmp.groupby(tmp["reservation_date"].dt.date, as_index=False)
        .size()
        .rename(columns={"size": "bookings"})
        .sort_values("reservation_date")
    )

    plt.figure()
    plt.plot(daily["reservation_date"], daily["bookings"])
    plt.title("Booking Trend (Daily) - December / January / February")
    plt.ylabel("Bookings per day")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.show()

    # Monthly totals for Dec/Jan/Feb
    monthly = (
        tmp.groupby("month_key", as_index=False)
        .size()
        .rename(columns={"size": "bookings"})
        .sort_values("month_key")
    )

    # Ensure all months appear even if zero
    monthly_full = pd.DataFrame({"month_key": month_keys}).merge(monthly, on="month_key", how="left").fillna(0)
    monthly_full["bookings"] = monthly_full["bookings"].astype(int)

    plt.figure()
    plt.bar(pretty_labels, monthly_full["bookings"])
    plt.title("Booking Totals - December / January / February")
    plt.ylabel("Number of Bookings")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.show()


def main():
    engine = make_engine()
    df = fetch_bookings(engine)

    if df.empty:
        print("No bookings found with the current filters.")
        return

    df = add_time_features(df)

    # 1) Average occupancy by time slot
    plot_avg_occupancy_by_time_slot(df)

    # 2) Bookings by day of week
    plot_bookings_by_day_of_week(df)

    # 3) Trends in last 3 months: Dec/Jan/Feb (explicit years in TARGET_MONTHS)
    plot_booking_trends_last_3_months(df)


if __name__ == "__main__":
    main()
