import re

def extract_job_metadata(job_text: str):
    """
    Very simple heuristics to infer job title and company.
    Works well for most postings.
    """
    lines = [l.strip() for l in job_text.splitlines() if l.strip()]

    job_title = lines[0] if lines else "Job Application"

    company = "Company"
    for line in lines[:15]:
        if re.search(r"at\s+[A-Z][A-Za-z0-9& ]+", line):
            company = line.split("at")[-1].strip()
            break

    return job_title[:80], company[:80]
