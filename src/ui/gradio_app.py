"""Interfaz mínima en Gradio para el MVP."""

import gradio as gr

from src.cv_parser.cv_pipeline import CVPipeline
from src.job_parser.job_pipeline import JobPipeline
from src.matching.similarity import CVJobMatcher


cv_pipeline = CVPipeline()
job_pipeline = JobPipeline()
matcher = CVJobMatcher()


def analyze(cv_text: str, job_text: str) -> str:
    cv_data = cv_pipeline.process_text(cv_text)
    job_data = job_pipeline.process(job_text)

    result = matcher.calculate_match(
        cv_data=cv_data.__dict__,
        job_data=job_data.__dict__,
    )

    return (
        f"Score global: {result.global_score}\n"
        f"Similitud semántica: {result.semantic_similarity}\n"
        f"Match de skills: {result.skill_match_score}\n"
        f"Match de experiencia: {result.experience_match_score}\n\n"
        f"Skills coincidentes: {', '.join(result.matched_skills) or '-'}\n"
        f"Skills faltantes: {', '.join(result.missing_skills) or '-'}\n"
        f"Recomendaciones:\n- " + "\n- ".join(result.recommendations)
    )


def main():
    with gr.Blocks() as demo:
        gr.Markdown("# OPEN CAREER COACH - MVP")
        cv_input = gr.Textbox(label="Texto del CV", lines=10)
        job_input = gr.Textbox(label="Texto de la oferta", lines=10)
        output = gr.Textbox(label="Resultado", lines=15)

        btn = gr.Button("Analizar matching")
        btn.click(analyze, inputs=[cv_input, job_input], outputs=output)

    demo.launch()


if __name__ == "__main__":
    main()
