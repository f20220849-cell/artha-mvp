import streamlit as st
import math
import time

st.set_page_config(
    page_title="ARTHA: Financial Clarity Engine",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

NAVY   = "#0C1E3A"
NAVY2  = "#132847"
TEAL   = "#0B7563"
TEAL2  = "#0D8B75"
GOLD   = "#B8820A"
CORAL  = "#C24A35"
INDIGO = "#2A4A8C"
SLATE  = "#334155"
STEEL  = "#64748B"
BORDER = "#E2E8F0"
MIST   = "#F1F5F9"
WHITE  = "#FFFFFF"
TEXT   = "#1E293B"
MINT   = "#3DD4B0"
S_BG   = {"good": "#E6F4F1", "warn": "#FFF8E6", "bad": "#FDF0EE"}
S_LBL  = {"good": "Good", "warn": "Watch", "bad": "Urgent"}
S_COL  = {"good": TEAL2, "warn": GOLD, "bad": CORAL}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&family=DM+Mono&display=swap');
html, body, [class*="css"], .stApp {{ font-family: 'DM Sans', sans-serif !important; background: {MIST} !important; }}
#MainMenu, footer, header, .stDeployButton {{ visibility: hidden !important; }}
section[data-testid="stSidebar"] {{ display: none !important; }}
.block-container {{ padding: 1.5rem 2rem 3rem !important; max-width: 100% !important; }}
[data-testid="stNumberInput"] input {{ background: {WHITE} !important; border: 1.5px solid {BORDER} !important; border-radius: 8px !important; font-size: 14px !important; color: {TEXT} !important; font-family: 'DM Sans', sans-serif !important; }}
[data-testid="stNumberInput"] input:focus {{ border-color: {TEAL2} !important; box-shadow: 0 0 0 2px rgba(13,139,117,0.15) !important; }}
[data-testid="stNumberInput"] label {{ font-size: 11px !important; font-weight: 600 !important; color: {SLATE} !important; text-transform: uppercase !important; letter-spacing: 0.04em !important; }}
[data-baseweb="select"] > div {{ background: {WHITE} !important; border: 1.5px solid {BORDER} !important; border-radius: 8px !important; font-size: 14px !important; color: {TEXT} !important; }}
.stSelectbox label {{ font-size: 11px !important; font-weight: 600 !important; color: {SLATE} !important; text-transform: uppercase !important; letter-spacing: 0.04em !important; }}
.stSlider label {{ font-size: 11px !important; font-weight: 600 !important; color: {SLATE} !important; text-transform: uppercase !important; letter-spacing: 0.04em !important; }}
div[data-testid="stButton"] > button {{ background: linear-gradient(135deg, {TEAL} 0%, {TEAL2} 100%) !important; color: white !important; border: none !important; border-radius: 10px !important; font-weight: 700 !important; font-size: 15px !important; height: 52px !important; width: 100% !important; font-family: 'DM Sans', sans-serif !important; box-shadow: 0 4px 16px rgba(11,117,99,0.3) !important; transition: all 0.2s !important; }}
div[data-testid="stButton"] > button:hover {{ box-shadow: 0 8px 24px rgba(11,117,99,0.45) !important; transform: translateY(-1px) !important; }}
.stTabs [data-baseweb="tab-list"] {{ background: {WHITE} !important; border-radius: 12px !important; padding: 5px !important; gap: 3px !important; border: 1px solid {BORDER} !important; box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important; }}
.stTabs [data-baseweb="tab"] {{ border-radius: 8px !important; font-size: 13px !important; font-weight: 500 !important; padding: 8px 20px !important; color: {STEEL} !important; font-family: 'DM Sans', sans-serif !important; }}
.stTabs [aria-selected="true"] {{ background: {NAVY} !important; color: white !important; box-shadow: 0 2px 8px rgba(12,30,58,0.25) !important; }}
.stTabs [data-baseweb="tab-panel"] {{ padding-top: 20px !important; }}
[data-testid="stMetric"] {{ background: {WHITE} !important; border: 1px solid {BORDER} !important; border-radius: 12px !important; padding: 16px 18px !important; box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important; }}
[data-testid="stMetric"] label {{ font-size: 11px !important; color: {STEEL} !important; text-transform: uppercase !important; letter-spacing: 0.06em !important; font-weight: 600 !important; }}
[data-testid="stMetricValue"] {{ font-family: 'DM Serif Display', serif !important; font-size: 26px !important; color: {NAVY} !important; }}
hr {{ border-color: {BORDER} !important; }}
.stSpinner > div {{ border-top-color: {TEAL2} !important; }}
</style>
""", unsafe_allow_html=True)


def analyse(d):
    cc_interest  = round(d["cc"] * 0.42 / 12)
    sip_return   = round(d["sip"] * 0.01)
    exp_target   = d["exp"] * 3
    emerg_months = round(d["sav"] / d["exp"], 1) if d["exp"] > 0 else 0.0
    emerg_gap    = max(0, round(exp_target - d["sav"]))
    net_after    = d["salary"] - d["exp"] - (round(d["cc"] * 0.05) if d["cc"] > 0 else 0)
    sav_rate     = max(0, round((net_after / d["salary"]) * 100)) if d["salary"] > 0 else 0

    if emerg_months >= 3:   ef = 20
    elif emerg_months >= 2: ef = 14
    elif emerg_months >= 1: ef = 8
    elif d["sav"] > 0:      ef = 4
    else:                   ef = 0

    dm = 20
    if d["cc"] > 0:
        ratio = d["cc"] / d["salary"] if d["salary"] > 0 else 99
        if   ratio > 1.5: dm = 2
        elif ratio > 0.8: dm = 6
        elif ratio > 0.4: dm = 10
        elif ratio > 0.1: dm = 14
        else:             dm = 17

    ins_map   = {"none": 2, "employer": 8, "partial": 13, "adequate": 20}
    ins_score = ins_map.get(d["ins"], 8)
    if d["dep"] > 1 and d["ins"] != "adequate":
        ins_score = max(2, ins_score - 4)

    if   sav_rate >= 30: ir = 20
    elif sav_rate >= 20: ir = 16
    elif sav_rate >= 12: ir = 11
    elif sav_rate >= 6:  ir = 7
    else:                ir = 3
    if d["sip"] > 0 and ir > 3:
        ir = min(20, ir + 2)

    req_map = {"stability": max(1, d["salary"]*0.10), "house": max(1, d["salary"]*0.25),
               "retirement": max(1, d["salary"]*0.15), "education": 8000, "business": max(1, d["salary"]*0.20)}
    req = req_map.get(d["goal"], max(1, d["salary"] * 0.10))
    if   d["sip"] >= req:        ga = 18
    elif d["sip"] >= req * 0.6:  ga = 13
    elif d["sip"] >= req * 0.3:  ga = 8
    else:                        ga = 4
    if ef < 8: ga = max(3, ga - 4)

    total = ef + dm + ins_score + ir + ga
    if   total >= 75: category = "Thriving"
    elif total >= 55: category = "On Track"
    elif total >= 35: category = "Attention Needed"
    else:             category = "Urgent Action Required"

    if   d["cc"] > d["salary"]*0.4 and d["sip"] > 0:                           profile = "Anxious Achiever"
    elif d["inv"] > d["salary"]*3   and d["ins"] != "adequate":                 profile = "Confident Optimiser"
    elif d["salary"] < 50000        and d["sav"] < d["exp"]:                    profile = "Overwhelmed Beginner"
    elif d["cc"] == 0 and d["ins"] == "employer" and d["inv"] > d["salary"]*2: profile = "Good But Exposed"
    else:                                                                        profile = "Steady Builder"

    def sf(sc): return "good" if sc >= 14 else ("warn" if sc >= 8 else "bad")

    debt_wins    = d["cc"] > 0 and cc_interest > sip_return * 1.5
    months_clear = math.ceil(d["cc"] / max(1, d["sip"] + cc_interest*0.3)) if (debt_wins and d["sip"] > 0) else 0

    if debt_wins and d["sip"] > 0:
        action = {"title": "Redirect your SIP to clear your credit card",
                  "desc": (f"Your credit card charges Rs {cc_interest:,} per month in interest at 42% annually. "
                           f"Your SIP grows by roughly Rs {sip_return:,} per month. "
                           f"You are losing Rs {cc_interest - sip_return:,} every month on this gap. "
                           f"Pause your SIP for {months_clear} months and redirect Rs {d['sip']:,} to your card. "
                           f"Once cleared, restart your SIP at a better market entry point."),
                  "saving": f"Rs {round(cc_interest*months_clear*0.7):,} in interest saved",
                  "timeframe": f"{months_clear} months to debt-free"}
    elif emerg_months < 1:
        months_build = math.ceil(emerg_gap / max(1, round(d["salary"]*0.15)))
        action = {"title": "Build your emergency fund before anything else",
                  "desc": (f"You have less than one month of liquid savings. "
                           f"A single unexpected expense would force you into debt or investment liquidation. "
                           f"Set aside Rs {round(d['salary']*0.15):,} per month into a liquid fund. "
                           f"Your target is Rs {exp_target:,}, which covers three months of your expenses."),
                  "saving": f"Rs {exp_target:,} safety net",
                  "timeframe": f"{months_build} months to build it"}
    elif d["ins"] in ("none", "employer") and d["dep"] > 0:
        action = {"title": "Get term insurance this month, not next month",
                  "desc": (f"{'You have no insurance.' if d['ins'] == 'none' else 'Your employer cover disappears if you switch or lose your job.'} "
                           f"With {d['dep']} financial dependant{'s' if d['dep'] > 1 else ''}, this is your most urgent financial risk. "
                           f"A Rs 1 crore term policy costs Rs 800 to Rs 1,200 per month at your age. "
                           f"Get quotes on PolicyBazaar or Ditto Insurance this week."),
                  "saving": "Rs 1 crore family protection",
                  "timeframe": "Policy active within 7 days"}
    elif sav_rate < 10:
        target = round(d["salary"]*0.20)
        action = {"title": "Fix your savings rate: it is critically low",
                  "desc": (f"You are saving approximately {sav_rate}% of your take-home salary. "
                           f"The target at your age is 20 to 25%. "
                           f"Automate a transfer of Rs {target:,} on your salary date, before you spend anything. "
                           f"What you do not see, you do not spend."),
                  "saving": f"Rs {target*12:,} more saved per year",
                  "timeframe": "Start this salary cycle"}
    else:
        increase = round(d["salary"]*0.05)
        action = {"title": "Increase your SIP by 5% of your salary",
                  "desc": (f"Your financial foundations are solid. The highest-leverage move now is compounding. "
                           f"Increasing your SIP by Rs {increase:,} per month adds approximately Rs {round(increase*12*15):,} "
                           f"to your corpus over 15 years at 12% annual return."),
                  "saving": f"Rs {round(increase*12*15):,} over 15 years",
                  "timeframe": "Set it up in 5 minutes"}

    fresh = ({"exists": True,
              "signal": "Your employer group cover is tied to your current job. It disappears on your last working day if you switch or are laid off.",
              "action": "Get a personal health policy with at least Rs 5 lakh sum insured, independent of your employer."}
             if d["ins"] == "employer" else
             {"exists": True,
              "signal": "You are simultaneously building wealth through your SIP and destroying it through credit card interest. Most people do not realise the net effect is negative.",
              "action": f"Your true net wealth-building rate is Rs {sip_return - cc_interest:,} per month. That is negative. Address the card first."}
             if d["cc"] > 0 and d["sip"] > 0 and cc_interest > sip_return else
             {"exists": False, "signal": "", "action": ""})

    corpus_x = round(d["inv"]/d["salary"], 1) if d["salary"] > 0 else 0
    comp = ({"observation": f"At your income and age, most peers have 6 to 8 times their monthly salary in investments. Your corpus is {corpus_x}x your monthly salary.",
             "attribute": f"Investment corpus of Rs {d['salary']*6:,} or more",
             "action": f"Increase your SIP to Rs {round(d['salary']*0.18):,} and stay invested through market cycles."}
            if d["inv"] < d["salary"]*6 and d["age"] > 27 else
            {"observation": "Professionals who complete a financial review treat personal term insurance as the first non-negotiable product.",
             "attribute": "Personal term insurance cover of 10 to 15 times annual income",
             "action": "Get a term policy this month. Quotes take 10 minutes on PolicyBazaar."}
            if d["ins"] != "adequate" else
            {"observation": f"Peers with your profile grow their SIP corpus aggressively rather than holding large amounts in savings accounts earning below inflation.",
             "attribute": "A diversified SIP across large-cap index, mid-cap, and international funds",
             "action": f"Ensure at least 70% of your portfolio is in equity for your {max(5, 55-d['age'])}-year horizon."})

    pillars = [
        {"name": "Emergency Fund",    "icon": "🛡️", "score": ef,        "status": sf(ef),
         "detail": f"Excellent. {emerg_months} months covered. Target fully met." if ef >= 18
                   else f"You have {emerg_months} months of coverage. Target: Rs {exp_target:,}. Gap: Rs {emerg_gap:,}."},
        {"name": "Debt Management",   "icon": "💳", "score": dm,        "status": sf(dm),
         "detail": f"Rs {d['cc']:,} outstanding at 42% annual costs Rs {cc_interest:,} per month in interest." if d["cc"] > 0
                   else "No high-interest debt. Your strongest pillar."},
        {"name": "Insurance Coverage","icon": "🔒", "score": ins_score, "status": sf(ins_score),
         "detail": {"none": "No insurance of any kind. The most critical gap in your entire profile.",
                    "employer": f"Employer cover only. Disappears if you change jobs.{' Urgent with dependants.' if d['dep'] > 0 else ''}",
                    "partial": "Health cover exists but no term insurance for income replacement.",
                    "adequate": "Full term and health cover in place. Well protected."}.get(d["ins"], "")},
        {"name": "Investment Rate",   "icon": "📈", "score": ir,        "status": sf(ir),
         "detail": f"Savings rate: {sav_rate}% of salary. Target: 20 to 25%. SIP: Rs {d['sip']:,} per month." if sav_rate < 20
                   else f"Strong savings rate of {sav_rate}%. SIP of Rs {d['sip']:,} per month building real wealth."},
        {"name": "Goal Alignment",    "icon": "🎯", "score": ga,        "status": sf(ga),
         "detail": f"Your SIP of Rs {d['sip']:,} per month is {'well aligned with' if ga >= 14 else 'below what is needed for'} your goal to {d['goal'].replace('_',' ')}."},
    ]

    if debt_wins and d["sip"] > 0:
        summary = f"Every month you run your SIP alongside this credit card balance, you lose Rs {cc_interest - sip_return:,} in net wealth. Your most urgent priority is not investment optimisation. It is stopping the leak first."
    elif emerg_months < 1:
        summary = "Your financial structure has a critical gap at the foundation. With less than one month of liquid savings, any unexpected expense forces you into debt or investment liquidation."
    elif d["ins"] == "none":
        summary = "You are building investments without any protection layer underneath. One medical emergency could wipe out everything you have accumulated. Getting cover is the single highest-leverage decision this month."
    elif total >= 65:
        summary = "Your financial foundations are genuinely solid. You are in the top quartile for your age and income. The opportunity now is optimisation: tighter goal alignment and efficient allocation as your corpus grows."
    else:
        summary = f"You have made a real start but specific gaps are holding your score back. Your savings rate of {sav_rate}% needs attention and your goal alignment can be improved with targeted changes this month."

    if debt_wins and d["sip"] > 0:
        roadmap = [
            ("This week", f"Pause your Rs {d['sip']:,} SIP. Set a standing instruction to pay that amount to your credit card on the 1st of each month.", CORAL),
            ("Month 1", "Your card balance drops visibly. Track the interest charge shrinking month on month.", GOLD),
            ("Month 3", "Every rupee cleared now reduces next month's interest charge too. Momentum builds.", TEAL2),
            (f"Month {months_clear}", f"Credit card cleared. Restart your SIP immediately and add the freed interest savings on top.", TEAL2),
            ("Month 12", f"Your ARTHA score should cross 65. Net monthly wealth accumulation has improved by Rs {cc_interest:,} vs where you started.", NAVY),
        ]
    elif emerg_months < 1.5:
        roadmap = [
            ("This week", f"Open a liquid mutual fund on Groww or Kuvera. Set a standing instruction for Rs {round(d['salary']*0.15):,} on your salary date.", TEAL2),
            ("Month 2", f"Emergency fund grows to Rs {round(d['salary']*0.3):,}. Any expense under this no longer requires borrowing.", GOLD),
            ("Month 4", "Approaching two months of coverage. Begin reviewing whether to increase your SIP in parallel.", TEAL2),
            ("Month 6", f"Three-month target reached: Rs {exp_target:,}. Your foundation is stable. Invest aggressively now.", TEAL2),
            ("Month 9", "Redirect the emergency savings amount into long-term equity SIPs. Wealth-building begins in earnest.", NAVY),
        ]
    else:
        roadmap = [
            ("This week", "Review your SIP allocation. Ensure you have at least one large-cap index fund as your core holding.", TEAL2),
            ("Month 1", "If insurance is missing, get quotes now. A Rs 1 crore term policy at your age costs less than one restaurant dinner per week.", CORAL),
            ("Month 3", f"Increase your SIP by Rs {round(d['salary']*0.03):,} using your next salary increment.", GOLD),
            ("Month 6", "Review your ARTHA score. Target: 65 or above. Fix any pillar in the warning zone before expanding investments.", TEAL2),
            ("Year 1", f"At current trajectory, your corpus should reach approximately Rs {round(d['inv']*1.12 + d['sip']*12*1.06):,}. Stay invested through corrections.", NAVY),
        ]

    return {"profile": profile, "total": total, "category": category, "summary": summary,
            "pillars": pillars, "action": action, "fresh": fresh, "comp": comp, "roadmap": roadmap,
            "data": {"cc_interest": cc_interest, "sip_return": sip_return, "emerg_months": emerg_months,
                     "emerg_gap": emerg_gap, "sav_rate": sav_rate, "exp_target": exp_target}}


SAMPLES = {
    "Priya, 27: Software Engineer":   dict(salary=93000,  cc=62000, sip=6000,  inv=180000, sav=32000,  exp=52000, dep=0, ins="employer", goal="stability",  age=27),
    "Arjun, 31: Product Manager":     dict(salary=185000, cc=5000,  sip=8000,  inv=750000, sav=140000, exp=85000, dep=2, ins="partial",  goal="house",       age=31),
    "Meera, 24: Marketing Executive": dict(salary=35000,  cc=0,     sip=1000,  inv=4200,   sav=8000,   exp=22000, dep=0, ins="none",     goal="stability",   age=24),
    "Raj, 33: Senior Analyst":        dict(salary=120000, cc=0,     sip=12000, inv=480000, sav=95000,  exp=55000, dep=1, ins="employer", goal="retirement",  age=33),
}
INS_OPTIONS  = ["none", "employer", "partial", "adequate"]
GOAL_OPTIONS = ["stability", "house", "retirement", "education", "business"]
INS_LABELS   = {"none": "No insurance at all", "employer": "Employer group cover only",
                "partial": "Health only, no term cover", "adequate": "Full term and health cover"}
GOAL_LABELS  = {"stability": "Build financial stability", "house": "Buy a home in 5 to 7 years",
                "retirement": "Early retirement / FIRE", "education": "Child education corpus",
                "business": "Start a business in 3 years"}

if "result" not in st.session_state:
    st.session_state.result = None
if "inputs" not in st.session_state:
    st.session_state.inputs = None

# ── TOP NAV ───────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:{NAVY};border-radius:14px;padding:16px 26px;margin-bottom:22px;
     display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px">
  <div style="display:flex;align-items:center;gap:12px">
    <div style="width:34px;height:34px;background:linear-gradient(135deg,{TEAL},{TEAL2});
         border-radius:9px;display:flex;align-items:center;justify-content:center;
         font-family:'DM Serif Display',serif;font-size:17px;color:white">A</div>
    <div>
      <div style="font-family:'DM Serif Display',serif;font-size:21px;color:white;letter-spacing:0.02em;line-height:1.1">ARTHA</div>
      <div style="font-size:10px;color:rgba(255,255,255,0.32);text-transform:uppercase;letter-spacing:0.1em">Financial Clarity Engine</div>
    </div>
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap">
    <span style="font-size:11px;color:rgba(255,255,255,0.4);border:1px solid rgba(255,255,255,0.1);padding:3px 11px;border-radius:20px">MVP v1.0</span>
    <span style="font-size:11px;color:rgba(255,255,255,0.4);border:1px solid rgba(255,255,255,0.1);padding:3px 11px;border-radius:20px">Portfolio Project by Aditya Bayar</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── INPUT FORM ────────────────────────────────────────────────────
if st.session_state.result is None:

    st.markdown(f"""
    <div style="text-align:center;padding:24px 20px 28px 20px">
      <div style="width:68px;height:68px;background:linear-gradient(135deg,#E6F4F1,#F0FBF8);
           border:1px solid {BORDER};border-radius:17px;display:flex;align-items:center;
           justify-content:center;font-size:32px;margin:0 auto 16px auto">📡</div>
      <h2 style="font-family:'DM Serif Display',serif;font-size:28px;color:{NAVY};font-weight:400;margin-bottom:9px">Your financial clarity starts here</h2>
      <p style="font-size:14px;color:{STEEL};max-width:460px;margin:0 auto;line-height:1.75">
        Fill in your numbers below and ARTHA will tell you exactly where your money is working and where it is quietly leaking.
      </p>
    </div>
    """, unsafe_allow_html=True)

    sample_key = st.selectbox(
        "Load a sample profile",
        ["Enter my own numbers"] + list(SAMPLES.keys()),
        key="sample_sel",
    )
    defaults = SAMPLES.get(sample_key, dict(salary=75000, cc=45000, sip=5000, inv=120000,
                                             sav=18000, exp=35000, dep=0, ins="employer",
                                             goal="stability", age=28))
    st.markdown("<br>", unsafe_allow_html=True)

    # Financial Profile section
    st.markdown(f"<div style='font-size:12px;font-weight:700;color:{NAVY};text-transform:uppercase;letter-spacing:0.07em;margin-bottom:12px;display:flex;align-items:center;gap:8px'><span style='width:4px;height:14px;background:{TEAL2};border-radius:2px;display:inline-block'></span>Financial Profile</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        salary = st.number_input("Monthly Take-Home Salary (Rs)", min_value=0, step=1000, value=int(defaults["salary"]))
        cc     = st.number_input("Credit Card Outstanding Balance (Rs)", min_value=0, step=1000, value=int(defaults["cc"]))
    with c2:
        sip = st.number_input("Monthly SIP Amount (Rs)", min_value=0, step=500, value=int(defaults["sip"]))
        inv = st.number_input("Total Investments (Rs)", min_value=0, step=5000, value=int(defaults["inv"]))
    with c3:
        sav = st.number_input("Liquid Savings / Emergency Fund (Rs)", min_value=0, step=1000, value=int(defaults["sav"]))
        exp = st.number_input("Monthly Fixed Expenses (Rs)", min_value=0, step=1000, value=int(defaults["exp"]))

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:12px;font-weight:700;color:{NAVY};text-transform:uppercase;letter-spacing:0.07em;margin-bottom:12px;display:flex;align-items:center;gap:8px'><span style='width:4px;height:14px;background:{GOLD};border-radius:2px;display:inline-block'></span>Life Situation</div>", unsafe_allow_html=True)
    c4, c5, c6, c7 = st.columns(4)
    with c4:
        dep  = st.selectbox("Financial Dependants", [0, 1, 2, 3], index=min(int(defaults["dep"]), 3))
    with c5:
        ins  = st.selectbox("Insurance Status", INS_OPTIONS, index=INS_OPTIONS.index(defaults["ins"]), format_func=lambda x: INS_LABELS[x])
    with c6:
        goal = st.selectbox("Primary Goal", GOAL_OPTIONS, index=GOAL_OPTIONS.index(defaults["goal"]), format_func=lambda x: GOAL_LABELS[x])
    with c7:
        age  = st.slider("Age", min_value=22, max_value=45, value=int(defaults["age"]))

    st.markdown("<br>", unsafe_allow_html=True)
    btn_col, _ = st.columns([2, 3])
    with btn_col:
        run = st.button("Generate My Health Report", use_container_width=True)

    if run:
        d_in = dict(salary=int(salary), cc=int(cc), sip=int(sip), inv=int(inv),
                    sav=int(sav), exp=int(exp), dep=int(dep), ins=str(ins),
                    goal=str(goal), age=int(age))
        with st.spinner("Analysing your complete financial picture..."):
            time.sleep(0.8)
            st.session_state.result = analyse(d_in)
            st.session_state.inputs = d_in
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:12px;font-weight:700;color:{STEEL};text-transform:uppercase;letter-spacing:0.07em;margin-bottom:12px'>Or explore a sample profile</div>", unsafe_allow_html=True)
    pc1, pc2, pc3, pc4 = st.columns(4)
    for col, name, desc, color, tag in [
        (pc1, "Priya, 27", "SIP running alongside Rs 62k credit card debt. No emergency fund.", CORAL, "Anxious Achiever"),
        (pc2, "Arjun, 31", "Good investments but concentrated portfolio and inadequate insurance.", INDIGO, "Confident Optimiser"),
        (pc3, "Meera, 24", "Invests before building any financial foundation. Priority inverted.", GOLD, "Overwhelmed Beginner"),
        (pc4, "Raj, 33",   "Zero debt and good corpus but entirely on employer insurance.", TEAL, "Good But Exposed"),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:{WHITE};border:1px solid {BORDER};border-radius:11px;padding:15px;
                 border-top:3px solid {color};box-shadow:0 1px 4px rgba(0,0,0,0.04)">
              <div style="font-size:13px;font-weight:600;color:{NAVY};margin-bottom:5px">{name}</div>
              <div style="font-size:12px;color:{STEEL};line-height:1.55;margin-bottom:8px">{desc}</div>
              <span style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;
                   padding:2px 8px;border-radius:4px;background:{color}1A;color:{color}">{tag}</span>
            </div>
            """, unsafe_allow_html=True)

# ── REPORT ────────────────────────────────────────────────────────
else:
    r  = st.session_state.result
    d  = st.session_state.inputs
    sc = TEAL2 if r["total"] >= 70 else (GOLD if r["total"] >= 50 else CORAL)
    cat_icons = {"Thriving": "✅", "On Track": "🟢", "Attention Needed": "🟡", "Urgent Action Required": "🔴"}

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{NAVY},{NAVY2});border-radius:16px;
         padding:30px 34px;margin-bottom:20px;box-shadow:0 6px 28px rgba(12,30,58,0.2)">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:24px;flex-wrap:wrap">
        <div style="flex:1;min-width:240px">
          <div style="font-family:'DM Serif Display',serif;font-size:27px;color:white;font-weight:400;margin-bottom:6px">Financial Health Report</div>
          <div style="font-size:12px;color:rgba(255,255,255,0.36);margin-bottom:14px;display:flex;gap:12px;flex-wrap:wrap">
            <span>Age {d['age']}</span><span style="opacity:0.3">|</span><span>{r['profile']}</span><span style="opacity:0.3">|</span><span>April 2026</span>
          </div>
          <div style="font-size:13px;color:rgba(255,255,255,0.68);line-height:1.75;max-width:500px">{r['summary']}</div>
        </div>
        <div style="text-align:center;flex-shrink:0">
          <div style="font-family:'DM Serif Display',serif;font-size:72px;color:{sc};line-height:1">{r['total']}</div>
          <div style="font-size:13px;color:rgba(255,255,255,0.32);margin-bottom:8px">out of 100</div>
          <div style="display:inline-block;font-size:12px;font-weight:600;padding:5px 14px;border-radius:20px;background:rgba(255,255,255,0.1);color:white">
            {cat_icons.get(r['category'],'')} {r['category']}
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    rc, _ = st.columns([1, 6])
    with rc:
        if st.button("← New Analysis"):
            st.session_state.result = None
            st.session_state.inputs = None
            st.rerun()

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    dat = r["data"]
    with m1:
        st.metric("Credit Card Interest Cost",
                  f"Rs {dat['cc_interest']:,}/mo" if dat["cc_interest"] > 0 else "Rs 0",
                  delta="at 42% annual rate" if dat["cc_interest"] > 0 else "No revolving debt",
                  delta_color="inverse" if dat["cc_interest"] > 0 else "normal")
    with m2:
        ok = dat["emerg_months"] >= 3
        st.metric("Emergency Fund Coverage", f"{dat['emerg_months']} months",
                  delta="Target met" if ok else f"Need Rs {dat['emerg_gap']:,} more",
                  delta_color="normal" if ok else "inverse")
    with m3:
        ok = dat["sav_rate"] >= 20
        st.metric("Net Savings Rate", f"{dat['sav_rate']}%",
                  delta="On target" if ok else "Target: 20 to 25%",
                  delta_color="normal" if ok else "inverse")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📊   Health Score", "⚡   Priority Action", "🚨   Alerts", "🗓️   Roadmap"])

    with tab1:
        st.markdown(f"<h3 style='font-family:\"DM Serif Display\",serif;font-size:21px;color:{NAVY};font-weight:400;margin-bottom:16px'>Your 5-Pillar Financial Health Score</h3>", unsafe_allow_html=True)
        for p in r["pillars"]:
            pc = S_COL[p["status"]]; pct = int(p["score"]/20*100)
            l, ri = st.columns([5, 1])
            with l:
                st.markdown(f"""
                <div style="background:{WHITE};border:1px solid {BORDER};border-radius:12px;padding:14px 18px;border-left:4px solid {pc};box-shadow:0 1px 4px rgba(0,0,0,0.04)">
                  <div style="display:flex;align-items:center;gap:10px;margin-bottom:9px">
                    <span style="font-size:16px">{p['icon']}</span>
                    <span style="font-size:13px;font-weight:600;color:{NAVY}">{p['name']}</span>
                    <span style="margin-left:auto;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;padding:2px 8px;border-radius:4px;background:{S_BG[p['status']]};color:{pc}">{S_LBL[p['status']]}</span>
                  </div>
                  <div style="height:7px;background:{MIST};border-radius:4px;margin-bottom:8px;overflow:hidden">
                    <div style="height:100%;width:{pct}%;background:{pc};border-radius:4px"></div>
                  </div>
                  <div style="font-size:12px;color:{SLATE};line-height:1.6">{p['detail']}</div>
                </div>
                """, unsafe_allow_html=True)
            with ri:
                st.markdown(f"""
                <div style="background:{WHITE};border:1px solid {BORDER};border-radius:12px;padding:10px 8px;text-align:center;height:100%;min-height:88px;display:flex;flex-direction:column;align-items:center;justify-content:center">
                  <div style="font-family:'DM Serif Display',serif;font-size:28px;color:{pc};line-height:1">{p['score']}</div>
                  <div style="font-size:12px;color:{STEEL}">/20</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<div style='height:7px'></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:{WHITE};border:1px solid {BORDER};border-radius:12px;padding:17px 21px;margin-top:4px">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:9px">
            <span style="font-size:13px;font-weight:600;color:{NAVY}">Overall Financial Health Score</span>
            <span style="font-family:'DM Serif Display',serif;font-size:20px;color:{sc}">{r['total']}/100</span>
          </div>
          <div style="height:10px;background:{MIST};border-radius:5px;overflow:hidden;margin-bottom:8px">
            <div style="height:100%;width:{r['total']}%;background:linear-gradient(90deg,{CORAL},{GOLD} 45%,{TEAL2});border-radius:5px"></div>
          </div>
          <div style="display:flex;justify-content:space-between">
            <span style="font-size:11px;color:{STEEL}">0 | Urgent</span>
            <span style="font-size:11px;color:{STEEL}">35 | Attention</span>
            <span style="font-size:11px;color:{STEEL}">55 | On Track</span>
            <span style="font-size:11px;color:{STEEL}">75 | Thriving | 100</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        a = r["action"]
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{NAVY},{NAVY2});border-radius:14px;padding:27px 29px;margin-bottom:16px;box-shadow:0 6px 24px rgba(12,30,58,0.18)">
          <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.12em;color:{TEAL2};margin-bottom:10px;display:flex;align-items:center;gap:7px">
            <span style="width:6px;height:6px;background:{TEAL2};border-radius:50%;display:inline-block"></span> PRIORITY ACTION THIS MONTH
          </div>
          <div style="font-family:'DM Serif Display',serif;font-size:22px;color:white;margin-bottom:11px;font-weight:400;line-height:1.3">{a['title']}</div>
          <div style="font-size:13px;color:rgba(255,255,255,0.70);line-height:1.75;margin-bottom:20px">{a['desc']}</div>
          <div style="display:flex;gap:12px;flex-wrap:wrap">
            <div style="background:rgba(13,139,117,0.18);border:1px solid rgba(13,139,117,0.3);border-radius:10px;padding:11px 17px">
              <div style="font-family:'DM Serif Display',serif;font-size:19px;color:{MINT};margin-bottom:2px">{a['saving']}</div>
              <div style="font-size:11px;color:rgba(255,255,255,0.4)">potential impact</div>
            </div>
            <div style="background:rgba(13,139,117,0.18);border:1px solid rgba(13,139,117,0.3);border-radius:10px;padding:11px 17px">
              <div style="font-family:'DM Serif Display',serif;font-size:19px;color:{MINT};margin-bottom:2px">{a['timeframe']}</div>
              <div style="font-size:11px;color:rgba(255,255,255,0.4)">to milestone</div>
            </div>
          </div>
        </div>
        <div style="background:{WHITE};border:1px solid {BORDER};border-radius:12px;padding:17px 21px">
          <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:{STEEL};margin-bottom:8px">Why this action specifically?</div>
          <div style="font-size:13px;color:{TEXT};line-height:1.75">ARTHA ranks every possible action by financial leverage. This action produces the greatest improvement in your overall score given your specific numbers across debt, savings, insurance, and goals. Once completed, ARTHA surfaces the next highest-leverage action.</div>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        cf, cc_col = st.columns(2)
        with cf:
            body = (f"""
            <div style="background:{WHITE};padding:16px">
              <p style="font-size:13px;color:{TEXT};line-height:1.7;margin-bottom:11px">{r['fresh']['signal']}</p>
              <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:{STEEL};margin-bottom:4px">What to do</div>
              <div style="font-size:13px;color:{NAVY};font-weight:500;line-height:1.6">{r['fresh']['action']}</div>
            </div>""" if r["fresh"]["exists"] else
            f'<div style="background:{WHITE};padding:16px"><p style="font-size:13px;color:{STEEL};line-height:1.7;margin:0">No critical stale signals detected. Your financial picture appears current.</p></div>')
            hd_col = CORAL if r["fresh"]["exists"] else STEEL
            hd_txt = "🚨 Freshness Alert" if r["fresh"]["exists"] else "Freshness Alert"
            st.markdown(f'<div style="border-radius:12px;overflow:hidden;border:1px solid {BORDER}"><div style="background:{hd_col};padding:10px 16px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:white">{hd_txt}</div>{body}</div>', unsafe_allow_html=True)
        with cc_col:
            st.markdown(f"""
            <div style="border-radius:12px;overflow:hidden;border:1px solid {BORDER}">
              <div style="background:{TEAL};padding:10px 16px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:white">📡 Competitive Signal</div>
              <div style="background:{WHITE};padding:16px">
                <p style="font-size:13px;color:{TEXT};line-height:1.7;margin-bottom:9px">{r['comp']['observation']}</p>
                <p style="font-size:13px;color:{TEXT};line-height:1.6;margin-bottom:11px">Peers typically have: <strong style="color:{NAVY}">{r['comp']['attribute']}</strong></p>
                <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:{STEEL};margin-bottom:4px">Recommended next step</div>
                <div style="font-size:13px;color:{NAVY};font-weight:500;line-height:1.6">{r['comp']['action']}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    with tab4:
        st.markdown(f"<h3 style='font-family:\"DM Serif Display\",serif;font-size:21px;color:{NAVY};font-weight:400;margin-bottom:16px'>Your 6-Month Clarity Roadmap</h3>", unsafe_allow_html=True)
        for i, (label, event, color) in enumerate(r["roadmap"]):
            is_last = (i == len(r["roadmap"]) - 1)
            st.markdown(f"""
            <div style="display:flex;gap:14px;padding:13px 0;{'border-bottom:none' if is_last else f'border-bottom:1px solid {BORDER}'}">
              <div style="width:105px;flex-shrink:0;padding-top:2px">
                <span style="font-size:11px;font-weight:700;color:{color};background:{color}1A;padding:3px 9px;border-radius:5px">{label}</span>
              </div>
              <div style="font-size:13px;color:{TEXT};line-height:1.7">{event}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:{NAVY};border-radius:13px;padding:19px 25px;text-align:center">
      <div style="font-family:'DM Serif Display',serif;font-size:17px;color:white;margin-bottom:5px;font-weight:400">ARTHA: Financial Clarity Engine</div>
      <div style="font-size:12px;color:rgba(255,255,255,0.3)">Portfolio Project by Aditya Bayar | April 2026 | MVP v1.0</div>
    </div>
    """, unsafe_allow_html=True)
