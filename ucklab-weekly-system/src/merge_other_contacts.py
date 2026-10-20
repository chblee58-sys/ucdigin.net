"""
merge_other_contacts.py - Multi-format Contacts Parser and Merger for UCKLab
Intelligently parses mixed/pasted contacts exports (Naver, Daum, Outlook)
and merges newly found unique contacts into data/subscribers.csv.
"""

import os
import sys
import csv
import re

# Windows console UTF-8 setup
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SUBSCRIBERS_FILE = os.path.join(DATA_DIR, "subscribers.csv")
RAW_FILE = os.path.join(DATA_DIR, "other_contacts_raw.csv")

EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

# Automated system/service emails to exclude from human newsletter
SYSTEM_EMAILS = {
    "adobecustomercare@adobe.com",
    "daouoffice@daou.co.kr",
    "issn@korea.kr",
    "webmaster@smartmaker.com",
    "market@help.envato.com",
    "sppost@korea.kr"
}

def clean_cell(val: str) -> str:
    """Removes single quotes, double quotes, and whitespace common in Naver exports."""
    if not val:
        return ""
    v = val.strip().strip('"').strip("'").strip()
    return v

def is_clean_name(name: str) -> bool:
    """Checks if a name looks like a valid person or organization name without encoding artifacts."""
    if not name or len(name) < 2:
        return False
    # Check if mostly corrupted characters
    corrupted_count = name.count('') + name.count('?')
    if corrupted_count > 1:
        return False
    # Check if it's just phone digits
    if re.match(r'^[\d\s\-\+\/\.]+$', name):
        return False
    return True

def merge_contacts():
    if not os.path.exists(RAW_FILE):
        print(f"❌ 파일을 찾을 수 없습니다: {RAW_FILE}")
        return

    # 1. Load existing subscribers
    existing_emails = set()
    existing_rows = []
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                em = r.get("email", "").strip().lower()
                if em:
                    existing_emails.add(em)
                    existing_rows.append(r)

    print(f"📊 기존 등록 구독자: {len(existing_rows)}명")

    # 2. Parse RAW_FILE
    with open(RAW_FILE, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    added_count = 0
    skipped_dup = 0
    skipped_system = 0

    for line_num, raw_line in enumerate(lines, 1):
        line = raw_line.strip()
        if not line:
            continue

        # Find all emails in this line
        emails_found = EMAIL_REGEX.findall(line)
        if not emails_found:
            continue

        for raw_email in emails_found:
            email = raw_email.lower().strip()

            # Skip system / spam / bounce emails
            if email in SYSTEM_EMAILS or "vresp.com" in email or email.startswith("+"):
                skipped_system += 1
                continue

            # Skip duplicates
            if email in existing_emails:
                skipped_dup += 1
                continue

            # Determine Name
            name = ""
            org = ""

            # Check if Naver format line (starts with quotes and commas)
            if '"\'' in line or "','전" in line or "','현" in line:
                parts = line.split(",")
                if len(parts) >= 8:
                    last_n = clean_cell(parts[0])
                    first_n = clean_cell(parts[1])
                    if last_n and first_n:
                        name = f"{last_n}{first_n}"
                    elif first_n:
                        name = first_n
                    elif last_n:
                        name = last_n

            # If name not yet found, check CSV columns
            if not is_clean_name(name):
                parts = line.split(",")
                candidate = clean_cell(parts[0])
                if candidate and candidate != raw_email and is_clean_name(candidate):
                    name = candidate

            # If still no valid name (e.g. was corrupted or empty)
            if not is_clean_name(name):
                # Use local part of email formatted nicely
                local_part = email.split("@")[0]
                local_part = re.sub(r'[\d_\.-]+', ' ', local_part).strip()
                name = local_part.title() if local_part else "구독자"

            # Check for organization hints in line
            if "교회" in line:
                match = re.search(r'([가-힣A-Za-z0-9]+교회)', line)
                if match:
                    org = match.group(1)
            elif "연구" in line or "협회" in line or "재단" in line:
                match = re.search(r'([가-힣A-Za-z0-9]+(연구소|협회|재단|사무국))', line)
                if match:
                    org = match.group(1)

            existing_rows.append({
                "email": email,
                "name": name,
                "organization": org,
                "group": "PortalContacts"
            })
            existing_emails.add(email)
            added_count += 1

    # 3. Write back to subscribers.csv
    with open(SUBSCRIBERS_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["email", "name", "organization", "group"])
        writer.writeheader()
        writer.writerows(existing_rows)

    print("\n=======================================================")
    print("✅ [주소록 통합 완료] 추가 연락처 파싱 및 구독자 명단 갱신")
    print("=======================================================")
    print(f"  • 신규 추가된 구독자: {added_count}명")
    print(f"  • 중복 제외 (기존 등록): {skipped_dup}건")
    print(f"  • 시스템/무효 메일 제외: {skipped_system}건")
    print(f"  • 최종 총 구독자 수: {len(existing_rows)}명")
    print(f"  • 저장 파일: {SUBSCRIBERS_FILE}")
    print("=======================================================\n")

if __name__ == "__main__":
    merge_contacts()
