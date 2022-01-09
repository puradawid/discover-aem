import json
import re

file = open("./final_result.jl")

def host(url):
    return re.search('^(?:https?)?:?//([^/]+)', url).group(1)

result = {}

for line in file:
    obj = json.loads(line)
    result[host(obj['page'])] = 1

for domain in result:
    print(domain)

print("Done")
