import anthropic

# Anthropic API 키 설정
API_KEY = 'your-anthropic-api-key'
client = anthropic.Client(api_key=API_KEY)


def analyze_program(info):
    prompt = (
        f"당신은 사용자가 업로드한 파일을 분석하고 위험성을 검증하는 챗봇입니다."
        f"{info}는 radare2가 사용자가 업로드한 파일을 바탕으로 분석한 결과입니다."
        f"당신이 사용해야 하는 정보는 {info}뿐이며, 거짓으로 정보를 생성해서는 절대 안됩니다."
        f"radare2로부터 information, function, strings, section을 전달받게 되며,위의 정보로부터 악성 코드의 여지가 있는지 분석합니다.예를 들어 사용자의 개인 정보를 요청하거나, 강제로 권한을 변경하는 함수, 네트워크 연결을 시도하거나 결제를 시도하는 함수는 악성 코드의 여지가 있습니다."
        f"받은 정보를 바탕으로 information(실행 가능한 파일인지, 어떠한 포맷인지 설명하세요.), function(호출되는 주요 함수와 의심스러운 함수를 나열하세요.), strings, section을 자연어로 10 줄 내외로 요약하고 악성 코드의 여지가 있는지 위험을 H, M, L로 나눠서 제시하세요."
        f"radare2로부터 전달받은 정보만을 사용해야하며, 임의적으로 프롬프트에 있는 내용을 그대로 쓰거나 존재하지 않는 정보를 가지고 판단해서는 안됩니다."
        f"1.'info'에서 찾을 수 있는 악성 코드 패턴: '불명확한 컴파일러 정보'->일반적인 컴파일러에서 생성되지 않는 특이한 파일 정보를 가지고 있으면 악성 코드로 의심할 수 있습니다.2.'functions'에서 찾을 수 있는 악성 코드 패턴: '의심스러운 시스템 호출'->CreateFile,CreateProcess,VirtualAlloc과 같이 시스템 자원을 직접 다루는 함수는 의심해볼 필요가 있습니다. '권한 상승 하수'->AdjustTokenPricielges,SetSecurityDescriptionDacl등 시스템 권한을 변경하거나 권한 상승을 시도하는 함수를 주의합니다. '코드 인젝션, 메모리 조작'->WriteProcessMemory, CreateRemoteThread와 같이 원격 프로세스에 코드를 삽입하거나 메모리를 조작하려는 함수는 의심할 여지가 있습니다.3.'strings'에서 찾을 수 있는 악성 코드 패턴: '의심스러운 URL 또는 IP', '악성 명령어와 경로'->'rm-rf나 del C:\\Windows'와 같이 시스템을 파괴할 수 있는 코드는 위험합니다."
        f"4. sections에서 찾을 수 있는 악성 코드 패턴->'비정상적인 섹션 이름': .text와 .data와 같이 일반적인 섹션 이름인 것이 아니라 일반적으로 사용되지 않는 섹션 이름은 의심할 수 있습니다. 위와 유사한 정황을 발견하면 위험도를 높게 평가합니다. 그렇지 않다면 안전한 코드로 판단합니다. 정상적인 코드에도 저러한 정황이 발견될 수 있으므로 중립성을 유지합니다. radare2로부터 제공받은 정보만을 이용해야합니다. "
        f"출력 포맷: information 요약, function 요약, strings 요약, section 요약, 위험도(H, M, L)와 판단 근거"
        f"위험도가 높은 부분으로 판단되는 부분이 있다면 그 부분을 추가로 설명해주세요."
        f"더하여, 분석 결과를 바탕으로 이 파일의 실행 로직과 목적에 대해 추측해서 설명하세요."
        #f"You are an AI that analyzes programs for potential malware threats. "
        #f"Based on the following information, provide a concise overview of the program and determine if it poses any malware risk:\n\n"
        #f"{info}\n\n"
        #f"Please provide the analysis in a clear and professional manner."
    )

    response = client.completions.create(
        model="claude-v1",
        prompt=anthropic.HUMAN_PROMPT + prompt + anthropic.AI_PROMPT,
        max_tokens_to_sample=500,
        temperature=0.7
    )

    return response.completion.strip()


def ask_llm(chat_history):
    # 대화 내역을 하나의 프롬프트로 결합
    prompt = "\n".join(chat_history)

    # LLM에 대화 내역을 전달하여 응답을 생성
    response = client.completions.create(
        model="claude-v1",
        prompt=anthropic.HUMAN_PROMPT + prompt + anthropic.AI_PROMPT,
        max_tokens_to_sample=500,
        temperature=0.7
    )
    return response.completion.strip()

