# 24 — Đánh dấu tiến độ, dùng lại kết quả và checkpoint Qwen

Ngày2026-11-04. Người dùng yêu cầu giảm việc chạy lại gây tốn token và bổ sung XKIRO_API_KEY3. Đã triển khai cache/index và routing ba khóa; không tăng ngân sách đã duyệt.

## 1. Vì sao trước đây bị chạy lại

Journal cũ ràng buộc toàn bộ artifact source. Sửa parser/guard/evaluator làm identity khác, nên phản hồi model đã có không tự được dùng lại. Ràng buộc đó cần giữ cho release freeze, nhưng quá rộng cho development. Các lượt npm test/E2E/build chỉ chạy máy local, không dùng token API model; Codex đọc code/log vẫn dùng ngữ cảnh, vì vậy log dài được lưu file và chỉ đọc phần tổng hợp.

Đã tách raw-response cache cho development khỏi artifact chấm điểm. Cùng model + messages/đầu vào + tham số request + endpoint/timeout/retry policy thì dùng lại raw response; chỉ loại opaque user ID khỏi hash. Đổi bộ chấm/guard: replay offline. Đổi model/prompt/đầu vào/tham số: cache miss, cần lượt live được cấp ngân sách. Giữ cả phản hồi model sai định dạng để không thử lại cùng ca rồi chọn câu trả lời tốt hơn.

## 2. Các mốc lưu bền vững

| Mốc | Ý nghĩa / hành động |
|---|---|
| PASS/FAIL | Kết quả đã chấm, gắn model/prompt/request/artifact và report gốc |
| older artifact / OFFLINE_REPLAY_FIRST | Dùng raw response để chấm lại trước; không mặc định gọi model |
| CACHE_MISS_NO_HTTP | Chưa có response khớp; cache-only không gọi mạng |
| BLOCKED_QUOTA / BLOCKED_PROVIDER | Lỗi429/503, không kết luận model hiểu sai |
| BLOCKED_UNCERTAIN_POST | Chưa biết POST có hoàn tất không; không phát lại mù |
| UNMEASURED | Ca chưa chạy hoặc bị dừng bởi dependency |

`assessment-progress.ts` tạo `.worknote-agent-evals/assessment-progress.json` và `.md`. Đây là index theo ca, không gộp kết quả các version thành pass rate release. Report gốc và ledger không sửa. Cache lưu response đã redact, hash và provenance; không lưu Authorization/key.

Đã bổ sung quy tắc vào DATN-BE/AGENTS.md: xem checkpoint trước live; chạy nhóm test liên quan lúc sửa, chỉ một lượt npm run check trên source ổn định trước bàn giao. Release validation/holdout vẫn độc lập và không dùng development cache.

## 3. Bằng chứng tiết kiệm thực tế

Đã nhập22 HTTP200 responses từ journal v31 được archive, đối chiếu SHA256 journal59456f357658a86def887e98e72f8d958aae190879d8e920d4f03450c1fcb7f3. Sau đó chặn global fetch và replay18 scenarios/22 analysis turns:

- Cache hits22; network invocations0; HTTP attempts0; reported/accounted tokens mới0; không đọc credentials hoặc tạo ledger phase mới.
- Kết quả offline14/18 PASS,4 FAIL; khác live13/18 trước đó vì guard câu ghép đã được sửa. Giữ nguyên live v31-probe.json; không gọi offline14/18 là lượt live mới.
- Các ca model fail vẫn fail, không resample. Đổi model/messages/timeout bị cache miss trong test; cache-only miss không có HTTP fallback.
- Test mới kiểm chứng POST không rõ kết quả bị chặn; budget từ chối trước mạng không bị gắn nhầm là POST không rõ kết quả.

Evidence: DATN-BE/.worknote-agent-evals/release-completion-20261104/v31-incremental-offline-replay-a5cb143a.json (lượt replay đã lưu trên artifact a5cb143a); bản replay đầu v31-incremental-offline-replay.json vẫn được giữ. Đây không phải human review hoặc release PASS.

## 4. Qwen — trạng thái provider, không phải quality verdict

Người dùng đã duyệt qwen/qwen3.8-max:free, tối đa48 attempts/650000 accounted tokens, pilot trước full. Lượt đầu dùng4 attempts: primary429, secondary503, secondary503, secondary429. Không nhận được model response; reported tokens0. Accounted170858 là reservation bảo thủ vì lỗi không có usage, không phải số token thực dùng đã được provider xác nhận.

Sau khi người dùng thêm key3: giữ nguyên ledger/caps; không thử lại hai khóa đã có bằng chứng429 trong phase. GET usage báo key3 còn1000000 free tokens. Ghi freeze revision mới vì user yêu cầu tối ưu harness; model/prompt/corpus và parser/guard semantic giữ nguyên. Phản hồi Qwen trước đó chưa có nên chỉ tiếp tục các ca interrupted/unmeasured, không resample model failure.

Đã gọi đúng1 POST bằng alias tertiary: vẫn429, Retry-After không có. Dừng ngay, không chạy các ca còn lại. Chưa đủ bằng chứng để xác định đây là giới hạn model, route, RPM/IP hay cơ chế khác; free-token allowance còn không đảm bảo một model đang có capacity. Không thử thêm request để truy lỗi khi provider đang chặn.

Checkpoint hiện tại:

| Trường | Giá trị |
|---|---:|
| Attempts đã dùng | 7/48 |
| Accounted tokens | 299453/650000 |
| Reported tokens | 0 |
| Model outputs để chấm | 0 |
| Attempts còn lại | 41 |
| Accounted token allowance còn lại | 350547 |
| Model quality verdict | NOT_ESTABLISHED |
| Full development | Chưa được chạy vì pilot chưa hoàn tất |

Không reset hoặc tăng ledger. Bản freeze/harness revision tại checkpoint 5 attempts: a5cb143a55fdb14ea23b1b2388babfe31fbb28a246917b8038279c962760b499; evaluator v4 chỉ bổ sung phân biệt cache-miss/no-response khỏi parser-format denominator. Các file qwen38-pilot.json (lượt đầu), qwen38-incremental-freeze.json, qwen38-pilot-incremental.json và source snapshot được giữ riêng. Controller từ chối chạy lại một stage đã checkpoint nếu không có bước resume rõ ràng sau external-state change.

Cập nhật sau checkpoint 5 attempts: một diagnostic có ngân sách trả503 `service_unavailable`, provider xác nhận model quá tải; không có model output. Khi người dùng yêu cầu tiếp tục bằng đúng key3, chạy đúng một ca pilot interrupted, ép kiểm tra Authorization chỉ dùng tertiary: trả429 `rate_limit_exceeded`, Retry-After không có, dừng ngay. Tổng hiện tại7 attempts settled /299453 accounted /0 reported tokens. Hai báo cáo thêm: `qwen38-production-blocker-diagnostic.json` và `qwen38-key3-user-resume.json`. Freeze lần resume key3 là35e2dcf1ecfbabe1a15deb4e50218d6e0d1784070c6405e4710c8feac5fe63cd (thêm production registry guard; model/prompt/corpus/provider request không đổi). Source sau đó có sửa lưu JSON kết quả `npm run check`, nên freeze trên là bằng chứng lịch sử, không đại diện mọi sửa đổi mới nhất. Không đổi sang model trả phí; yêu cầu dùng key3 không được diễn giải thành duyệt chi tiền.

## 5. Kiểm tra và sử dụng

Nhóm test cache/routing/journal/evaluator/release-integrity: 5 suites /51 tests PASS; lint scripts/targeted và TypeScript PASS. Tại checkpoint trước production guard, npm run check EXIT 0:224 suites /2218 unit tests PASS (15 suites /137 tests skip),19 suites /176 E2E tests PASS (2 suites /4 tests skip),build PASS;lint0 errors /6 warnings. Đây là lượt local; không tiêu token API model. Kết quả engineering mới nhất sau sửa production guard, fixture và Redis shutdown nằm trong [báo cáo25](25-production-98-acceptance-2026-11-04.md): BE2358/2359 ca unique, E2E180/180; không gộp thành AI release PASS.

Log và xác nhận hash/ledger của checkpoint cũ lưu tại incremental-engineering-final-check.log và incremental-final-evidence.json trong evidence root. Tại checkpoint đó ledger Qwen có5 attempts settled; hiện là7 như bảng cập nhật trên. Ledger vòng2 vẫn đúng SHA256 cũ. Không có model call trong lúc chạy check/cache replay; diagnostic và key3 resume được ghi riêng, tính chung ngân sách Qwen.

Xem bảng tiến độ:

```powershell
node -r ts-node/register/transpile-only scripts/work-note-agent/assessment-progress.ts
```

Ví dụ replay một ca có cache, tuyệt đối không gọi provider:

```powershell
node -r ts-node/register/transpile-only scripts/work-note-agent/assessment-run.ts --cache-only --corpus dev-v30 --batch full --split development --model mistralai/ministral-14b --editor-limit 0 --cases dev27-completion-1
```

Lượt tiếp theo phải đọc index/checkpoint, dùng lại các response khớp, chỉ gọi phần chưa đo khi provider phục hồi và vẫn trong41 attempts/350547 tokens còn lại. Approval hiện tại không cho phép tự đổi model trả phí, thay ngưỡng, chạy holdout hoặc promote registry. [Báo cáo chất lượng trước](22-release-completion-execution-2026-11-04.md), [model/budget đã duyệt](23-alternative-model-evaluation-proposal-2026-11-04.md), [tiêu chí release local 98%](25-production-98-acceptance-2026-11-04.md).
