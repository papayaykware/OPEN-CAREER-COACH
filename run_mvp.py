from src.cv_parser_simple import parse_cv
from src.job_parser_simple import parse_job
from src.matching_simple import compute_match
from src.recommender import recommend_actions

def main():
    print("\n=== OPEN CAREER COACH — MVP ===\n")

    cv = input("Introduce tus habilidades separadas por comas:\n> ")
    job = input("\nIntroduce los requisitos de la oferta separados por comas:\n> ")

    cv_data = parse_cv(cv)
    job_data = parse_job(job)

    match = compute_match(cv_data, job_data)
    recomendaciones = recommend_actions(match)

    print("\n--- RESULTADOS ---")
    print(f"Score de compatibilidad: {match['score']}")
    print(f"Habilidades coincidentes: {match['matched_skills']}")
    print(f"Habilidades faltantes: {match['missing_skills']}")

    print("\n--- RECOMENDACIONES ---")
    for r in recomendaciones:
        print(f"- {r}")

if __name__ == "__main__":
    main()
