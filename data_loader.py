import json
import os
from datetime import datetime, date
import math

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "officers.json")

def date_diff_calendar(start_d, end_d):
    """Calculates the exact calendar difference between two dates as (years, months, days)"""
    if start_d > end_d:
        return (0, 0, 0)
    
    years = end_d.year - start_d.year
    months = end_d.month - start_d.month
    days = end_d.day - start_d.day
    
    if days < 0:
        # Borrow days from the previous month
        # Find the number of days in the previous month of end_d
        prev_month = end_d.month - 1 if end_d.month > 1 else 12
        prev_year = end_d.year if end_d.month > 1 else end_d.year - 1
        
        # In administrative calendar diff, it's common to borrow the actual number of days in the previous month
        # Let's determine the last day of the previous month:
        if prev_month in [1, 3, 5, 7, 8, 10, 12]:
            days_in_prev = 31
        elif prev_month in [4, 6, 9, 11]:
            days_in_prev = 30
        else:
            # February
            is_leap = (prev_year % 4 == 0 and prev_year % 100 != 0) or (prev_year % 400 == 0)
            days_in_prev = 29 if is_leap else 28
            
        days += days_in_prev
        months -= 1
        
    if months < 0:
        months += 12
        years -= 1
        
    return (years, months, days)

def add_ymd(t1, t2):
    """Adds two YMD durations using administrative math (30 days = 1 month, 12 months = 1 year)"""
    y1, m1, d1 = t1
    y2, m2, d2 = t2
    
    d_total = d1 + d2
    d_rem = d_total % 30
    d_carry = d_total // 30
    
    m_total = m1 + m2 + d_carry
    m_rem = m_total % 12
    m_carry = m_total // 12
    
    y_total = y1 + y2 + m_carry
    return [y_total, m_rem, d_rem]

def sub_ymd(t1, t2):
    """Subtracts t2 from t1 using administrative math (borrowing 30 days/month, 12 months/year). Returns (0, 0, 0) if t1 <= t2."""
    if list(t1) <= list(t2):
        return [0, 0, 0]
        
    y1, m1, d1 = t1
    y2, m2, d2 = t2
    
    if d1 < d2:
        d1 += 30
        m1 -= 1
    d_diff = d1 - d2
    
    if m1 < m2:
        m1 += 12
        y1 -= 1
    m_diff = m1 - m2
    
    y_diff = y1 - y2
    return [y_diff, m_diff, d_diff]

def days_to_ymd(days):
    """Converts a number of days to YMD using administrative conversion (365 days/year, 30 days/month)"""
    if days <= 0:
        return [0, 0, 0]
    years = days // 365
    rem = days % 365
    months = rem // 30
    d = rem % 30
    return [years, months, d]

def calculate_officer_retirement(entry_date_str, ffaa_time, civil_time, current_date_str="19/08/2026"):
    """Calculates PMDF service, total service, toll, required service, remaining time and RR status."""
    # Parse dates
    entry_date = datetime.strptime(entry_date_str, '%d/%m/%Y').date()
    current_date = datetime.strptime(current_date_str, '%d/%m/%Y').date()
    
    # 1. PMDF Service
    pmdf_time = date_diff_calendar(entry_date, current_date)
    
    # 2. Total Service = PMDF + FFAA + Civil
    total_time = add_ymd(pmdf_time, ffaa_time)
    total_time = add_ymd(total_time, civil_time)
    
    # 3. Toll (Pedágio)
    cutoff_date = date(2019, 12, 31)
    
    # Target: Entry Date + 30 calendar years
    try:
        target_date = entry_date.replace(year=entry_date.year + 30)
    except ValueError:
        # Handle leap year Feb 29 anniversary
        target_date = date(entry_date.year + 30, 2, 28)
        
    missing_days = (target_date - cutoff_date).days
    if missing_days <= 0:
        toll_days = 0
    else:
        # Rule determined: round(missing_days * 0.17)
        toll_days = int(round(missing_days * 0.17))
        
    toll_time = days_to_ymd(toll_days)
    
    # 4. Required Service = 30 Years + Toll
    required_time = add_ymd([30, 0, 0], toll_time)
    
    # 5. Remaining Time & RR Status
    if list(total_time) >= list(required_time):
        rr_status = True
        missing_time = [0, 0, 0]
    else:
        rr_status = False
        missing_time = sub_ymd(required_time, total_time)
        
    return {
        'pmdf_time': pmdf_time,
        'total_time': total_time,
        'toll_time': toll_time,
        'required_time': required_time,
        'missing_time': missing_time,
        'rr_status': rr_status,
        'target_date': target_date.strftime('%d/%m/%Y'),
        'missing_days_at_cutoff': max(0, missing_days),
        'toll_days': toll_days
    }

def load_officers():
    """Loads officers list from DB_PATH and calculates current data for all of them."""
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for officer in data:
        # Re-calculate calculated fields based on current date
        calcs = calculate_officer_retirement(
            officer['entry_date'],
            officer['ffaa_time'],
            officer['civil_time'],
            officer.get('current_date', '19/08/2026')
        )
        officer.update(calcs)
        
    return data

def save_officers(officers_list):
    """Saves officers list to database/officers.json after stripping calculated fields."""
    stripped_list = []
    for off in officers_list:
        stripped = {
            'id': off['id'],
            'rank': off['rank'],
            'name': off['name'],
            'agregado': off['agregado'],
            'entry_date': off['entry_date'],
            'current_date': off.get('current_date', '19/08/2026'),
            'ffaa_time': off['ffaa_time'],
            'civil_time': off['civil_time']
        }
        stripped_list.append(stripped)
        
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(stripped_list, f, ensure_ascii=False, indent=2)
