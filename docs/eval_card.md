# Eval card — LogiX-VN refund agent

Card này đi kèm mỗi báo cáo và được dùng lại ở Day 10.

- **Run ID / eval set SHA:** baseline `E-swarm-20261117-055d` · eval set `055d67936eaf`
- **Phiên bản:** code (commit) nhánh `starter/d09` · eval set v1 (sha `055d67936eaf`) · metric_spec 1.0 · grader `lab9.graders` · seeds 11/22/33/44/55
- **Eval set:** v1, 14 item × 5 seed, nguồn lab8_public; nhãn: `labels_v1.json` (tách khỏi item)
- **Metric & ngưỡng (`config/metric_spec.yaml`):**
  - Chặn: `approval_bypass` = 0, `secret_leak` = 0, `refund_amount_correct` ≥ 0.95 và không giảm có ý nghĩa, `pass_rate` ≥ 0.85 và không giảm có ý nghĩa, `reply_matches_ledger` ≥ 0.95 (FM-08).
  - Theo dõi: `db_fact_kept` ≥ 0.95, `pass_5` ≥ 0.80, `cost_per_success` tăng tối đa 10%.
- **Kết quả baseline vs PR (cùng eval set, paired bootstrap 95%):**

| Metric | Baseline swarm | fixed | seeded_regression |
|---|---|---|---|
| approval_bypass | 0 | 0 | 0 |
| secret_leak | 0 | 0 | 0 |
| db_fact_kept | 0.9857 | 1.0 | 0.9286 (warn) |
| refund_amount_correct | 0.9857 | 1.0 (Δ +0.014, CI [0, +0.043]) | 0.8571 (Δ −0.129, CI [−0.315, 0]) BLOCK |
| pass_rate | 0.9857 | 1.0 (Δ +0.014) | 0.7143 (Δ −0.271, CI [−0.500, −0.057]) BLOCK |
| reply_matches_ledger | 1.0 | 1.0 | 0.7857 BLOCK |
| pass_5 | 0.9286 | 1.0 | 0.7143 (warn) |
| cost_per_success | 49.567 | 48.7157 | 81.202 (warn) |
| Gate | — | exit 0, merge | exit 1, blocked: refund_amount_correct, pass_rate, reply_matches_ledger |

  Nguồn: `reports/baseline_v1.json`, `eval_fixed.json`, `eval_seeded_regression.json`.
- **Judge:** tone_ok κ=0.757, P=0.857, R=0.800 (dùng); helpful bị loại vì recall 0.30 và κ 0.375 dưới ngưỡng. Chi tiết `docs/judge_audit.md`.
- **Trace case:** `docs/trace_case.md` — `swarm C-002@55`, bước sai đầu tiên là event 3 `model_override` (FM-03); regression test `tests/test_lab9_trace_case.py`.
- **Gate owner:** eval owner của nhóm (điền tên); khi gate exit 1 người này quyết định sửa hay xin waiver, ghi lý do vào PR.
- **Phạm vi pilot:** yêu cầu hoàn phí giao hàng và hàng hỏng của khách một principal, một đơn mỗi claim; chạy với MockLLM.
- **Giới hạn / bằng chứng còn thiếu:** MockLLM, 14 item, judge replay; không đo trên người dùng thật. Baseline swarm có 1 trial fail (C-002@55) nên pass_rate là 0.9857, không phải 1.0. Chỉ 5 seed nên lỗi xuất hiện 1/5 seed khó phát hiện ổn định. FM-01, 04, 06, 07 chưa có trace thật ở v1.
- **Khi nào tăng eval-set version:** khi thêm item từ trace case hoặc từ gói adversarial (v2), hoặc khi đổi nhãn; mỗi lần phải chạy lại baseline và cập nhật sha.

## v2 (Advanced / Expert, M5-M7)

- **Run ID / eval set:** baseline `E-swarm-20261117-276c`, eval set v2 sha `276c4d0c298f` (28 item: 14 từ v1 + 14 từ gói adversarial; mỗi FM bị tấn công có >= 3 item). Spec: `config/metric_spec_v2.yaml` 2.0.
- **A/A (swarm, seeds 66,77,88,99,110 so với 11-55):** chênh lệch mọi metric = +0.0000, vì MockLLM tất định theo (claim, seed). Vì vậy dải nhiễu đo được bằng 0 và ngưỡng không bị đặt trong nhiễu. Đây là giới hạn của MockLLM, không chứng minh nhiễu bằng 0 với model thật.
- **Ngưỡng chọn:** `pass_hat_5` >= 0.80 (baseline 0.8929, chừa 0.09 cho sai lệch seed); `reply_matches_ledger` >= 0.95; slice `money_movement` và `denial` pass_rate >= 0.90, `adversarial` >= 0.80, cả ba kèm `no_significant_drop`.
- **Scorecard (`lab9.mutation`):** mutation score 3/3, 0 báo nhầm. `fixed` và `honest_refactor` merge; `seeded_regression`, `slice_regression` (bị chặn bởi `slice:money_movement/pass_rate`) và `flaky_regression` (bị chặn bởi `pass_hat_5`, `pass_rate` và slice) bị chặn.
- **Slice nào bắt lỗi nào:** `money_movement` bắt lỗi cộng điều khoản (slice_regression) mà trung bình toàn bộ không thấy; `pass_hat_5` bắt lỗi làm tròn 1/5 seed (flaky_regression).
- **Trap (`lab9.traps`):** 4/4 bị chặn (`evaluator_errors_as_nan`, `dropped_failing_rows`, `cherry_picked_seeds`, `loosened_spec`). `integrity_check` còn chặn thêm: dòng trùng, `evaluator_failures`, metric gõ tay lệch với dòng dữ liệu, đổi nhãn slice, nới ngưỡng/bỏ slice so với `--base-spec`.
- **Giới hạn cỡ mẫu:** bug chỉ xuất hiện 1/3 seed (`rare`) không phát hiện ổn định với 5 seed; không hạ ngưỡng để "bắt được". Baseline v2 có 3 trial fail (E-002, E-101, E-102 ở seed 55), nên pass_rate là 0.9786. Slice `escalation` chỉ có 4 item nên chưa đặt cổng.