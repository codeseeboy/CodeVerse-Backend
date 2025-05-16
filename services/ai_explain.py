import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_code_explanation(code: str, language: str) -> str:
    """Get an explanation of code using DeepSeek AI."""
    try:
        api_key = os.getenv('DEEPSEEK_API_KEY')
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        prompt = (
            f"Explain the following {language} code in a clear and concise way for a beginner:\n\n{code}"
        )
        data = {
            "model": "deepseek-coder",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 512
        }
        response = requests.post(url, headers=headers, json=data, timeout=15)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Could not generate explanation: {str(e)}" 