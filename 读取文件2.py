from pathlib import Path  # pathlib is recommended

#repofile = Path('../repo_file.txt')  # 读取上一级目录文件
repofile = Path('./repo_file.txt')  # 读取上一级目录文件
with repofile.open() as f: 
    print(f.readline())