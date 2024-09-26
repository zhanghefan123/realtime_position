#!/bin/bash

# 进入包含 .proto 文件的目录
PROTO_DIR="./"

# 为每个 .proto 文件生成 Python 文件
protoc --proto_path="$PROTO_DIR" --python_out="$PROTO_DIR" "$PROTO_DIR/link/link.proto"
protoc --proto_path="$PROTO_DIR" --python_out="$PROTO_DIR" "$PROTO_DIR/node/node.proto"

echo "Python files generated successfully."
