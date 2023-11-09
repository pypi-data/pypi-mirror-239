# Tik4Free
Developed by Fhivo aka vardxg (c) 2023
> All tools are listed here

- short2long ['convert any short link back to normal link.']
- aweme ['To get the aweme_id - videoid']
- checkExist ['Check if a user exist, not check if banned or private.']
- long2short ['Convert any long link to short.']
- removeWm ['Give u the link to get video without watermark']
- getSound ['Give u the link to the full sound.']
- getUserid ['Get Userid from any user.']



```python
from tik4free import Tik4Free

# for Example Check if a user exist.
test = Tik4Free.checkExist(input("Enter Usename >>> "))
print(test)

# or Convert short link to long so back to normal.
test = Tik4Free.short2long(Tik4Free.aweme(input("Enter Link >>> "))) # here we use the aweme func direct to get only the aweme_id.
print(test)
```

