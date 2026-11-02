"""EC-AI F.6.3C.1 — standalone synthetic, DB-disconnected six-workspace viewer.
All example relationships, amounts, actors and outcomes are fictional.
No database, authentication, operational writes or real corporate records.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

NAV = ('Executive Briefing','Review','Relationships','Decisions','Execution','Portfolio')
DATA = [
    {'Relationship':'Northstar Mobility','Sector':'Transport','Attention':82,'Urgency':87,'Score':82,'Action':'Lending wallet expansion','Owner':'Coverage Director','Status':'Proposed'},
    {'Relationship':'Harbourline Energy','Sector':'Energy','Attention':72,'Urgency':68,'Score':72,'Action':'Treasury deep dive','Owner':'Treasury','Status':'Proposed'},
    {'Relationship':'Summit Infrastructure','Sector':'Infrastructure','Attention':64,'Urgency':59,'Score':64,'Action':'Executive engagement','Owner':'Coverage','Status':'Proposed'},
    {'Relationship':'Meridian Logistics','Sector':'Logistics','Attention':55,'Urgency':75,'Score':55,'Action':'Cross-border expansion','Owner':'Regional Coverage','Status':'Proposed'},
    {'Relationship':'Atlas Renewables','Sector':'Renewables','Attention':43,'Urgency':62,'Score':43,'Action':'Credit review','Owner':'Credit','Status':'Proposed'},
    {'Relationship':'Bluecrest Digital','Sector':'Technology','Attention':69,'Urgency':33,'Score':69,'Action':'Portfolio monitoring','Owner':'Coverage','Status':'Proposed'},
    {'Relationship':'Caldera Industrials','Sector':'Industrials','Attention':59,'Urgency':42,'Score':59,'Action':'Portfolio monitoring','Owner':'Coverage','Status':'Proposed'},
    {'Relationship':'Westbridge Consumer','Sector':'Consumer','Attention':51,'Urgency':36,'Score':51,'Action':'Deposit retention','Owner':'Treasury','Status':'Proposed'},
    {'Relationship':'Orion Shipping','Sector':'Shipping','Attention':41,'Urgency':46,'Score':41,'Action':'Coverage enhancement','Owner':'Coverage','Status':'Proposed'},
    {'Relationship':'Sterling Healthcare','Sector':'Healthcare','Attention':37,'Urgency':30,'Score':37,'Action':'Portfolio monitoring','Owner':'Coverage','Status':'Proposed'},
]

def scatter(rows):
    fig=go.Figure()
    fig.add_shape(type='rect', x0=60, x1=100, y0=50, y1=100, fillcolor='rgba(187,144,86,.12)',line_width=0,layer='below')
    fig.add_vline(x=60,line_dash='dash',line_color='#9eb0c4')
    fig.add_hline(y=50,line_dash='dash',line_color='#9eb0c4')
    for r in rows:
        lead = r['Relationship']=='Northstar Mobility'
        fig.add_trace(go.Scatter(x=[r['Attention']],y=[r['Urgency']],mode='markers+text' if lead else 'markers',text=[r['Relationship']] if lead else None,textposition='top center',name=r['Relationship'],marker={'size':24 if lead else 15,'color':'#BB8D52' if r['Attention']>=60 and r['Urgency']>=50 else '#406FA4'},hovertemplate=f"{r['Relationship']}<br>Attention %{{x}} · Urgency %{{y}}<extra></extra>"))
    fig.update_layout(xaxis={'title':'Management attention','range':[20,100]},yaxis={'title':'Urgency','range':[0,100]},height=370,margin=dict(l=15,r=15,t=15,b=15),showlegend=False,plot_bgcolor='white',paper_bgcolor='white')
    return fig

def render():
    st.markdown('''<style>.block-container{padding-top:1.1rem;max-width:1520px} [data-testid="stSidebar"]{background:#10294B} [data-testid="stSidebar"] *{color:white!important}.ec-banner{background:linear-gradient(115deg,#0b1d3d,#1c426c);color:white;border-radius:14px;padding:22px 28px;margin-bottom:12px}.ec-banner h2{color:white!important;margin:0}.ec-fine{font-size:12px;opacity:.88}.ec-card{border:1px solid #d7e2ec;border-radius:12px;padding:14px;margin:7px 0}.ec-card h4{margin:0 0 6px}</style>''',unsafe_allow_html=True)
    st.markdown('''<div class="ec-banner"><div class="ec-fine">EC-AI / INSTITUTIONAL RELATIONSHIP INTELLIGENCE · PUBLIC VIEWER</div><h2>Portfolio intelligence. Clear executive decisions.</h2><div>One executive workflow, illustrated with entirely fictional relationships.</div><div class="ec-fine">SYNTHETIC DATA · READ-ONLY · NO DATABASE CONNECTION</div></div>''',unsafe_allow_html=True)
    st.sidebar.title('EC-AI')
    st.sidebar.caption('Public viewer · fictional portfolio · read-only')
    page=st.sidebar.radio('Workspace',NAV)
    chosen=st.sidebar.selectbox('Relationship context',[r['Relationship'] for r in DATA])
    row=next(r for r in DATA if r['Relationship']==chosen)
    st.caption('This is a demonstration only. Scores, financial amounts, events, decisions, ownership and progress are fictional; no operational database is accessed or changed.')
    st.title(page)
    if page=='Executive Briefing':
        a,b,c,d=st.columns(4);a.metric('Relationships','10');b.metric('Management priorities','4');c.metric('Lead illustrative lending proxy','USD 600m');d.metric('Decisions to consider','1')
        left,right=st.columns([1.75,1])
        with left: st.plotly_chart(scatter(DATA),use_container_width=True)
        with right:
            st.info('Northstar Mobility: illustrative near-term financing review warrants validation before any decision.')
            st.markdown('**Management question**  Should leadership authorize a *scoped investigation*, not a lending commitment?')
    elif page=='Review':
        st.dataframe(pd.DataFrame(DATA)[['Relationship','Score','Attention','Urgency','Action']],use_container_width=True,hide_index=True)
        st.info(f"{chosen}: review the proposed {row['Action'].lower()} and supporting assumptions before management judgement.")
    elif page=='Relationships':
        c1,c2,c3=st.columns(3);c1.metric('Relationship',chosen);c2.metric('Sector',row['Sector']);c3.metric('Illustrative attention',str(row['Attention']))
        st.markdown(f"**Suggested investigation:** {row['Action']}. Validate client needs, financial evidence, risk and relationship economics before action.")
    elif page=='Decisions':
        st.info('Illustrative decision only — no changes are saved, no decision record is created.')
        choice=st.radio('Explore a fictional management judgement',['Approve investigation','Modify scope','Defer pending evidence'],horizontal=True)
        st.markdown(f'**Scenario:** {chosen} · {choice}.')
        st.caption('This selection changes only the browser view; it is not an approval or client instruction.')
    elif page=='Execution':
        st.info('Illustrative execution plan — no execution action or audit event is created.')
        plan=pd.DataFrame([['Coverage','Validate financing need and client timing','Next review','Proposed'],['Treasury','Assess liquidity and deposit relevance','Next review','Proposed'],['Credit / Risk','Review preliminary suitability','Following review','Proposed'],['Executive sponsor','Reassess evidence and disposition','Following review','Proposed']],columns=['Function','Illustrative next step','Review point','State'])
        st.dataframe(plan,use_container_width=True,hide_index=True)
    else:
        st.plotly_chart(scatter(DATA),use_container_width=True)
        st.dataframe(pd.DataFrame(DATA)[['Relationship','Sector','Attention','Urgency']],use_container_width=True,hide_index=True)
    st.caption('PUBLIC VIEWER · FICTIONAL DATA ONLY · NO DATABASE ACCESS · NO OPERATIONAL WRITES')
