from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")

class LLMService:
    def __init__(self, api_key=None):
        # Using Groq via OpenAI Client
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.model = "llama-3.3-70b-versatile" # Updated to supported model

    def analyze_match(self, resume_text: str, jd_text: str) -> dict:
        prompt = f"""
        You are an expert HR AI. Analyze the following Resume against the Job Description.
        
        Job Description:
        {jd_text}
        
        Resume:
        {resume_text}
        
        Provide the output in STRICT JSON format with the following keys:
        - match_score: (integer 0-100)
        - strengths: (list of strings)
        - gaps: (list of strings)
        - summary: (short paragraph)
        
        Do not include markdown backticks ```json ... ```, just the raw JSON string.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful HR assistant."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" }
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            if "insufficient_quota" in str(e) or "429" in str(e):
                # Fallback MOCK response for Demo purposes
                print("Quota exceeded, returning MOCK analysis.")
                return {
                    "match_score": 88,
                    "strengths": [
                        "Demonstrates strong adaptation to technical challenges",
                        "Experience with Python and React (inferred)",
                        "Proactive problem solver"
                    ],
                    "gaps": [
                        "API Quota limitations detected",
                        "Real-time analysis unavailable"
                    ],
                    "summary": "NOTE: This is a generated MOCK analysis because the OpenAI API Quota was exceeded. In a production environment with a valid key, this would be a real analysis of the resume."
                }
            return {
                "match_score": 0,
                "strengths": [],
                "gaps": [f"Error analyzing with OpenAI: {str(e)}"],
                "summary": "Failed to analyze."
            }

    def ask_question(self, context: str, question: str) -> str:
        prompt = f"""
        Answer the question strictly based on the provided Resume Context.
        
        Resume Context:
        {context}
        
        Question:
        {question}
        
        Answer:
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            if "insufficient_quota" in str(e) or "429" in str(e):
                return "MOCK ANSWER: This candidate seems to have relevant experience based on the document provided. (Real-time answers unavailable due to API Quota)."
            return f"Error: {str(e)}"
