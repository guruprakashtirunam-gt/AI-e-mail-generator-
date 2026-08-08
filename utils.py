def parse_generated_email(raw_text):
    """
    Extracts the subject and the body from the raw text returned by the model.
    Assumes the model follows the prompt structure.
    """
    lines = raw_text.strip().split('\n')
    subject = "Generated Email"
    body = raw_text
    
    for i, line in enumerate(lines):
        if line.lower().startswith("subject:"):
            subject = line.replace("Subject:", "", 1).replace("**", "").strip()
            # The body is everything after the subject line
            # Skip any immediate empty lines after subject
            start_index = i + 1
            while start_index < len(lines) and not lines[start_index].strip():
                start_index += 1
            body = "\n".join(lines[start_index:])
            break
            
    return subject, body
