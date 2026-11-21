import math

# Коэффициенты градообразовательного буфера (случайные примерные значения)
COHESION = 0.8          # Коэффициент сцепления
FRICTION_ANGLE = math.radians(30)  # Угол трения в радианах
DEEP = 10.0              # Глубина слоя в метрах
AREA = 5000.0            # Площадь буфера в м²
STRENGTH_THRESHOLD = 200.0  # Пороговое значение прочности (МПа)

def compute_strength(cohesion: float, friction_angle: float, depth: float, area: float) -> float:
    """
    Расчёт суммарной прочности буфера по модели Ной-
    2 (simplified for educational purposes).
    """
    normal_force = cohesion * depth * area
    shear_force = math.tan(friction_angle) * normal_force
    return shear_force / area  # прочность на площадь, МПа

strength = compute_strength(COHESION, FRICTION_ANGLE, DEEP, AREA)

print(f"Прочность градообразовательного буфера: {strength:.2f} МПа")