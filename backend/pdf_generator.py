from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO

def generate_analysis_pdf(data: dict) -> BytesIO:
    """Synthesizes a premium clinical report from analysis data."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    
    # Custom Styles for Premium Aesthetic
    title_style = ParagraphStyle(
        'VaidyaTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#10b981'), # Vaidya Green
        spaceAfter=20
    )
    
    content = []
    
    # Header
    content.append(Paragraph("Vaidya.ai — Clinical Analysis Report", title_style))
    content.append(Spacer(1, 12))
    
    # Summary Section
    content.append(Paragraph("<b>Executive Summary:</b>", styles['Heading2']))
    content.append(Paragraph(data.get("answer", ""), styles['Normal']))
    content.append(Spacer(1, 12))
    
    # Metadata Table
    meta_data = [
        ["Confidence Tier:", data.get("confidence_tier", "N/A")],
        ["Corroborating Chunks:", str(data.get("corroborating_chunks", 0))],
        ["Source:", data.get("source_text", "Unknown")]
    ]
    t = Table(meta_data, colWidths=[120, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    content.append(t)
    content.append(Spacer(1, 24))
    
    # Modern Parallel Correlation
    content.append(Paragraph("<b>Modern Clinical Parallel:</b>", styles['Heading3']))
    content.append(Paragraph(data.get("modern_parallel", ""), styles['Italic']))
    
    # Verbatim Classical Citation
    content.append(Spacer(1, 12))
    content.append(Paragraph("<b>Verbatim Classical Citation:</b>", styles['Heading3']))
    citation_style = ParagraphStyle('Citation', parent=styles['Normal'], leftIndent=20, fontName='Times-Italic')
    content.append(Paragraph(f"\"{data.get('source_line', '')}\"", citation_style))
    
    # Extracted Entities Glossary
    entities = data.get("extracted_entities", [])
    if entities:
        content.append(Spacer(1, 24))
        content.append(Paragraph("<b>Clinical Glossary (Ayurvedic Entities):</b>", styles['Heading3']))
        for ent in entities:
            content.append(Paragraph(f"<b>{ent['term']}:</b> {ent['definition']}", styles['Normal']))
            content.append(Spacer(1, 6))

    # Footer Disclaimer
    content.append(Spacer(1, 40))
    content.append(Paragraph("<font size=8 color='grey'>Disclaimer: This report is synthesized by Vaidya.ai for educational purposes only. Consult a qualified practitioner for clinical diagnosis.</font>", styles['Normal']))
    
    doc.build(content)
    buffer.seek(0)
    return buffer
