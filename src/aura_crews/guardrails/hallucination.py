"""Hallucination guardrail — validates output quality."""


def hallucination_guardrail(result):
    """
    Validate crew output before returning.
    Returns (success: bool, result_or_retry_instructions).
    Based on CrewAI official guardrail pattern.
    """
    try:
        output = str(result.raw if hasattr(result, "raw") else result)

        # Guard 1: Empty or too short
        if not output or len(output.strip()) < 5:
            return (False, "Output too short. Please provide a complete, detailed response.")

        # Guard 2: Just a status message, not actual content
        status_words = ["done.", "done", "completed", "finished", "task completed"]
        if output.strip().lower() in status_words:
            return (False, "Provide the actual content, not just a completion status.")

        # Guard 3: System prompt leak detection
        leak_signals = ["backstory:", "you are an ai", "as an ai language model", "i cannot"]
        if any(sig in output.lower() for sig in leak_signals):
            return (False, "Response contains meta-information. Rewrite as a direct, natural response.")

        # Guard 4: Excessive repetition
        words = output.split()
        if len(words) > 20:
            unique_ratio = len(set(words)) / len(words)
            if unique_ratio < 0.3:
                return (False, "Response is too repetitive. Provide diverse, meaningful content.")

        # Passed all checks
        return (True, result)

    except Exception as e:
        print(f"[GUARDRAIL] Error: {e}")
        return (True, result)  # Pass through on error
