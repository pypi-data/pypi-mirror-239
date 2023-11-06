# 项目名称
Windmill Model Python API

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## 简介
Windmill Model Python API 是一个用于操作 Windmill 构件的 Python API。它提供了一组方便的功能，用于构建、测试和管理 Windmill 构件。

## 快速开始
由于不是开源代码，你可以通过以下两种方式获取并安装 Windmill Train Python API：

### 本地构建
1. 执行以下命令来构建项目：
sh windmill-model/sdk/python/build.sh
2. 构建完成后，你可以在 `output/dist/` 目录下找到生成的 `windmill_model-1.0.0-py3-none-any.whl` 文件。
3. 执行以下命令来安装构建好的包：
pip install -r windmill_model-1.0.0-py3-none-any.whl

### 直接安装
你也可以直接安装已构建好的包：
- pip install https://bj.bcebos.com/v1/windmill/common/windmill_python_api/windmill_model-1.0.0-py3-none-any.whl?authorization=bce-auth-v1%2Fde0472630db3405fbab8c469aa03f05e%2F2023-08-24T08%3A54%3A31Z%2F-1%2Fhost%2F7b7991392a236d534f31e250a4615d6b377c933f556e19e80101fb83b861f843

## 如何使用
from windmillmodelv1.client.model_client import ModelClient

model_cli = ModelClient(
    endpoint="http://windmill.baidu-int.com:8340",
    ak="aaa",
    sk="bbb"
)

## 测试


## 贡献
我们欢迎你为 Windmill Model Python API 贡献代码

## 讨论
如果你有任何问题、建议或想参与讨论，欢迎加入我们的讨论群：

百度Hi讨论群：XXXX


