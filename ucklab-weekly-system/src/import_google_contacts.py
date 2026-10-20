"""
import_google_contacts.py - Google Contacts CSV to UCKLab Subscribers Converter
Reads standard Google Contacts export CSV and merges it into data/subscribers.csv.
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

def is_korean(text: str) -> bool:
    """Checks if text contains Korean characters."""
    return bool(re.search(r'[가-힣]', text))

def clean_contact_name(first_name: str, middle_name: str, last_name: str, email: str) -> str:
    """Combines first, middle, last name into a natural, respectful Korean or International format."""
    f = (first_name or "").strip()
    m = (middle_name or "").strip()
    l = (last_name or "").strip()

    # If first_name contains email, don't use it as name
    if "@" in f:
        f = ""

    # Case 1: Korean name combination (e.g. 성: 계, 이름: 혜영 -> 계혜영)
    if is_korean(f) or is_korean(l):
        if l and f:
            return f"{l}{f}"
        elif f:
            return f
        elif l:
            return l

    # Case 2: Western / Latin name combination
    name_parts = [p for p in [f, m, l] if p]
    if name_parts:
        return " ".join(name_parts)

    # Fallback to local part of email
    if email and "@" in email:
        local_part = email.split("@")[0]
        return local_part.capitalize()
    return "구독자"

def import_contacts(source_csv_path: str):
    """
    Imports Google Contacts exported CSV into UCKLab subscribers.csv.
    """
    if not os.path.exists(source_csv_path):
        print(f"❌ 파일을 찾을 수 없습니다: {source_csv_path}")
        return False

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

    added_count = 0
    encodings = ["utf-8-sig", "utf-8", "cp949"]
    parsed = False

    for enc in encodings:
        try:
            with open(source_csv_path, "r", encoding=enc) as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames or []

                for row in reader:
                    # 1. Extract email from any email field
                    email = (row.get("E-mail 1 - Value") or row.get("이메일") or row.get("Email") or row.get("E-mail") or "").strip()
                    if not email:
                        email = (row.get("E-mail 2 - Value") or row.get("이메일 2") or "").strip()
                    if not email:
                        for k, v in row.items():
                            if k and any(x in k.lower() for x in ["e-mail", "email", "이메일", "메일"]) and v and "@" in v:
                                email = v.strip()
                                break
                    if not email:
                        for v in row.values():
                            if v and "@" in v and "." in v:
                                email = v.strip()
                                break

                    if not email or "@" not in email:
                        continue

                    # If multiple emails separated by ::: or ; or ,
                    if ":::" in email:
                        email = email.split(":::")[0].strip()
                    elif ";" in email:
                        email = email.split(";")[0].strip()

                    email_clean = email.strip("<>").strip()
                    email_lower = email_clean.lower()

                    if email_lower in existing_emails:
                        continue

                    # 2. Extract Name (Supports Google, Naver, Daum, Outlook)
                    first_name = row.get("First Name") or row.get("이름") or row.get("Name") or row.get("성명") or ""
                    middle_name = row.get("Middle Name") or ""
                    last_name = row.get("Last Name") or row.get("성") or ""
                    name = clean_contact_name(first_name, middle_name, last_name, email_clean)

                    # 3. Extract Organization & Title
                    org_name = (row.get("Organization Name") or row.get("회사") or row.get("직장") or row.get("소속") or row.get("회사명") or row.get("Company") or "").strip()
                    org_title = (row.get("Organization Title") or row.get("직책") or row.get("직위") or row.get("Job Title") or "").strip()
                    if org_name and org_title:
                        organization = f"{org_name} ({org_title})"
                    elif org_name:
                        organization = org_name
                    elif org_title:
                        organization = org_title
                    else:
                        organization = ""

                    # 4. Extract Group/Category
                    labels = (row.get("Labels") or "").strip()
                    group = "VIP" if "starred" in labels.lower() else "GoogleContacts"

                    existing_rows.append({
                        "email": email_clean,
                        "name": name,
                        "organization": organization,
                        "group": group
                    })
                    existing_emails.add(email_lower)
                    added_count += 1

            parsed = True
            break
        except Exception as e:
            continue

    if not parsed:
        print(f"❌ CSV 파일 처리 실패: {source_csv_path}")
        return False

    with open(SUBSCRIBERS_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["email", "name", "organization", "group"])
        writer.writeheader()
        writer.writerows(existing_rows)

    print(f"\n=======================================================")
    print(f"✅ [Google Contacts Importer] 구글 주소록 구독자 연동 완료!")
    print(f"=======================================================")
    print(f"  • 원본 파일: {source_csv_path}")
    print(f"  • 신규 추가 구독자: {added_count}명")
    print(f"  • 총 등록 구독자: {len(existing_rows)}명")
    print(f"  • 저장 위치: {SUBSCRIBERS_FILE}")
    print(f"=======================================================\n")
    return True

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(DATA_DIR, "google_contacts_export.csv")
    import_contacts(target)
