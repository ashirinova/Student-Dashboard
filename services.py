from typing import List, Dict, Any, Tuple
from config import GRADE_BOUNDARIES

def calculate_grade(score: float) -> str:
    """Tələbənin topladığı bala görə Grade hərfini təyin edir."""
    if score >= GRADE_BOUNDARIES['A']:
        return 'A'
    elif score >= GRADE_BOUNDARIES['B']:
        return 'B'
    elif score >= GRADE_BOUNDARIES['C']:
        return 'C'
    elif score >= GRADE_BOUNDARIES['D']:
        return 'D'
    else:
        return 'F'

def calculate_statistics(students: List[Tuple[int, str, float]]) -> Dict[str, Any]:
    """Tələbə siyahısına əsasən statistik göstəriciləri hesablayır."""
    if not students:
        return {
            "total_students": 0,
            "average_score": 0.0,
            "highest_score": 0.0,
            "lowest_score": 0.0,
            "pass_rate": 0.0
        }

    scores = [student[2] for student in students]
    passed_students = sum(1 for score in scores if score >= GRADE_BOUNDARIES['D'])
    
    return {
        "total_students": len(scores),
        "average_score": round(sum(scores) / len(scores), 1),
        "highest_score": max(scores),
        "lowest_score": min(scores),
        "pass_rate": round((passed_students / len(scores)) * 100, 1)
    }

def get_grade_distribution(students: List[Tuple[int, str, float]]) -> Dict[str, int]:
    """Grade-lərin say paylanmasını qaytarır."""
    distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    for student in students:
        grade = calculate_grade(student[2])
        distribution[grade] += 1
    return distribution