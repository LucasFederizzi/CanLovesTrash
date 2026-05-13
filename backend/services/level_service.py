def calculate_fill_percentage(distance):

    MAX_DISTANCE = 20

    percentage = 100 - (
        (distance / MAX_DISTANCE) * 100
    )

    if percentage < 0:
        percentage = 0

    if percentage > 100:
        percentage = 100

    return int(percentage)