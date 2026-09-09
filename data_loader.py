import json
import os
from datetime import datetime, date, timedelta
import math

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "officers.json")

def ymd_to_days(ymd):
    """Converts a (years, months, days) duration into days using 365 days/year and 30 days/month."""
    if not ymd or len(ymd) < 3:
        return 0
    return ymd[0] * 365 + ymd[1] * 30 + ymd[2]

def date_diff_calendar(start_d, end_d):
    """Calculates the difference between two dates as (years, months, days) following Methodology 2 (365/30 days)."""
    if start_d > end_d:
        return [0, 0, 0]
    days = (end_d - start_d).days
    return days_to_ymd(days)

def add_ymd(t1, t2):
    """Adds two YMD durations using Methodology 2 (converting to total days, then 365/30 conversion)"""
    d1 = ymd_to_days(t1)
    d2 = ymd_to_days(t2)
    return days_to_ymd(d1 + d2)

def sub_ymd(t1, t2):
    """Subtracts t2 from t1 using Methodology 2 (converting to total days, then 365/30 conversion)"""
    d1 = ymd_to_days(t1)
    d2 = ymd_to_days(t2)
    return days_to_ymd(max(0, d1 - d2))

def days_to_ymd(days):
    """Converts a number of days to YMD using administrative conversion (365 days/year, 30 days/month)"""
    if days <= 0:
        return [0, 0, 0]
    years = days // 365
    rem = days % 365
    months = rem // 30
    d = rem % 30
    return [years, months, d]

def calculate_officer_retirement(entry_date_str, ffaa_time, civil_time, current_date_str="02/09/2026"):
    """
    Calculates PMDF service, total service, toll, required service, remaining time and RR status
    following Methodology 2 (Official SIGRH / PMDF standard):
    - All service time is calculated in elapsed days.
    - External time (FFAA + Civil) is converted to days (365 days/year, 30 days/month).
    - Days are converted to (Years, Months, Days) using:
        years = days // 365
        months = (days % 365) // 30
        days = (days % 365) % 30
    - Toll (17%): floor(missing_days_at_cutoff * 0.17).
    - Required: 30 * 365 + toll_days.
    - Remaining: required_days - total_days.
    """
    # Parse dates
    entry_date = datetime.strptime(entry_date_str, '%d/%m/%Y').date()
    current_date = datetime.strptime(current_date_str, '%d/%m/%Y').date()
    
    # 1. PMDF Service in days
    pmdf_days = max(0, (current_date - entry_date).days)
    pmdf_time = days_to_ymd(pmdf_days)
    
    # 2. External Service & Total Service
    ffaa_days = ymd_to_days(ffaa_time)
    civil_days = ymd_to_days(civil_time)
    external_days = ffaa_days + civil_days
    
    total_days = pmdf_days + external_days
    total_time = days_to_ymd(total_days)
    
    # 3. Toll (Pedágio) - Cutoff 31/12/2019
    cutoff_date = date(2019, 12, 31)
    
    # Target: Entry Date + 30 calendar years
    try:
        target_date = entry_date.replace(year=entry_date.year + 30)
    except ValueError:
        # Handle leap year Feb 29 anniversary
        target_date = date(entry_date.year + 30, 2, 28)
        
    missing_days_at_cutoff = max(0, (target_date - cutoff_date).days - external_days)
    if missing_days_at_cutoff <= 0:
        toll_days = 0
    else:
        # Official SIGRH rule: floor(missing_days * 0.17)
        toll_days = math.floor(missing_days_at_cutoff * 0.17)
        
    toll_time = days_to_ymd(toll_days)
    
    # 4. Required Service = 30 Years (10.950 days) + Toll
    required_days = 30 * 365 + toll_days
    required_time = days_to_ymd(required_days)
    
    # 5. Remaining Time & RR Status
    if total_days >= required_days:
        rr_status = True
        missing_days = 0
        missing_time = [0, 0, 0]
        req_pmdf_days = max(0, required_days - external_days)
        apto_date = entry_date + timedelta(days=req_pmdf_days)
        predicted_date = f"Apto ({apto_date.strftime('%d/%m/%Y')})"
        predicted_date_sort = int(datetime.combine(apto_date, datetime.min.time()).timestamp() * 1000)
    else:
        rr_status = False
        missing_days = required_days - total_days
        missing_time = days_to_ymd(missing_days)
        pred_date = current_date + timedelta(days=missing_days)
        predicted_date = pred_date.strftime('%d/%m/%Y')
        predicted_date_sort = int(datetime.combine(pred_date, datetime.min.time()).timestamp() * 1000)
        
    return {
        'pmdf_time': pmdf_time,
        'total_time': total_time,
        'toll_time': toll_time,
        'required_time': required_time,
        'missing_time': missing_time,
        'rr_status': rr_status,
        'target_date': target_date.strftime('%d/%m/%Y'),
        'missing_days_at_cutoff': missing_days_at_cutoff,
        'toll_days': toll_days,
        'pmdf_days': pmdf_days,
        'total_days': total_days,
        'required_days': required_days,
        'missing_days': missing_days,
        'predicted_date': predicted_date,
        'predicted_date_sort': predicted_date_sort
    }

def load_officers():
    """Loads officers list from DB_PATH and calculates current data for all of them."""
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    today_str = date.today().strftime('%d/%m/%Y')
    for officer in data:
        # Re-calculate calculated fields based on current date
        calcs = calculate_officer_retirement(
            officer['entry_date'],
            officer['ffaa_time'],
            officer['civil_time'],
            officer.get('current_date') or today_str
        )
        officer.update(calcs)
        
    return data

def save_officers(officers_list):
    """Saves officers list to database/officers.json after stripping calculated fields."""
    today_str = date.today().strftime('%d/%m/%Y')
    stripped_list = []
    for off in officers_list:
        stripped = {
            'id': off['id'],
            'rank': off['rank'],
            'name': off['name'],
            'agregado': off['agregado'],
            'entry_date': off['entry_date'],
            'current_date': off.get('current_date') or today_str,
            'ffaa_time': off['ffaa_time'],
            'civil_time': off['civil_time']
        }
        stripped_list.append(stripped)
        
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(stripped_list, f, ensure_ascii=False, indent=2)

def calculate_major_vacancies(officers_list, total_quota=20):
    """
    Calculates vacancy statistics for the Major rank in QOPMA.
    - Total quota (Quadro Fixado): 20
    - Occupied: rank == 'MAJ' and not agregado
    - Aggregated (not occupying vacancy): rank == 'MAJ' and agregado
    - Available: max(0, total_quota - occupied)
    """
    majors_active = [o for o in officers_list if o.get('rank') == 'MAJ' and not o.get('agregado', False)]
    majors_aggregated = [o for o in officers_list if o.get('rank') == 'MAJ' and o.get('agregado', False)]
    majors_rr = [o for o in officers_list if o.get('rank') == 'MAJ RR']
    
    occupied = len(majors_active)
    available = max(0, total_quota - occupied)
    
    return {
        'total_quota': total_quota,
        'occupied': occupied,
        'aggregated': len(majors_aggregated),
        'majors_rr': len(majors_rr),
        'total_majors_active_cadre': len(majors_active) + len(majors_aggregated),
        'available': available
    }

