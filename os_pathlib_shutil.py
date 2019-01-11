import os
import shutil
from pathlib import Path

#遍历目录
def iter_dir(p):
    for d in p.rglob(''):
        print (d)

#遍历目录下文件
def iter_file(p):
    for f in p.rglob('*.*'):
        #文件大小
        s = Path(f).stat().st_size
        #mtime时间戳
        m = Path(f).stat().st_mtime
        #向文文件中写入
        w = Path(f).write_text("这是一条测试信息")
        r = Path(f).read_text()
        print ("文件名:{}, 文件大小:{}, 文件mtime:{}, 文件信息:{}".format(f,s,m,r))

#修改并查询文件权限
def chmod_file(p, num):
    for f in p.rglob('*.*'):
        #修改文件权限
        tmp = Path(f).chmod(int(num))
        c = Path(f).stat().st_mode
        print ("当前文件权限：{}".format(c))

#删除目录
def del_dir(p):
    shutil.rmtree(str(p))
    print ("{} 目录已被删除".format(str(p)))

#创建新目录,新文件
def create_dir(p, dirname, newfile):
    d = os.listdir(p)
    new_path = str(p) + '/' +d[0] + '/' + dirname 
    Path(new_path).mkdir(parents=True, exist_ok=True)
    file_path = "{0}/{1}".format(new_path, newfile)
    os.popen("touch {0}".format(file_path))
    #修改文件名为 test.txt
    dst_file = "{}/{}".format(new_path, "test.txt")
    os.rename(file_path, dst_file)
    print ("更名后新文件为：{0}".format(dst_file))
    
if __name__ == "__main__":
    path = input("输入要查询的目录：")
    p = Path(path)
    iter_file(p)
    isch = input("是否修改文件权限(y/n)：")
    if isch == "y":    
        print("参考几个权限:0o644=420,0o444=292,0o755=493,0o777=511,0o666=438")
        num = input("指定查询目录级联文件的权限(eg:292 => -r--r--r--):")
        chmod_file(p, num)
    create = input("是否创建目录/新增文件并重命名？(y/n)")
    if create == "y":
        create_dir(p, 'new_dir', 'one.txt')
    delete = input("是否删除空目录(y/n)：")
    if delete == "y":
        del_dir(p)
