def get_response(user_input: str) -> str:
    
    lowered: str = user_input.lower()

    if not lowered.strip():
        return 'Você quis dizer algo ? '
    
    if 'adicionarberry' in lowered:
        return 'Vamos Adicionar'
    
    return 'Não consegui entender isso'

