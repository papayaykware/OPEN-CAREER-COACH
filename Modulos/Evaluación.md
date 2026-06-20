# 📊 MÓDULO 11: Evaluación

> **Duración estimada:** 4-5 horas | **Nivel:** Avanzado

---

## 1. Métricas de Evaluación

| Métrica | Fórmula | Uso |
|---------|---------|-----|
| **Precision** | TP / (TP + FP) | Exactitud de matches positivos |
| **Recall** | TP / (TP + FN) | Cobertura de matches correctos |
| **F1-Score** | 2 × (P × R) / (P + R) | Balance P y R |
| **MAP** | Mean Average Precision | Ranking quality |
| **NDCG** | Normalized DCG | Ranking con relevancia graduada |
| **Semantic Sim.** | Cosine(embeddings) | Similitud semántica |

---

## 2. Implementación

```python
# src/evaluation/metrics.py
"""Métricas de evaluación del sistema."""

import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class EvaluationResult:
    precision: float
    recall: float
    f1_score: float
    map_score: float
    semantic_similarity: float


class Evaluator:
    """Evalúa calidad del sistema de matching."""
    
    def evaluate(
        self,
        predictions: List[Dict],
        ground_truth: List[Dict]
    ) -> EvaluationResult:
        """Evalúa predicciones contra ground truth."""
        
        # Calcular TP, FP, FN
        tp, fp, fn = self._calculate_confusion_matrix(predictions, ground_truth)
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        # MAP
        map_score = self._calculate_map(predictions, ground_truth)
        
        # Similitud semántica promedio
        sem_sim = self._calculate_semantic_similarity(predictions, ground_truth)
        
        return EvaluationResult(
            precision=round(precision, 3),
            recall=round(recall, 3),
            f1_score=round(f1, 3),
            map_score=round(map_score, 3),
            semantic_similarity=round(sem_sim, 3)
        )
    
    def _calculate_confusion_matrix(
        self,
        predictions: List[Dict],
        ground_truth: List[Dict]
    ) -> Tuple[int, int, int]:
        """Calcula matriz de confusión."""
        tp, fp, fn = 0, 0, 0
        
        pred_ids = {p.get("job_id") for p in predictions}
        gt_ids = {g.get("job_id") for g in ground_truth if g.get("relevant", False)}
        
        tp = len(pred_ids & gt_ids)
        fp = len(pred_ids - gt_ids)
        fn = len(gt_ids - pred_ids)
        
        return tp, fp, fn
    
    def _calculate_map(
        self,
        predictions: List[Dict],
        ground_truth: List[Dict]
    ) -> float:
        """Calcula Mean Average Precision."""
        # Simplificado - implementación completa requiere relevancia por posición
        return 0.0
    
    def _calculate_semantic_similarity(
        self,
        predictions: List[Dict],
        ground_truth: List[Dict]
    ) -> float:
        """Calcula similitud semántica promedio."""
        # Implementar con embeddings
        return 0.0
```

---

## 3. Ejercicios

### 🟢 Básico
1. Crear dataset de prueba con 20 CVs y 10 ofertas
2. Calcular métricas básicas

### 🟡 Intermedio
3. Implementar evaluación A/B de dos versiones del matcher
4. Crear visualización de métricas con tiempo

### 🔴 Avanzado
5. Sistema de evaluación continua (CI/CD)
6. Benchmark contra soluciones comerciales

---

**[⬅️ Módulo 10](10-interfaz.md) | [➡️ Módulo 12](12-despliegue.md)**
```

---
