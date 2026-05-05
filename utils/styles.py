import streamlit as st
import streamlit.components.v1 as components
import time
import base64
import os

def inject_global_css():
    st.markdown("""
        <style>
        /* ──── AURA AI STUDIO: EXTREME NEON & ANIMATION THEME ──── */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono&display=swap');

        :root {
            --primary: #818CF8;
            --secondary: #22D3EE;
            --accent: #FB7185;
            --matrix: #34D399;
            --bg-main: #0A0E1A;
            --card-bg: rgba(15, 22, 41, 0.7);
            --text-main: #E2E8F0;
            --text-sub: #94A3B8;
            --border: rgba(34, 211, 238, 0.2);
            --glow-indigo: 0 0 25px rgba(129, 140, 248, 0.6);
            --glow-cyan: 0 0 25px rgba(34, 211, 238, 0.6);
            --glow-emerald: 0 0 25px rgba(52, 211, 153, 0.5);
            --glow-rose: 0 0 25px rgba(251, 113, 133, 0.5);
        }

        /* ──── ANIMATIONS ──── */
        @keyframes liquid-bg {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes float-heavy {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-12px) rotate(1deg); }
        }
        @keyframes border-breathe {
            0%, 100% { border-color: rgba(34, 211, 238, 0.2); box-shadow: 0 0 10px rgba(34, 211, 238, 0.1); }
            50% { border-color: rgba(129, 140, 248, 0.7); box-shadow: 0 0 30px rgba(129, 140, 248, 0.4); }
        }
        @keyframes text-glow {
            from { text-shadow: 0 0 10px rgba(226, 232, 240, 0.2); }
            to { text-shadow: 0 0 20px rgba(226, 232, 240, 0.8), 0 0 30px var(--secondary); }
        }

        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"],
        [data-testid="stMain"], .main, [data-testid="stBlockContainer"],
        [data-testid="stVerticalBlock"], .block-container, section {
            background-color: transparent !important;
            color: var(--text-main) !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        p, span, div, label, h1, h2, h3, h4, h5, h6 { color: var(--text-main); }

        /* ──── PREMIUM DARK GLASS CARDS w/ ANIMATIONS ──── */
        .premium-card {
            background: var(--card-bg);
            backdrop-filter: blur(25px) saturate(200%);
            -webkit-backdrop-filter: blur(25px) saturate(200%);
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 32px;
            margin-bottom: 24px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
            transition: all 0.5s cubic-bezier(0.25, 1, 0.5, 1);
            position: relative;
            overflow: hidden;
            animation: border-breathe 4s infinite ease-in-out;
        }

        .premium-card::before {
            content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--secondary), var(--matrix), var(--primary));
            background-size: 300% 300%;
            animation: liquid-bg 4s linear infinite;
        }

        .premium-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 50px rgba(0,0,0,0.8), var(--glow-indigo);
            border-color: rgba(34, 211, 238, 0.8);
        }

        /* ──── OVERRIDE NATIVE CONTAINERS ──── */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(10, 14, 26, 0.7) !important;
            backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(129, 140, 248, 0.25) !important;
            border-radius: 20px !important;
            padding: 26px !important;
            margin-bottom: 22px !important;
            box-shadow: 0 8px 30px rgba(0,0,0,0.5) !important;
            transition: all 0.4s ease !important;
        }
        [data-testid="stVerticalBlockBorderWrapper"]:hover {
            border-color: rgba(34, 211, 238, 0.6) !important;
            box-shadow: 0 12px 40px rgba(0,0,0,0.7), var(--glow-cyan) !important;
        }

        /* ──── GLOWING BUTTONS ──── */
        .stButton>button {
            border-radius: 12px !important;
            padding: 0.8rem 2.5rem !important;
            font-weight: 800 !important;
            letter-spacing: 1px !important;
            text-transform: uppercase !important;
            font-size: 0.85rem !important;
            color: #FFFFFF !important;
            background: linear-gradient(45deg, #4F46E5, #06B6D4, #4F46E5) !important;
            background-size: 200% 200% !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4) !important;
            transition: all 0.3s ease !important;
            animation: liquid-bg 3s infinite linear !important;
        }

        .stButton>button:hover {
            transform: scale(1.08) translateY(-3px) !important;
            box-shadow: 0 10px 30px rgba(129, 140, 248, 0.8), 0 0 20px rgba(34, 211, 238, 0.8) !important;
            border-color: #FFFFFF !important;
            color: #FFFFFF !important;
            background: linear-gradient(45deg, #6366F1, #22D3EE, #8B5CF6) !important;
            background-size: 200% 200% !important;
        }

        /* Primary override */
        .stButton>button[kind="primary"] {
            background: linear-gradient(45deg, #E11D48, #D97706, #E11D48) !important;
            box-shadow: 0 4px 20px rgba(225, 29, 72, 0.5) !important;
        }
        .stButton>button[kind="primary"]:hover {
            box-shadow: 0 10px 35px rgba(225, 29, 72, 0.8), 0 0 25px rgba(217, 119, 6, 0.8) !important;
        }

        /* ──── SIDEBAR NEON BUTTONS ──── */
        [data-testid="stSidebar"] .stButton>button {
            position: relative !important;
            background: linear-gradient(45deg, rgba(139, 92, 246, 0.8), rgba(225, 29, 72, 0.8)) !important;
            height: 4rem !important;
            width: 100% !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            text-align: left !important;
            justify-content: flex-start !important;
            padding: 0.75rem !important;
            color: #ffffff !important;
            font-size: 1.05rem !important;
            font-weight: 900 !important;
            border-radius: 0.5rem !important;
            overflow: hidden !important;
            text-decoration: none !important;
            transition-duration: 500ms !important;
            box-shadow: none !important;
            animation: none !important;
            z-index: 1 !important;
            transform: none !important;
        }
        [data-testid="stSidebar"] .stButton>button p {
            position: relative !important;
            z-index: 20 !important;
            margin: 0 !important;
            font-weight: 900 !important;
        }
        [data-testid="stSidebar"] .stButton>button::before {
            position: absolute !important;
            content: '' !important;
            width: 3rem !important;
            height: 3rem !important;
            right: 0.25rem !important;
            top: 0.25rem !important;
            z-index: 10 !important;
            background-color: #a21caf !important;
            border-radius: 9999px !important;
            filter: blur(16px) !important;
            transition-duration: 500ms !important;
            box-shadow: none !important;
        }
        [data-testid="stSidebar"] .stButton>button::after {
            position: absolute !important;
            content: '' !important;
            width: 5rem !important;
            height: 5rem !important;
            right: 2rem !important;
            top: 0.75rem !important;
            z-index: 10 !important;
            background-color: #fda4af !important;
            border-radius: 9999px !important;
            filter: blur(16px) !important;
            transition-duration: 500ms !important;
        }
        [data-testid="stSidebar"] .stButton>button:hover {
            border-color: #ffffff !important;
            color: #ffffff !important;
            transform-origin: left !important;
            transform: scale(1.02) !important;
            background: linear-gradient(45deg, #8b5cf6, #e11d48) !important;
        }
        [data-testid="stSidebar"] .stButton>button:hover::before {
            box-shadow: 20px 20px 20px 30px #a21caf !important;
            right: 3rem !important;
            bottom: -2rem !important;
            top: auto !important;
            filter: blur(4px) !important;
        }
        [data-testid="stSidebar"] .stButton>button:hover::after {
            right: -2rem !important;
        }

        /* ──── METRICS ──── */
        .stMetric {
            background: rgba(15, 22, 41, 0.8); padding: 20px; border-radius: 18px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5); border: 1px solid rgba(52, 211, 153, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .stMetric:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.7), var(--glow-emerald); border-color: var(--matrix); }
        .stMetric [data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 800; text-shadow: 0 0 10px rgba(255,255,255,0.3); }

        /* Inputs */
        input, textarea, select, [data-testid="stNumberInput"] input {
            background: rgba(10, 14, 26, 0.9) !important; color: #FFFFFF !important;
            border: 1px solid rgba(129, 140, 248, 0.4) !important; border-radius: 8px !important;
            transition: all 0.3s ease !important;
        }
        input:focus, textarea:focus {
            border-color: #22D3EE !important; box-shadow: 0 0 15px rgba(34, 211, 238, 0.5) !important;
            background: rgba(15, 22, 41, 1) !important;
        }

        hr { border-color: rgba(129, 140, 248, 0.2) !important; box-shadow: 0 0 5px rgba(129, 140, 248, 0.1); }
        
        .g-glow { animation: text-glow 2s infinite alternate; }
        </style>
    """, unsafe_allow_html=True)
    
    # ── LIVE ABSTRACT BACKGROUND ──
    components.html("""
        <script>
            const parentDoc = window.parent.document;
            if(parentDoc.getElementById('aura-bg-canvas')) parentDoc.getElementById('aura-bg-canvas').remove();
            const canvas = parentDoc.createElement('canvas'); canvas.id = 'aura-bg-canvas';
            canvas.style.position = 'fixed'; canvas.style.top = '0'; canvas.style.left = '0';
            canvas.style.width = '100vw'; canvas.style.height = '100vh'; canvas.style.zIndex = '-1'; canvas.style.pointerEvents = 'none';
            parentDoc.body.insertBefore(canvas, parentDoc.body.firstChild);
            const ctx = canvas.getContext('2d');
            let w = canvas.width = parentDoc.defaultView.innerWidth; let h = canvas.height = parentDoc.defaultView.innerHeight;
            parentDoc.defaultView.addEventListener('resize', () => { w = canvas.width = parentDoc.defaultView.innerWidth; h = canvas.height = parentDoc.defaultView.innerHeight; });

            class Particle {
                constructor() {
                    this.x = Math.random() * w; this.y = Math.random() * h;
                    this.vx = (Math.random() - 0.5) * 1.5; this.vy = (Math.random() - 0.5) * 1.5;
                    this.size = Math.random() * 3 + 1; this.hue = [190, 280, 320, 150][Math.floor(Math.random() * 4)];
                }
                update() {
                    this.x += this.vx; this.y += this.vy;
                    if(this.x < 0 || this.x > w) this.vx *= -1;
                    if(this.y < 0 || this.y > h) this.vy *= -1;
                }
                draw() {
                    ctx.beginPath(); ctx.arc(this.x, this.y, this.size, 0, Math.PI*2);
                    ctx.fillStyle = `hsl(${this.hue}, 100%, 60%)`; ctx.fill();
                    ctx.shadowBlur = 20; ctx.shadowColor = `hsl(${this.hue}, 100%, 50%)`;
                }
            }
            const particles = Array(50).fill().map(() => new Particle());
            function animate() {
                ctx.fillStyle = 'rgba(10, 14, 26, 0.15)'; ctx.fillRect(0, 0, w, h);
                particles.forEach(p => { Object.assign(ctx, {shadowBlur:0}); p.update(); p.draw(); });
                for(let i=0; i<particles.length; i++) {
                    for(let j=i+1; j<particles.length; j++) {
                        let dx = particles[i].x - particles[j].x, dy = particles[i].y - particles[j].y;
                        let dist = Math.sqrt(dx*dx + dy*dy);
                        if(dist < 150) {
                            ctx.beginPath(); ctx.moveTo(particles[i].x, particles[i].y); ctx.lineTo(particles[j].x, particles[j].y);
                            ctx.strokeStyle = `rgba(34, 211, 238, ${1 - dist/150})`; ctx.lineWidth = 1; ctx.stroke();
                        }
                    }
                }
                parentDoc.defaultView.requestAnimationFrame(animate);
            }
            animate();
        </script>
    """, height=0, width=0)

def get_base64_bin_str(bin_file):
    """Helper to convert local file to base64 for CSS url()."""
    if not os.path.exists(bin_file):
        return None
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def section_header(title, subtitle):
    st.markdown(f"""
<div style="margin-bottom:30px; position: relative;">
<div style="border-left: 5px solid #22D3EE; padding-left: 20px; text-shadow: 0 0 15px rgba(34,211,238,0.4);">
<h2 style="margin:0; font-size:32px; color: #FFFFFF; font-weight: 800; letter-spacing: -1px; text-transform:uppercase;">{title}</h2>
<div style="color:#22D3EE; font-size:13px; font-weight:700; margin-top:8px; letter-spacing: 2px; text-transform:uppercase;">{subtitle}</div>
</div>
</div>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# GLOWING GLASS BUTTONS WITH NEON EFFECTS
# ═════════════════════════════════════════════════════════════════════════════
def glowing_button(label, icon="", color="#818CF8", glow_color="#818CF8", on_click=None, key=None, use_container_width=False, animated=True, size="medium"):
    """
    Create a colorful glowing button with glass finish and neon effects.
    
    Parameters:
    - label: Button text
    - icon: Optional emoji or icon
    - color: Main button color (hex)
    - glow_color: Glow effect color (hex)
    - on_click: Callback function
    - key: Unique button key
    - use_container_width: Full width button
    - animated: Enable glow animation
    - size: "small", "medium", "large"
    """
    animation = "btn-glow-animation" if animated else ""
    size_styles = {
        "small": "padding: 8px 20px; font-size: 12px;",
        "medium": "padding: 12px 28px; font-size: 14px;",
        "large": "padding: 16px 40px; font-size: 16px;"
    }
    current_size = size_styles.get(size, size_styles["medium"])
    
    glow_rgba = glow_color.lstrip('#')
    r, g, b = int(glow_rgba[0:2], 16), int(glow_rgba[2:4], 16), int(glow_rgba[4:6], 16)
    
    st.markdown(f"""
    <style>
    @keyframes btn-glow-animation {{
        0%, 100% {{ 
            box-shadow: 0 0 10px rgba({r}, {g}, {b}, 0.5), 
                        0 0 20px rgba({r}, {g}, {b}, 0.3);
        }}
        50% {{ 
            box-shadow: 0 0 20px rgba({r}, {g}, {b}, 0.8), 
                        0 0 40px rgba({r}, {g}, {b}, 0.5),
                        0 0 60px rgba({r}, {g}, {b}, 0.2);
        }}
    }}
    
    .glow-btn-{key} {{
        all: unset;
        {current_size}
        background: linear-gradient(135deg, {color}dd, {glow_color}99);
        color: #FFFFFF;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        cursor: pointer;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4), 
                    0 0 15px rgba({r}, {g}, {b}, 0.4);
        transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1);
        animation: {animation} 2s ease-in-out infinite;
        display: inline-block;
        white-space: nowrap;
        text-align: center;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    
    .glow-btn-{key}:hover {{
        transform: translateY(-4px) scale(1.05);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5),
                    0 0 30px rgba({r}, {g}, {b}, 0.8),
                    0 0 60px rgba({r}, {g}, {b}, 0.4),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.6);
    }}
    
    .glow-btn-{key}:active {{
        transform: translateY(-1px) scale(0.98);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.4),
                    0 0 20px rgba({r}, {g}, {b}, 0.6);
    }}
    </style>
    """, unsafe_allow_html=True)
    
    button_text = f"{icon} {label}" if icon else label
    width_style = "width: 100%; display: block;" if use_container_width else ""
    
    st.markdown(f"""
    <button class="glow-btn-{key}" style="{width_style}">{button_text}</button>
    """, unsafe_allow_html=True)
    
    if on_click:
        on_click()

def glow_button_group(buttons, columns=3, spacing="small"):
    """
    Create a group of glowing buttons in a grid layout.
    
    buttons: List of dicts with keys: label, icon, color, glow_color, on_click, key
    columns: Number of columns in grid
    spacing: "small", "medium", "large"
    """
    spacing_map = {"small": "10px", "medium": "15px", "large": "20px"}
    current_spacing = spacing_map.get(spacing, "15px")
    
    cols = st.columns(columns, gap="small")
    for idx, btn_config in enumerate(buttons):
        with cols[idx % columns]:
            glowing_button(
                label=btn_config.get("label", "Button"),
                icon=btn_config.get("icon", ""),
                color=btn_config.get("color", "#818CF8"),
                glow_color=btn_config.get("glow_color", "#818CF8"),
                on_click=btn_config.get("on_click"),
                key=btn_config.get("key", f"btn_{idx}"),
                use_container_width=True,
                animated=btn_config.get("animated", True),
                size=btn_config.get("size", "medium")
            )

# ═════════════════════════════════════════════════════════════════════════════
# PRESET COLORFUL BUTTONS
# ═════════════════════════════════════════════════════════════════════════════
def btn_indigo(label, icon="", on_click=None, key=None, use_container_width=False, animated=True):
    """Indigo glowing button"""
    return glowing_button(label, icon, "#818CF8", "#6366F1", on_click, key or "btn_indigo", use_container_width, animated)

def btn_cyan(label, icon="", on_click=None, key=None, use_container_width=False, animated=True):
    """Cyan glowing button"""
    return glowing_button(label, icon, "#22D3EE", "#06B6D4", on_click, key or "btn_cyan", use_container_width, animated)

def btn_emerald(label, icon="", on_click=None, key=None, use_container_width=False, animated=True):
    """Emerald glowing button"""
    return glowing_button(label, icon, "#34D399", "#10B981", on_click, key or "btn_emerald", use_container_width, animated)

def btn_rose(label, icon="", on_click=None, key=None, use_container_width=False, animated=True):
    """Rose glowing button"""
    return glowing_button(label, icon, "#FB7185", "#F43F5E", on_click, key or "btn_rose", use_container_width, animated)

def btn_gold(label, icon="", on_click=None, key=None, use_container_width=False, animated=True):
    """Gold glowing button"""
    return glowing_button(label, icon, "#F59E0B", "#D97706", on_click, key or "btn_gold", use_container_width, animated)

def btn_purple(label, icon="", on_click=None, key=None, use_container_width=False, animated=True):
    """Purple glowing button"""
    return glowing_button(label, icon, "#A855F7", "#7C3AED", on_click, key or "btn_purple", use_container_width, animated)

def btn_pink(label, icon="", on_click=None, key=None, use_container_width=False, animated=True):
    """Pink glowing button"""
    return glowing_button(label, icon, "#EC4899", "#DB2777", on_click, key or "btn_pink", use_container_width, animated)

def btn_blue(label, icon="", on_click=None, key=None, use_container_width=False, animated=True):
    """Blue glowing button"""
    return glowing_button(label, icon, "#3B82F6", "#1D4ED8", on_click, key or "btn_blue", use_container_width, animated)

# ═════════════════════════════════════════════════════════════════════════════
# ADVANCED EFFECTS BUTTONS
# ═════════════════════════════════════════════════════════════════════════════
def btn_rainbow(label, icon="", on_click=None, key=None):
    """Rainbow animated gradient button with cycling glow"""
    st.markdown(f"""
    <style>
    @keyframes rainbow-shift {{
        0% {{ filter: hue-rotate(0deg); background: linear-gradient(135deg, #818CF8, #22D3EE); }}
        25% {{ filter: hue-rotate(90deg); background: linear-gradient(135deg, #22D3EE, #34D399); }}
        50% {{ filter: hue-rotate(180deg); background: linear-gradient(135deg, #34D399, #FB7185); }}
        75% {{ filter: hue-rotate(270deg); background: linear-gradient(135deg, #FB7185, #F59E0B); }}
        100% {{ filter: hue-rotate(360deg); background: linear-gradient(135deg, #818CF8, #22D3EE); }}
    }}
    
    .rainbow-btn {{
        all: unset;
        padding: 14px 32px;
        font-size: 14px;
        color: #FFFFFF;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        border: 2px solid rgba(255, 255, 255, 0.4);
        border-radius: 12px;
        cursor: pointer;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
        animation: rainbow-shift 4s ease-in-out infinite;
        display: inline-block;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    
    .rainbow-btn:hover {{
        transform: translateY(-5px) scale(1.08);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.6), 0 0 50px rgba(255, 100, 100, 0.5);
        border-color: rgba(255, 255, 255, 0.8);
    }}
    </style>
    <button class="rainbow-btn">{"🌈 " + label if not icon else f"{icon} {label}"}</button>
    """, unsafe_allow_html=True)

def btn_neon_pulse(label, icon="", color="#22D3EE", on_click=None, key=None):
    """Button with pulsing neon effect"""
    glow_rgba = color.lstrip('#')
    r, g, b = int(glow_rgba[0:2], 16), int(glow_rgba[2:4], 16), int(glow_rgba[4:6], 16)
    
    st.markdown(f"""
    <style>
    @keyframes neon-pulse {{
        0%, 100% {{ 
            box-shadow: 0 0 5px rgba({r}, {g}, {b}, 0.5),
                        inset 0 0 5px rgba({r}, {g}, {b}, 0.1);
        }}
        50% {{
            box-shadow: 0 0 20px rgba({r}, {g}, {b}, 1),
                        0 0 40px rgba({r}, {g}, {b}, 0.8),
                        inset 0 0 10px rgba({r}, {g}, {b}, 0.3),
                        0 0 60px rgba({r}, {g}, {b}, 0.4);
        }}
    }}
    
    .neon-pulse-btn {{
        all: unset;
        padding: 14px 32px;
        font-size: 14px;
        background: rgba({r}, {g}, {b}, 0.15);
        color: #{color.lstrip('#')};
        border: 2px solid #{color.lstrip('#')};
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        border-radius: 12px;
        cursor: pointer;
        backdrop-filter: blur(12px);
        animation: neon-pulse 1.5s ease-in-out infinite;
        display: inline-block;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    
    .neon-pulse-btn:hover {{
        transform: scale(1.08);
        border-color: rgba(255, 255, 255, 0.8);
        color: #FFFFFF;
    }}
    </style>
    <button class="neon-pulse-btn">{f"{icon} {label}" if icon else label}</button>
    """, unsafe_allow_html=True)

def gradient_header(title, sub, icon="", img_path=None):
    img_layer = ""
    if img_path:
        is_url = img_path.startswith(("http://", "https://"))
        is_data = img_path.startswith("data:")
        
        full_path = img_path
        if not (is_url or is_data):
            b64 = get_base64_bin_str(img_path)
            if b64:
                full_path = f"data:image/png;base64,{b64}"
            else:
                full_path = "https://images.unsplash.com/photo-1620712943543-bcc4638ef80b?auto=format&fit=crop&q=80&w=1200"
        
        img_layer = f"""<div style="position:absolute; inset:0; background-image: url('{full_path}'); background-size: cover; background-position: center; opacity: 0.65; filter: brightness(0.9) contrast(1.1);"></div>"""
    
    st.markdown(f"""
<div style="background:
radial-gradient(circle at 18% 20%, rgba(129,140,248,0.2), transparent 24%),
radial-gradient(circle at 82% 24%, rgba(34,211,238,0.15), transparent 22%),
linear-gradient(135deg, rgba(5,8,22,1) 0%, rgba(15,23,42,0.95) 42%, rgba(17,24,39,1) 100%);
border-radius: 24px; position:relative; overflow: hidden;
box-shadow: 0 15px 50px rgba(0,0,0,0.8), 0 0 30px rgba(129,140,248,0.3); margin-bottom: 40px; min-height: 220px;">
{img_layer}
<div style="position:absolute; inset:0; background:
linear-gradient(135deg, rgba(10,14,26,0.4), rgba(20,27,55,0.3));
backdrop-filter: blur(4px);"></div>
<div style="position:absolute; inset:0; opacity:0.15; background:
linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.08) 50%, transparent 100%);
transform: skewY(-8deg) scale(1.2);"></div>
<div style="position: absolute; bottom: 0; left: 0; right: 0; height: 5px; background: linear-gradient(90deg, #818CF8, #22D3EE, #34D399, #818CF8); background-size: 300%; animation: liquid-bg 3s linear infinite;"></div>
<div style="padding: 50px; display: flex; align-items: center; gap: 35px; position: relative; z-index: 2;">
<div style="font-size: 70px; padding: 20px; background: rgba(255,255,255,0.08); border-radius: 50%; border: 2px inset rgba(34,211,238,0.5);
box-shadow: 0 0 30px rgba(34,211,238,0.3); animation: float-heavy 4s infinite ease-in-out;">{icon}</div>
<div>
<h1 class="g-glow" style="font-size: 52px; margin: 0; color: #FFFFFF; font-weight: 800; letter-spacing: -2px; text-transform: uppercase;">{title}</h1>
<div style="display:inline-block; border:1px solid #22D3EE; background:rgba(34,211,238,0.15); padding:8px 20px; border-radius:30px; margin-top:15px; box-shadow:0 0 15px rgba(34,211,238,0.2);">
<span style="color:#22D3EE; font-size:14px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase;">
{sub}
</span>
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

def image_card(title, desc, img_path):
    is_url = img_path.startswith(("http://", "https://"))
    is_data = img_path.startswith("data:")
    
    full_path = img_path
    if not (is_url or is_data):
        b64 = get_base64_bin_str(img_path)
        if b64:
            full_path = f"data:image/png;base64,{b64}"
        else:
            full_path = "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=800"

    st.markdown(f"""
<div class="premium-card" style="padding: 0; overflow: hidden; border: 1px solid rgba(129,140,248,0.3);">
    <div style="height: 160px; background-image: url('{full_path}'); background-size: cover; background-position: center; position: relative;">
        <div style="position: absolute; inset: 0; background: linear-gradient(to bottom, transparent, rgba(10,14,26,0.9));"></div>
    </div>
    <div style="padding: 24px;">
        <div style="font-size:11px; letter-spacing:1.7px; color:#22D3EE; font-weight:800; text-transform: uppercase;">MODULE</div>
        <h3 style="font-size:24px; color:#F8FAFC; margin:10px 0 8px; font-weight:800;">{title}</h3>
        <p style="color:#CBD5E1; font-size:13px; line-height:1.6; margin-bottom: 0;">{desc}</p>
    </div>
</div>
""", unsafe_allow_html=True)

def render_log(placeholder, logs):
    curr_time = time.strftime("%H:%M:%S")
    log_html = "".join([f'<div style="color: #34D399; font-family: \'JetBrains Mono\', monospace; font-size: 13px; margin-bottom: 12px; border-bottom: 1px dotted rgba(52,211,153,0.3); padding-bottom:8px;">'
                        f'<span style="color: #22D3EE; font-weight: 700; text-shadow:0 0 5px #22D3EE;">[{curr_time}]</span> <span style="margin-left:12px;">{msg}</span></div>' for msg in logs[-8:]])
    placeholder.markdown(f"""
<div class="premium-card">
<div style="font-size: 16px; color: #FFFFFF; margin-bottom: 25px; font-weight: 800; display: flex; align-items: center; gap: 15px; letter-spacing: 1px;">
<div style="width: 15px; height: 15px; border-radius: 50%; background: #FB7185; box-shadow: 0 0 15px #FB7185; animation: text-glow 1s infinite alternate;"></div>
SYSTEM CONSOLE STREAM
</div>
<div style="max-height: 400px; overflow-y: auto;">
{log_html if logs else '<div style="color: #475569; font-style: italic;">AWAITING NEURAL INJECTION.</div>'}
</div>
</div>
""", unsafe_allow_html=True)

def stat_card(label, val, icon="", delta=None, color="#22D3EE"):
    d_html = f'<div style="color:{"#34D399" if delta >= 0 else "#FB7185"}; font-size:12px; font-weight:800; margin-top:8px;">{"↑" if delta>=0 else "↓"} {abs(delta)}% DELTA</div>' if delta is not None else ""
    st.markdown(f"""
<div class="premium-card" style="padding: 25px; border-left: 4px solid {color}; border-top:none;">
<div style="display:flex; justify-content:space-between; align-items:flex-start;">
<div>
<div style="color:#CBD5E1; font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:2px; margin-bottom:10px;">{label}</div>
<div style="color:#FFFFFF; font-size:36px; font-weight:800; text-shadow: 0 0 15px {color};">{val}</div>
{d_html}
</div>
<div style="font-size:32px; background: rgba(255,255,255,0.05); padding:10px; border-radius:12px; box-shadow: inset 0 0 10px {color};">{icon}</div>
</div>
</div>
""", unsafe_allow_html=True)

def render_theory_card(title, content, formulas=None, color="#818CF8"):
    formula_html = ""
    if formulas:
        formula_html = '<div style="margin-top: 20px; display: flex; flex-wrap: wrap; gap: 12px;">'
        for f in formulas:
            formula_html += f'<div style="background: rgba(10,14,26,0.8); border: 1px solid {color}; padding: 12px 20px; border-radius: 8px; font-family: \'JetBrains Mono\'; font-size: 15px; color: #FFF; box-shadow: 0 0 15px rgba(129,140,248,0.2);">{f}</div>'
        formula_html += '</div>'
    
    card_id = abs(hash(title)) % 100000
    st.markdown(f"""
<style>
.theory-card-{card_id} b {{ color: {color}; text-shadow: 0 0 8px {color}88; font-weight:800; }}
.theory-card-{card_id} strong {{ color: {color}; text-shadow: 0 0 8px {color}88; font-weight:800; }}
</style>
<div class="premium-card theory-card-{card_id}" style="border-top: 5px solid {color}; background:
radial-gradient(circle at 12% 18%, rgba(129,140,248,0.18), transparent 24%),
radial-gradient(circle at 88% 20%, rgba(34,211,238,0.14), transparent 20%),
linear-gradient(145deg, rgba(15,22,41,0.95), rgba(8,15,31,0.98));">
<div style="position:absolute; inset:0; background:
linear-gradient(135deg, rgba(255,255,255,0.03), transparent 28%, rgba(34,211,238,0.04) 100%);
backdrop-filter:blur(8px);"></div>
<div style="position:relative; z-index:2;">
<h4 style="color: #FFFFFF; font-size: 22px; font-weight: 800; text-transform:uppercase; letter-spacing:1px; margin-top:0;">{title}</h4>
<div style="color: #E2E8F0; font-size: 15px; line-height: 2; font-weight:500;">
{content}
</div>
{formula_html}
</div>
</div>
""", unsafe_allow_html=True)

def render_nlp_insight(text, label, clr="#22D3EE"):
    st.markdown(f"""
<div class="premium-card" style="border-right: 4px solid {clr};">
<div style="font-size:14px; color:{clr}; font-weight: 800; margin-bottom:15px; text-transform:uppercase; letter-spacing:2px; text-shadow:0 0 10px {clr};">
{label}
</div>
<div style="font-size:16px; color:#FFFFFF; line-height: 1.8; font-weight: 600; background: rgba(0,0,0,0.4); padding: 25px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
{text}
</div>
</div>
""", unsafe_allow_html=True)

def premium_card_wrapper(title, sub, content):
    st.markdown(f"""
<div class="premium-card">
<div style="font-size:11px; color:#94A3B8; font-weight:800; text-transform:uppercase; letter-spacing:2px; margin-bottom:5px;">{sub}</div>
<h3 style="margin-top:0; color:white; font-size:24px; font-weight:800; letter-spacing:-1px;">{title}</h3>
<div style="color:#CBD5E1; line-height:1.6;">{content}</div>
</div>
""", unsafe_allow_html=True)

MODULE_THEMES = {'opencv': {'primary': '#4F46E5', 'secondary': '#06B6D4'}}

def inject_module_theme(theme):
    pass

def render_content_card(title, content, accent_color='#22D3EE', icon=''):
    st.markdown(f'<div class="premium-card"><h4>{icon} {title}</h4><div>{content}</div></div>', unsafe_allow_html=True)

def render_info_grid(data):
    for key, value in data.items():
        st.markdown(f'**{key}**: {value}')

