"""EC-AI Stage 1-F.6.3C.2 — institutional public viewer.

Standalone fictional demonstration. No operational DB access, imports or writes.
Uses the Stage 1-C design vocabulary; it is NOT the operator application's
source-of-truth, review authority, or governance engine.
"""
from __future__ import annotations

from html import escape
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

NAV = ("Executive Briefing", "Review", "Relationships", "Decisions", "Execution", "Portfolio")
DATA = [
    dict(name="Northstar Mobility", sector="Transport", attention=82, urgency=87, action="Lending Wallet Expansion", driver="Wallet Opportunity", owner="Coverage Director", risk="Medium", capex=4000, debt=25, bank=60, event="CAPEX financing review", evidence="Confirm CAPEX, debt mix, maturities and lender participation"),
    dict(name="Harbourline Energy", sector="Energy", attention=72, urgency=68, action="Treasury Deep Dive", driver="Wallet Opportunity", owner="Treasury Team", risk="Medium", capex=2300, debt=22, bank=45, event="Cash management re-tender", evidence="Validate operating cash, regional accounts and liquidity structure"),
    dict(name="Summit Infrastructure", sector="Infrastructure", attention=64, urgency=59, action="Executive Engagement", driver="Strategic Importance", owner="Coverage Director", risk="Low", capex=1500, debt=30, bank=55, event="Fictional investment committee milestone", evidence="Validate project schedule, sponsor and financing scope"),
    dict(name="Meridian Logistics", sector="Logistics", attention=55, urgency=75, action="Cross-Border Expansion", driver="Growth Signals", owner="Regional Coverage", risk="Medium", capex=920, debt=20, bank=55, event="Regional expansion planning", evidence="Confirm jurisdiction, funding currencies and client demand"),
    dict(name="Atlas Renewables", sector="Renewables", attention=43, urgency=62, action="Credit Review", driver="Risk Signals", owner="Credit / Risk", risk="High", capex=1400, debt=35, bank=40, event="Covenant review window", evidence="Validate leverage, covenant headroom and proposed mitigants"),
    dict(name="Bluecrest Digital", sector="Technology", attention=69, urgency=33, action="Portfolio Monitoring", driver="Growth Signals", owner="Relationship Manager", risk="Low", capex=500, debt=15, bank=55, event="Annual strategy refresh", evidence="Verify financial outlook and relationship growth assumptions"),
    dict(name="Caldera Industrials", sector="Industrials", attention=59, urgency=42, action="Portfolio Monitoring", driver="Relationship Health", owner="Relationship Manager", risk="Medium", capex=780, debt=25, bank=50, event="Annual results cycle", evidence="Refresh turnover, profitability and credit suitability"),
    dict(name="Westbridge Consumer", sector="Consumer", attention=51, urgency=36, action="Deposit Retention", driver="Relationship Health", owner="Treasury Team", risk="Medium", capex=320, debt=20, bank=55, event="Liquidity review", evidence="Confirm operating balances and account behavior"),
    dict(name="Orion Shipping", sector="Shipping", attention=41, urgency=46, action="Coverage Enhancement", driver="Coverage Strength", owner="Relationship Manager", risk="Medium", capex=650, debt=28, bank=48, event="Relationship touchpoint", evidence="Assess coverage frequency and wallet opportunities"),
    dict(name="Sterling Healthcare", sector="Healthcare", attention=37, urgency=30, action="Portfolio Monitoring", driver="Portfolio Profile", owner="Coverage", risk="Low", capex=280, debt=15, bank=40, event="Annual results preparation", evidence="Refresh financial statements and pipeline assumptions"),
]
DF = pd.DataFrame(DATA)

CSS = r"""
<style>
:root{--navy:#071B3A;--navy2:#0B2C55;--blue:#365F9C;--muted:#526173;--line:#D8DEE6;--light:#F5F7FA;--gold:#BD8D4A}
html,body,[class*="css"]{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}
.stApp{background:#F5F7FA;color:var(--navy)}
header[data-testid="stHeader"]{background:transparent;height:0}
#MainMenu,footer{visibility:hidden}
.block-container{max-width:1440px!important;padding:1.3rem 2.0rem 2rem!important}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#071B3A,#0B2C55)!important;border-right:1px solid #294663}
section[data-testid="stSidebar"] [data-testid="stSidebarContent"]{padding-top:1rem}
section[data-testid="stSidebar"] label p,section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p{color:#E9F0F8}
section[data-testid="stSidebar"] [data-baseweb="select"]>div{background:white}
section[data-testid="stSidebar"] [data-baseweb="select"] span{color:#071B3A}
section[data-testid="stSidebar"] div[role="radiogroup"]{gap:3px}
section[data-testid="stSidebar"] div[role="radiogroup"]>label{min-height:39px;padding:5px 10px;border-radius:9px}
section[data-testid="stSidebar"] div[role="radiogroup"]>label:has(input:checked){background:#FFF}
section[data-testid="stSidebar"] div[role="radiogroup"]>label:has(input:checked) p{color:#071B3A!important;font-weight:800}
.ec-brand{padding:12px 4px 17px;border-bottom:1px solid #ffffff2b;margin-bottom:12px}
.ec-brand-name{font-size:27px;font-weight:900;color:white;letter-spacing:-.04em}
.ec-brand-sub{font-size:12px;color:#E2ECF6;font-weight:700;margin-top:4px}
.ec-brand-tag{font-size:10px;color:#AFC4DD;letter-spacing:.08em;font-weight:850;margin-top:12px}
.ec-rail-note{border:1px solid #ffffff25;background:#ffffff0e;border-radius:10px;color:#DDE8F6;padding:11px 13px;font-size:11px;line-height:1.55;margin:12px 0}
/* Unclipped single-surface, fully rounded hero. No negative margins, clipping or fixed height. */
.ec-hero{display:block;box-sizing:border-box;width:100%;background:linear-gradient(115deg,#071B3A 0%,#153C66 100%);border-radius:17px;overflow:hidden;padding:20px 26px 21px;margin:0 0 18px;border:1px solid #18375F;box-shadow:0 4px 12px #071B3A13}
.ec-hero-kicker{color:#BBD5F6;font-size:10px;font-weight:900;letter-spacing:.09em;text-transform:uppercase;margin-bottom:8px}
.ec-hero-title{font-size:26px;font-weight:900;color:#FFFFFF;letter-spacing:-.035em;line-height:1.19;margin:0 0 9px}
.ec-hero-sub{color:#E9F1FA;font-size:13px;line-height:1.45}
.ec-hero-pill{display:inline-block;border:1px solid #8EAACB55;color:#DCEAF8;background:#ffffff12;padding:5px 10px;border-radius:100px;margin-top:10px;font-size:9px;font-weight:800;letter-spacing:.03em}
.ec-topbar{display:flex;justify-content:space-between;align-items:start;gap:15px;border-bottom:1px solid #D8DEE6;padding:0 0 17px;margin:0 0 19px}
.ec-eyebrow{font-size:10px;color:#365F9C;font-weight:900;letter-spacing:.10em;text-transform:uppercase;margin-bottom:5px}
.ec-title{font-size:29px;font-weight:900;color:#071B3A;line-height:1.1;letter-spacing:-.03em}
.ec-subtitle{font-size:13px;color:#526173;margin-top:7px;line-height:1.48;max-width:780px}
.ec-context{display:flex;gap:9px}.ec-context-chip{background:white;border:1px solid #D8DEE6;border-radius:9px;padding:9px 12px;min-width:100px}.ec-chip-label{color:#7B8794;font-size:9px;font-weight:900;text-transform:uppercase}.ec-chip-value{font-size:12px;font-weight:800;color:#071B3A;margin-top:3px}
.ec-card{background:white;border:1px solid #D8DEE6;border-radius:13px;padding:15px 17px;box-shadow:0 2px 7px #071B3A08;min-height:101px}
.ec-card-label{font-size:10px;color:#526173;font-weight:900;text-transform:uppercase;letter-spacing:.04em}.ec-card-value{font-size:27px;font-weight:920;color:#071B3A;margin:6px 0}.ec-card-sub{font-size:11px;color:#718091}
.ec-panel{background:#fff;border:1px solid #D8DEE6;border-radius:13px;padding:17px 19px;box-shadow:0 2px 8px #071B3A08;margin:8px 0 12px}
.ec-panel-kicker{font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:#365F9C;font-weight:900;margin-bottom:7px}.ec-panel-title{font-size:17px;color:#071B3A;font-weight:900;line-height:1.25;margin-bottom:7px}.ec-panel-body{font-size:12.5px;color:#526173;line-height:1.55}
.ec-note{background:#E7F0FB;border-left:3px solid #365F9C;color:#173D6C;padding:13px 15px;border-radius:7px;font-size:12.5px;line-height:1.5;margin:7px 0 13px}
.ec-amber{background:#FFF3D3;border-left-color:#D79D37;color:#51391D}.ec-label{font-weight:900;font-size:12px;color:#071B3A;margin:12px 0 8px}
.ec-section{font-size:17px;color:#071B3A;font-weight:900;margin:15px 0 9px}
.ec-divider{height:1px;background:#D8DEE6;margin:15px 0}
.ec-disclaimer{color:#738093;font-size:10px;padding:13px 0 7px;border-top:1px solid #D8DEE6;margin-top:16px}
[data-testid="stDataFrame"]{border:1px solid #D8DEE6;border-radius:10px;overflow:hidden}
[data-testid="stMetric"]{background:white;border:1px solid #D8DEE6;border-radius:12px;padding:12px}
div.stButton>button[kind="primary"]{background:#071B3A;border-color:#071B3A;border-radius:8px}
@media(max-width:1050px){.block-container{padding:.9rem 1.1rem 2rem!important}.ec-topbar{display:block}.ec-context{margin-top:11px}.ec-title{font-size:25px}.ec-hero-title{font-size:23px}}
</style>
"""


def safe(value):
    return escape(str(value), quote=True)


def html(content):
    st.markdown(content, unsafe_allow_html=True)


def card(label, value, sub=""):
    html(f'<div class="ec-card"><div class="ec-card-label">{safe(label)}</div><div class="ec-card-value">{safe(value)}</div><div class="ec-card-sub">{safe(sub)}</div></div>')


def panel(kicker, title, body):
    html(f'<div class="ec-panel"><div class="ec-panel-kicker">{safe(kicker)}</div><div class="ec-panel-title">{safe(title)}</div><div class="ec-panel-body">{safe(body)}</div></div>')


def note(message, amber=False):
    html(f'<div class="ec-note{" ec-amber" if amber else ""}">{safe(message)}</div>')


def heading(text):
    html(f'<div class="ec-section">{safe(text)}</div>')


def matrix(df, height=340, show_labels=False):
    fig=go.Figure()
    fig.add_shape(type='rect',x0=60,x1=100,y0=50,y1=100,fillcolor='rgba(187,141,74,.11)',line_width=0,layer='below')
    fig.add_vline(x=60,line_dash='dash',line_color='#9AAFC5',line_width=1.2)
    fig.add_hline(y=50,line_dash='dash',line_color='#9AAFC5',line_width=1.2)
    for _,r in df.iterrows():
        lead=r['name']=='Northstar Mobility'
        highlight=r['attention']>=60 and r['urgency']>=50
        fig.add_trace(go.Scatter(x=[r['attention']],y=[r['urgency']],mode='markers+text' if lead or show_labels else 'markers',
            text=[r['name']] if lead or show_labels else None,textposition='top center',
            textfont=dict(size=10,color='#071B3A'),name=r['name'],
            marker=dict(size=27 if lead else 15 if highlight else 12,color='#C29350' if highlight else '#426C9F',line=dict(color='white',width=1)),
            customdata=[[r['action']]],hovertemplate='%{fullData.name}<br>Attention: %{x}<br>Urgency: %{y}<br>%{customdata[0]}<extra></extra>'))
    fig.add_annotation(x=88,y=95,text='ACT NOW',showarrow=False,font=dict(size=10,color='#976A2D'))
    fig.update_layout(height=height,showlegend=False,paper_bgcolor='white',plot_bgcolor='white',margin=dict(l=4,r=6,t=12,b=10),
        xaxis=dict(title=dict(text='Management attention',font=dict(size=11,color='#637C9A')),range=[20,100],gridcolor='#E7ECF2',zeroline=False,tickfont=dict(size=10,color='#637C9A')),
        yaxis=dict(title=dict(text='Urgency',font=dict(size=11,color='#637C9A')),range=[0,100],gridcolor='#E7ECF2',zeroline=False,tickfont=dict(size=10,color='#637C9A')))
    st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})


def topbar(page, selected):
    subtitles={
      'Executive Briefing':'Portfolio intelligence distilled into a clear management agenda: what requires attention now, what changed and what to review next.',
      'Review':'Work through material relationship issues, management questions and recommendations requiring judgment.',
      'Relationships':'Relationship 360 — opportunity, financing evidence, risk and coverage priorities.',
      'Decisions':'Explore executive management judgments and their implications. Public viewer is read-only.',
      'Execution':'Track proposed implementation, accountability and outcomes without creating operational records.',
      'Portfolio':'Deep portfolio evidence supporting the executive management agenda.'}
    html(f'<div class="ec-topbar"><div><div class="ec-eyebrow">EC-AI / INSTITUTIONAL RELATIONSHIP INTELLIGENCE</div><div class="ec-title">{safe(page)}</div><div class="ec-subtitle">{safe(subtitles[page])}</div></div><div class="ec-context"><div class="ec-context-chip"><div class="ec-chip-label">REVIEW CYCLE</div><div class="ec-chip-value">Illustrative</div></div><div class="ec-context-chip"><div class="ec-chip-label">CONTEXT</div><div class="ec-chip-value">{safe(selected)}</div></div></div></div>')


def metrics(items):
    cols=st.columns(len(items),gap='small')
    for c,(label,value,subtitle) in zip(cols,items):
        with c: card(label,value,subtitle)


def source_table(selected=None):
    rows=[]
    for i, r in DF.sort_values(['attention','urgency'],ascending=False).reset_index(drop=True).iterrows():
        level='Management Attention' if r.attention>=80 else 'Review' if r.attention>=50 else 'Monitor'
        rows.append(dict(Priority=i+1,Relationship=r['name'],Score=f'{r.attention:.1f}',Rating=level,Driver=r.driver,Recommendation=r.action))
    return pd.DataFrame(rows)


def briefing(selected):
    metrics([('Relationships','10','Fictional relationship universe'),('Average score','57.3','Illustrative attention index'),('Management attention','1','Score ≥ 80'),('High urgency','5','Urgency ≥ 50'),('Execution exceptions','0','No operational actions')])
    heading('Attention × Urgency · Management View')
    left,right=st.columns([1.8,1],gap='medium')
    with left:
        html('<div class="ec-label">Which relationships deserve management attention first?</div>')
        matrix(DF,height=355)
    with right:
        panel('Executive interpretation','Northstar Mobility requires attention','The largest fictional opportunity coincides with an illustrative near-term financing milestone. A scoped wallet review is warranted before any management commitment.')
        panel('This cycle’s agenda','From insight to management action','Validate Northstar financing needs, review hypothetical deposit retention exposure, assess credit suitability and coordinate regional coverage.')
    note('Management question: Should leadership authorize a scoped investigation—not a lending commitment?')


def review(selected):
    metrics([('Review items','10','Illustrative queue'),('Management attention','1','Score ≥ 80'),('Review band','6','Score 50–79'),('Action types','8','Synthetic taxonomy')])
    heading('Relationship Review Queue')
    st.dataframe(source_table(),use_container_width=True,hide_index=True,height=300)
    r=DF.set_index('name').loc[selected]
    note(f"Management Review Item · {selected} | Rating {r.attention} · {r.driver} | Recommended action: {r.action} | Expected outcome: evidence-backed management prioritization.",amber=True)
    heading('Why this relationship appears in the queue')
    cols=st.columns(4)
    for c,(lab,val,sub) in zip(cols,[('Attention',r.attention,'Management prioritization'),('Urgency',r.urgency,'Timing sensitivity'),('Primary driver',r.driver,'Illustrative logic'),('Risk view',r.risk,'Unverified fixture')]):
        with c: card(lab,val,sub)
    c1,c2=st.columns(2)
    with c1:
        if st.button('Open Relationship Intelligence',use_container_width=True):
            st.session_state.page='Relationships';st.rerun()
    with c2:
        if st.button('Prepare Illustrative Decision',use_container_width=True):
            st.session_state.page='Decisions';st.rerun()


def relationships(selected):
    r=DF.set_index('name').loc[selected]
    metrics([('Relationship',selected,'Fictional company'),('Sector',r.sector,'Illustrative coverage'),('Attention',r.attention,'Management score'),('Urgency',r.urgency,'Illustrative index')])
    heading('Relationship Intelligence · 360 View')
    c1,c2=st.columns(2,gap='medium')
    with c1:
        panel('Relationship assessment','Opportunity & coverage',f'{r.action}. Relationship manager: {r.owner}. The opportunity requires client validation, internal coverage assessment and a documented management judgment.')
        panel('Financial evidence','Assumption-driven illustrative wallet',f'Forecast CAPEX USD {r.capex:,.0f}m × {r.debt}% debt financing × {r.bank}% bank financing = USD {r.capex*r.debt*r.bank/10000:,.0f}m illustrative notional. Not revenue, market share or a credit commitment.')
    with c2:
        panel('Event intelligence','What changed / why now',f'{r.event}. This is an invented event and must not be treated as an actual client milestone.')
        panel('Evidence & risk','Before management action',f'{r.evidence}. Risk designation {r.risk} is fictional and not a credit risk rating.')
    note('Publication gate: No wallet assessment is published; all values are ASSUMPTIONS / fictional demonstrations.',amber=True)
    if st.button('Review this relationship',use_container_width=True):
        st.session_state.page='Review';st.rerun()


def decisions(selected):
    r=DF.set_index('name').loc[selected]
    heading('Executive Decision Preparation')
    note('PUBLIC VIEWER · This is a simulation. No decision, ReviewItem, ExecutionAction or AuditEvent is created.')
    panel('Decision required',f'Authorize diligence, not lending — {selected}',f'Assess the {r.action.lower()} proposal and validate {r.evidence.lower()}. Executive decision authority remains with the institution.')
    choice=st.radio('Illustrative management disposition',['Approve investigation','Modify scope','Defer pending evidence'],horizontal=True,key='demo_choice')
    texts={
      'Approve investigation':('APPROVE SCOPED INVESTIGATION',f'Request coverage, treasury and credit assessment for {selected}. No facility approval or client mandate.'),
      'Modify scope':('MODIFY THE SCOPE',f'Limit the {selected} review to essential evidence and a defined coverage question.'),
      'Defer pending evidence':('DEFER PENDING EVIDENCE',f'Hold the recommendation until the required client and financial evidence has been validated.')}
    title,copy=texts[choice]
    note(f'{title} — {copy}')
    metrics([('Decision authority','Executive','Illustrative only'),('Evidence quality','Assumptions','Must be validated'),('Write operations','None','No DB connection')])
    st.caption('This selection is local to this viewer session and has no operational effect.')


def execution(selected):
    heading('Execution Exceptions')
    note('No operational exceptions are available. The execution register below is an illustrative proposal only.')
    heading('Action Register')
    decision=st.session_state.get('demo_choice','Approve investigation')
    actions=[
      ['Coverage',f'Validate financing requirements and client timing for {selected}','Next review','Proposed'],
      ['Treasury','Assess deposits, cash and liquidity relevance','Next review','Proposed'],
      ['Credit / Risk','Review preliminary credit suitability and financial evidence','Following review','Proposed'],
      ['Executive Sponsor',f'Consider {decision.lower()} and define follow-up','Following review','Proposed']]
    st.dataframe(pd.DataFrame(actions,columns=['Accountable function','Illustrative next step','Review point','State']),use_container_width=True,hide_index=True,height=190)
    panel('Expected outcome','Decision accountability, not dashboard activity','At the next fictional executive review: identify which assumptions were validated, which relationship opportunity remains credible, and what management should decide next.')
    metrics([('Assigned','0','Illustrative records only'),('In progress','0','No live actions'),('Completed','0','No closure claims'),('Audit writes','0','No DB connection')])


def portfolio(selected):
    metrics([('Universe','10','Fictional relationships'),('High attention','1','Attention ≥ 80'),('Urgency ≥ 50','5','Illustrative events'),('Priorities','4','Editorial selection')])
    heading('Portfolio Intelligence · Attention × Urgency')
    matrix(DF,height=335)
    heading('Relationship Evidence Register')
    details=DF[['name','sector','attention','urgency','driver','action','risk']].rename(columns={'name':'Relationship','sector':'Sector','attention':'Attention','urgency':'Urgency','driver':'Driver','action':'Management action','risk':'Risk label'})
    st.dataframe(details,use_container_width=True,hide_index=True,height=320)
    note('All scores, balance-sheet proxies, events and risk labels are illustrative fixtures. No live financial intelligence or published wallet assessment is represented.')


def run():
    st.markdown(CSS,unsafe_allow_html=True)
    if 'page' not in st.session_state:st.session_state.page=NAV[0]
    if 'selected' not in st.session_state:st.session_state.selected='Northstar Mobility'
    with st.sidebar:
        html('<div class="ec-brand"><div class="ec-brand-name">EC-AI</div><div class="ec-brand-sub">Executive Review Workspace</div><div class="ec-brand-tag">INSTITUTIONAL VIEWER · SYNTHETIC</div></div>')
        st.radio('WORKSPACE',NAV,key='page')
        st.selectbox('Relationship context',list(DF['name']),key='selected')
        html('<div class="ec-rail-note"><strong>PUBLIC VIEWER</strong><br>10 fictional relationships<br>Read-only · No credentials<br>No database connection or writes</div>')
    page=st.session_state.page
    selected=st.session_state.selected
    html('<div class="ec-hero"><div class="ec-hero-kicker">EC-AI / INSTITUTIONAL RELATIONSHIP INTELLIGENCE</div><div class="ec-hero-title">Portfolio intelligence. Clear executive decisions.</div><div class="ec-hero-sub">Identify portfolio priorities, understand the evidence, make the decision and track accountability — in one executive workflow.</div><div class="ec-hero-pill">FICTIONAL DEMO · 10 SYNTHETIC RELATIONSHIPS · READ-ONLY</div></div>')
    topbar(page,selected)
    {'Executive Briefing':briefing,'Review':review,'Relationships':relationships,'Decisions':decisions,'Execution':execution,'Portfolio':portfolio}[page](selected)
    html('<div class="ec-disclaimer">PUBLIC VIEWER · All companies, financial values, attention scores, events, actors and outcomes are fictional. No operational database is accessed, updated or published. Stage 1-C design vocabulary is reused for demonstration; this is not the institutional operator application.</div>')
