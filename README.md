# 跨站求职提醒试验的外溢分析与下一轮抽签

服务站试验演练包含已经执行的一波试验和拟议的第二波。候选及分派使用合成标识。一次到岗以 employer 和 placement_id 的组合为来源键。

## 资料约定

CSV 使用 UTF-8，首行为列名。多值字段以竖线分隔。空单元格表示来源未填。

- circles.csv。各服务圈的候选与运营上限。fixed_recipients 是不能暂停提醒的人，holdout 由研究计划要求预留。
  字段为 `wave`、`circle`、`roster`、`capacity`、`fixed_recipients`、`holdout`。
- links.csv。事前知道的跨圈服务联系及共用招聘岗位。dir=both 表示两向。 W1 的事前接触度以预登记相邻圈中 high 圈数量为例，个人直接鼓励以原始分派为准。
  字段为 `wave`、`left`、`right`、`posting`、`dir`。
- designs.csv。覆盖级别和圈数限制。人数按 fraction 乘事前名册人数向下取整，划保留范围的圈当波级别为 zero。 W1 已冻结每种可行的圈层级别分派机会均等，在给定级别下圈内同一人数的个人组合机会均等。W2 是新计划输入。
  字段为 `wave`、`level`、`fraction`、`min_circles`、`max_circles`、`seed`、`cutoff`。
- assignment.csv。首波实际冻结分派，以决定日前的名册为准。
  字段为 `wave`、`circle`、`level`、`people_assigned`。
- contacts.csv。提醒发送与外站口头转告的现场流水。
  字段为 `wave`、`person`、`serving_circle`、`posting`、`kind`、`at`。
- placements.csv。到岗来源回执。unconfirmed 表示该人当波结果仍缺可核凭据。双站提交同一雇主键可供对账。
  字段为 `wave`、`reporting_circle`、`person`、`employer`、`placement_id`、`posting`、`result`、`at`。
- amendments.csv。候选别名与事后补记的转介联系。found_after 表示相对于处置波次何时获得此信息。
  字段为 `change`、`wave`、`kind`、`left`、`right`、`found_after`、`recorded`。

## 检查演练资料

使用 Python 3.11.2 标准库，无需安装第三方依赖。在项目根目录运行下列命令可检查 CSV 读取、资料关联及样例记录完整性。

```bash
python3 -m unittest discover -s tests -v
```
