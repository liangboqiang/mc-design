# Task Receipts

本目录用于存放所有执行智能体和审计智能体的任务回执。

每个任务必须使用独立目录：

```text
.tasks/receipts/<TASK_ID>/
```

执行类任务必须写：

```text
.tasks/receipts/<TASK_ID>/EXECUTION_RECEIPT.md
```

审计类任务必须写：

```text
.tasks/receipts/<TASK_ID>/AUDIT_RECEIPT.md
```

建议回执结构：

```text
# <TASK_ID> 回执

## 任务边界

## 改动/审计文件清单

## 关键结论

## 测试命令和结果

## 产物路径

## 未完成/阻塞项

## 需要 PM 裁决的问题
```

没有回执的任务，不进入完成状态。
