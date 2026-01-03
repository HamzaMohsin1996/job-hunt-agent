# Job Hunt Multi-Agent System

Run locally:
```bash
pip install -r requirements.txt
python app.py

---

## 2️⃣ `graph/` — the brain (MOST IMPORTANT)

### `graph/state.py`
```python
from pydantic import BaseModel
from typing import Optional, Dict

class JobHuntState(BaseModel):
    cv_text: str
    job_title: str
    job_description: str

    task: str  # cover | networking | review

    cover_letter: Optional[str] = None
    networking: Optional[Dict[str, str]] = None
    review: Optional[Dict] = None

    feedback: Optional[str] = None
    satisfied: bool = False
