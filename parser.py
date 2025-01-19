import re

def parsePython(file_path):
    packagesToImport = []
    memberFunctions = []
    with open(file_path, 'r') as file:
        file_content = file.read()
        pattern = re.compile(r'(?<=#\$START\$)(.*?)(?=^#\$END\$)', re.MULTILINE | re.DOTALL)
        match = pattern.search(file_content)
        if match:
            imports = match.group(1).split('\n')
            for imp in imports:
                    if len(imp) > 0:
                        packagesToImport.append(imp.split(' ')[1].strip())

        pattern = r"def\s+(\w+)\(.*?\):.*?\"\"\"(.*?)\"\"\""
        matches = re.findall(pattern, file_content, re.MULTILINE | re.DOTALL)
        memberFunctions = [{"function_name": match[0], "description": match[1].strip()} for match in matches]
    return (packagesToImport, memberFunctions)
    
# print(parsePython("sample.py"))