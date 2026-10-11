"""
PDF Report Generator
Uses ReportLab to export PDF prediction reports containing design metrics, predictions, recommendations, and IEEE plots.
"""

import os
import sys
import datetime
import logging
from typing import Dict, Any, List

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image

logger = logging.getLogger("PDFGenerator")

class PDFReportGenerator:
    def __init__(self, output_path: str = "reports/prediction_report.pdf"):
        self.output_path = os.path.abspath(output_path)
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

    def generate_report(
        self,
        design_name: str,
        clock_period: float,
        prediction_label: str,
        confidence: float,
        probability: float,
        feature_metrics: Dict[str, Any],
        recommendations: List[Dict[str, str]],
        graphs_dir: str = "graphs"
    ):
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=letter,
            rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#1A365D"),
            alignment=1,
            spaceAfter=8
        )

        subtitle_style = ParagraphStyle(
            "DocSubTitle",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#4A5568"),
            alignment=1,
            spaceAfter=14
        )

        h2_style = ParagraphStyle(
            "SectionHeader",
            parent=styles["Heading2"],
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#2B6CB0"),
            spaceBefore=12,
            spaceAfter=6
        )

        normal_style = styles["Normal"]
        normal_style.fontSize = 8.5
        normal_style.leading = 11

        story = []

        story.append(Paragraph("An Explainable AI-Assisted Early Timing Violation Prediction Report", title_style))
        story.append(Paragraph(
            f"Open-Source EDA Integration &bull; Generated: {datetime.datetime.now().strftime('%B %d, %Y - %H:%M:%S')}",
            subtitle_style
        ))
        story.append(Spacer(1, 6))

        is_viol = (prediction_label.upper() == "YES")
        banner_bg = colors.HexColor("#FFF5F5") if is_viol else colors.HexColor("#F0FFF4")
        banner_border = colors.HexColor("#E53E3E") if is_viol else colors.HexColor("#38A169")
        verdict_text = "CRITICAL TIMING VIOLATION PREDICTED" if is_viol else "TIMING CONSTRAINTS SATISFIED (NO VIOLATION)"

        verdict_data = [
            [Paragraph(f"<b>Design Module:</b> {design_name}", normal_style), Paragraph(f"<b>Clock Constraint:</b> {clock_period:.3f} ns ({1000.0/max(0.1, clock_period):.1f} MHz)", normal_style)],
            [Paragraph(f"<b>Prediction Verdict:</b> <font color='{banner_border.hexval()}'><b>{verdict_text}</b></font>", normal_style),
             Paragraph(f"<b>Confidence Score:</b> {confidence:.1f}% (Prob: {probability:.3f})", normal_style)]
        ]

        verdict_table = Table(verdict_data, colWidths=[270, 270])
        verdict_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), banner_bg),
            ("BOX", (0, 0), (-1, -1), 1.5, banner_border),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(verdict_table)
        story.append(Spacer(1, 10))

        story.append(Paragraph("Synthesized Microarchitectural & Physical Layout Features", h2_style))
        feat_table_data = [["Parameter Feature", "Value", "Parameter Feature", "Value"]]
        keys = list(feature_metrics.keys())
        for i in range(0, len(keys), 2):
            k1 = keys[i]
            v1 = str(feature_metrics[k1])
            k2 = keys[i+1] if i+1 < len(keys) else ""
            v2 = str(feature_metrics[k2]) if i+1 < len(keys) else ""
            feat_table_data.append([k1, v1, k2, v2])

        feat_table = Table(feat_table_data, colWidths=[160, 110, 160, 110])
        feat_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EDF2F7")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#2D3748")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ]))
        story.append(feat_table)
        story.append(Spacer(1, 10))

        story.append(Paragraph("Automated VLSI Timing Closure Optimization Directives", h2_style))
        rec_table_data = [["Parameter", "Status", "Recommended Action Directive", "Technical Rationale"]]
        for r in recommendations:
            rec_table_data.append([
                Paragraph(r["Parameter"], normal_style),
                Paragraph(f"<b>{r['Status']}</b>", normal_style),
                Paragraph(f"<b>{r['Action']}</b>", normal_style),
                Paragraph(r["Description"], normal_style)
            ])

        rec_table = Table(rec_table_data, colWidths=[95, 50, 145, 250])
        rec_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2B6CB0")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(rec_table)
        story.append(Spacer(1, 10))

        fig1_path = os.path.join(graphs_dir, "feature_importance.png")
        fig2_path = os.path.join(graphs_dir, "confusion_matrix.png")
        if os.path.exists(fig1_path) and os.path.exists(fig2_path):
            story.append(Paragraph("IEEE Model Verification & Feature Driver Plots", h2_style))
            img_table_data = [[
                Image(fig1_path, width=250, height=170),
                Image(fig2_path, width=240, height=170)
            ]]
            img_table = Table(img_table_data, colWidths=[270, 270])
            img_table.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
            story.append(img_table)

        doc.build(story)
        logger.info(f"PDF prediction report created: {self.output_path}")
        return self.output_path

if __name__ == "__main__":
    pass
