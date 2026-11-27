# Kết quả kiểm thử toàn bộ WorkNote theo lĩnh vực — 29/10/2026

## Kết luận

Đã thử 80/80 kịch bản. Đạt rubric tự động cho toàn bộ lượt phân tích của 27 kịch bản; nếu tính thêm chốt an toàn Editor khi có gọi thì 25 kịch bản đạt. Đây là số ca đạt bộ chấm được viết trước, không phải độ chính xác hiểu mọi task. Release gate: **NOT_PASSED**; independent semantic review: **NOT_ESTABLISHED**.

Đọc cùng15-cross-domain-test-catalogue-2026-10-29.md để xem test theo lĩnh vực, note mẫu và cách chạy riêng. Domain tags chỉ dùng chọn test/báo cáo, không được gửi làm gợi ý cho model.

**Lưu ý hạ tầng:** năm ca challenge mới nhận429, không có phản hồi model để chấm. Vì vậy0/8 challenge không phải bằng chứng model hiểu sai cả8 ca. Kết quả baseline và lượt kiểm tra bù được giữ riêng.

## Phương pháp và bằng chứng

- Giữ nguyên analysisv12/Editorv3, parser, examples và rubric từ lúc bắt đầu đến lúc kết thúc. Manifest lưu SHA256 từng file. Không chỉnh prompt, tự nới rubric hoặc thử lại ca trượt trong lượt này.
- Thứ tự:12 validation gốc,24 holdout gốc,36 development gốc,8 domain challenge mới. Challenge được báo riêng với validation gốc. Source/answer đều giả lập, không gửi note thật hoặc dữ liệu Atlas.
- Mỗi kịch bản là phiên độc lập. Ca critical trượt vẫn bị đóng trong runner gốc, không Apply/Save; chiến dịch sau đó bắt đầu fixture khác và giữ kết quả trượt. Không bỏ qua giới hạn câu hỏi/không tiến bộ trong cùng phiên.
- Không có lượt trả lời tự động khi model không tạo câu hỏi phù hợp. Lượt không đến được và lỗi context/API được ghi riêng, không coi như đã đánh giá đúng.
- 112 bước phân tích dự kiến; 110 bước có bản ghi, 99 output model hợp lệ, 4 output bị parser từ chối, 1 ca từ chối context đúng kỳ vọng mà không gọi model.
- 26 bản ghi Editor; 24 đề xuất được guard chấp nhận. Điều đó không có nghĩa người dùng đã Apply/Save hoặc xác minh Task.

| Bộ dữ liệu | Số ca đã thử | Đạt mọi lượt phân tích | Đạt cả Editor khi có gọi |
|---|---:|---:|---:|
| validation | 12 | 4 | 3 |
| holdout | 24 | 5 | 5 |
| development | 36 | 18 | 17 |
| domain-challenge | 8 | 0 | 0 |

## Kết quả từng lĩnh vực

Một ca có thể thuộc nhiều lĩnh vực. Không cộng các dòng thành tổng80. Cột đạt phân tích yêu cầu mọi bước của ca khớp rubric raw và runtime; cột có lỗi bao gồm cả Editor. Từng ID lỗi có trong JSON kết quả.

| Lĩnh vực | Đã thử/kế hoạch | Ca đạt phân tích | Ca có lỗi |
|---|---:|---:|---:|
| Frontend và trạng thái giao diện | 8/8 | 5 | 3 |
| Thiết kế UX và accessibility | 4/4 | 0 | 4 |
| Backend và API contract | 10/10 | 6 | 5 |
| Database và migration | 6/6 | 2 | 4 |
| QA và chất lượng bằng chứng | 14/14 | 6 | 8 |
| Bảo mật và phân quyền | 12/12 | 5 | 7 |
| DevOps và vận hành sự cố | 8/8 | 2 | 6 |
| Dữ liệu và import/export | 6/6 | 3 | 4 |
| AI/ML và đánh giá model | 2/2 | 0 | 2 |
| BA/Product và quy tắc nghiệp vụ | 8/8 | 2 | 7 |
| Tài liệu và bàn giao | 8/8 | 1 | 7 |
| Tích hợp, hàng đợi và thông báo | 10/10 | 5 | 5 |
| Hiệu năng và cache | 6/6 | 0 | 6 |

## Các nhóm lỗi

| Lỗi rubric raw | Số bước bị gắn cờ |
|---|---:|
| NOTE_ADEQUACY | 29 |
| UNNECESSARY_QUESTION | 32 |
| QUESTION_GAP_KIND | 27 |
| REQUIRED_QUESTION_MISSING | 2 |
| RESOLVED_OR_DECLINED_GAP_REPEATED | 1 |

| Lỗi rubric sau runtime | Số bước bị gắn cờ |
|---|---:|
| NOTE_ADEQUACY | 35 |
| UNNECESSARY_QUESTION | 31 |
| QUESTION_GAP_KIND | 26 |
| REQUIRED_QUESTION_MISSING | 2 |

| Lỗi protocol/hạ tầng ngoài kỳ vọng | Số bản ghi |
|---|---:|
| INVALID_SOURCE_REFERENCE | 1 |
| UNSUPPORTED_REQUIREMENT | 1 |
| XKIRO_TIMEOUT | 1 |
| SCHEMA_KEYS_TEXT | 2 |
| XKIRO_HTTP_ERROR_429 | 5 |

| Lỗi Editor | Số bản ghi |
|---|---:|
| REWRITE_PROTECTED_CONTENT_CHANGED | 2 |

Các cờ có thể cùng xuất hiện trên một bước. Sai nhãn gap theo rubric, câu hỏi không cần thiết, schema/nguồn không hợp lệ và timeout là các hiện tượng khác nhau; không được gộp làm độ chính xác semantic.

## Ví dụ chẩn đoán đã đối chiếu nguồn

Đây là tự kiểm tra kỹ thuật của người triển khai, không thay thế reviewer độc lập:

1. audit-event-a: tác giả nói chưa triển khai audit nhưng model hỏi phần audit nào đã làm. keyboard-dialog-b: note QA đã nêu chỉ thử nhập tiếng Việt/chưa thử focus trap nhưng model tiếp tục đòi test focus. Hai ví dụ chỉ ra việc purpose và giới hạn tác giả chưa được tuân thủ ổn định.
2. contract-schema-b: tác giả đã báo client cũ đọc items thành công; model hỏi client cũ có đọc pagination mới không. Cần phân biệt tương thích được Task yêu cầu với điều kiện mới do câu hỏi thêm vào.
3. feature-flag-a: raw model ENOUGH và coverage SUPPORTED, parser hạ một criterion thành PARTIAL vì quote/claim có “không khai báo” ở một mệnh đề khác. report-save-a: “chưa kiểm thử file đính kèm” làm hạ kết quả Save/Submit vốn đã được báo đủ. Đây là false downgrade ở guard phủ định theo toàn quote, không thể quy toàn bộ cho prompt.
4. Parser vẫn từ chối câu trích sai/paraphrase thay cho yêu cầu Task. Không sửa source hoặc nới parser để biến output sai thành pass.
5. Editor có các đề xuất bị guard từ chối thay đổi protected content. Guard chặn được output không an toàn để đưa ra, nhưng điều đó không chứng minh chất lượng biên tập đạt.

## Việc cần làm sau baseline

- Ưu tiên sửa phạm vi phủ định và độ hạt claim/citation; giữ chốt chặn bỏ “chưa/không” khi nó thực sự phủ định chính claim, không xét keyword trên toàn đoạn không phân biệt phạm vi.
- Cân chỉnh purpose và tính cần thiết của câu hỏi, đặc biệt PROGRESS/QA với phần chưa làm đã được nói rõ. Không thêm tiêu chí không có trong Task.
- Giảm sai format/trích nguồn bằng contract model rõ hơn hoặc tham chiếu passage/requirement do code kiểm soát, không tự chữa nội dung bằng phỏng đoán.
- Đánh giá Editor riêng: bảo toàn protected fragments, phủ định, dữ kiện và scope deliverable thiết kế/tài liệu.
- Reviewer độc lập cần chấm các worksheet và phân xử rubric; nếu dùng lỗi validation/holdout này để chỉnh prompt thì các ca đã xem phải trở thành regression, cần bộ unseen mới trước quyết định phát hành.

## Kiểm thử code, dữ liệu và ngân sách

BE npm run check: lint/typecheck/build và 1743 unit (137 skipped), 169 e2e (4 skipped) đạt. FE lint/typecheck đạt,974 tests đạt; build webpack đạt trên snapshot c079968 trong E:/DATN/audit-output/worknote-cross-domain-fe-build-20261029 để không ghi đè .next của app đang chạy. DB branch a159b5e:13 migration/policy tests và8 schema tests đạt, MongoDB replica set tạm, không Atlas.

Phase cross-domain-20261029: trần 176 HTTP, thực dùng 135; provider báo 1108536 tokens, 6 attempt không có usage đầy đủ. Bộ đếm tính 1413715/2000000 tokens theo reservation bảo thủ. Chi phí tiền NOT_ESTABLISHED. Không reset ledger cũ hoặc retry ca trong chiến dịch.

Dừng chiến dịch: không dừng sớm. Ca chưa thử: không có.

Evidence: BE/scripts/work-note-agent/assessment-cross-domain-results-2026-10-29.json gồm từng case, lỗi, lĩnh vực, hash manifest/report và usage. Ma trận ở assessment-cross-domain-matrix-2026-10-29.json; corpus gốc/errata giữ nguyên. Raw synthetic reports và worksheet trống nằm trong BE/.worknote-agent-evals, không commit key/.env/raw note.

## Bàn giao

Tiếp tục package chưa merge trên BE feat/DanhDEV-worknote-task-assessment-be-api (main base f41b57b, product baseline d56bfaa) và DOC docs/DanhDEV-worknote-task-assessment (main base d9aa106). Chỉ thêm/đổi harness, bộ test và tài liệu; không thay API công khai, schema, migration, FE hoặc prompt/parser runtime. Hai feature flags vẫn defaultfalse. Không auto Apply/Save, không nhắn Jira/team, không merge. Jira ID do người dùng bổ sung sau.

Không có kết luận bao phủ mọi task hay mọi ngành. AUTO/OTHER chưa có live semantic fixtures trong đợt này;8 challenge mới chỉ kiểm tra complete/incomplete của4 loại deliverable. Browser UI và lưu note thật trên Atlas không được chạy lại trong chiến dịch này. Các tín hiệu Apply, Save, author validation và semantic reviewer vẫn độc lập và không được suy từ việc chạy test.

## Kiểm tra bù hạ tầng và rà soát harness

Sau cooldown, chỉ thăm dò lại domain-ai-model-evaluation-incomplete, vẫn nhận XKIRO_HTTP_ERROR_429 nên dừng ngay. Bốn ca BA/runbook còn lại không bị gọi bù tiếp. Không thử model khác, thay key hoặc reset ledger. Kết quả baseline80 ca phía trên không bị ghi đè.

Lượt chính dùng135 HTTP; lượt bù dùng1. Tổng cùng phase136/176 HTTP,1,108,536 reported tokens,7 attempt không có usage đầy đủ; accounted reservation1,464,563/2,000,000. Còn40 call trong ledger nhưng không tiếp tục gọi khi429 chưa hết. Chi phí tiền NOT_ESTABLISHED. Chi tiết và hash report bù nằm trong assessment-cross-domain-recovery-2026-10-29.json.

Rà soát phát hiện baseline chỉ tính network/timeout/HTTP5xx vào ngưỡng ba lỗi hạ tầng; vì vậy năm HTTP429 cuối chưa kích hoạt ngưỡng đó. Sau khi chiến dịch đóng, đã sửa classifier để401/429 và các4xx cũng được tính; lượt bù dừng ngay khi vẫn lỗi hạ tầng. Đồng thời chặn cấu hình campaign live với trần per-case thấp hơn176 nhưng ledger phase vẫn176, tránh hiểu nhầm trần cấp quyền toàn đợt. Có test đỏ rồi xanh cho hai chốt này. Không đổi prompt, parser, rubric hoặc tính lại điểm baseline.

Bản harness đúng thời điểm frozen được lưu cục bộ tại .worknote-agent-evals/campaign-frozen-baseline-20261029.ts; SHA256 e23bded4a3a08f1c07b9f2017664c34085d331da66b539a65e64ad649d0c938e khớp manifest. Bản review sau đó chỉ thay các chốt ngân sách/lỗi hạ tầng nói trên. Focused assessment suite cuối đạt160 tests.
