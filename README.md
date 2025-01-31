# generate-data
> perplexity api를 이용해 데이터 생성하는 코드

## 사용 방법
1. results/ 빈 폴더 생성
2. prompt/*.yaml 파일 작성
```yaml
prompt_ver: 
summary: ...
role:
  system:
    content: 당신은 예시 json을 출력하는 역할이다. 반드시 다른 부연설명 없이 json만 반환하라. # 시스템 프롬프트
  user:
    content: 다음과 같은 형태로 key는 동일하지만 value는 다른 예시 10개를 생성하라. 이름, 나라, 주소 등을 겹치지 않게 다양하게 바꿔라.  # 유저 프롬프트
model: "llama-3.1-sonar-large-128k-online" # perplexity
temperature: 
max_tokens: 
top_p: 
frequency_penalty: 
presence_penalty: 
search_domain_filter: 
return_images: 
return_related_questions: 
search_recency_filter: 
top_k: 
```
3. __run__.py 파일 실행
`python __run__.py prompt/*.yaml {join/trip/experience}`

## 데이터 변형을 위한 샘플 조정
- prompt/join.json, prompt/trip.json, prompt/experience.json는 각각의 샘플 파일입니다.
- 해당 파일은 LLM에 예시로 들어가므로 수정하면 다른 결과를 반환할 수 있습니다.