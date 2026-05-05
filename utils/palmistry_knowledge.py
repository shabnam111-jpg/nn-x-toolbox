"""
Comprehensive palmistry knowledge base and professional system prompts.
Supports advanced palm reading analysis with multiple dimensions.
"""

# ═════════════════════════════════════════════════════════════════════════════
# HAND TYPES & ELEMENTS
# ═════════════════════════════════════════════════════════════════════════════
HAND_TYPES = {
    'fire': {
        'description': 'Energetic, passionate, impulsive',
        'keywords': ['energetic', 'passionate', 'action-oriented', 'creative'],
        'career_paths': ['entrepreneurship', 'sales', 'creative fields', 'leadership'],
        'health_focus': 'cardiovascular health, stress management',
        'element_symbol': '🔥'
    },
    'earth': {
        'description': 'Practical, grounded, stable',
        'keywords': ['practical', 'reliable', 'grounded', 'realistic'],
        'career_paths': ['engineering', 'finance', 'administration', 'farming'],
        'health_focus': 'digestive health, stability',
        'element_symbol': '🌍'
    },
    'air': {
        'description': 'Intellectual, communicative, curious',
        'keywords': ['intellectual', 'communicative', 'analytical', 'adaptable'],
        'career_paths': ['writing', 'teaching', 'science', 'communication'],
        'health_focus': 'mental clarity, respiratory health',
        'element_symbol': '💨'
    },
    'water': {
        'description': 'Emotional, intuitive, artistic',
        'keywords': ['intuitive', 'emotional', 'creative', 'empathetic'],
        'career_paths': ['arts', 'therapy', 'psychology', 'healing'],
        'health_focus': 'emotional balance, fluid retention',
        'element_symbol': '💧'
    }
}

# ═════════════════════════════════════════════════════════════════════════════
# PALM MOUNTS ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
MOUNT_ANALYSIS = {
    'Venus': {'area': 'base of thumb', 'qualities': 'love, beauty, pleasure, sensuality', 'symbol': '♀'},
    'Jupiter': {'area': 'base of index', 'qualities': 'ambition, leadership, authority, wisdom', 'symbol': '♃'},
    'Saturn': {'area': 'base of middle', 'qualities': 'responsibility, introspection, limitations', 'symbol': '♄'},
    'Apollo': {'area': 'base of ring', 'qualities': 'creativity, success, reputation, joy', 'symbol': '☉'},
    'Mercury': {'area': 'base of pinky', 'qualities': 'communication, intellect, commerce, wit', 'symbol': '☿'},
    'Luna': {'area': 'opposite thumb', 'qualities': 'imagination, intuition, travel, spirituality', 'symbol': '☾'},
    'Mars_active': {'area': 'between thumb & Luna', 'qualities': 'courage, passion, strength', 'symbol': '♂+'},
    'Mars_passive': {'area': 'between Mercury & Luna', 'qualities': 'resilience, resistance, protection', 'symbol': '♂-'},
}

# ═════════════════════════════════════════════════════════════════════════════
# COMPREHENSIVE LINE READINGS
# ═════════════════════════════════════════════════════════════════════════════
LINE_COMPREHENSIVE = {
    'Life': {
        'represents': 'vitality, longevity, health, major life events',
        'long_curved': 'strong health, adventurous spirit, many life experiences',
        'short_straight': 'practical approach, shorter but intense experiences',
        'broken': 'major life changes, health challenges overcome',
        'chained': 'periods of restriction followed by freedom',
        'starts_Jupiter': 'ambitious start to life, parental influence',
    },
    'Head': {
        'represents': 'intellect, mental approach, creativity, decision-making',
        'long_straight': 'logical, practical, realistic thinking',
        'curved_long': 'imaginative, creative, artistic thinking',
        'short': 'focused thinking, quick decisions',
        'wavy': 'scattered thoughts, difficulty concentrating',
        'starts_Jupiter': 'learning from experience, educated decisions',
    },
    'Heart': {
        'represents': 'emotions, relationships, romantic capacity, mood',
        'long_curve_Jupiter': 'emotional, idealistic, romantic',
        'straight': 'realistic about love, practical relationships',
        'short': 'selectively emotional, independent spirit',
        'broken': 'emotional trauma, healing process',
        'touches_Life': 'love influences major life decisions',
    },
    'Fate': {
        'represents': 'career destiny, life purpose, major turning points',
        'straight_Saturn_to_future': 'predetermined path, stable career',
        'curved': 'changes in direction, multiple careers',
        'branching': 'multiple opportunities, choices ahead',
        'starts_wrist': 'family legacy, inherited destiny',
        'starts_Life': 'self-made destiny, personal effort',
    },
    'Mercury': {
        'represents': 'communication, business sense, intellectual pursuits',
        'prominent': 'excellent communicator, business potential',
        'faint': 'communication challenges, introversion',
        'curved': 'intuitive communication, sensitivity',
        'straight': 'logical communication, clear speech',
    },
}

# ═════════════════════════════════════════════════════════════════════════════
# TIMING SYSTEM FOR PREDICTIONS
# ═════════════════════════════════════════════════════════════════════════════
TIMING_SYSTEM = {
    'wrist_to_life_line': 'ages 0-20 (foundation, childhood)',
    'life_line_below_head': 'ages 20-40 (active years)',
    'life_line_below_heart': 'ages 40-60 (maturity)',
    'life_line_to_edge': 'ages 60+ (later years)',
    'right_hand_timing': 'current/future projection',
    'left_hand_timing': 'past/potential energy',
    'major_crossings': 'significant turning points',
}

# ═════════════════════════════════════════════════════════════════════════════
# HEALTH INDICATORS
# ═════════════════════════════════════════════════════════════════════════════
HEALTH_INDICATORS = {
    'Life line quality': ['strong/weak', 'continuous/broken', 'clear/faint'],
    'Islands on life line': 'health challenges, recovery periods',
    'Cross marks': 'significant life-altering events',
    'Color of palm': 'pale=low energy, pink=healthy, red=hyperactive',
    'Temperature': 'warm=active, cold=low circulation',
    'Hand flexibility': 'flexible=adaptable, rigid=resistant to change',
    'Nails': 'strong=health, brittle=deficiency, pale=anemia',
    'Skin texture': 'smooth=good health, rough=stress',
}

# ═════════════════════════════════════════════════════════════════════════════
# PERSONALITY PROFILES
# ═════════════════════════════════════════════════════════════════════════════
PERSONALITY_PROFILES = {
    'The Leader': {
        'traits': ['ambitious', 'confident', 'decisive', 'authoritative'],
        'mounts': ['Jupiter dominant', 'Mars active prominent'],
        'lines': ['strong head line', 'long fate line'],
        'archetype': 'Natural leader with vision',
    },
    'The Creator': {
        'traits': ['imaginative', 'artistic', 'intuitive', 'unconventional'],
        'mounts': ['Luna prominent', 'Apollo strong'],
        'lines': ['curved lines', 'Mercury well-formed'],
        'archetype': 'Artist or innovator',
    },
    'The Thinker': {
        'traits': ['analytical', 'logical', 'studious', 'reserved'],
        'mounts': ['Saturn prominent', 'Mercury strong'],
        'lines': ['straight head line', 'clear Mercury line'],
        'archetype': 'Intellectual or scholar',
    },
    'The Romantic': {
        'traits': ['emotional', 'sensitive', 'loving', 'idealistic'],
        'mounts': ['Venus prominent', 'Luna moderate'],
        'lines': ['long heart line', 'curved life line'],
        'archetype': 'Lover or empath',
    },
    'The Adventurer': {
        'traits': ['free-spirited', 'exploratory', 'courageous', 'restless'],
        'mounts': ['Mars active strong', 'Luna prominent'],
        'lines': ['traveling lines', 'branching fate line'],
        'archetype': 'Explorer or nomad',
    },
    'The Healer': {
        'traits': ['empathetic', 'compassionate', 'helpful', 'intuitive'],
        'mounts': ['Venus strong', 'Saturn moderate'],
        'lines': ['long heart line', 'healing stigmata'],
        'archetype': 'Helper or counselor',
    },
}

# ═════════════════════════════════════════════════════════════════════════════
# SYSTEM PROMPTS & GREETINGS
# ═════════════════════════════════════════════════════════════════════════════

def build_professional_system_prompt():
    """Generate professional palmistry analysis system prompt."""
    return """You are an expert palmistry reader with decades of experience. Analyze palms with precision, empathy, and wisdom.

PALM ANALYSIS FRAMEWORK:
1. **Hand Shape & Size**: Element correspondence (Fire, Earth, Air, Water)
2. **Palm Mounts**: Energy centers (Venus, Jupiter, Saturn, Apollo, Mercury, Luna, Mars)
3. **Major Lines**: Life, Head, Heart, Fate lines characteristics
4. **Minor Lines**: Mercury, Sun, Intuition lines when present
5. **Markers**: Crosses, islands, branches, breaks, chains
6. **Timing**: Age correlation using traditional timing system
7. **Integration**: Synthesis of all elements into coherent narrative

TONE: Professional yet warm, insightful yet non-judgmental, specific yet holistic.

RESPONSE STRUCTURE:
- Start with element/hand type observation
- Cover line-by-line analysis
- Highlight mount influences
- Provide timing predictions
- Offer practical wisdom without determinism
- End with empowering guidance

AVOID:
- Absolute predictions or deterministic language
- Fear-based messaging
- Oversimplification
- Generic readings
- Ignoring contradictions (explain instead)

EMBRACE:
- Nuance and complexity
- Personal agency and choice
- Psychological depth
- Cultural sensitivity
- The paradox: destiny and free will coexist"""

def get_professional_greeting():
    """Get a professional greeting for palm readings."""
    return """Welcome to your palm reading session. 🌙✋

I'm here to offer insights into your life's patterns, potentials, and paths forward. Your palms contain the story of who you are, what you're capable of, and the journey ahead.

Remember: palmistry reveals tendencies and potential, not fixed destiny. You always have the power to shape your path.

Let's explore what your hands reveal."""

def get_reading_structure():
    """Return the standard reading structure."""
    return {
        'hand_shape': 'Element analysis',
        'mounts': 'Energy centers and personality traits',
        'life_line': 'Vitality, health, major events',
        'head_line': 'Mental approach, intellect, creativity',
        'heart_line': 'Emotions, relationships, capacity for love',
        'fate_line': 'Career, destiny, life purpose',
        'timing': 'Age correlation and predictions',
        'integration': 'Holistic synthesis and guidance'
    }

def analyze_line_characteristic(line_name, characteristic):
    """Provide detailed interpretation of a line characteristic."""
    if line_name not in LINE_COMPREHENSIVE:
        return "Unknown line"
    
    line_data = LINE_COMPREHENSIVE[line_name]
    if characteristic in line_data:
        return line_data[characteristic]
    return "Characteristic not found in database"

def get_mount_interpretation(mount_name):
    """Get detailed interpretation of a mount."""
    if mount_name not in MOUNT_ANALYSIS:
        return "Mount not found"
    
    mount = MOUNT_ANALYSIS[mount_name]
    return f"{mount_name}: Located at {mount['area']}, represents {mount['qualities']} ({mount['symbol']})"

def classify_hand_element(hand_characteristics):
    """Classify hand element based on characteristics."""
    # Simple heuristic - can be enhanced
    for element, data in HAND_TYPES.items():
        for keyword in data['keywords']:
            if keyword.lower() in str(hand_characteristics).lower():
                return element, data
    return None, None

# ═════════════════════════════════════════════════════════════════════════════
# PALM READING DATABASE
# ═════════════════════════════════════════════════════════════════════════════

PALM_READINGS_DB = {
    'interpretation_cache': {},
    'user_histories': {},
}

def cache_interpretation(hand_type, lines, mounts, interpretation):
    """Cache a palm reading interpretation."""
    key = f"{hand_type}_{hash(str(lines))}"
    PALM_READINGS_DB['interpretation_cache'][key] = interpretation
    return key

def retrieve_cached_interpretation(key):
    """Retrieve a cached interpretation."""
    return PALM_READINGS_DB['interpretation_cache'].get(key)

# ═════════════════════════════════════════════════════════════════════════════
# ADVANCED PALM MARKERS
# ═════════════════════════════════════════════════════════════════════════════

ADVANCED_MARKERS = {
    'crosses': 'significant events or turning points',
    'islands': 'periods of difficulty or blockage',
    'branches': 'multiple paths or opportunities',
    'chains': 'repetitive patterns or cycles',
    'breaks': 'major interruptions or changes',
    'forks': 'choices or decisions ahead',
    'triangles': 'protection or spiritual guidance',
    'squares': 'protection from difficult circumstances',
    'circles': 'warning signs or health concerns',
    'grilles': 'confusion or scattered energy',
    'stars': 'significant events or fame',
}

def interpret_marker(marker_type, location_line, hand_position):
    """Interpret a specific marker on a palm."""
    if marker_type not in ADVANCED_MARKERS:
        return None
    
    description = ADVANCED_MARKERS[marker_type]
    return f"{marker_type.capitalize()} on {location_line} (at {hand_position}): {description}"
