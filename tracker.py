import json
import datetime
from typing import List, Dict

JOB_STAGES = ["Applied", "Interview", "Assessment", "Offer", "Rejected"]
DATA_FILE = "jobs.json"

def clear_jobs(index):
    jobs = list_jobs()
    if 0 <= index < len(jobs):
        del jobs[index]
        save_jobs(jobs)

def load_jobs() -> List[Dict]:
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_jobs(jobs: List[Dict]) -> None:
    with open(DATA_FILE, "w") as file:
        json.dump(jobs, file, indent=4)


def add_job(company: str, role: str) -> None:
    jobs = load_jobs()
    jobs.append({
        "company": company,
        "role": role,
        "applied_date": datetime.date.today().isoformat(),
        "status": JOB_STAGES[0]  # Start with "Applied"
    })
    save_jobs(jobs)


def list_jobs() -> List[Dict]:
    return load_jobs()


def update_status(index: int, new_status: str) -> None:
    jobs = load_jobs()
    if 0 <= index < len(jobs):
        jobs[index]["status"] = new_status
        save_jobs(jobs)
