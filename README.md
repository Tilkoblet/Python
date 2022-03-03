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
