import urllib.request, tarfile, os

url = 'https://chroma-onnx-models.s3.amazonaws.com/all-MiniLM-L6-v2/onnx.tar.gz'
dest_dir = '/root/.cache/chroma/onnx_models/all-MiniLM-L6-v2'
dest_file = os.path.join(dest_dir, 'onnx.tar.gz')

os.makedirs(dest_dir, exist_ok=True)

print(f'Downloading model from {url}...')
urllib.request.urlretrieve(url, dest_file)
print(f'Downloaded {os.path.getsize(dest_file)} bytes')

with tarfile.open(dest_file, 'r:gz') as tar:
    tar.extractall(path=dest_dir)
print('Model extracted successfully')
