# Trace case: từ trace tới quyết định sai đầu tiên

```bash
cd src
python -m lab9.trace_case --shape swarm --claim C-002 --seed 55
python -m lab9.trace_case --shape swarm --claim C-002 --seed 11    # đối chứng cùng shape, seed khác
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11    # đối chứng shape fixed
```

| Trường | Nội dung |
|---|---|
| Trial | `swarm C-002@55`, trong baseline `E-swarm-20261117-055d` (trial duy nhất fail, nên pass_rate = 0.9857). |
| Triệu chứng | Grader Lab 8 FAIL: `status resolved != denied`. Ledger ghi 20.000đ, 1 refund; nhãn là 0đ, `denied`. |
| Bước sai đầu tiên | Event 3 `model_override {"delay_days": 5}`: agent ghi đè số ngày trễ của DB bằng số trong ticket ("giao trễ 5 ngày"). |
| Vì sao là bước *đầu tiên* | Event 1 `handoff` và event 2 `investigator` (`lookup_order` O-202, `visible: true`) đúng. Sai bắt đầu khi event 3 thay dữ kiện DB; event 4 `quote` ra 20.000đ "entitled" chỉ là hệ quả. |
| Failure mode | FM-03 ticket_trust (`docs/failure_taxonomy.md`). |
| Đối chứng | `swarm C-002@11`: không có `model_override`, event 3 `quote` = 0đ `no_entitlement`, ledger 0, `denied`. Cùng agent, seed khác, kết quả khác: lỗi không ổn định. |
| Regression test | `tests/test_lab9_trace_case.py::test_ticket_trust_is_caught_on_seeded_regression` (`DbFactKept` và `RefundAmountCorrect` đều False) và `test_ticket_trust_is_absent_on_fixed` (cả hai True). Đã thấy fail trên `seeded_regression` và pass trên `fixed`. |
| Chưa chắc chắn | Trace không chứng minh vì sao seed 55 lại tin ticket còn seed 11 thì không; mới biết đây là hành vi theo seed của shape tham chiếu. Chỉ có 5 seed nên chưa ước lượng được tần suất. |

Case phụ (FM-08): `seeded_regression C-008@11` có reply "35.000đ" nhưng ledger 20.000đ trong khi Lab 8 grader PASS. Bị bắt bởi `ReplyMatchesLedger`, test `test_misreport_is_caught_on_c008`.
