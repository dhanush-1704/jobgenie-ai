import json

import ollama

from src.ai.prompts import (
    SYSTEM_PROMPT,
    build_resume_prompt,
)


class ResumeParser:
    """
    Uses Ollama to convert raw resume text into structured JSON.
    """

    MODEL = "llama3:latest"

    @classmethod
    def parse(cls, resume_text: str) -> dict:
        """
        Parse resume text using Ollama.
        """

        response = ollama.chat(
            model=cls.MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": build_resume_prompt(resume_text),
                },
            ],
            options={
                "temperature": 0,
            },
        )

        content = response["message"]["content"]

        try:
            return json.loads(content)

        except json.JSONDecodeError:
            raise ValueError(
                "Failed to parse JSON returned by Ollama."
            )