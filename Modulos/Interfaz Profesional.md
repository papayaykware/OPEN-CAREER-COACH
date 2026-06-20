# 🖥️ MÓDULO 10: Interfaz Profesional

> **Duración estimada:** 4-6 horas | **Nivel:** Intermedio

---

## 1. Introducción

Desarrollo de interfaces web profesionales con Gradio y Streamlit para integrar todas las funcionalidades del sistema.

---

## 2. Implementación Gradio

```python
# src/ui/gradio_app.py
"""Aplicación web con Gradio."""

import gradio as gr
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.cv_parser.cv_pipeline import CVPipeline
from src.job_parser.job_scraper import JobParser
from src.matching.ranking import CVJobMatcher
from src.cv_enhancer.cv_rewriter import CVRewriter
from src.cover_letter.generator import CoverLetterGenerator
from src.rag_system.chat_engine import CareerChat


class CareerCoachApp:
    """Aplicación completa de Career Coach."""
    
    def __init__(self):
        self.cv_pipeline = CVPipeline()
        self.job_parser = JobParser()
        self.matcher = CVJobMatcher()
        self.enhancer = CVRewriter()
        self.cover_gen = CoverLetterGenerator()
        self.chat = CareerChat()
        self.current_cv = None
        self.current_job = None
    
    def build_ui(self):
        """Construye la interfaz de Gradio."""
        
        with gr.Blocks(title="OPEN CAREER COACH", theme=gr.themes.Soft()) as app:
            gr.Markdown("""
            # 🎯 OPEN CAREER COACH
            ## Asistente de IA para Empleabilidad
            """)
            
            with gr.Tab("📄 Analizar CV"):
                with gr.Row():
                    with gr.Column():
                        cv_file = gr.File(label="Subir CV (PDF/DOCX/TXT)")
                        analyze_btn = gr.Button("Analizar", variant="primary")
                    
                    with gr.Column():
                        cv_output = gr.JSON(label="Datos Extraídos")
                
                analyze_btn.click(
                    fn=self._analyze_cv,
                    inputs=cv_file,
                    outputs=cv_output
                )
            
            with gr.Tab("🔍 Matching"):
                with gr.Row():
                    with gr.Column():
                        job_text = gr.Textbox(
                            label="Descripción de la Oferta",
                            lines=10
                        )
                        match_btn = gr.Button("Calcular Match", variant="primary")
                    
                    with gr.Column():
                        match_output = gr.JSON(label="Resultado del Matching")
                        match_plot = gr.Plot(label="Visualización")
                
                match_btn.click(
                    fn=self._calculate_match,
                    inputs=job_text,
                    outputs=[match_output, match_plot]
                )
            
            with gr.Tab("✨ Mejorar CV"):
                improve_btn = gr.Button("Generar Mejoras", variant="primary")
                improvements = gr.Markdown()
                
                improve_btn.click(
                    fn=self._improve_cv,
                    outputs=improvements
                )
            
            with gr.Tab("📝 Carta de Presentación"):
                style = gr.Radio(
                    choices=["classic", "technical", "executive"],
                    value="classic",
                    label="Estilo"
                )
                letter_btn = gr.Button("Generar Carta", variant="primary")
                letter_output = gr.Textbox(label="Carta", lines=15)
                
                letter_btn.click(
                    fn=self._generate_letter,
                    inputs=style,
                    outputs=letter_output
                )
            
            with gr.Tab("💬 Chat RAG"):
                chatbot = gr.Chatbot()
                msg = gr.Textbox(label="Pregunta")
                chat_btn = gr.Button("Enviar", variant="primary")
                
                chat_btn.click(
                    fn=self._chat,
                    inputs=[msg, chatbot],
                    outputs=chatbot
                )
        
        return app
    
    def _analyze_cv(self, file):
        """Analiza un CV subido."""
        if file is None:
            return {"error": "No se subió archivo"}
        
        self.current_cv = self.cv_pipeline.process(file.name)
        return self.current_cv.to_dict() if hasattr(self.current_cv, 'to_dict') else vars(self.current_cv)
    
    def _calculate_match(self, job_text):
        """Calcula matching con oferta."""
        if self.current_cv is None:
            return {"error": "Primero analiza un CV"}, None
        
        self.current_job = self.job_parser.parse(job_text)
        result = self.matcher.calculate_match(
            self.current_cv.__dict__ if hasattr(self.current_cv, '__dict__') else self.current_cv,
            self.current_job.__dict__ if hasattr(self.current_job, '__dict__') else self.current_job
        )
        
        # Crear visualización
        import matplotlib.pyplot as plt
        import numpy as np
        
        categories = ['Técnico', 'Competencial', 'Contextual', 'ATS']
        scores = [
            result.technical_score,
            result.competencial_score,
            result.contextual_score,
            result.ats_score
        ]
        
        fig, ax = plt.subplots(figsize=(8, 4))
        bars = ax.barh(categories, scores, color=['#2ecc71', '#3498db', '#9b59b6', '#e74c3c'])
        ax.set_xlim(0, 1)
        ax.set_xlabel('Score')
        ax.set_title(f'Match Global: {result.global_score:.1%}')
        
        for bar, score in zip(bars, scores):
            ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                   f'{score:.1%}', va='center')
        
        plt.tight_layout()
        
        return result.__dict__, fig
    
    def _improve_cv(self):
        """Genera mejoras para el CV."""
        if self.current_cv is None:
            return "Primero analiza un CV"
        
        profile = self.enhancer.rewrite_profile(self.current_cv.__dict__ if hasattr(self.current_cv, '__dict__') else self.current_cv)
        return f"## Perfil Mejorado\n\n{profile}"
    
    def _generate_letter(self, style):
        """Genera carta de presentación."""
        if self.current_cv is None or self.current_job is None:
            return "Necesitas CV y oferta primero"
        
        letter = self.cover_gen.generate(
            self.current_cv.__dict__ if hasattr(self.current_cv, '__dict__') else self.current_cv,
            self.current_job.__dict__ if hasattr(self.current_job, '__dict__') else self.current_job,
            style=style
        )
        return letter
    
    def _chat(self, message, history):
        """Procesa mensaje del chat."""
        if self.current_cv is None:
            return history + [[message, "Primero sube tu CV"]]
        
        # Indexar CV si es primera vez
        if not self.chat.vector_store.documents:
            self.chat.index_cv(self.current_cv.__dict__ if hasattr(self.current_cv, '__dict__') else self.current_cv)
        
        response = self.chat.ask(message)
        return history + [[message, response]]


def main():
    app = CareerCoachApp()
    ui = app.build_ui()
    ui.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()
```

---

## 3. Ejercicios

### 🟢 Básico
1. Ejecutar la app y probar todas las pestañas
2. Personalizar tema de Gradio

### 🟡 Intermedio
3. Implementar versión Streamlit alternativa
4. Añadir autenticación de usuarios

### 🔴 Avanzado
5. Desplegar en Hugging Face Spaces
6. Implementar PWA (Progressive Web App)

---

**[⬅️ Módulo 9](09-sistema-rag.md) | [➡️ Módulo 11](11-evaluacion.md)**
```

---

