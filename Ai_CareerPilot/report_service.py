from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def make_report(analysis):
    buf=BytesIO(); doc=SimpleDocTemplate(buf,pagesize=letter,rightMargin=48,leftMargin=48,topMargin=48,bottomMargin=48)
    styles=getSampleStyleSheet(); styles.add(ParagraphStyle(name='PurpleTitle',parent=styles['Title'],textColor=colors.HexColor('#7C3AED'),fontSize=22,spaceAfter=14))
    story=[Paragraph('AI CareerPilot',styles['PurpleTitle']),Paragraph('Resume Analysis Report',styles['Heading1']),Paragraph(f'Target role: {analysis.job_title}',styles['Normal']),Paragraph(f'Skill coverage: {analysis.coverage}% (not a probability of being hired)',styles['Normal']),Spacer(1,12)]
    for title, values in [('Matched skills',analysis.matched_skills or []),('Missing skills',analysis.missing_skills or []),('Strengths',analysis.strengths or []),('Improvement suggestions',analysis.improvements or []),('Project ideas',analysis.projects or [])]:
        story.append(Paragraph(title,styles['Heading2']))
        story.append(ListFlowable([ListItem(Paragraph(str(v),styles['BodyText'])) for v in values] or [ListItem(Paragraph('None recorded.',styles['BodyText']))],bulletType='bullet'))
        story.append(Spacer(1,8))
    doc.build(story); buf.seek(0); return buf
