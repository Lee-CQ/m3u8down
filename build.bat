cd %~dp0

:: ���ع��� - ���� : setuptools wheel 
:: setup.py�ļ���д��� - 
python setup.py sdist bdist_wheel

:: �ϴ��� -- ���� : python -m pip install --upgrade twine
:: �û��������� home\.pypirc û���ֶ�
pause ��������ϴ��� pypi ...
python -m twine upload dist/*

pause