# Kiểm thử sau cập nhật key xKiro — 29/10/2026

Key mới đã gọi thành công xKiro. Toàn bộ 29 HTTP trong lượt tiếp tục có usage được provider báo; không ghi key hoặc fingerprint của key. Giữ model `mistralai/ministral-14b`, không fallback hoặc reset ledger. Đã dừng tại giới hạn 29 call bổ sung; phần ngân sách cũ còn lại không phải quyền tự mở một pilot mới.

## Kết quả thực tế

| Prompt | HTTP | Output phân tích hợp lệ | Ca đạt toàn bộ phân tích | Editor được harness chấp nhận |
| --- | ---: | ---: | ---: | ---: |
| v13 | 8 | 4/7 | 1/5 | 1 |
| v14 | 11 | 9/9 | 2/5 | 2 |
| v15 | 2 | 2/2 | 0/2 | 0 |
| v16 | 8 | 7/7 | 1/4 | 1 |

Các mẫu khác nhau: v13/v14 cùng năm case development retry-upload-a, mail-queue-a/b, permission-matrix-b và csv-unicode-b; v15 chỉ hai case Progress/Decision; v16 gồm hai case đó và hai case loop. Không lấy số ca đạt ở các mẫu khác nhau để tính mức tăng chính xác, không gộp các lượt cùng case như quan sát độc lập. Các output đã thấy đều là regression data; chưa có unseen evaluation hoặc người chấm độc lập.

## Sửa và lựa chọn phiên bản

Chọn v14 để giữ trên draft branch. Hash toàn bộ năm file runtime trong manifest v14 đã được đối chiếu khớp source cuối, gồm prompt/protocol/context/polarity/state. v15/v16 được thử nhưng không chọn: ví dụ đối chiếu và system ngắn hơn chưa sửa hai lỗi purpose; v16 xuất hiện thêm câu hỏi không cần thiết ở correction turn. Không âm thầm gọi v14 là v16 hoặc sửa lại log cũ.

v14 thêm kiểu dữ liệu cụ thể và ràng buộc sourceRefs trong outputContract, đưa mục đích hiện tại vào system prompt từ enum tin cậy, bổ sung ví dụ Progress mơ hồ và Decision thiếu lý do, cùng ví dụ Handover nhận “chưa biết”. Không nội suy nội dung note/answer vào system prompt. Parser vẫn từ chối scope object, requirements bị lồng vào scope và gap không có citation; không sửa JSON sai nghĩa để biến thành đạt.

Quan sát v13 có ba lỗi protocol (MISSING_SOURCE_REFERENCE, INVALID_STRING, SCHEMA_KEYS_OBJECTIVE); v14 có 9/9 lượt phân tích được parser nhận trên năm ca. Luồng Handover của v14 đi đủ hai lượt và không hỏi lặp; CSV đi đủ hai lượt, Editor được harness chấp nhận. Permission matrix đi được correction và Editor nhưng vẫn sai loại gap/độ liên quan ở câu hỏi, nên cả ca vẫn trượt. Đây là quan sát trên mẫu nhỏ, không phải bảo đảm hết lỗi schema ở mọi task.

## Gate còn chặn

- retry-upload-a: note PROGRESS đã nêu phần làm và giới hạn nhưng vẫn bị hỏi thêm kết quả kiểm thử.
- mail-queue-a: note DECISION đã nêu lựa chọn/lý do nhưng vẫn bị đòi hướng dẫn vận hành của toàn Task.
- permission-matrix-b: còn sai gap kind/question relevance; v16 còn lặp câu hỏi trên correction.

Gate `NOT_PASSED`, reviewer semantic `NOT_ESTABLISHED`. Chưa đo lại toàn bộ 80 ca, chưa kiểm thử browser/Atlas Save, chưa chứng minh runtime Editor parity. Key hoạt động chỉ giải quyết lỗi truy cập provider; nó không chứng minh agent hiểu đúng Task. Cần sửa cơ chế đánh giá mục đích và xác minh lại gap taxonomy trước khi mở feature, sau đó dùng tập mới và reviewer độc lập.

## Kiểm tra và phạm vi

Final selected source: lint/typecheck/build đạt; 1783 unit (137 skipped), 169 e2e (4 skipped), 200 focused assessment tests. Có 6 lint warnings cũ. Test mới giữ parser nghiêm ngặt với ba shape lỗi đã quan sát, kiểm tra source không vào system message và tách quyền sửa note khỏi xác nhận Task Completion.

Một test mới ban đầu giả định Completion thiếu thông tin không được rewrite. Đã đối chiếu contract/state hiện hành: người dùng vẫn được biên tập thủ công với ambiguity, nhưng adequacy không thành ENOUGH, Save/Apply chưa xảy ra. Sửa đúng giả định test, không đổi state machine hoặc ép runtime để làm xanh test. Log full-check cũ dùng giả định đó bị trượt được giữ cục bộ; kết quả trên thuộc full-check mới trên source v14 cuối.

Ledger cross-domain-20261029 hiện 166/176 HTTP, 1286522 reported tokens, 8 unknown usage, 1675646/2000000 accounted tokens; còn 10 call. Không đổi ceiling, phase ID hoặc ghi đè báo cáo 16/17. Chi phí tiền NOT_ESTABLISHED.

BE tiếp tục feat/DanhDEV-worknote-task-assessment-be-api (main base f41b57b); DOC tiếp tục docs/DanhDEV-worknote-task-assessment (main base d9aa106). Thay đổi chỉ prompt/protocol version và tests, evidence/report; không HTTP/storage schema, FE/DB source, migration, Atlas write, bật shared flags, auto Apply/Save, Jira/team message hoặc merge. Draft PR BE109/DOC67 được cập nhật sau kiểm tra; Jira ID do DanhDEV bổ sung.

Evidence: `scripts/work-note-agent/assessment-key-resume-2026-10-29.json` ghi từng case/turn/version, lỗi, request hash và SHA-256 raw artifact. Raw synthetic responses, manifest và logs giữ ignored cục bộ.
