"""
Base personality class that all specific personalities will inherit from.
Integrates voice-optimized templates from prompts.py with model spec loading.
"""
import os
from typing import List, Dict, Any, Optional
from langchain.prompts import PromptTemplate
from src.config import PROJECT_ROOT
from src.prompts import VOICE_QA_PROMPT


class BasePersonality:
    """Base class for AI personalities with voice optimization and model spec loading."""

    id: str = "base"
    name: str = "Base Personality"
    tags: List[str] = []

    # Voice optimization guidelines
    VOICE_GUIDELINES = """
<voice_guidelines>
- Use natural speech patterns that would sound good when read aloud
- Keep sentences short to moderate in length (15-20 words maximum)
- Avoid using visual formatting like bullet points, headings, tables, or markdown
- Use transition phrases instead of visual separators
- When listing items, use "such as" or natural numbering in a conversational way
- Pause between main ideas by starting new paragraphs
- Use a conversational tone that sounds natural when spoken
- Never reference visual elements or formatting
</voice_guidelines>
"""

    # Language matching guidelines
    LANGUAGE_GUIDELINES = """
<language_guidelines>
1. The MOST IMPORTANT rule: Your response language MUST MATCH the question language
2. IGNORE any language in the context documents - use ONLY the question language
3. Use the information in the context for content, but TRANSLATE it to match the question language
4. If the answer is not in the context, provide an appropriate "I don't know" response in the question's language
</language_guidelines>
"""

    # Response guidelines
    RESPONSE_GUIDELINES = """
<response_guidelines>
1. Answer based ONLY on the information provided in the context
2. Focus on providing factual, accurate information without speculation
3. Be concise but complete in your explanation
4. Structure your response in a way that flows naturally when spoken
</response_guidelines>
"""
    # Reasoning guidelines
    REASONING_GUIDELINES = """
<reasoning_guidelines>
1. First, analyze if the question can be answered with the provided context
2. Identify the most relevant pieces of information
3. Formulate a response that directly addresses the question
4. Verify that your response doesn't contain information not present in the context
</reasoning_guidelines>
"""

    @classmethod
    def _load_model_spec(cls) -> str:
        """
        Load the model spec from file.

        Looks for a model-spec.md file in the corresponding directory
        for this personality.
        """
        # Determine path based on personality ID
        model_spec_path = os.path.join(
            PROJECT_ROOT, "lib", "deepgov-modelspec", "agents", cls.id, "model-spec.md"
        )

        # Try to load the file
        try:
            if os.path.exists(model_spec_path):
                with open(model_spec_path, "r", encoding="utf-8") as f:
                    model_spec = f.read().strip()
                print(f"Loaded model spec for {cls.id} from {model_spec_path}")
                return model_spec
            else:
                print(f"No model spec found for {cls.id} at {model_spec_path}")
                return ""
        except Exception as e:
            print(f"Error reading model spec for {cls.id}: {e}")
            return ""

    @classmethod
    def _extract_principles(cls, model_spec: str) -> Optional[List[str]]:
        """Extract numbered principles from the model spec."""
        if not model_spec:
            return None

        principles = []
        lines = model_spec.split("\n")

        for line in lines:
            # Look for lines starting with a number followed by period or bracket
            if line.strip().startswith(
                ("1.", "2.", "3.", "4.", "5.", "1)", "2)", "3)", "4)", "5)")
            ):
                principles.append(line.strip())

        return principles if principles else None

    @classmethod
    def get_model_spec_section(cls) -> str:
        """Get the model spec as a formatted section."""
        model_spec = cls._load_model_spec()
        if not model_spec:
            return ""

        return model_spec

    @classmethod
    def get_principles_section(cls) -> str:
        """Get principles as a formatted section."""
        model_spec = cls._load_model_spec()
        principles = cls._extract_principles(model_spec)

        if not principles:
            return ""

        principles_section = """<principles>"""
        for principle in principles:
            principles_section += f"{principle}\n"
        principles_section += """</principles>"""
        return principles_section

    @classmethod
    def get_base_instructions(cls) -> str:
        """Get base instructions common to all personalities."""
        return """You are an AI assistant that answers questions based on specific document knowledge.
IMPORTANT: Your responses will be read aloud by a voice system.
You must ALWAYS respond in the EXACT SAME LANGUAGE as the user's question."""

    @classmethod
    def get_system_prompt(cls) -> str:
        """Get the system prompt template with voice optimization and model spec."""
        # Load model spec if available
        model_spec = cls.get_model_spec_section()
        principles_section = cls.get_principles_section()

        # Integrate model spec if available
        model_spec_instruction = f"""{model_spec}""" if model_spec else ""
        # Build the complete prompt from sections
        return f"""<instructions>
{cls.get_base_instructions()}{model_spec_instruction}
</instructions>

<context>
{{context}}
</context>

{cls.VOICE_GUIDELINES}

{cls.LANGUAGE_GUIDELINES}

{principles_section}
{cls.RESPONSE_GUIDELINES}

{cls.REASONING_GUIDELINES}

<question>{{question}}</question>
"""

    @classmethod
    def get_prompt_template(cls) -> PromptTemplate:
        """Get the prompt template configured for this personality."""
        # If you want to use the default template from prompts.py directly:
        # return VOICE_QA_PROMPT

        # Or use the custom template with model spec integration:
        return PromptTemplate(
            template=cls.get_system_prompt(), input_variables=["context", "question"]
        )

    @classmethod
    def get_info(cls) -> Dict[str, Any]:
        """Get basic information about this personality."""
        return {"id": cls.id, "name": cls.name, "tags": cls.tags}
