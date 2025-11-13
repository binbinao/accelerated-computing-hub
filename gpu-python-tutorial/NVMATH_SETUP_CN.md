# nvmath-python 环境配置指南

## 问题描述

在使用 `nvmath.device.random` 时遇到以下错误：

```
ImportError: cannot import name 'make_attribute_wrapper' from 'numba.cuda.extending'
```

## 解决方案

### 1. 安装兼容的包版本

nvmath-python 0.6.0 需要特定版本的依赖包：

```bash
# 安装 nvmath-python-dx（包含设备 API）
conda install -n nvidia -c conda-forge -c rapidsai nvmath-python-dx "pynvjitlink>=0.2" cuda-version=12 -y

# 安装兼容的 numba 和 numpy 版本
conda run -n nvidia pip install "numba==0.58.1" "numpy==1.26.4" --force-reinstall --no-deps
```

### 2. 设置 CUDA_HOME 环境变量

nvmath-python 需要访问 CUDA Toolkit 的头文件（如 `curand_kernel.h`）。

**在 Jupyter Notebook 中**，在导入 nvmath 之前添加：

```python
import os
os.environ['CUDA_HOME'] = '/usr/local/cuda-12.4'  # 根据你的 CUDA 安装路径调整
```

**或者在启动 Jupyter 之前设置**：

```bash
export CUDA_HOME=/usr/local/cuda-12.4
jupyter notebook
```

### 3. 重启 Jupyter 内核

安装完成后，务必重启 Jupyter 内核（Kernel → Restart Kernel）。

## 验证安装

运行以下代码验证环境配置：

```python
import os
os.environ['CUDA_HOME'] = '/usr/local/cuda-12.4'

import numpy as np
import numba
import cupy as cp
from numba import config as numba_config

print(f"NumPy 版本: {np.__version__}")  # 应该是 1.26.4
print(f"Numba 版本: {numba.__version__}")  # 应该是 0.58.1
print(f"CuPy 版本: {cp.__version__}")

# 测试 nvmath.linalg.advanced
import nvmath
a = cp.random.rand(10, 30)
b = cp.random.rand(30, 20)
result = nvmath.linalg.advanced.matmul(a, b)
print(f"✓ nvmath.linalg.advanced 工作正常")

# 测试 nvmath.device.random
numba_config.CUDA_ENABLE_PYNVJITLINK = True
from nvmath.device import random
compiled_apis = random.Compile()
print(f"✓ nvmath.device.random 工作正常")
```

## 版本兼容性

| 包 | 推荐版本 | 说明 |
|---|---|---|
| nvmath-python | 0.6.0 | 最新版本 |
| numba | 0.58.1 | 更高版本缺少 `make_attribute_wrapper` |
| numpy | 1.26.4 | numba 0.58.1 需要 numpy < 1.27 |
| cuda-bindings | 12.9.4 | 匹配 CUDA 12.4 |
| CuPy | 13.6.0+ | 任何兼容版本 |

## 常见问题

### Q: 为什么需要降级 numba？

A: nvmath-python 0.6.0 使用了 `numba.cuda.extending.make_attribute_wrapper`，这个函数在 numba 0.59+ 版本中被移除了。

### Q: 为什么需要设置 CUDA_HOME？

A: nvmath.device 模块需要编译 CUDA 内核，需要访问 CUDA Toolkit 的头文件（如 `curand_kernel.h`）。

### Q: 如何找到我的 CUDA 安装路径？

A: 运行以下命令：

```bash
which nvcc
# 输出类似：/usr/local/cuda-12.4/bin/nvcc
# 则 CUDA_HOME 为 /usr/local/cuda-12.4
```

或者：

```bash
find /usr/local/cuda* -name "curand_kernel.h" 2>/dev/null
```

## 参考资源

- [nvmath-python 官方文档](https://docs.nvidia.com/cuda/nvmath-python/)
- [nvmath-python GitHub](https://github.com/NVIDIA/nvmath-python)
- [Numba 文档](https://numba.readthedocs.io/)
