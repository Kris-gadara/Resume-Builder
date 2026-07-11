import os
import re
import time

from google import genai
import yaml


_client = None


def configure_gemini():
    global _client
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if api_key:
        _client = genai.Client(api_key=api_key)
    return api_key


configure_gemini()


def extract_skills_from_job(job_description, current_skills, max_retries=3, retry_delay=2):
    """Extract skills from a job description with a retry mechanism."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Set GEMINI_API_KEY in the environment or in the Streamlit sidebar.")

    attempt = 0
    while attempt < max_retries:
        try:
            prompt = f"""
            Below is a list of skills grouped by categories. Restructure this list into
            a similar format, add any relevant missing skills, and ensure proper organization.

            Current Skills:
            {yaml.dump(current_skills)}

            Based on the following job description, extract the key technical and soft skills:

            {job_description}

            Format the response in YAML with categories like Programming Languages, AI/ML Frameworks,
            AI Techniques, etc. Ensure it includes both the original and additional skills.
            """
            global _client
            if _client is None:
                _client = genai.Client(api_key=api_key)

            response = _client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            raw_content = response.text
            match = re.search(r"```yaml\n(.*?)\n```", raw_content, re.DOTALL)
            if match:
                yaml_content = match.group(1).strip()
                return yaml.safe_load(yaml_content)

        except Exception as exc:
            print(f"Attempt {attempt + 1} failed: {exc}")
            time.sleep(retry_delay)
            attempt += 1

    print(f"All {max_retries} attempts failed. Proceeding with an empty skill structure.")
    return {"Skills": {}}
