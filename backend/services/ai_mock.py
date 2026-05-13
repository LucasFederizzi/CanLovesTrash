def analyze_fill_level(level):

    if level >= 90:

        return (
            'ALERTA SEVERO - '
            'Lixeira cheia'
        )

    elif level >= 70:

        return (
            'Coleta recomendada'
        )

    return 'Nível normal'