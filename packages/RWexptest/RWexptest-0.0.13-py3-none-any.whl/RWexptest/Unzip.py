import os
import zipfile
import tarfile
import rarfile


def extract_all(archive_path, output_path=None):
    if output_path is None:
        output_path = archive_path

    for root, dirs, files in os.walk(archive_path):
        for file in files:
            # 拼接完整的文件路径
            file_path = os.path.join(root, file)

            # 判断文件类型并解压
            if file_path.lower().endswith('.zip'):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(output_path)
            elif file_path.lower().endswith('.rar'):
                with rarfile.RarFile(file_path, 'r') as rar_ref:
                    rar_ref.extractall(output_path)
            elif file_path.lower().endswith('.tar.gz') or file_path.lower().endswith('.gz'):
                with tarfile.open(file_path, 'r:gz') as tar_ref:
                    tar_ref.extractall(output_path)
            elif file_path.lower().endswith('.tar'):
                with tarfile.open(file_path, 'r:') as tar_ref:
                    tar_ref.extractall(output_path)


# 调用函数
# source_path 是包含压缩文件的目录
# output_path 是解压缩目标目录，如果为None，则在source_path中解压
# extract_all(source_path, output_path=None)


def extract_file(file_path, file_name, output_path=None):
    # 如果output_path为None，解压到压缩文件所在目录
    if output_path is None:
        output_path = os.path.dirname(file_path)

    file_path = file_path + "/" + file_name
    # 检查文件类型并解压
    if file_path.lower().endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(output_path)
    elif file_path.lower().endswith('.rar'):
        with rarfile.RarFile(file_path, 'r') as rar_ref:
            rar_ref.extractall(output_path)
    elif file_path.lower().endswith('.tar.gz') or file_path.lower().endswith('.gz'):
        with tarfile.open(file_path, 'r:gz') as tar_ref:
            tar_ref.extractall(output_path)
    elif file_path.lower().endswith('.tar'):
        with tarfile.open(file_path, 'r:') as tar_ref:
            tar_ref.extractall(output_path)
    else:
        print(f"Unsupported file format: {file_path}")

# 使用示例
# file_path = '/path/to/your/file.zip'  # 替换为你的压缩文件路径
# output_path = '/path/to/output/directory'  # 替换为解压目标目录，或者使用None
# extract_file(file_path, output_path)