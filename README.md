# httpsend
Simple Python Based HTTP(S) Send Tool For Api Testing

# Motivation
- Tools like "Advanced REST Client", "Postman", "Paw" exist and that those tools are useful.
- But in my opinion, those tools are sometimes not very useful:
  * They distribute a lot of information on different screens.
  * Their complexity brings bugs.
  * It is non-trivial to use them in a chain of other tools.
  * They are not fast.
  * They use proprietary data formats to store a collection of requests. Export to other formats do generally lack feature completeness and brings additional bugs.
- Curl exists to send requests with a single command line and is incredibly useful but could be more convenient in many scenarios.

# What is this thing doing?
- You write RFC 2068 / RFC 2616 / RFC 7230 compliant https requests in files.
- You POST them with this python skript.
- That is all.

# How-To:
python HTTPSend.py [-s] [-q] filename.http [filename1.http] ...

Skript works on files containing http requests in given order.  
If -s option is provided, use https  
If -q option is provided, do not print response  

Possible future improvements:
- When folder is provided instead of files, go through files in folder alphabetically.
- add error handling
