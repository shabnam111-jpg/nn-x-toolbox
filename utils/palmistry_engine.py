import random

def build_palm_report(features, observations):
    """
    Builds a comprehensive palm reading report based on extracted features and observations.
    """
    # Get classification from features
    classification = classify_palm(features)
    
    # Calculate detection quality (simple heuristic based on line lengths)
    total_length = sum([features.get(f'{line.lower()}_length', 0) for line in ['life', 'head', 'heart']])
    detection_quality = min(1.0, total_length / 1000.0) if total_length > 0 else 0.5
    
    # Line strengths
    lengths = {
        'Life': features.get('life_length', 0),
        'Head': features.get('head_length', 0),
        'Heart': features.get('heart_length', 0)
    }
    total = sum(lengths.values()) or 1
    line_strengths = {k: v/total for k, v in lengths.items()}
    
    # Dominant line and strength
    dominant_line = classification.get('dominant_line', 'Life')
    dominant_strength_pct = round(line_strengths.get(dominant_line, 0) * 100, 1)
    
    # Hand shape label (from observations or default)
    hand_shape_label = observations.get('hand_shape', 'Auto / unsure')
    
    # Generate summary
    summary = generate_palm_summary(classification, dominant_line, detection_quality)
    
    # Line readings
    line_readings = generate_line_readings(lengths, classification)
    
    # Themes
    themes = generate_themes(classification, features)
    
    # Shared notes
    shared_notes = generate_shared_notes(features, classification)
    
    # Guidance
    guidance = generate_guidance(classification, dominant_line)
    
    # Questions
    questions = generate_questions(classification)
    
    # Chat context
    chat_context = f"Palm reading report: Dominant line is {dominant_line} with {dominant_strength_pct}% strength. " \
                   f"Palm type: {classification.get('palm_type', 'Unknown')}. " \
                   f"Career shift indicator: {classification.get('career_shift_indicator', 'No')}."
    
    report = {
        "dominant_line": dominant_line,
        "dominant_strength_pct": dominant_strength_pct,
        "detection_quality": detection_quality,
        "career_shift_indicator": classification.get('career_shift_indicator', 'No'),
        "hand_shape_label": hand_shape_label,
        "summary": summary,
        "line_readings": line_readings,
        "themes": themes,
        "shared_notes": shared_notes,
        "guidance": guidance,
        "questions": questions,
        "line_strengths": line_strengths,
        "observations": observations,
        "chat_context": chat_context,
    }
    
    return report

def classify_palm(features):
    """
    Classify palm based on features (adapted from existing code).
    """
    classification = {}
    lengths = {'Life': features.get('life_length', 0), 'Head': features.get('head_length', 0), 'Heart': features.get('heart_length', 0)}
    total_length = sum(lengths.values())
    if total_length == 0:
        classification['dominant_line'] = 'Unknown'
        classification['confidence'] = 0.0
    else:
        dominant_line = max(lengths, key=lengths.get)
        classification['dominant_line'] = dominant_line
        classification['confidence'] = round(lengths[dominant_line] / total_length, 3)
    
    avg_curvature = (features.get('life_curvature', 0) + features.get('head_curvature', 0) + features.get('heart_curvature', 0)) / 3
    if avg_curvature > 1.3: classification['palm_type'] = 'Curved/Expressive'
    elif avg_curvature > 1.1: classification['palm_type'] = 'Balanced'
    else: classification['palm_type'] = 'Straight/Practical'
    
    head_angle = abs(features.get('head_angle', 0))
    intersections = features.get('life_head_intersection', 0)
    if head_angle > 10 and intersections > 0:
        classification['career_shift_indicator'] = 'Yes'
        classification['career_shift_confidence'] = 0.7
    else:
        classification['career_shift_indicator'] = 'No'
        classification['career_shift_confidence'] = 0.6
    return classification

def generate_palm_summary(classification, dominant_line, detection_quality):
    """
    Generate a summary text for the palm reading.
    """
    palm_type = classification.get('palm_type', 'Balanced')
    career_shift = classification.get('career_shift_indicator', 'No')
    
    summary = f"Your dominant palm line is the {dominant_line} line, suggesting a focus on "
    if dominant_line == 'Life':
        summary += "vitality, longevity, and life experiences. "
    elif dominant_line == 'Head':
        summary += "intellect, learning, and mental pursuits. "
    elif dominant_line == 'Heart':
        summary += "emotions, relationships, and matters of the heart. "
    
    summary += f"Your palm type is {palm_type.lower()}, indicating "
    if palm_type == 'Curved/Expressive':
        summary += "an expressive and adaptable nature. "
    elif palm_type == 'Balanced':
        summary += "a well-rounded and harmonious approach to life. "
    else:
        summary += "a practical and straightforward disposition. "
    
    if career_shift == 'Yes':
        summary += "There are indications of potential career changes or shifts in direction."
    else:
        summary += "Your path appears stable with consistent direction."
    
    if detection_quality < 0.7:
        summary += " (Note: Scan quality is moderate; results may vary with better imaging.)"
    
    return summary

def generate_line_readings(lengths, classification):
    """
    Generate detailed readings for each line.
    """
    readings = []
    descriptions = {
        'Life': ("Life Line", "Represents vitality, energy levels, and major life changes. A strong life line suggests robust health and resilience.", "Health & Vitality"),
        'Head': ("Head Line", "Indicates intellect, learning style, and mental approach to challenges. Shows how you process information and solve problems.", "Intellect & Learning"),
        'Heart': ("Heart Line", "Relates to emotional expression, relationships, and capacity for love. Reveals how you connect with others emotionally.", "Emotions & Relationships")
    }
    
    for line, length in lengths.items():
        if length > 0:
            name, detail, emphasis = descriptions[line]
            readings.append({
                'line': name,
                'detail': detail,
                'emphasis': emphasis
            })
    
    return readings

def generate_themes(classification, features):
    """
    Generate thematic interpretations.
    """
    dominant = classification.get('dominant_line', 'Life')
    palm_type = classification.get('palm_type', 'Balanced')
    
    themes = {
        'mindset': "Your mental approach is analytical and methodical, with a focus on practical solutions." if dominant == 'Head' else "You process information intuitively, trusting your instincts alongside logic.",
        'relationships': "You form deep, meaningful connections and value emotional authenticity in partnerships." if dominant == 'Heart' else "Relationships are approached with warmth and consideration for others' feelings.",
        'energy': "Your energy flows steadily and sustainably, with good reserves for long-term endeavors." if palm_type == 'Balanced' else "You have dynamic energy that adapts well to changing circumstances.",
        'career': "Career paths that allow intellectual growth and problem-solving will be most fulfilling." if dominant == 'Head' else "Seek roles that align with your emotional values and provide stability.",
        'visibility': "You prefer working behind the scenes but have the potential to lead when called upon." if palm_type == 'Straight/Practical' else "Your expressive nature draws attention and opportunities naturally."
    }
    
    return themes

def generate_shared_notes(features, classification):
    """
    Generate pattern notes.
    """
    notes = []
    if classification.get('dominant_line') == 'Life':
        notes.append("Strong life line suggests good physical vitality")
    if classification.get('career_shift_indicator') == 'Yes':
        notes.append("Potential career transitions indicated by line intersections")
    if features.get('life_curvature', 0) > 1.2:
        notes.append("Curved lines suggest adaptability and flexibility")
    
    if not notes:
        notes = ["Lines show balanced development across life areas"]
    
    return notes

def generate_guidance(classification, dominant_line):
    """
    Generate guidance points.
    """
    guidance = []
    if dominant_line == 'Life':
        guidance.append("Focus on maintaining physical health and embracing new experiences")
    elif dominant_line == 'Head':
        guidance.append("Continue developing your intellectual pursuits and learning new skills")
    else:
        guidance.append("Nurture emotional connections and trust your heart's wisdom")
    
    if classification.get('career_shift_indicator') == 'Yes':
        guidance.append("Be open to career changes; they may bring unexpected opportunities")
    else:
        guidance.append("Build steadily on your current path for long-term success")
    
    guidance.append("Remember that palmistry offers insights, not certainties - your choices shape your destiny")
    
    return guidance

def generate_questions(classification):
    """
    Generate suggested questions for further exploration.
    """
    questions = [
        "How does my dominant line influence my daily decision-making?",
        "What does my palm type suggest about my communication style?",
        "Are there any signs of upcoming life changes in my reading?",
        "How can I best utilize my natural strengths shown in the lines?",
        "What areas of personal growth are highlighted by this palm analysis?"
    ]
    
    return questions

def answer_palm_question(question, palm_report):
    """
    Answer a question based on the palm report.
    """
    dominant = palm_report.get('dominant_line', 'Life')
    palm_type = palm_report.get('palm_type', 'Balanced')
    career_shift = palm_report.get('career_shift_indicator', 'No')
    
    # Simple keyword-based answering
    question_lower = question.lower()
    
    if 'dominant' in question_lower or 'line' in question_lower:
        if dominant == 'Life':
            return "Your dominant Life line suggests a focus on vitality and life experiences. It indicates good energy levels and resilience in facing life's challenges."
        elif dominant == 'Head':
            return "Your dominant Head line points to strong intellectual abilities and a logical approach to problem-solving. You likely excel in analytical thinking."
        else:
            return "Your dominant Heart line reveals emotional depth and strong interpersonal connections. Relationships and emotional intelligence are key strengths."
    
    elif 'career' in question_lower or 'job' in question_lower:
        if career_shift == 'Yes':
            return "Your palm shows indications of potential career changes. Look for opportunities that align with your evolving interests and skills."
        else:
            return "Your reading suggests career stability. Continue building on your current path, focusing on steady growth and expertise development."
    
    elif 'relationship' in question_lower or 'love' in question_lower:
        return "Your Heart line suggests you form deep, meaningful connections. Trust your emotional intuition when navigating relationships."
    
    elif 'health' in question_lower:
        return "Your Life line indicates good vitality. Maintain balance in your lifestyle to support ongoing health and energy."
    
    else:
        return f"Based on your palm reading with dominant {dominant} line, I see patterns of {palm_type.lower()} energy. The lines suggest {palm_report.get('summary', 'balanced development')}. For more specific insights, try asking about career, relationships, or personal strengths."