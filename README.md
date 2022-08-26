#### 介绍
用来清理项目中的过期的日志文件，通过yaml配置选项

#### 使用

- 配置文件
```yaml
# 应用列表
application:
  - name: '财务中心'
    path: 'D:\finance\runtime'
  - name: '订单中心'
    path: 'D:\order\runtime'
  - name: '用户中心'
    path: 'D:\user\runtime'
  - name: '商品中心'
    path: 'D:\goods\runtime'
# 删除10天前的文件
deadtime:
   10
# 日志后缀
extension:
  '.log'
# 文件大小
file-size:
  0
```

- 启动
```
python Main.py
```
```
订单中心
┌──────────┬─────────────────────────────────────────────────────────────────┬─────────────────────┐
│  文件大小 │                             文件名                              │      创建时间        │
├──────────┼─────────────────────────────────────────────────────────────────┼─────────────────────┤
│   2KB    │ runtime\logs\20201214\app.log                                │ 2020-12-14 16:19:57 │
│   7KB    │ runtime\logs\20201215\app.log                                │ 2020-12-15 14:54:41 │
│   5KB    │ runtime\logs\20201216\app.log                                │ 2020-12-16 16:12:43 │
│   10KB   │ runtime\logs\20201217\app.log                                │ 2020-12-17 14:50:34 │
│   11KB   │ runtime\logs\20210107\app.log                                │ 2021-01-07 10:06:55 │
│   9KB    │ runtime\logs\20210111\app.log                                │ 2021-01-11 15:31:09 │
│  254KB   │ runtime\logs\error.log                                        │ 2020-12-14 16:19:57 │
└──────────┴─────────────────────────────────────────────────────────────────┴─────────────────────┘
删除:runtime\logs\20201214\app.log
删除:runtime\logs\20201215\app.log
删除:runtime\logs\20201216\app.log
删除:runtime\logs\20201217\app.log
删除:runtime\logs\20210107\app.log
删除:runtime\logs\20210111\app.log
删除:runtime\logs\error.log
进度 ---------------------------------------- 100% 0:00:00
```