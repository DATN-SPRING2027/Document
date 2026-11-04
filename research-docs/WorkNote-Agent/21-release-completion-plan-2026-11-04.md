# 21 — Kế hoạch hoàn thiện Work Note Agent đến release

Ngày lập: 2026-11-04 (UTC+7). Trạng thái lúc lập: PROPOSED. Người dùng sau đó đã chấp thuận thực hiện; tiến độ và ngân sách bổ sung được ghi tại [báo cáo thực thi](22-release-completion-execution-2026-11-04.md). Chấp thuận thực hiện không đồng nghĩa các gate đã PASS hoặc đã chấp thuận release.
Phạm vi: TASK_NOTE assessment/editor, history, rewrite PROJECT_DOCUMENT/WORK_REPORT, no-change UI/parser, feedback persistence, CI, triển khai và rollback. Mục tiêu là có đủ bằng chứng để release; kế hoạch không chứng nhận trước kết quả model.

## 1. Điểm xuất phát và phạm vi cho phép

Yêu cầu: “lên plan để hoàn thiện toàn bộ đảm bảo release”. Lượt này chỉ đọc source/bằng chứng và tạo tài liệu kế hoạch; không chạy live, đổi source, đổi Git, ghi registry PASS hoặc triển khai.

- BE HEAD: 2129085d00b71417ce84203e60ad60d651468f4e, branch fix/DanhDEV-worknote-review-fixes-be-api, working tree còn nhiều thay đổi/untracked. HEAD không đại diện các file đang sửa.
- FE HEAD: dc381c50fab0438f3632aab86592f2ef0207439f; branch feat/DanhDEV-worknote-prompt-audit-fe-ui, có thay đổi no-change UI.
- Docs: docs/DanhDEV-worknote-review-fixes. DB schema/index/migration hiện đang chung working tree BE; phải tách gói DB trước delivery.
- Candidate: task-note-assessment/2026-11-03.v27, chưa có live eval. Hash candidate quan sát bằng buildFreezeManifest(v6): dbbb333fc7efb7ae981837bb93bce96721cf1284232bca623eebe92f75d2160a. Đây chỉ là dấu vết snapshot, không phải manifest release mới đã được phê duyệt.
- v26: validation đủ 20/20 nhưng FAIL; holdout 32/40 với 3 false-sufficient, còn 8 ca. Manifest v26 1ca18bec34bf2f11484ef465b179597ea49daaaca9778d13ca19e00ed2e50478 là lịch sử.
- Kiểm tra kỹ thuật gần nhất 2026-11-03: BE check exit 0; 2168 unit pass/137 skip; 176 e2e pass/4 skip; lint 0 lỗi/6 warning. Không dùng số liệu đó thay live quality v27.
- Registry PASS đang rỗng. Migration TTL mới được test MongoDB tạm, chưa áp dụng DB đích. Production migration và runtime readiness chưa được chứng minh.

Tài liệu nguồn: [audit v26](20-v26-release-gate-audit-2026-11-03.md), [PROMPT_AUDIT_PLAN](../../../DATN-BE/src/services/capture/application/work-note-agent/PROMPT_AUDIT_PLAN.md), checkpoint validation/holdout trong DATN-BE/.worknote-agent-evals/plan-v4-release60-v26-20261103.*-rows.json.

## 2. Điều kiện release bắt buộc

Mỗi validation và holdout assessment phải đạt độc lập; báo cáo gộp không được che một stage trượt:

| Tiêu chí | Ngưỡng |
|---|---:|
| Runtime fabrication, polarity inversion, false-sufficient | 0 từng loại |
| Accepted source reference validity | 1.00 |
| Adequacy Macro-F1 | >= 0.90 |
| Question precision và recall | >= 0.90 từng chỉ số |
| Answer usage accuracy | >= 0.95 |
| First-pass output validity theo định nghĩa đã freeze ở G1 | >= 0.98 |
| Editor acceptance trên lượt đủ điều kiện tạo proposal | >= 0.95 |
| Sample size mỗi lớp adequacy, mỗi stage | n >= 8 |
| Hoàn tất scenario/turn bắt buộc | 100%, không provisional |

Phải báo cả output model và runtime; mọi critical raw error được chặn phải có test và adjudication, không được biến mất khỏi báo cáo. Không thay ngưỡng để một candidate qua gate.

Các gate ngoài assessment: workflow/history PASS theo G5; không còn lỗi P0/P1 hoặc P2 ảnh hưởng correctness, privacy, migration, traceability; CI pass; semantic review hoàn tất; registry khớp artifact đã đo; migration DB đích ready; staging smoke pass; rollback được diễn tập; người có thẩm quyền chấp thuận release.

## 3. G0 — Chốt snapshot và chia phạm vi delivery

1. Kiểm kê diff/untracked BE/FE/DB/docs; giữ lại thay đổi có sẵn và ghi hash các file liên quan.
2. Tách DB schema + persistence definition + migration + test vào DB branch/PR riêng; BE/FE/docs thành các gói phụ thuộc rõ ràng, theo AI_WORKFLOW. Khi triển khai mới thực hiện Git workflow; kế hoạch này không tự đổi branch.
3. Đóng gói evidence v26/v25 gồm manifest, checkpoint, ledger, rubric, lỗi và phiên bản evaluator; kiểm tra khả năng lưu giữ artifact, không chỉ giữ hash. Không ghi secret/note người dùng vào gói.
4. Lập bảng mỗi lỗi -> expected/actual -> lớp phát sinh -> test tái hiện -> sửa -> bằng chứng xác minh.

Đầu ra: inventory + danh sách PR/phụ thuộc + snapshot có thể truy xuất. G0 PASS khi không còn file/schema/evidence chưa xác định chủ sở hữu hoặc nguồn phiên bản.

## 4. G1 — Kiểm chứng evaluator và harness trước khi tune model

Đây là công việc ưu tiên đầu tiên. Hiện computeLayerMetrics tính firstPassOk từ errorCode/output của mọi analysis row. SCRIPTED_QUESTION_NOT_PRODUCED có thể bị tính thành lỗi format dù lượt đó không có phản hồi LLM. Các số format cũ vì vậy là độ thành công đầu ra theo pipeline, chưa chứng minh toàn bộ là lỗi JSON.

- Kiểm tra từng lỗi: HTTP/provider; JSON/schema/parser; semantic; runtime guard; harness dependency/skipped turn. Giữ lại lỗi thiếu câu hỏi ở lượt gây lỗi và ghi rõ lỗi dây chuyền ở lượt sau.
- Định nghĩa trước freeze hai số: output validity trên request thực sự gọi LLM và tỷ lệ hoàn tất workflow. Không bỏ lỗi dây chuyền khỏi end-to-end correctness; không gọi nó là lỗi JSON nếu không có raw response.
- Đối chiếu TP/FP/FN question, answer-use và confusion matrix bằng tập kết quả nhỏ có nhãn thủ công; kiểm tra cùng một lỗi không vô tình làm sai mẫu số ở nhiều metric.
- Phân biệt raw response, parsed output, runtime result; tên raw_model_output hiện không được hiểu là dữ liệu chưa qua parser nếu thực tế sử dụng output đã parse.
- Kiểm tra resume: manifest phải khớp, checkpoint ghi nguyên tử trong quá trình chạy, khôi phục sau kill process, đủ số turn từng case, không đánh dấu hoàn tất chỉ vì có một row, không chạy lại các call đã xong để chọn kết quả tốt hơn.
- Thêm hỗ trợ corpus/phase mới vào runner có kiểm tra CLI và test; hiện release runner chỉ nhận v5/v6, chưa có lệnh release v7 được kiểm chứng. Không viết lệnh v7 giả định là đã chạy được.
- Freeze evaluator, grader, harness, rubric, provider policy/recovery, model runtime và artifact source cùng corpus. Manifest 22 file hiện tại chưa bao phủ toàn bộ harness/evaluation có thể đổi kết quả.

Đầu ra: evaluator spec + test/fixture kiểm chứng + báo cáo re-audit v26 có version mới, đặt cạnh bản cũ. Không ghi đè báo cáo v26 gốc, không đổi nhãn để model qua. G1 PASS khi phép đo được tái hiện và mọi thay đổi mẫu số có giải thích trước khi chạy mới.

## 5. G2 — Sửa đủ các nhóm lỗi chức năng

| Nhóm | Công việc | Nghiệm thu trên development |
|---|---|---|
| False-sufficient, mâu thuẫn số liệu | Đối chiếu đơn vị/điều kiện/phủ định; thử cặp hợp lệ và vi phạm; guard chỉ làm điều có thể chứng minh từ nguồn | 0 critical; không biến quyết định hợp lệ thành CONTRADICTORY |
| Note mơ hồ / AUTO purpose | Phân biệt tên hạng mục với phần việc cụ thể; giải quyết purpose trước khi dùng rubric | Thiếu scope thì hỏi scope.completed_part; chọn purpose đúng |
| Hỏi thừa HANDOVER/COMPLETION | Dùng thông tin đã có; không tự đòi command/log/header ngoài rubric | Ca đủ không hỏi thêm |
| Progress bị blocked | Trạng thái blocked có lý do là thông tin tiến độ hợp lệ | Không ép hoàn thành Task hoặc test phần còn lại |
| Multi-turn answer/correct/skip | Dùng answer ledger, giữ sourceId đúng; hỏi phần thực sự còn thiếu, dừng khi skip/unknown | Không bỏ câu hỏi bắt buộc, không lặp câu đã trả lời/từ chối |
| Câu ghép, quote và coverage | Tái hiện việc claim FULL nhưng coverage PARTIAL; giữ điều kiện, phủ định, outcome | Chấp nhận claim hợp lệ; từ chối cắt nguồn làm đảo nghĩa |
| JSON/schema | Xử lý INVALID_STRING, null/empty, gapIndex, sourceId; test theo hợp đồng | First-pass đạt ngưỡng, recovery không che lỗi lần đầu |

PROGRESS không mặc định phải báo kết quả kiểm thử. Hai ca PDF/Gzip trong báo cáo trước cần phân tích theo purpose/scope cụ thể; không coi “thiếu số liệu test” là nguyên nhân tất yếu của mọi PROGRESS mơ hồ. V27 guard chỉ hạ DECISION/COMPLETION khi coverage đã CONTRADICTORY; nó không tự phát hiện model đã gán sai PARTIAL hoặc bỏ qua mâu thuẫn. Không được coi guard đó đã sửa ba false-sufficient v26.

Viết test tái hiện trước thay đổi hành vi; dùng trường hợp development tổng quát và cặp đối chứng. Các ca v26 đã xem chỉ còn giá trị regression/diagnostic; không sao chép nội dung, oracle hay ví dụ holdout vào prompt và rồi gọi lượt đo lại là độc lập. Mỗi thay đổi prompt có version/fingerprint, nêu giả thuyết và đo development riêng. V27 là điểm xuất phát; bump tiếp nếu sửa prompt, không ép giữ số v27.

Đầu ra: unit/integration/replay và báo cáo live development theo nhóm. G2 PASS khi mọi case bắt buộc L1–L5 và nhóm lỗi mới xanh trên cùng candidate, không có critical, không có lỗi regression mới; không gộp các batch của nhiều version thành “10/10”.

## 6. G3 — Corpus mới và live development

- Soạn development mới tối thiểu 24 scenario, gồm các purpose và tối đa 48 analysis turns; có sufficient/insufficient/contradictory, biến thể đơn vị, câu ghép, blocked, answer/correct/unknown/skip/reset và nguồn SELF/related/outdated.
- Sau khi G2 ổn định, soạn release corpus v7 mới 60 scenario với domain/family mới; giữ hình dạng 20 validation + 40 holdout, tối đa 88 analysis turns nếu giữ ceiling hiện tại. Mỗi family thuộc đúng một split.
- Thiết kế phân bố đề xuất: validation 28 turns (8 contradictory, 10 insufficient, 10 sufficient); holdout 60 turns (10 contradictory, 25 insufficient, 25 sufficient). Validator kiểm tra cả phân bố, đa dạng cơ chế và n >= 8 từng lớp; không chỉ đếm tên scenario.
- Người kiểm tra dữ liệu xác nhận expected purpose, adequacy, câu hỏi, rubric trước chạy. Seal holdout sau khi tác giả/validator duyệt; người sửa prompt không xem output holdout trước final freeze. Ghi rõ giới hạn độc lập nếu cùng một người làm nhiều vai trò.
- Kiểm tra rò rỉ giữa dev/validation/holdout theo family, template và semantic situation; đổi tên domain không đủ để biến ca cũ thành chưa thấy.

Đầu ra: corpus được review, hash cố định, split manifest và bản ghi provenance. Corpus được đề xuất ở đây chưa tồn tại; chưa có kết quả chất lượng v7.

## 7. G4 — Freeze và release gate độc lập

1. Chạy lint/typecheck/unit/e2e/build BE và FE phù hợp diff; chạy riêng scripts evaluator và migration tests vì npm check không bao phủ mọi script. Giải thích các test skip, kích hoạt integration cần thiết trên môi trường tạm.
2. Lưu artifact build + source đã review, dependency lock, fingerprints và toàn bộ frozen manifest. Không đổi file frozen sau bước này.
3. Chạy validation v7. Nếu FAIL: dừng trước holdout; sửa trên development, bump version và freeze lại. Nếu dùng validation để tune, ghi rõ đã dùng; đợt xác nhận cuối cần validation mới chưa bị tune nếu tuyên bố cả hai split độc lập.
4. Validation PASS mới chạy toàn bộ holdout một lượt. Chỉ resume transport interruption dưới cùng manifest/model/policy và cùng ledger; thay khóa xác thực không thay model/policy.
5. Nếu holdout FAIL: đánh dấu candidate không đạt. Phân tích để sửa phiên bản sau; không chạy lại chọn lọc rồi gộp để được PASS. Lượt release độc lập kế tiếp cần holdout mới và ngân sách được chốt trước.
6. Sinh quality report: số case/turn dự kiến và thực tế, n/per-class F1, TP/FP/FN, raw/parsed/runtime, critical traces, workflow completion, editor acceptance, latency p50/p95, token/accounted cost, interruption, semantic-review status và verdict.

Ngân sách đề xuất, chưa được tiêu thụ bởi tài liệu này:

| Phase | Trần HTTP attempts | Trần accounted tokens | Ghi chú |
|---|---:|---:|---|
| Development candidate | 64 | 2.000.000 | Tổng cho mọi iteration của phase, không reset ledger |
| Assessment release v7 | 148 | 3.000.000 | Validation 50, holdout 98; 88 analysis + tối đa 60 editor là ceiling lý thuyết, lỗi/retry dùng cùng ngân sách |
| Feature measurements G5 | 128 | 4.000.000 | History + workflow + no-change; chốt split/turn/call trước khi chạy |

Dry-run tính lại số call và token reservation theo corpus thực tế trước khi bắt đầu. Thiếu budget thì dừng với kết quả incomplete; không tăng trần hoặc tạo phase để lách. Phase mới sau candidate FAIL phải ghi lý do và ngân sách riêng trước khi chạy.

API key: dùng key chính; khi 429 dùng XKIRO_API_KEY2 theo ủy quyền của người dùng. Runner hiện đọc XKIRO_API_KEY, nên phải triển khai và test routing khóa ở wrapper/client; không mặc định đã có fallback. Tối đa một lần đổi khóa cho một attempt bị 429, theo Retry-After/phản hồi provider; nếu cả hai 429 thì checkpoint và dừng. Mọi HTTP request, kể cả 429 và call sau đổi khóa, tính vào cùng ledger. Log chỉ alias primary/secondary, requestId, mã lỗi; redact cả hai khóa. Không đổi model để né quota, không thử chuyển khóa đối với 401/403 hay lỗi validation. Không commit .env.

## 8. G5 — Hoàn tất history, workflows, no-change và security

- History: chạy dev/validation/holdout đã kiểm tra leakage; SELF conflict có anchor hiện tại, PARENT/CHILD/LINKED, OUTDATED/SUPERSEDED, permission/budget unavailable. Cấm cross-task leakage và false blocking. Source validity 1.00, critical 0; adequacy/question/answer đạt ngưỡng G4 ở nơi metric áp dụng. Lớp quá ít mẫu phải bổ sung heldout family trước freeze, hoặc ghi provisional và chưa công bố hoàn tất tính năng.
- Rewrite PROJECT_DOCUMENT và WORK_REPORT: đo riêng từng workflow và operation; hỗ trợ đủ 8 operations theo contract. Không pool để che workflow trượt. Boundary/marker validity 1.00, critical/polarity violation 0, clarification precision/recall >= 0.90 trên ca có nhãn phù hợp, proposal acceptance >= 0.95 trên ca expected proposal. Báo n; không lấy 0 mẫu làm PASS.
- No-change: replacement giống hệt theo chuẩn đã chốt được chấp nhận; summary rỗng với nội dung hoặc title thay đổi phải bị từ chối; scope selection, CRLF/NFC, marker restoration đều có cặp đối chứng. False acceptance 0; kiểm tra UI tiếng Việt/Anh và thao tác tạo lại/lưu note.
- Security E2E: masking/redaction, injection, quyền organization/project, cross-scope, model mismatch, hết quota và unavailable. Cấm gửi dữ liệu ngoài quyền hoặc secret vào request/log. Feedback không lưu note text.

Corpus history 18/workflows 32/no-change 12 hiện có là đầu vào kiểm kê, không tự coi là đã đủ coverage độc lập hay đủ n. Đầu ra là feature report từng cohort và transcript/rubric; validator PASS chưa phải live feature PASS.

## 9. G6 — Semantic review, registry, CI và DB readiness

- Sinh blinded pack sau G4/G5; reviewer chấm đúng/sai/mơ hồ, ích lợi câu hỏi và editor fidelity. Đề xuất freeze trước khi chấm: >= 95% transcript được chấp nhận, 0 semantic critical; mọi disagreement được adjudicate. Một reviewer đọc toàn bộ, reviewer thứ hai đọc toàn bộ critical/bất đồng và mẫu còn lại đã chốt trước. Ghi người chấm, candidate/hash và thời điểm; không tự ghi human PASS.
- Gán release approver/runtime owner/DB owner theo người có thẩm quyền thực tế; tên chưa biết giữ UNKNOWN. Thời gian chờ review là dependency, không bị thay bằng đánh giá AI.
- Chỉ ghi validated-config entry cho surface/model/architecture/provider policy đã có bằng chứng PASS tương ứng. PASS combined không làm split hoặc rewrite tự động PASS. Registry entry phải gắn manifest và gateRunId cụ thể.
- Thêm gate CI/deployment kiểm tra artifact/hash/registry trước deploy; test mismatch model/prompt/policy và chế độ không có PASS. Runtime warn-only trước PASS không phải hàng rào ngăn deploy.
- DB PR gồm schema, index, migration idempotent, test và runbook. Migration hiện chỉ loopback/non-production, vì vậy cần đường triển khai DB đích qua cơ chế migration được phép; không đơn giản bỏ guard để chạy production.
- Trước TTL: thống kê metadata recordedAt thiếu/sai/đã quá 180 ngày và đánh giá tác động. Tạo TTL có thể khiến MongoDB xóa record cũ; “chỉ tạo index” không có nghĩa không có data impact. Có backup/retention decision, plan xử lý index conflict, inspect/apply/post-inspect và bằng chứng tên/key/expireAfterSeconds.
- Rollback index không khôi phục được dữ liệu đã hết hạn; ghi rõ recovery từ backup nếu cần. Dùng report/log đã redact làm evidence DB ready.

G6 PASS khi semantic sign-off, registry đúng surface, deployment gate và migration readiness đều có bằng chứng. Tách DB PR trước BE phụ thuộc, không gộp schema/index vào PR ứng dụng.

## 10. G7 — Staging, rollout và bàn giao

1. Deploy đúng artifact đã gate PASS lên staging; xác nhận provenance model/prompt/config và registry khớp, không build lại từ working tree khác.
2. Smoke UI/API: đủ/thiếu/mâu thuẫn, answer/correct/skip/reset, no-change, rewrite document/report, feedback persistence, quota/unavailable. Người dùng luôn còn đường lưu/chỉnh note thủ công.
3. Diễn tập rollback artifact/config đã xác định và tắt agent bằng WORKNOTE_AGENT_ENABLED khi chưa có bản PASS để quay lại. Không fallback sang model/config chưa validate.
4. Rollout hạn chế theo cơ chế triển khai thực tế sau phê duyệt; quan sát tối thiểu 24 giờ hoặc cửa sổ traffic đại diện do runtime owner chốt trước. Đối chiếu error/429/latency/telemetry với SLO đã ghi trước canary. Không lấy ít traffic làm đủ bằng chứng.
5. Critical false-sufficient xác nhận, rò rỉ dữ liệu hoặc config mismatch: dừng rollout/tắt agent, bảo toàn bằng chứng và mở correction. Không tự thay prompt tại production.
6. Bàn giao PR/commit/build digests, đầy đủ report, migration receipt, semantic sign-off, rollback rehearsal và người nhận vận hành. Người có thẩm quyền quyết định merge/deploy; kế hoạch không tự approve/merge.

## 11. Trình tự, thời gian và báo cáo bắt buộc

Thứ tự bắt buộc: G0 -> G1 -> G2/G3 -> G4 -> G5 -> G6 -> G7. Có thể soạn corpus/chuẩn bị DB/CI khi G2 đang sửa, nhưng không chạy holdout trước freeze hoặc promote trước các gate phụ thuộc.

Ước lượng một candidate: 5–7 ngày làm việc sau khi có đủ quota/reviewer/môi trường. Ngày 1 inventory + evaluator; ngày 2–3 sửa lỗi/corpus/development; ngày 4 freeze + validation/holdout + feature measurements; ngày 5 review/DB/staging; ngày 6–7 rollout/quan sát/bàn giao. Đây là ước lượng, không phải lịch release đã cam kết; candidate FAIL cần iteration và fresh holdout mới.

Sau mỗi live batch phải xuất quality report ngay, không chỉ báo “đã chạy xong”: candidate/hash, corpus/split, n, từng metric/threshold, từng ca fail và nguyên nhân đã chứng minh hoặc UNKNOWN, budget, key alias, điều kiện resume, bước kế tiếp. Báo riêng ENGINEERING_PASS, AUTOMATED_QUALITY_PASS, HUMAN_REVIEW_PASS, DB_READY, RELEASE_READY và DEPLOYED.

Người thực hiện có thể chuẩn bị code/test/corpus/report; human reviewer/DB owner/runtime approver nhận phần xác nhận thuộc quyền của họ. Không coi kế hoạch này là bằng chứng họ đã chấp thuận. Release chỉ được đề xuất khi G0–G7 có bằng chứng đầy đủ; nếu thiếu một gate thì ghi rõ BLOCKED/INCOMPLETE thay vì DONE.
