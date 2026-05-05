# 🌟 Glowing Glass Buttons - Quick Reference Guide

## Overview
Your project now includes premium glowing buttons with glass morphism finish and animated neon effects. These buttons are production-ready and can be used throughout your application.

---

## 📦 Available Button Functions

### Main Function: `glowing_button()`
```python
from utils.styles import glowing_button

glowing_button(
    label="Button Text",           # Button label (required)
    icon="🚀",                     # Optional emoji/icon
    color="#818CF8",               # Primary button color (hex)
    glow_color="#6366F1",          # Glow effect color (hex)
    on_click=None,                 # Callback function
    key="btn_unique_id",           # Unique button key
    use_container_width=False,     # Full width button
    animated=True,                 # Enable glow animation
    size="medium"                  # "small", "medium", "large"
)
```

### Preset Color Buttons

| Function | Color | Use Case |
|----------|-------|----------|
| `btn_indigo()` | 🎨 Indigo | Default, professional actions |
| `btn_cyan()` | 💎 Cyan | Primary actions, selections |
| `btn_emerald()` | 🌿 Emerald | Success, confirmations |
| `btn_rose()` | 🌹 Rose | Delete, warnings |
| `btn_gold()` | ⭐ Gold | Important, premium features |
| `btn_purple()` | 🎭 Purple | Creative, special modes |
| `btn_pink()` | 💕 Pink | Fun, secondary actions |
| `btn_blue()` | 🌊 Blue | Info, help, navigation |

### Special Effects

| Function | Effect | Animation |
|----------|--------|-----------|
| `btn_rainbow()` | Rainbow gradient | Color cycling |
| `btn_neon_pulse()` | Neon outline | Pulsing glow |

---

## 🎯 Usage Examples

### Example 1: Simple Button
```python
from utils.styles import btn_cyan

btn_cyan("Start Analysis", "🚀")
```

### Example 2: Full Width Button
```python
from utils.styles import btn_emerald

btn_emerald(
    "Process Data", 
    "⚡", 
    use_container_width=True
)
```

### Example 3: Small Button Group
```python
from utils.styles import glow_button_group

buttons = [
    {"label": "Save", "icon": "💾", "color": "#818CF8", "glow_color": "#6366F1"},
    {"label": "Export", "icon": "📤", "color": "#22D3EE", "glow_color": "#06B6D4"},
    {"label": "Share", "icon": "🔗", "color": "#34D399", "glow_color": "#10B981"},
]

glow_button_group(buttons, columns=3)
```

### Example 4: Different Sizes
```python
from utils.styles import glowing_button

# Small button - compact, fits in tight spaces
glowing_button("Compact", size="small", key="small_btn")

# Medium button - standard, balanced
glowing_button("Standard", size="medium", key="med_btn")

# Large button - prominent, attention-grabbing
glowing_button("Prominent", size="large", key="large_btn")
```

### Example 5: Button Row
```python
from utils.styles import btn_indigo, btn_rose, btn_emerald

col1, col2, col3 = st.columns(3)

with col1:
    btn_indigo("Option A", "1️⃣")
with col2:
    btn_rose("Option B", "2️⃣")
with col3:
    btn_emerald("Option C", "3️⃣")
```

### Example 6: Special Effects
```python
from utils.styles import btn_rainbow, btn_neon_pulse

st.markdown("**Choose your style:**")

col1, col2 = st.columns(2)

with col1:
    btn_rainbow("Rainbow Effect", "🌈")
    
with col2:
    btn_neon_pulse("Neon Pulse", "💫", "#22D3EE")
```

---

## 🎨 Color Customization

### RGB to Hex Conversion
```python
# If you want a custom color
# RGB(255, 100, 50) → #FF6432
custom_color = "#FF6432"

glowing_button(
    "Custom Color",
    color=custom_color,
    glow_color=custom_color,
)
```

### Creating Your Own Preset
```python
# Add to utils/styles.py to create a custom button
def btn_custom(label, icon="", on_click=None, key=None):
    return glowing_button(
        label, 
        icon, 
        "#YOUR_COLOR", 
        "#YOUR_GLOW_COLOR", 
        on_click, 
        key or "btn_custom"
    )
```

---

## 🌟 Features Explained

### Glass Morphism
- Frosted glass appearance with `backdrop-filter: blur()`
- Semi-transparent background
- Creates depth and premium feel

### Neon Glow
- Animated glow effect that intensifies on hover
- Multi-layered shadow for depth
- Synchronized with button interaction

### Animations
- **Hover**: Scale (1.05), lift (translateY), enhanced glow
- **Active**: Scale (0.98), slight depression
- **Continuous**: Optional glow animation (pulsing effect)

### Responsiveness
- Works on all screen sizes
- Touch-friendly hit targets
- Maintains readability

---

## 🔧 Integration Examples

### In Your AI Assistant Module
```python
# glowing_buttons_demo.py
from utils.styles import btn_cyan, btn_emerald, btn_rose

# In your ai_assistant_page() function
col1, col2, col3 = st.columns(3)

with col1:
    btn_cyan("Get Answer", "🤖")
with col2:
    btn_emerald("Save Response", "💾")
with col3:
    btn_rose("Clear History", "🗑️")
```

### In Your OpenCV Module
```python
# In your _face_scan_module() function
from utils.styles import glowing_button

st.markdown("**Detection Options**")

col1, col2, col3 = st.columns(3)

with col1:
    glowing_button(
        "📸 Capture", 
        color="#22D3EE",
        use_container_width=True,
        key="capture_btn"
    )
```

### In Dashboard
```python
# In your app.py home() function
from utils.styles import glow_button_group

modules = [
    {"label": "Perceptron", "icon": "🧠", "color": "#818CF8", "glow_color": "#6366F1"},
    {"label": "Vision", "icon": "👁️", "color": "#22D3EE", "glow_color": "#06B6D4"},
    {"label": "Neural Net", "icon": "⚡", "color": "#34D399", "glow_color": "#10B981"},
]

glow_button_group(modules, columns=3)
```

---

## 🎬 Animation Parameters

### Glow Animation
- **Duration**: 2 seconds per cycle
- **Direction**: In-out easing
- **Intensity**: Increases on hover

### Hover Animation
- **Duration**: 0.4 seconds
- **Transform**: Scale + translateY
- **Glow**: Multi-layer shadow enhancement

### Pulse Effect (Special)
- **Duration**: 1.5 seconds
- **Pattern**: Smooth breathing effect
- **Color-based**: Uses provided glow color

---

## 📱 Best Practices

1. **Use Appropriate Colors**
   - Cyan/Emerald: Primary actions
   - Rose: Delete/Destructive actions
   - Gold: Premium features
   - Purple: Special/Advanced options

2. **Icon Selection**
   - Match emoji to action (📸 for capture, 💾 for save)
   - Keep icons consistent
   - Use sparingly (1-2 per button)

3. **Button Sizing**
   - Small: Secondary, less important
   - Medium: Standard, balanced
   - Large: Primary, call-to-action

4. **Group Organization**
   - Related buttons together
   - Max 3-4 buttons per row on desktop
   - Stack vertically on mobile (auto with Streamlit columns)

5. **Accessibility**
   - Always include descriptive labels
   - Use high contrast colors
   - Ensure sufficient click target size

---

## 🚀 Demo Page

Run the showcase to see all buttons in action:
```bash
streamlit run glowing_buttons_demo.py
```

---

## 💡 Tips & Tricks

### Disable Animation for Static Feel
```python
glowing_button("Static", animated=False, key="static_btn")
```

### Create Icon-Only Buttons
```python
glowing_button("", icon="🚀", key="icon_btn", size="small")
```

### Group Related Actions
```python
from utils.styles import glow_button_group

action_buttons = [
    {"label": "Run", "icon": "▶️"},
    {"label": "Pause", "icon": "⏸️"},
    {"label": "Stop", "icon": "⏹️"},
]

glow_button_group(action_buttons, columns=3)
```

---

## 📊 Color Palette Reference

| Color | Hex | Primary | Glow | Use |
|--------|-----|---------|------|-----|
| Indigo | #818CF8 | #818CF8 | #6366F1 | Professional |
| Cyan | #22D3EE | #22D3EE | #06B6D4 | Primary Action |
| Emerald | #34D399 | #34D399 | #10B981 | Success |
| Rose | #FB7185 | #FB7185 | #F43F5E | Delete/Warning |
| Gold | #F59E0B | #F59E0B | #D97706 | Important |
| Purple | #A855F7 | #A855F7 | #7C3AED | Creative |
| Pink | #EC4899 | #EC4899 | #DB2777 | Fun |
| Blue | #3B82F6 | #3B82F6 | #1D4ED8 | Info |

---

## 🎯 Common Patterns

### Navigation Buttons
```python
nav_buttons = [
    {"label": "Dashboard", "icon": "📊"},
    {"label": "Analysis", "icon": "📈"},
    {"label": "Settings", "icon": "⚙️"},
]
glow_button_group(nav_buttons, columns=3)
```

### Action Buttons
```python
btn_cyan("Start", "▶️", use_container_width=True)
btn_rose("Cancel", "✕", use_container_width=True)
```

### Status Buttons
```python
btn_emerald("Active", "✓")
btn_rose("Inactive", "✕")
btn_gold("Pending", "⏳")
```

---

## 🐛 Troubleshooting

**Buttons not appearing?**
- Ensure `inject_global_css()` is called first
- Check browser console for CSS errors

**Glow not visible?**
- Verify color hex codes are valid
- Check that animations are enabled
- Ensure backdrop-filter is supported (most modern browsers)

**Performance issues?**
- Reduce number of buttons with animation=True
- Use static buttons (animated=False) for many buttons
- Consider lazy loading

---

## 📝 Updates & Customization

To add your own button style:

1. Add function to `utils/styles.py`
2. Define unique CSS class with animations
3. Return `st.markdown()` with button HTML
4. Test in `glowing_buttons_demo.py`

Example:
```python
def btn_custom(label, icon=""):
    st.markdown(f"""
    <style>
    .custom-btn {{ /* Your CSS */ }}
    </style>
    <button class="custom-btn">{icon} {label}</button>
    """, unsafe_allow_html=True)
```

---

**Happy building! Your Aura AI Studio now has premium glowing buttons! ✨**
