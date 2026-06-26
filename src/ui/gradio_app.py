"""
OPEN-CAREER-COACH · src/ui/gradio_app.py
Interfaz Gradio — v1.1.0 (Matching Explicable + Exportación)

Autor conceptual: Claude (Anthropic)
Director del proyecto: Javi Ciborro (@papayaykware)
Licencia: MIT
"""

import gradio as gr

from src.cv_parser.cv_pipeline import CVPipeline
from src.job_parser.job_pipeline import JobPipeline
from src.matching.similarity import CVJobMatcher
from src.matching.explainer import MatchingExplainer
from src.exporter.report_exporter import ReportExporter

# ─────────────────────────────────────────────
# INICIALIZACIÓN DE PIPELINES
# ─────────────────────────────────────────────

cv_pipeline = CVPipeline()
job_pipeline = JobPipeline()
matcher      = CVJobMatcher()
explainer    = MatchingExplainer()
exporter     = ReportExporter()


# ─────────────────────────────────────────────
# FUNCIONES
# ─────────────────────────────────────────────

def analyze(cv_text: str, job_text: str):
    """Pipeline completo: parsing → matching base → matching explicable."""
    if not cv_text.strip() or not job_text.strip():
        msg = "⚠️ Por favor, introduce tanto el texto del CV como el de la oferta."
        return msg, "", "", ""

    cv_data  = cv_pipeline.process_text(cv_text)
    job_data = job_pipeline.process(job_text)

    base = matcher.calculate_match(
        cv_data=cv_data.__dict__,
        job_data=job_data.__dict__,
    )
    explained = explainer.explain(cv_text, job_text)

    score_pct = int(explained.global_score * 100)
    if score_pct >= 65:
        nivel_emoji, nivel_texto = "🟢", "Alto encaje"
    elif score_pct >= 40:
        nivel_emoji, nivel_texto = "🟡", "Encaje moderado"
    else:
        nivel_emoji, nivel_texto = "🔴", "Encaje bajo"

    # Salida 1: Resumen ejecutivo
    resumen = (
        f"{nivel_emoji} **{nivel_texto}** — Score explicable: {score_pct}%\n\n"
        f"Score base (embeddings): {base.global_score:.2f} | "
        f"Similitud semántica: {base.semantic_similarity:.2f} | "
        f"Match de skills: {base.skill_match_score:.2f}\n\n"
        f"{explained.narrative}"
    )

    # Salida 2: Desglose dimensional
    filas = []
    for ds in explained.dimension_scores:
        barra = _barra(ds.score)
        filas.append(
            f"**{ds.dimension.replace('_', ' ').title()}** "
            f"(peso {int(ds.weight*100)}%)\n"
            f"{barra} {int(ds.score*100)}%\n"
            f"CV: {', '.join(ds.cv_fragments[:5]) or '—'}\n"
            f"Oferta: {', '.join(ds.offer_fragments[:5]) or '—'}"
        )
    dimensional = "\n\n".join(filas)

    # Salida 3: Gap analysis
    gap_lines = []
    for rm in explained.gap_analysis:
        icono = {"cubierto": "✅", "parcial": "🔶", "ausente": "❌"}.get(rm.status, "❓")
        evidencia = f" → *{rm.cv_evidence}*" if rm.cv_evidence else ""
        gap_lines.append(f"{icono} {rm.requirement[:100]}{evidencia}")
    gap_md = (
        "\n".join(gap_lines)
        if gap_lines
        else "No se detectaron requisitos estructurados en la oferta."
    )

    # Salida 4: Skills motor base
    skills_base = (
        f"✅ **Skills coincidentes:** {', '.join(base.matched_skills) or '—'}\n\n"
        f"❌ **Skills faltantes:** {', '.join(base.missing_skills) or '—'}\n\n"
        f"💡 **Recomendaciones:**\n"
        + "\n".join(f"  · {r}" for r in base.recommendations)
    )

    return resumen, dimensional, gap_md, skills_base


def export_report(cv_text: str, job_text: str):
    """Genera informes MD y JSON y devuelve las rutas para descarga."""
    if not cv_text.strip() or not job_text.strip():
        return None, None

    cv_data  = cv_pipeline.process_text(cv_text)
    job_data = job_pipeline.process(job_text)
    base     = matcher.calculate_match(
        cv_data=cv_data.__dict__,
        job_data=job_data.__dict__,
    )
    explained = explainer.explain(cv_text, job_text)
    rutas = exporter.export(explained, base, nombre_base="informe_matching")

    return str(rutas.get("md", "")), str(rutas.get("json", ""))


def _barra(score: float, longitud: int = 20) -> str:
    llenos = int(score * longitud)
    return "█" * llenos + "░" * (longitud - llenos)


# ─────────────────────────────────────────────
# INTERFAZ GRADIO
# ─────────────────────────────────────────────

def main():
    with gr.Blocks(title="Open Career Coach", theme=gr.themes.Soft()) as demo:

        gr.Markdown(
            """
            # 🎯 OPEN CAREER COACH
            **Matching explicable entre CV y oferta de empleo**
            *v1.1.0 · Open Source · [@papayaykware](https://github.com/papayaykware)*
            """
        )

        # Inputs
        with gr.Row():
            cv_input = gr.Textbox(
                label="📄 Texto del CV",
                placeholder="Pega aquí el contenido de tu CV...",
                lines=14,
            )
            job_input = gr.Textbox(
                label="💼 Texto de la oferta",
                placeholder="Pega aquí la descripción de la oferta...",
                lines=14,
            )

        btn = gr.Button("🔍 Analizar matching", variant="primary", size="lg")

        # Outputs en tabs
        with gr.Tabs():
            with gr.Tab("📊 Resumen"):
                out_resumen = gr.Markdown()
            with gr.Tab("📐 Desglose dimensional"):
                out_dimensional = gr.Markdown()
            with gr.Tab("🔎 Gap analysis"):
                out_gaps = gr.Markdown()
            with gr.Tab("🛠️ Skills (motor base)"):
                out_skills = gr.Markdown()

        btn.click(
            fn=analyze,
            inputs=[cv_input, job_input],
            outputs=[out_resumen, out_dimensional, out_gaps, out_skills],
        )

        # Exportación
        gr.Markdown("### 📥 Exportar informe")
        with gr.Row():
            btn_export = gr.Button("Generar informe MD + JSON", variant="secondary")
            out_md     = gr.File(label="Informe Markdown")
            out_json   = gr.File(label="Informe JSON")

        btn_export.click(
            fn=export_report,
            inputs=[cv_input, job_input],
            outputs=[out_md, out_json],
        )

        gr.Markdown(
            """
            ---
            *Autor conceptual: Claude (Anthropic) · Director: Javi Ciborro (@papayaykware) · Licencia MIT*
            """
        )

    demo.launch()


if __name__ == "__main__":
    main()
