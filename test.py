import requests
import json
import subprocess
import time
import os

# الرابط المستهدف للتحقق من الطاقة
url = "https://gold-eagle-api.fly.dev/user/me/progress"

# الرؤوس المحدثة بناءً على الطلب السابق
headers = {
    "sec-ch-ua-platform": "Windows",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
    "accept": "application/json, text/plain, */*",
    "sec-ch-ua": 'Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
    "sec-ch-ua-mobile": "?0",
    "origin": "https://telegram.geagle.online",
    "sec-fetch-site": "cross-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://telegram.geagle.online/",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "ar, en;q=0.9, en-GB;q=0.8, en-US;q=0.7",
    "priority": "u=1, i"
}

# قراءة التوكنات من ملف
def read_tokens(file_path):
    tokens = []
    try:
        with open(file_path, "r") as file:
            tokens = [line.strip() for line in file if line.strip()]  # إزالة الأسطر الفارغة
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"Error reading file: {e}")
    return tokens

# كتابة التوكنات إلى ملف
def write_tokens(file_path, tokens):
    try:
        with open(file_path, "w") as file:
            for token in tokens:
                file.write(token + "\n")
    except Exception as e:
        print(f"Error writing to file {file_path}: {e}")

# التحقق من الطاقة لتوكن معين مع معالجة أفضل للأخطاء
def check_energy(token):
    headers = {
    'authorization': f'{token}',
    "accept": "application/json, text/plain, */*"
}
    headers["authorization"] = f"Bearer {token}"
    max_retries = 3  # عدد المحاولات
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            # التحقق من رمز الحالة
            if response.status_code != 200:
                print(f"Token: {token[:10]}... | Failed to fetch energy, Status Code: {response.status_code}")
                print(f"Response Text: {response.text}")
                if attempt < max_retries - 1:
                    print(f"Retrying in 5 seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(5)
                continue

            # محاولة تحويل الرد إلى JSON
            try:
                data = response.json()
                energy = data.get("energy", 0)
                print(f"Token: {token[:10]}... | Energy: {energy}")
                return energy
            except ValueError as e:
                print(f"Token: {token[:10]}... | Error decoding JSON: {e}")
                print(f"Response Text: {response.text}")
                if attempt < max_retries - 1:
                    print(f"Retrying in 5 seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(5)
                continue

        except requests.exceptions.RequestException as e:
            print(f"Token: {token[:10]}... | Error checking energy: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in 5 seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(5)
            continue
    
    print(f"Token: {token[:10]}... | Max retries reached. Could not fetch energy.")
    return None

# تشغيل الكود المشفر لمدة محددة بناءً على عدد التوكنات
def run_encrypted_script(token_count):
    # حساب المدة الزمنية بناءً على عدد التوكنات (15 ثانية لكل توكن)
    run_duration = token_count * 7  # المدة بالثواني
    print(f"Running encrypted script for {run_duration} seconds ({token_count} tokens, 7 seconds each)...")

    try:
        # تحديد مسار العمل
        working_dir = r"G:\neew\free"
        # نسخ متغيرات البيئة الحالية
        env = os.environ.copy()
        
        # تشغيل الكود المشفر كعملية منفصلة
        process = subprocess.Popen(
            ["python", "gold-a.py"],  # استبدل "python" بـ "python3.9" إذا لزم الأمر
            cwd=working_dir,  # تحديد مجلد العمل
            env=env  # تمرير متغيرات البيئة
        )

        # الانتظار للمدة المحددة
        time.sleep(run_duration)

        # إيقاف الكود المشفر
        process.terminate()
        try:
            process.wait(timeout=5)  # الانتظار لمدة 5 ثوانٍ للتأكد من الإغلاق
            print("Encrypted script terminated successfully.")
        except subprocess.TimeoutExpired:
            print("Encrypted script did not terminate gracefully. Forcing termination...")
            process.kill()  # إجبار العملية على الإغلاق إذا لم تتوقف

    except Exception as e:
        print(f"Error running encrypted script: {e}")
        if process.poll() is None:  # التحقق مما إذا كانت العملية لا تزال قيد التشغيل
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

# الدالة الرئيسية
def main():
    # مسار الملف الأصلي (dataa.txt) والملف المستخدم (data.txt)
    original_file = "dataa.txt"
    working_file = "data.txt"
    
    while True:
        print("\n=== Starting new cycle ===")
       
        # قراءة جميع التوكنات من الملف الأصلي
        tokens = read_tokens(original_file)
        
        if not tokens:
            print(f"No tokens found in {original_file}. Exiting...")
            return
        
        # التحقق من الطاقة لكل توكن
        tokens_to_process = []
        for token in tokens:
            energy = check_energy(token)
            if energy is not None and energy > 900:
                tokens_to_process.append(token)
            # إضافة تأخير بين الطلبات لتجنب الحظر
            time.sleep(1)  # تأخير 1 ثانية بين كل طلب
        
        # إذا لم يكن هناك توكنات بطاقة 1000، انتظر 17 دقيقة وكرر
        if not tokens_to_process:
            print("No accounts with energy = 1000. Sleeping for 17 minutes...")
            time.sleep(15 * 60)  # 17 دقيقة = 1020 ثانية
            continue
        
        # كرر حتى لا يتبقى أي حساب بطاقة 1000
        while tokens_to_process:
            print(f"\nFound {len(tokens_to_process)} accounts with energy = 1000. Processing...")
            
            # كتابة التوكنات التي تحتاج إلى معالجة في data.txt
            write_tokens(working_file, tokens_to_process)
            
            # تشغيل الكود المشفر لمدة محددة بناءً على عدد التوكنات
            print("Running encrypted script...")
            run_encrypted_script(len(tokens_to_process))
            
            # إعادة التحقق من الطاقة لنفس الحسابات
            remaining_tokens = []
            for token in tokens_to_process:
                energy = check_energy(token)
                if energy is not None and energy == 1000:
                    remaining_tokens.append(token)
                # إضافة تأخير بين الطلبات
                time.sleep(1)  # تأخير 1 ثانية بين كل طلب
            
            # تحديث القائمة للحسابات التي لا تزال تحتاج إلى معالجة
            tokens_to_process = remaining_tokens
        
        # بعد الانتهاء، انتظر 17 دقيقة وكرر العملية
        print("All accounts processed. Sleeping for 17 minutes...")
        time.sleep(14 * 60)  # 17 دقيقة = 1020 ثانية

if __name__ == "__main__":
    main()