import re

def parseModelTools(file_content):
    packagesToImport = []
    memberFunctions = []
    pattern = re.compile(r'(?<=#\$START\$)(.*?)(?=^#\$END\$)', re.MULTILINE | re.DOTALL)
    match = pattern.search(file_content)
    if match:
        imports = match.group(1).split('\n')
        for imp in imports:
                if len(imp) > 0:
                    lib_name = imp.split(' ')[1].split('.')[0]
                    if lib_name not in packagesToImport:
                        packagesToImport.append(lib_name)

    pattern = r"def\s+(\w+)\(.*?\):.*?\"\"\"(.*?)\"\"\""
    matches = re.findall(pattern, file_content, re.MULTILINE | re.DOTALL)
    memberFunctions = [{"function_name": match[0], "description": match[1].strip()} for match in matches]
    return (packagesToImport, memberFunctions)
    
# print(parsePython("demo.py"))