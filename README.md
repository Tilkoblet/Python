## Python
Python 프로젝트의 소스코드입니다.

## 모듈 설치
```
> python -m pip install --upgrade pip
> python -m pip install requests
> python -m pip install asn1crypto
> python -m pip install pycryptodome
```

## 자주 발생하는 오류
- Microsoft Visual C++ 14.0 or greater is required 오류 발생시 아래 링크를 통해 다운로드 및 설치하세요.
https://visualstudio.microsoft.com/ko/visual-cpp-build-tools/

- pycryptodome 을 설치했는데도 실행시 No module named 'Crypto' 오류가 발생하면 아래와 같이 해보세요.
  ```
  > python -m pip uninstall pycryptodome
  > python -m pip uninstall crypto
  > python -m pip uninstall pycrypto
  > python -m pip install pycryptodome
  ```

## 데이터 형태별 샘플 코드
|파일명|설명|API 예시|
|---|---|---|
|UnitTest/TestCase1.py|인증서 필요 없음, 파라미터 암호화 필요 없음|인터넷등기소 등기물건 주소검색|
|UnitTest/TestCase2.py|인증서 필요 없음, 파라미터 암호화 필요함|경찰청교통민원24 운전면허진위여부|
|UnitTest/TestCase3.py|인증서 필요함|정부24 주민등록진위여부|
|UnitTest/TestCase4-1.py|간편인증 요청|국민건강보험공단 간편인증 요청|
|UnitTest/TestCase4-2.py|간편인증용 API 호출|국민건강보험공단 건강검진내역|
|UnitTest/TestCase5.py|바이너리 데이터를 파일로 저장|정부24 건축물대장 발급|
