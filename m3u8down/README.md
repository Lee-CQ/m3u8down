# m3u8_6 ȫ�¼ܹ������ļ����ȫ��������һվʽ���������

## 1. �洢�ļ��ṹ��

/\<Root>/.allInfo.sqlite  
/\<Root>/<movie>/\*.m3u8  
/\<Root>/<movie>/\*.ts  
/\<Root>/<movie>.mp4

## 2. SQLite���ݽṹ��

_main: moviesHeaders  
_id | name | m3u8Url | Description | is_parse | is_down | is_combine

```
    names: everyMovie - > ���� = <name>  
              "idd      INTEGER PRIMARY KEY AUTOINCREMENT, "  
              "abs_uri  varchar(160) not null UNIQUE, "    
              "segment_name varchar(50) , "  
              "duration float, "  
              "key      blob, "  
              "key_uri   varchar(160), "  
              "key_name varchar(50), "  
              "method   varchar(10), "  
              "iv       varchar(50)"  
```

## 3. �ӿں����� m3u8down: ��һ��m3u8����������һ����Ƶ

m3u8downs: ����һ��m3u8down�������ļ����������ص�Root | m3u8�б� | Key����У�

## 4. ʵ�ַ����ӿڣ�

```python
from m3u8 import M3U8
from requests import Session


def load(uri, timeout=None, headers={}, custom_tags_parser=None, verify_ssl=True) -> M3U8:
    """
    Retrieves the content from a given URI and returns a M3U8 object.  
    Raises ValueError if invalid content or IOError if request fails.  
    �Ӹ�����URI�м������ݲ�����M3U8����  
    ������ЧValueError������ʧ�ܷ���IOError��  
    :return M3U8  
    """
    pass


class HttpClient(retry=3, timeout=30, *args, **kwargs) -> Session:
    """����һ��HTTP�ͻ�������ͬһ�ĵ��������ļ���  
    :return requests.Session  
    """


class SQL():
    """�������й����е�SQL������
     :return sql�������
    """


class M3U8Down():
    """��������m3u8��ts�ļ���"""


class M3U8Combine():
    """����ϲ�ts�ļ���"""


class M3U8Reload:
    """����M3U8�ļ�  """

```

## 5. ������������ʵ�֣�

5.1. ��ӡ����ӿ� - ʵ���ڲ�ͬλ���в�ͬ�������  
5.2. �����ļ������ӿ� -  
5.3. �����ļ�ģ������ӿ� -  
5.4. ���������� -  
5.5. �����������ļ�У�� -

## 6. ʵ�ֵĹ��ܣ�

6.1. ���ز�����m3u8�ļ���  
6.2. ���ݽ����õ���m3u8��������ts�ļ���  
6.3. �ϲ�ts�ļ��õ�mp4�ļ���  
6.4. ���������ļ������õ������б�

* ������־  
  2020-8-28�����m3u8downģ�������ܹ�����ϸ�����ĵ�����ɴ�ŵĴ�ܹ���  

