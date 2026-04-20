import os
import google.generativeai as genai
import subprocess

# 1. تهيئة الوكيل
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro')

def get_data():
    # جلب الفروقات في الكود
    diff = subprocess.check_output(['git', 'diff']).decode('utf-8')
    # جلب نص المهمة المطلوبة
    with open('current_task.md', 'r') as f:
        task = f.read()
    return diff, task

def ops_review():
    diff, task = get_data()
    
    if not diff:
        print("✅ No changes detected.")
        return

    prompt = f"""
    You are the Ops & Quality Agent for 'Wobbly Waiter'. 
    I will provide you with the 'Requested Task' and the 'Actual Code Changes (Diff)'.
    
    [Requested Task]:
    {task}
    
    [Actual Code Changes]:
    {diff}
    
    Your Goals:
    1. Compare the implementation with the request. Did Trae follow all instructions?
    2. Check if 'window.gameState' was used correctly as per .traerules.
    3. Generate a professional Git Commit message in ENGLISH summarizing the changes.
    
    Output Format:
    - Status: (Success/Partial/Failed)
    - Review: (Brief notes on implementation)
    - Commit Message: (English text only)
    """
    
    response = model.generate_content(prompt)
    print("🤖 Ops Agent Review:\n", response.text)

if __name__ == "__main__":
    ops_review()
