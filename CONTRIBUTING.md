# Contributing

感谢你参与 Open Admin。

## 提交前检查

提交前请运行以下检查，确保前后端基础质量：

```bash
# frontend
npm run typecheck
npm run test

# backend
ruff check .
pytest
```

如果当前任务还没有对应目录或脚本，请在提交说明中写明原因，并在相关脚手架任务完成后补齐检查。

## 提交建议

- 保持变更聚焦，避免把无关重构和格式化混入同一次提交。
- 提交信息使用清晰的英文动词前缀，例如 `feat:`、`fix:`、`chore:`、`docs:`。
- 涉及配置、接口或数据模型变更时，同步更新文档或示例。
