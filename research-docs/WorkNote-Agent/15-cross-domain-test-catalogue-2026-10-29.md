# Bộ test Agent WorkNote theo lĩnh vực — 29/10/2026

Phạm vi được người dùng chọn: FE/UX, BE/API, DB, QA, bảo mật, DevOps, dữ liệu/AI, BA/Product, tài liệu/bàn giao và nghiệp vụ thanh toán. Ma trận tách thành 13 nhóm để theo dõi hiệu năng và tích hợp riêng.

Có 80 kịch bản:72 kịch bản gốc giữ nguyên dữ liệu và phân chia 36 development/12 validation/24 holdout, cộng 8 ca challenge mới cho UX design, AI/ML, BA và tài liệu. Tag validation của 8 ca mới thuộc challenge riêng, không được gộp thành bộ validation gốc 20 ca. Một kịch bản có thể thuộc nhiều nhóm; không cộng số từng nhóm thành tổng.

Lượt kiểm thử giữ nguyên promptv12/Editorv3, parser và rubric trong suốt chiến dịch. Bắt đầu với validation, tiếp đến holdout, development và challenge. Mỗi kịch bản được thử đúng một lần; ca lỗi dừng luồng của chính nó, không biến thành pass. Nếu không tạo được câu hỏi thì lượt trả lời phụ thuộc có thể không chạy và được báo thiếu lượt. Dừng chiến dịch khi hết ngân sách hoặc ba lỗi hạ tầng liên tiếp. Không chỉnh prompt theo các ca validation/holdout vừa đọc.

## Ma trận theo lĩnh vực

| Nhóm | Domain ID | Số ca | Phạm vi |
|---|---|---:|---|
| Frontend và trạng thái giao diện | frontend | 8 | timezone-date, locale-plural, organization-selector, human-message |
| Thiết kế UX và accessibility | ux-design | 4 | keyboard-dialog, ux-design-spec |
| Backend và API contract | backend | 10 | workspace-context, webhook-idempotency, contract-schema, task-scope, task-fetch-status |
| Database và migration | database | 6 | migration-replay, file-dedup, import-validation |
| QA và chất lượng bằng chứng | qa | 14 | permission-matrix, attachment-mime, human-message, waiting-feedback, injection-log, multilang-negation, task-fetch-status |
| Bảo mật và phân quyền | security | 12 | refresh-token, signed-url, audit-event, cache-header, permission-matrix, attachment-mime |
| DevOps và vận hành sự cố | devops | 8 | release-claim, feature-flag, rollback-check, trace-cause |
| Dữ liệu và import/export | data | 6 | csv-unicode, import-validation, file-dedup |
| AI/ML và đánh giá model | ai-ml | 2 | ai-model-evaluation |
| BA/Product và quy tắc nghiệp vụ | product-ba | 8 | invoice-rounding, task-scope, product-acceptance-spec, report-save |
| Tài liệu và bàn giao | documentation | 8 | mail-queue, project-archive, reset-progress, runbook-documentation |
| Tích hợp, hàng đợi và thông báo | integration | 10 | retry-upload, notification-duplicate, mail-queue, billing-webhook, webhook-idempotency |
| Hiệu năng và cache | performance | 6 | search-latency, cache-header, reset-progress |

## Test trọng tâm của từng nhóm

| Lĩnh vực | Dữ liệu thiếu hoặc dễ hiểu sai | Hành vi cần kiểm tra |
|---|---|---|
| Frontend | “Đã sửa ngày hạn” nhưng chưa nói lấy timezone từ đâu | Hỏi đúng IMPLEMENTATION; không đổi instant UTC hoặc tự nhận test đã đạt |
| UX design | Bản thiết kế có đủ loading/empty/error và focus/Escape, nhưng chưa có code | Đủ cho task thiết kế; không đòi deploy hay browser test không nằm trong Task |
| BE/API | Nói xử lý webhook trùng nhưng không nêu khóa chống trùng và kết quả replay | Hỏi chi tiết liên quan; không suy idempotency từ việc endpoint trả200 |
| DB | Migration chạy hai lần nhưng chưa có số bản ghi/giá trị trước-sau | Phân biệt kết quả quan sát với kết luận idempotent; giữ lịch sử/canonical và giới hạnTTL |
| QA | “Đã kiểm tra quyền” nhưng chưa nêu actor/vai trò và kết quả từng ca | Hỏi EVIDENCE; “chưa có thông tin mới” vẫn thiếu, không hỏi lặp và không tính tiến bộ |
| Bảo mật | Task DONE hoặc giao diện ẩn nút nhưng chưa có kết quả kiểm tra quyền ở server | Không xem đó là bằng chứng authorization; không dùng yêu cầu Task làm kết quả tác giả |
| DevOps | Note nói đã deploy, câu trả lời nói chưa deploy/mới build local | CONTRADICTORY/contradiction; dừng câu hỏi tự động và chờ đính chính thủ công |
| Dữ liệu | CSV UTF-8 mất dấu trên spreadsheet, chưa sửa/chưa biết nguyên nhân | Có thể đủ cho INCIDENT nếu đã rõ hiện tượng/phạm vi; không tự ghi đã sửa hay chặn editor chỉ vì chưa đạt Task |
| AI/ML | “Model tốt” không có tập dữ liệu, metric hoặc baseline | Hỏi EVIDENCE; số liệu validation tác giả báo không trở thành kiểm chứng độc lập hoặc kết quả production |
| BA/Product và thanh toán | Đặc tả mới viết, chưa có code; hoặc làm tròn hóa đơn chưa rõ quy tắc | Đánh giá đúng deliverable, đối chiếu quy tắc được cung cấp; không tự đặt chính sách nghiệp vụ hay xác nhận stakeholder đã duyệt |
| Tài liệu/bàn giao | Runbook có rollback/điều kiện dừng/người phụ trách nhưng chưa diễn tập | Đủ cho task viết tài liệu; bảo toàn “chưa diễn tập”, không biến thành đã rollback thành công |
| Tích hợp | Hàng đợi/email/notification đã cấu hình nhưng chưa rõ retry hoặc kết quả giao nhận | Hỏi phần thực sự cần cho purpose; không suy đã giao thành công từ việc gửi job |
| Hiệu năng | Chỉ có trung bình hoặc số đo khác môi trường thay cho p95 so baseline | Không kết luận đáp ứng chỉ tiêu; hỏi đúng phép đo/phạm vi được Task yêu cầu |

## Các ca mới có thể dùng trực tiếp

### domain-ux-design-spec-complete

Task: **Thiết kế màn chọn tổ chức**

- Bản thiết kế mô tả trạng thái loading, empty và lỗi.
- Mô tả thứ tự focus và hành vi phím Escape cho dialog.

Note đầu vào:

> Bản thiết kế đã có loading, empty, lỗi; thứ tự focus đi từ ô tìm kiếm đến danh sách và nút xác nhận; Escape đóng dialog. Chưa triển khai code.

Kỳ vọng: ENOUGH_FOR_PURPOSE; câu hỏi=none; loại gap khi cần=EVIDENCE.

Completion means the design specification is complete. Do not require implemented UI or executed browser tests when the Task asks only for design.

### domain-ux-design-spec-incomplete

Task: **Thiết kế màn chọn tổ chức**

- Bản thiết kế mô tả trạng thái loading, empty và lỗi.
- Mô tả thứ tự focus và hành vi phím Escape cho dialog.

Note đầu vào:

> Đã hoàn thành bản thiết kế màn chọn tổ chức.

Kỳ vọng: NEEDS_AUTHOR_INPUT hoặc UNDETERMINED; câu hỏi=required; loại gap khi cần=EVIDENCE.

Completion means the design specification is complete. Do not require implemented UI or executed browser tests when the Task asks only for design.

### domain-ai-model-evaluation-complete

Task: **Đánh giá bộ phân loại mức ưu tiên**

- Đo macro-F1 trên tập validation đóng băng.
- So sánh với baseline trên cùng bộ dữ liệu.

Note đầu vào:

> Đã đo trên tập validation đóng băng eval-01: macro-F1 của model là 0.78, baseline là 0.73 trên cùng tập. Chưa đo production.

Kỳ vọng: ENOUGH_FOR_PURPOSE; câu hỏi=none; loại gap khi cần=EVIDENCE.

Treat supplied metrics as synthetic author reports, not independent verification or production performance. Ask for evaluation context/comparison when absent.

### domain-ai-model-evaluation-incomplete

Task: **Đánh giá bộ phân loại mức ưu tiên**

- Đo macro-F1 trên tập validation đóng băng.
- So sánh với baseline trên cùng bộ dữ liệu.

Note đầu vào:

> Model hiện cho kết quả tốt.

Kỳ vọng: NEEDS_AUTHOR_INPUT hoặc UNDETERMINED; câu hỏi=required; loại gap khi cần=EVIDENCE.

Treat supplied metrics as synthetic author reports, not independent verification or production performance. Ask for evaluation context/comparison when absent.

### domain-product-acceptance-spec-complete

Task: **Viết tiêu chí mời thành viên**

- Đặc tả chỉ cho phép quản lý gửi lời mời thành viên.
- Nêu phản hồi khi email đã có lời mời đang chờ.

Note đầu vào:

> Đặc tả đã ghi chỉ quản lý được gửi lời mời; email có lời mời đang chờ thì hiển thị thông báo đã mời và không tạo lời mời trùng. Chưa triển khai API.

Kỳ vọng: ENOUGH_FOR_PURPOSE; câu hỏi=none; loại gap khi cần=EVIDENCE.

Assess specification content; do not require deployed APIs, stakeholder approval or a new policy absent from the Task.

### domain-product-acceptance-spec-incomplete

Task: **Viết tiêu chí mời thành viên**

- Đặc tả chỉ cho phép quản lý gửi lời mời thành viên.
- Nêu phản hồi khi email đã có lời mời đang chờ.

Note đầu vào:

> Đã chốt đặc tả mời thành viên.

Kỳ vọng: NEEDS_AUTHOR_INPUT hoặc UNDETERMINED; câu hỏi=required; loại gap khi cần=EVIDENCE.

Assess specification content; do not require deployed APIs, stakeholder approval or a new policy absent from the Task.

### domain-runbook-documentation-complete

Task: **Viết runbook rollback**

- Runbook có thao tác rollback và tiêu chí dừng.
- Nêu rõ nhóm chịu trách nhiệm vận hành.

Note đầu vào:

> Runbook hướng dẫn hoàn nguyên về bản build trước; dừng khi healthcheck lỗi; nhóm vận hành chịu trách nhiệm. Chưa diễn tập rollback.

Kỳ vọng: ENOUGH_FOR_PURPOSE; câu hỏi=none; loại gap khi cần=EVIDENCE.

Writing a runbook is distinct from executing rollback. Preserve the explicit untested limitation without inventing an execution requirement.

### domain-runbook-documentation-incomplete

Task: **Viết runbook rollback**

- Runbook có thao tác rollback và tiêu chí dừng.
- Nêu rõ nhóm chịu trách nhiệm vận hành.

Note đầu vào:

> Đã viết xong runbook rollback.

Kỳ vọng: NEEDS_AUTHOR_INPUT hoặc UNDETERMINED; câu hỏi=required; loại gap khi cần=EVIDENCE.

Writing a runbook is distinct from executing rollback. Preserve the explicit untested limitation without inventing an execution requirement.

## Guardrails phải kiểm tra chéo mọi lĩnh vực

- Mọi claim/tiêu chí phải tham chiếu đúng nguồn, trích đúng đoạn và giữ phủ định; URL chưa đọc, Task DONE, Save/Apply hoặc im lặng không chứng minh đúng.
- Phân biệt thiếu yêu cầu Task với context chưa tải được/API lỗi; lỗi kỹ thuật không được chấm như câu trả lời tác giả.
- PROGRESS, INCIDENT, QA, DECISION, HANDOVER và COMPLETION có mục tiêu đủ thông tin khác nhau. Hoàn thành một bản đặc tả không đồng nghĩa hoàn thành code.
- Không hỏi lại answered/unknown/skipped; giới hạn 3 câu hỏi, dừng sau 2 lượt không tiến bộ; correction gắn đúng claim/gap và không sửa authority Task.
- Reset mục đích/task không mang câu trả lời ngoài ngữ cảnh; thay đổi Task/note tạo stale; kiểm tra CAS, lease và idempotency.
- Chỉ người dùng Apply/Save, không tự gửi tin/Jira. Save vẫn hoạt động khi AI lỗi. Save, Apply, author validation và semantic reviewer là tín hiệu riêng.
- Draft/chat/correction/feedback hết hạn tối đa 24h, tách người dùng/tổ chức, không học chéo note hoặc gửi dữ liệu thật trong đánh giá này.

## Chạy riêng một lĩnh vực

Chạy trong DATN-BE. Dry-run chỉ kiểm tra lựa chọn/phạm vi, không gọi model và không chứng minh chất lượng hiểu task:

```powershell
node -r ts-node/register scripts/work-note-agent/assessment-domain-run.ts --domain ux-design --dry-run
node -r ts-node/register scripts/work-note-agent/assessment-domain-run.ts --domain ai-ml --dry-run
```

Có thể thay domain bằng bất kỳ ID ở bảng trên. Khi chủ động chạy live, dùng model và phase ID mới được cấp ngân sách; ledger cũ không được xóa/reset. Ví dụ lệnh, chưa được tự chạy thêm bởi tài liệu này:

```powershell
node -r ts-node/register scripts/work-note-agent/assessment-domain-run.ts --domain ux-design --live --model mistralai/ministral-14b --phase-id ux-evaluation-unique-id --max-attempts 29 --max-total-tokens 500000
```

Mỗi report riêng giữ nguyên policy dừng khi lỗi critical. Chiến dịch toàn bộ có wrapper để bắt đầu phiên độc lập cho ca tiếp theo và ghi lỗi cũ, không bỏ qua guardrail của luồng đang lỗi.

## Danh sách đầy đủ 80 kịch bản

| ID | Nhóm | Nguồn/split | Purpose | Lượt |
|---|---|---|---|---:|
| assessment-audit-event-a | security | original-v4-with-development-errata1/validation | PROGRESS | 1 |
| assessment-audit-event-b | security | original-v4-with-development-errata1/validation | PROGRESS | 1 |
| assessment-human-message-a | frontend, qa | original-v4-with-development-errata1/validation | PROGRESS | 1 |
| assessment-human-message-b | frontend, qa | original-v4-with-development-errata1/validation | QA | 1 |
| assessment-contract-schema-a | backend | original-v4-with-development-errata1/validation | COMPLETION | 1 |
| assessment-contract-schema-b | backend | original-v4-with-development-errata1/validation | COMPLETION | 2 |
| assessment-locale-plural-a | frontend | original-v4-with-development-errata1/validation | PROGRESS | 1 |
| assessment-locale-plural-b | frontend | original-v4-with-development-errata1/validation | COMPLETION | 2 |
| assessment-feature-flag-a | devops | original-v4-with-development-errata1/validation | COMPLETION | 1 |
| assessment-feature-flag-b | devops | original-v4-with-development-errata1/validation | COMPLETION | 2 |
| assessment-task-scope-a | backend, product-ba | original-v4-with-development-errata1/validation | PROGRESS | 1 |
| assessment-task-scope-b | backend, product-ba | original-v4-with-development-errata1/validation | COMPLETION | 3 |
| assessment-cache-header-a | security, performance | original-v4-with-development-errata1/holdout | COMPLETION | 1 |
| assessment-cache-header-b | security, performance | original-v4-with-development-errata1/holdout | PROGRESS | 1 |
| assessment-keyboard-dialog-a | ux-design | original-v4-with-development-errata1/holdout | COMPLETION | 1 |
| assessment-keyboard-dialog-b | ux-design | original-v4-with-development-errata1/holdout | QA | 1 |
| assessment-signed-url-a | security | original-v4-with-development-errata1/holdout | PROGRESS | 1 |
| assessment-signed-url-b | security | original-v4-with-development-errata1/holdout | INCIDENT | 1 |
| assessment-trace-cause-a | devops | original-v4-with-development-errata1/holdout | INCIDENT | 1 |
| assessment-trace-cause-b | devops | original-v4-with-development-errata1/holdout | INCIDENT | 1 |
| assessment-report-save-a | product-ba | original-v4-with-development-errata1/holdout | COMPLETION | 1 |
| assessment-report-save-b | product-ba | original-v4-with-development-errata1/holdout | COMPLETION | 2 |
| assessment-rollback-check-a | devops | original-v4-with-development-errata1/holdout | PROGRESS | 1 |
| assessment-rollback-check-b | devops | original-v4-with-development-errata1/holdout | COMPLETION | 2 |
| assessment-billing-webhook-a | integration | original-v4-with-development-errata1/holdout | PROGRESS | 1 |
| assessment-billing-webhook-b | integration | original-v4-with-development-errata1/holdout | COMPLETION | 2 |
| assessment-file-dedup-a | database, data | original-v4-with-development-errata1/holdout | COMPLETION | 1 |
| assessment-file-dedup-b | database, data | original-v4-with-development-errata1/holdout | COMPLETION | 2 |
| assessment-organization-selector-a | frontend | original-v4-with-development-errata1/holdout | COMPLETION | 1 |
| assessment-organization-selector-b | frontend | original-v4-with-development-errata1/holdout | COMPLETION | 2 |
| assessment-migration-replay-a | database | original-v4-with-development-errata1/holdout | COMPLETION | 1 |
| assessment-migration-replay-b | database | original-v4-with-development-errata1/holdout | COMPLETION | 3 |
| assessment-waiting-feedback-a | qa | original-v4-with-development-errata1/holdout | PROGRESS | 1 |
| assessment-waiting-feedback-b | qa | original-v4-with-development-errata1/holdout | COMPLETION | 3 |
| assessment-multilang-negation-a | qa | original-v4-with-development-errata1/holdout | PROGRESS | 1 |
| assessment-multilang-negation-b | qa | original-v4-with-development-errata1/holdout | COMPLETION | 3 |
| assessment-workspace-context-a | backend | original-v4-with-development-errata1/development | QA | 1 |
| assessment-workspace-context-b | backend | original-v4-with-development-errata1/development | PROGRESS | 1 |
| assessment-retry-upload-a | integration | original-v4-with-development-errata1/development | PROGRESS | 1 |
| assessment-retry-upload-b | integration | original-v4-with-development-errata1/development | INCIDENT | 1 |
| assessment-timezone-date-a | frontend | original-v4-with-development-errata1/development | COMPLETION | 1 |
| assessment-timezone-date-b | frontend | original-v4-with-development-errata1/development | COMPLETION | 2 |
| assessment-csv-unicode-a | data | original-v4-with-development-errata1/development | INCIDENT | 1 |
| assessment-csv-unicode-b | data | original-v4-with-development-errata1/development | INCIDENT | 2 |
| assessment-release-claim-a | devops | original-v4-with-development-errata1/development | PROGRESS | 1 |
| assessment-release-claim-b | devops | original-v4-with-development-errata1/development | COMPLETION | 2 |
| assessment-permission-matrix-a | qa, security | original-v4-with-development-errata1/development | COMPLETION | 1 |
| assessment-permission-matrix-b | qa, security | original-v4-with-development-errata1/development | COMPLETION | 3 |
| assessment-mail-queue-a | documentation, integration | original-v4-with-development-errata1/development | DECISION | 1 |
| assessment-mail-queue-b | documentation, integration | original-v4-with-development-errata1/development | HANDOVER | 2 |
| assessment-webhook-idempotency-a | backend, integration | original-v4-with-development-errata1/development | COMPLETION | 1 |
| assessment-webhook-idempotency-b | backend, integration | original-v4-with-development-errata1/development | COMPLETION | 2 |
| assessment-refresh-token-a | security | original-v4-with-development-errata1/development | PROGRESS | 1 |
| assessment-refresh-token-b | security | original-v4-with-development-errata1/development | COMPLETION | 2 |
| assessment-invoice-rounding-a | product-ba | original-v4-with-development-errata1/development | DECISION | 1 |
| assessment-invoice-rounding-b | product-ba | original-v4-with-development-errata1/development | COMPLETION | 2 |
| assessment-attachment-mime-a | qa, security | original-v4-with-development-errata1/development | QA | 1 |
| assessment-attachment-mime-b | qa, security | original-v4-with-development-errata1/development | COMPLETION | 3 |
| assessment-search-latency-a | performance | original-v4-with-development-errata1/development | PROGRESS | 1 |
| assessment-search-latency-b | performance | original-v4-with-development-errata1/development | COMPLETION | 2 |
| assessment-notification-duplicate-a | integration | original-v4-with-development-errata1/development | INCIDENT | 1 |
| assessment-notification-duplicate-b | integration | original-v4-with-development-errata1/development | INCIDENT | 1 |
| assessment-project-archive-a | documentation | original-v4-with-development-errata1/development | DECISION | 1 |
| assessment-project-archive-b | documentation | original-v4-with-development-errata1/development | HANDOVER | 1 |
| assessment-import-validation-a | database, data | original-v4-with-development-errata1/development | COMPLETION | 1 |
| assessment-import-validation-b | database, data | original-v4-with-development-errata1/development | COMPLETION | 3 |
| assessment-task-fetch-status-a | backend, qa | original-v4-with-development-errata1/development | QA | 1 |
| assessment-task-fetch-status-b | backend, qa | original-v4-with-development-errata1/development | QA | 1 |
| assessment-injection-log-a | qa | original-v4-with-development-errata1/development | INCIDENT | 1 |
| assessment-injection-log-b | qa | original-v4-with-development-errata1/development | PROGRESS | 1 |
| assessment-reset-progress-a | documentation, performance | original-v4-with-development-errata1/development | PROGRESS | 1 |
| assessment-reset-progress-b | documentation, performance | original-v4-with-development-errata1/development | COMPLETION | 3 |
| domain-ux-design-spec-complete | ux-design | domain-challenge-v1/validation | COMPLETION | 1 |
| domain-ux-design-spec-incomplete | ux-design | domain-challenge-v1/validation | COMPLETION | 1 |
| domain-ai-model-evaluation-complete | ai-ml | domain-challenge-v1/validation | COMPLETION | 1 |
| domain-ai-model-evaluation-incomplete | ai-ml | domain-challenge-v1/validation | COMPLETION | 1 |
| domain-product-acceptance-spec-complete | product-ba | domain-challenge-v1/validation | COMPLETION | 1 |
| domain-product-acceptance-spec-incomplete | product-ba | domain-challenge-v1/validation | COMPLETION | 1 |
| domain-runbook-documentation-complete | documentation | domain-challenge-v1/validation | COMPLETION | 1 |
| domain-runbook-documentation-incomplete | documentation | domain-challenge-v1/validation | COMPLETION | 1 |

## Giới hạn diễn giải

Bộ này bao phủ các tình huống được liệt kê và kiểm tra contract/guardrails liên quan. Không có bộ test hữu hạn nào chứng minh hiểu đúng mọi task hoặc mọi ngành. AUTO/OTHER, ngành ngoài phạm vi đã chọn và các tổ hợp mới cần thêm semantic fixtures trước khi khẳng định coverage. Nhãn kỳ vọng do tác giả test tạo, không phải ground truth độc lập. Kết quả chạy thực tế, ca lỗi và lượt chưa chạy nằm trong báo cáo 16; release gate vẫn chờ review độc lập.

Các nhãn lĩnh vực chỉ dùng để chọn test/báo cáo, không gửi cho model. Campaign live toàn bộ yêu cầu khai báo rõ --max-attempts 176 cho ledger 176; CLI từng domain vẫn cho phép giới hạn thấp hơn theo lần chạy. Không tự động gọi bù khi429; baseline và recovery ở báo cáo 16 được ghi riêng.
