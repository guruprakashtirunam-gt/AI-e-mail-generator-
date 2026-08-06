def build_email_prompt(email_type, recipient, tone, length, additional_details):
    """
    Builds the prompt string to send to the Gemini API based on user input.
    """
    prompt = f"""You are an expert business communication assistant.

Generate a complete email.

Email Type:
{email_type}

Recipient:
{recipient}

Tone:
{tone}

Length:
{length}

Additional Details:
{additional_details}

Return exactly in the following format with 'Subject:' on the first line and the rest as the body:

Subject: [Generated Subject]

[Generated Email Body]
"""
    return prompt
