# 23 — Đề xuất đánh giá model khác cho Work Note Agent

Ngày: 2026-11-04, UTC+7. Trạng thái lúc lập: PROPOSED_NOT_AUTHORIZED_NO_INFERENCE. Sau khi xem đề xuất, người dùng đã duyệt: “Duyệt qwen/qwen3.8-max:free: 48 attempts / 650.000 accounted tokens (đề xuất)”. Phase development được phép chạy theo đúng trần và điều kiện pilot trước full; đây không phải semantic sign-off hay release approval.

Người dùng chọn: “Chuẩn bị đánh giá model khác; chốt model và ngân sách trước khi chạy”. Tài liệu này chốt đề xuất để duyệt, chưa cho phép gọi model. [Báo cáo vòng 2](22-release-completion-execution-2026-11-04.md) đã kết thúc ở 64/64 attempts, 868654 accounted tokens; ledger đó giữ nguyên.

## 1. Khuyến nghị cụ thể

Đề xuất đo `qwen/qwen3.8-max:free` qua xKiro, architecture combined, trên cùng prompt v31 và artifact sau sửa guard `0e6093d1442236b7efb091c525e53dd9a3f802fd7017e0bc8fabae31e76069d8`. Giữ nguyên corpus development/nhãn/evaluator/threshold; chỉ thay model trong lượt đo này.

Lý do chọn là giả thuyết cần đo: các lỗi còn lại chủ yếu là hiểu scope và làm theo rubric; Qwen3.8-Max là model tổng quát cấp Max mà nhà phát triển mô tả có năng lực reasoning/understanding cao trong họ Qwen, và đang có bản miễn phí trong catalog xKiro. Điều này chưa chứng minh nó đúng hơn Ministral trên Work Note Agent. Không dùng benchmark vendor thay cho development hoặc release gate. Nguồn: [Qwen chính thức](https://qwen.ai/blog?id=qwen3.8), [hướng dẫn chọn model QwenCloud](https://docs.qwencloud.com/developer-guides/getting-started/text-generation-models).

## 2. Danh mục và điều kiện tài khoản đã xác minh

Đã đọc GET /v1/models công khai: 103 model, lưu snapshot nguyên JSON và hash; không dùng inference để kiểm tra danh mục. Catalog là nguồn cho model ID/tier/pricing qua xKiro, không lấy giá API trực tiếp của hãng làm giá xKiro. [Catalog trực tiếp](https://api.xkiro.com/v1/models), [mô tả List models](https://docs.xkiro.com/api/list-models/).

| Candidate | Tier xKiro / giá USD mỗi 1M input/output tại snapshot | Context / output ceiling của xKiro | Quyết định |
|---|---|---|---|
| qwen/qwen3.8-max:free | free /0/0 | 1000000 /65536 | Đề xuất đánh giá đầu tiên; chưa có Work Note Agent live result |
| mistralai/mistral-large-4-0 | paid /0.68/2.09 | 256000 /65536 | Dự phòng trả phí; cần chốt tiền, quyền truy cập và reasoning policy riêng trước chạy |
| mistralai/mistral-large-2512 | free /0/0 | 256000 /16384 | Không chọn làm hướng release mới: hãng đánh dấu deprecated từ 31/10/2026, dù xKiro vẫn liệt kê |

Thông tin deprecated/replacement lấy từ [Mistral Large3](https://docs.mistral.ai/models/mistral-large-3-25-12); Large4 hiện được hãng ghi Public Preview, nên bản trả phí cũng cần đánh giá vòng đời/support trước release. Context hãng Large4 ghi1M nhưng xKiro snapshot chỉ256k: với route này dùng giới hạn xKiro bảo thủ hơn. [Mistral Large4](https://docs.mistral.ai/models/mistral-large-4-0).

GET /v1/usage cho hai alias, lúc2026-11-04T09:34:20Z: primary còn 0 free tokens; secondary còn 701432/1000000. Cả hai không có paid spend window hoặc wallet dương. Không lưu tên/email/avatar hoặc số dư cụ thể trong evidence; per-key spend limit chưa được endpoint này báo. Chỉ ghi snapshot điều kiện chạy, không cam kết quota vẫn nguyên khi bắt đầu. [Usage API](https://docs.xkiro.com/api/usage/) xác nhận đây là endpoint chỉ đọc, không tốn token/rate allowance, và số liệu là theo account.

Chuẩn bị lần này gồm 1 GET catalog + 2 GET usage; inference attempts=0. Không reset ledger vòng1/vòng 2, không đổi .env, runtime model hoặc registry PASS.

## 3. Ngân sách đề nghị để người dùng chốt

| Hạng mục | Trần đề xuất |
|---|---:|
| Model duy nhất trong phase | qwen/qwen3.8-max:free |
| HTTP inference attempts tổng, kể cả429/fallback/lỗi | 48 |
| Accounted tokens tổng, gồm reservation khi usage không biết | 650000 |
| Editor calls | 0 |
| Giá input/output phải còn bằng0 theo catalog trước live | 0 USD/token |
| Số lượt phân tích tối thiểu nếu hoàn tất full development | 38 |

650k thấp hơn 701432 free tokens đang còn, giữ khoảng 51k headroom. Đây là hard cap có thể làm stage INCOMPLETE nếu model dùng reasoning/output dài hoặc quota bị dùng nơi khác; không bảo đảm chắc chắn đủ 38 turn. Số token của Ministral chỉ giúp ước lượng, tokenizer và hidden reasoning của model khác có thể khác. Cap 48 chừa 10 attempts ngoài 38 logical calls cho failover/lỗi được phép xử lý; không cấp quyền chạy lại ca model fail để chọn kết quả tốt hơn.

Trước inference đầu: đọc lại catalog, xác nhận ID còn free và giá0; đọc lại usage. Nếu tier/giá đổi hoặc quota không phù hợp, dừng để chốt lại. Khóa chính vẫn theo routing đã duyệt; primary429 mới chuyển XKIRO_API_KEY2; mỗi POST đều tính vào cùng phase. Cả hai429 thì checkpoint/dừng; không tự đổi sang model trả phí hay dùng khóa khác.

Phase đề xuất: release-completion-qwen38-dev-20261104. Chưa có ledger phase này; chưa được cấp ngân sách. Phương án chỉ pilot nếu người dùng chọn riêng: tối đa 20 attempts/300000 accounted tokens, cùng model, không tự mở full stage sau đó.

## 4. Thiết kế đo đã chuẩn bị

Giữ combined; prompt task-note-assessment/2026-11-04.v31; corpus dev-v30 hash505cc0510d4087f125d6c6d1ac71dd898bbe307d1788378a1284e2c5c4ac5563; evaluator v3; max_tokens 8192, timeout 85000ms, json_object, temperature 0.1, retries 0, formatting recovery không bật. Runtime/guard sau sửa đã qua check EXIT 0: 2205 unit /176 E2E, build PASS.

Qwen catalog báo reasoning=true nhưng reasoning_efforts=null. Request giữ field reasoning_effort ở trạng thái omitted như policy hiện tại; không tuyên bố reasoning đã tắt hoặc đã đặt low. Provider có thể áp dụng default/ignore temperature khi reasoning; pilot phải đo latency, finish_reason, usage và parser acceptance. Không đổi timeout, token ceiling, prompt hoặc recovery giữa phase để cứu kết quả. Nếu cần đổi policy thì đó là candidate/snapshot khác, phải ghi riêng. [Reasoning xKiro](https://docs.xkiro.com/guides/reasoning/), [Chat Completions](https://docs.xkiro.com/api/chat-completions/).

Pilot 12 scenarios/16 turns đã dry-run:

- Bốn ca semantic còn mở: dev26-l3-qa-action-only-b; dev27-progress-3; dev27-handover-1; dev27-handover-3.
- Bốn ca multi-turn L1/L2: dev26-l1-compound-multianswer-a/b; dev26-l2-reset-purpose-a/b.
- Bốn đối chứng: dev27-decision-2 (thiếu rationale), dev27-decision-3 (vi phạm), dev27-incident-2 (mơ hồ), dev27-completion-1 (đủ bằng chứng câu ghép).

Chỉ pilot đủ 16 turns, mọi scenario/runtime grade PASS, critical0, reference validity1.0 và không có lỗi model/transport mới chạy phần full. Nếu pilot FAIL thì lưu báo cáo và dừng, không đổi model hoặc prompt trong cùng phase. Nếu pilot PASS: full 34 scenarios /38 turns dùng cùng journal scope/identity; 16 turn đã xong được replay từ cache, chỉ 22 logical calls chưa đo mới tiêu quota. Hash/request phải khớp; pending POST không rõ kết quả vẫn fail closed. Các kiểm chứng journal/replay gồm multi-turn đã có từ vòng trước.

G2 chỉ PASS khi toàn bộ 34 scenarios/38 turns trên cùng candidate đạt, không có regression/critical, các ngưỡng quality tương ứng đạt. CONTRADICTORY development n=3 vẫn là low-sample; không thay thế n>=8 ở validation/holdout release. Không pool PASS của Ministral vào Qwen. Có thể đối chiếu các turn development trùng nhau theo model và phiên bản parser, nhưng baseline v31 cũ chỉ là probe; không gọi đó là full-suite A/B.

## 5. Bằng chứng và giới hạn ủy quyền

Gốc: DATN-BE/.worknote-agent-evals/release-completion-20261104/.

- xkiro-model-catalog-20261104.json, SHA256=2691d33ca51ebb0d9486275476b1adf8fe4e80969d3424eef352ee24b1937076.
- model-evaluation-capacity-sanitized.json: hai usage metadata đã lọc dữ liệu nhận dạng.
- model-candidate-qwen38-proposal.json: model/caps, case IDs, exact CLI args và hai kết quả dry-run; status PROPOSED_NOT_AUTHORIZED_NO_INFERENCE.
- prepare-model-candidate.cjs chỉ cho dry-run; live bị chặn vì chưa có quyết định model/ngân sách.

Dry-run pilot16/full38 là tính ceiling offline, không xác nhận route đang phục vụ đúng model hoặc chất lượng inference. Metadata field model của xKiro luôn phản ánh model được request theo tài liệu gateway; không coi nó là chứng thực độc lập weights/upstream route.

Đề xuất này chưa cấp quyền dùng model trả phí, nạp tiền, đổi cấu hình production, chạy editor/history/rewrite hoặc validation/holdout. Nếu Qwen qua G2, các gate G3–G7 và ngân sách/định danh model cho release vẫn phải được chốt theo [kế hoạch](21-release-completion-plan-2026-11-04.md).

## 6. Kết quả thực hiện sau chấp thuận

Phase Qwen đã được cấp theo đúng48 attempts/650000 accounted tokens. Lượt đầu bị503/429; người dùng sau đó yêu cầu tối ưu checkpoint và thêm key3. Đã tiếp tục đúng1 POST với key3 theo evidence hai khóa trước429, vẫn nhận429 dù usage báo còn quota. Tổng5/48 attempts,0 model outputs, chất lượng Qwen chưa được xác lập; không chạy full khi pilot chưa hoàn tất. Source/harness revision, ledger và tối ưu cache ghi trong [báo cáo24](24-incremental-evaluation-and-qwen-checkpoint-2026-11-04.md). Các câu “chưa cấp phase” ở các phần đề xuất phía trên là trạng thái lúc lập, không phải trạng thái hiện tại.
