# Tối ưu WorkNote v13 — 29/10/2026

## Kết quả chính

Đã sửa bốn false downgrade đã tái hiện được bằng output lưu sẵn: feature-flag-a, report-save-a, timezone-date-a và domain-ux-design-spec-complete. Replay offline chuyển số ca đạt toàn bộ bước phân tích từ27 sang31, không có ca đang đạt chuyển thành trượt. Đây không phải kết quả model chạy lại với promptv13 hoặc tỷ lệ hiểu đúng mọi task. Chất lượng câu hỏi mới củav13 chưa được đo vì xKiro vẫn429. Gate phát hành vẫn NOT_PASSED, independent semantic reviewer NOT_ESTABLISHED.

## Nguyên nhân và sửa đổi

1. Guard cũ xét từ phủ định trên toàn đoạn nên “chưa test file” phủ định cả kết quả Save/Submit, hoặc “không khai báo cấu hình” ảnh hưởng defaultfalse. Guard mới đối chiếu phạm vi câu/mệnh đề và đối tượng cụ thể với criterion; giữ quote nguyên văn và chỉ veto kết quả model đề nghị, không tạo evidence mới.

2. Guard cũ có thể bỏ lọt quote cắt mất phủ định đứng ngay trước đoạn trích. Bản mới đọc ngữ cảnh nguồn quanh từng vị trí trích, chặn “not tested”/“No evidence” bị cắt thành “tested”. Yêu cầu Task cũng không được trích thành điều ngược lại. Các lần xuất hiện mơ hồ được kiểm tra; quá64 vị trí bị từ chối thay vì quét không giới hạn. Tìm phạm vi dùng binary search để hạn chế chi phí.

3. Phân biệt phủ định chức năng với chưa thực hiện/xác minh. Criterion phủ định như “không thoát focus” không được xem là hoàn thành bằng “chưa test focus”. Không bỏ sót phủ định ở vế kết quả của câu điều kiện. Giữ API A/B riêng. Với Task chỉ viết/thiết kế tài liệu, phần chưa code/triển khai/diễn tập ngoài criterion không tự chặn bản ghi; Task vừa thiết kế vừa triển khai hoặc criterion yêu cầu diễn tập vẫn bị chặn khi chưa làm.

4. Hai output SCHEMA_KEYS_TEXT trong baseline đã chép id/verificationStatus từ previous.correctionTarget. Request mới chỉ truyền targetType, nội dung và nguồn cần hiểu; không truyền hai trường server này trong target. Parser vẫn từ chối key thừa, enum sai, quote sai và requirement paraphrase, không tự chữa nội dung để đạt điểm.

5. Promptv13 tách rõ trạng thái đã báo với thông tin thiếu theo purpose. PROGRESS có thể ghi chưa bắt đầu/đang chờ; QA đánh giá đúng phạm vi đã thử; DECISION không yêu cầu đã triển khai quyết định; HANDOVER cần thông tin vận hành hữu ích thay vì tự đòi xác nhận; INCIDENT không bắt biết nguyên nhân khi chưa biết. COMPLETION chỉ nghiệm thu đúng deliverable Task yêu cầu. Không tự đổi adequacy bằng regex “chưa”.

6. Request có outputContract do code tạo, nêu exact keys, enum và giới hạn; đây là dữ liệu hướng dẫn trong messages, không bật chế độ JSON Schema chưa được xác minh của provider. Có passage nguyên văn ngắn cho criteria/claims/giới hạn, giữ dấu Unicode và điều kiện. Chọn tối đa4 examples theo purpose/lượt trả lời, không theo domain/case ID; metadata test ghi hash template từng request.

7. Hints là phụ trợ, không phải danh sách criteria được duyệt. Tổng hints được giới hạn, passageAidsComplete báo thiếu; nếu hints làm vượt65000 ký tự thì bỏ hints, vẫn giữ nguyên sources, không cắt note/Task. Nếu ngay payload bắt buộc vượt cap thì từ chối trước provider theo contract cũ.

## Kiểm thử và giới hạn bằng chứng

- Kiểm tra cuối: lint/typecheck/build đạt; 1778 unit (137 skipped), 169 e2e (4 skipped), 195 focused assessment tests. Có test đỏ rồi xanh cho metadata correction, request cap/example pack, phủ định bị cắt, đối tượng khác nhau, điều kiện và giới hạn xử lý quote mơ hồ.
- Replay kiểm110 bước đã lưu, giữ nguyên hội thoại gốc, không tạo câu trả lời hoặc hai bước chưa từng đến được. Baseline reconstruction có0 state mismatch, số ca baseline27 khớp báo cáo frozen. Không đổi rubric hoặc ghi đè báo cáo16. Không dùng replay để nhận xét câu hỏi mới củav13.

Các scope veto vẫn là heuristic VI/EN có giới hạn, không phải NLI tổng quát hoặc bảo đảm ALCE semantic entailment. Câu lồng, ngôn ngữ khác, code/log và miền mới vẫn cần reviewer. Source tồn tại không đồng nghĩa claim đúng; AUTHOR_REPORTED không trở thành TOOL_VERIFIED. Những validation/holdout đã xem để tối ưu nay là regression; cần tập unseen mới và chấm độc lập trước phát hành.

## Provider và ngân sách

Chỉ thử1 HTTP cho case development retry-upload-a, xKiro trả429; không gọi Editor và dừng. Dùng lại phần ngân sách còn của ledger cross-domain-20261029, không tạo phase mới hoặc reset. Tổng ledger hiện137/176 HTTP,1108536 reported tokens,8 unknown-usage attempts,1497660/2000000 accounted tokens; còn39 call. Chi phí tiền NOT_ESTABLISHED. Không thử model khác/key khác để vượt giới hạn.

## Files và bàn giao

BE: work-note-assessment.polarity.ts/spec, protocol.ts/spec, context.ts, prompt.ts; audit evaluator/run ghi request template hash; assessment-replay.ts cung cấp replay offline kiểm hash. Evidence tổng hợp ở scripts/work-note-agent/assessment-optimization-v13-2026-10-29.json, raw/snapshot/replay logs giữ ignored cục bộ.

Tiếp tục BE feat/DanhDEV-worknote-task-assessment-be-api (base main f41b57b, trước tối ưu e4d5ed8) và DOC docs/DanhDEV-worknote-task-assessment (base main d9aa106). Source FE/DB không đổi; không lặp lại test FE/DB đã chạy trên cùng commit ở báo cáo16. Không public API/storage schema, migration, Atlas write, auto Apply/Save, team/Jira message, SAG activation hoặc merge. Hai feature flags vẫn defaultfalse. Jira ID do người dùng bổ sung sau.

Bản sửa được commit/push vào draft PR109/67 sau review/checks; không merge. Chưa xác nhận cải thiện tổng quát hoặc đạt gate phát hành; bước còn lại là đánh giá live khi provider nhận request trở lại và đánh giá unseen/reviewer độc lập.

Rà soát sau triển khai cũng đồng bộ few-shot với yêu cầu claim nguyên tử: kết quả và giới hạn được tách thành các claim riêng, vẫn giữ đủ nội dung. Chốt test bảo đảm examples không dạy model gộp cả đoạn. Coverage example SUPPORTED trích các claim kết quả, không dùng giới hạn chưa làm để chứng minh đã hoàn thành.

Metadata evaluator hiện ghi hash đúng pack của scenario được chọn và cả request thất bại. Probe429 đã lưu trước các sửa audit/example cuối nên header cũ của probe vẫn được giữ nguyên; nó không được dùng làm bằng chứng chất lượng pack cuối. Không gọi lại chỉ để thay metadata.

Rà soát cuối bổ sung regression cho “tests are pending”, “testing is still pending”, “pending deployment”: đây là chưa xác minh, không được hỗ trợ kết luận đã kiểm thử/triển khai. “Pending review” vẫn là trạng thái workflow hợp lệ. Test cadence Work Report dùng chung một mốc thời gian để tránh lệch mili giây tạo thêm kỳ; chỉ sửa fixture, không đổi nghiệp vụ cadence.
