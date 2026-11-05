# 25 — Release candidate và tiêu chí 98%

Ngày 2026-11-04. Người dùng yêu cầu production và toàn bộ test đạt trung bình ít nhất 98%; sau đó xác nhận hiện chỉ có local. Phạm vi thực thi hiện tại là hoàn thiện, kiểm định và đóng gói release candidate trên local. Chưa có đích triển khai production; không được ghi nhận local PASS thành deployment hoặc production smoke PASS.

## Tiêu chí chấp nhận

- Từng cohort BE unit, BE E2E, FE và từng workflow AI phải đạt ít nhất 98% số ca kế hoạch. Báo cả pass/executed và pass/planned; skipped, blocked, cache miss và unmeasured không phải PASS.
- Không lấy hàng nghìn unit test bù cho tỷ lệ AI thấp. Không làm tròn 97.x% lên 98%. Mọi lỗi critical phải bằng 0; các gate release đã duyệt trong tài liệu 21 vẫn áp dụng.
- Development 34 scenarios cần 34/34 để đạt 98%. Pilot không thay full development; replay offline không thay fresh release validation/holdout. Không gọi lại một lỗi model không đổi để chọn response tốt hơn.
- Registry chỉ được promote khi có đầy đủ manifest/hash, automated gate và semantic review thật. Production luôn chặn mọi surface không có baseline, kể cả flag opt-in bị đặt false. Các chứng cứ human/production còn thiếu phải ghi NOT_ESTABLISHED.

## Checkpoint đã xác minh

| Nhóm | Bằng chứng gần nhất | Kết luận |
|---|---|---|
| BE unit | 2218 PASS, 137 skip trên artifact a5cb143a | 100% executed; 94.18% planned, chưa đủ 98% planned |
| BE E2E | 176 PASS, 4 skip | 100% executed; 97.78% planned, chưa đủ 98% planned |
| FE | 1257 PASS; lint/build PASS | Local engineering PASS; chưa phải production smoke |
| Ministral v31 | Live 13/18; sau sửa guard replay 14/18 | Còn 4 lỗi ngữ nghĩa; không đạt release |
| Qwen pilot | 0 model outputs; 7/48 HTTP attempts, 299453/650000 accounted tokens | BLOCKED_PROVIDER/QUOTA; không có quality verdict |
| DB | Draft PR #131, commit bd02387; 8 CI checks PASS | Chưa review/merge; chưa apply target DB |
| Production | Người dùng xác nhận hiện chỉ local | Chưa có môi trường để deploy/smoke |

Các số BE trên là baseline trước bản sửa production guard. Lượt integration và npm check mới phải ghi riêng artifact và kết quả, không sửa report lịch sử. Kết quả sẽ bổ sung bên dưới khi chạy xong.

## Provider blocker và quyết định model còn thiếu

Một diagnostic có ngân sách trên ca pilot đang bị gián đoạn trả HTTP 503, code `service_unavailable`, nội dung provider cho biết model tạm không khả dụng vì nhu cầu cao. Không có Retry-After hoặc scope/window. Sau đề xuất paid pilot, người dùng chọn tiếp tục bằng key3. Một POST có ngân sách, cưỡng chế chỉ key3, trả429 `rate_limit_exceeded`; dừng ngay, không chuyển sang khóa khác. Không đủ chứng cứ quy mọi 429 cho cùng nguyên nhân; không có response để chấm chất lượng Qwen. Còn 41 attempts và 350547 accounted-token allowance trong phase Qwen đã duyệt; không reset ledger, không tăng cap khi thêm key. Paid pilot bên dưới **chưa được duyệt**.

Nếu cần chuyển sang trả phí, đề xuất **pilot riêng** `anthropic/claude-sonnet-5.5`: tối đa 20 HTTP attempts / 300000 accounted tokens, dừng ngay khi pilot không đạt hoặc provider lỗi. Giá catalog xKiro khi kiểm tra là $2/$10 mỗi triệu input/output tokens; giá danh nghĩa bảo thủ tối đa $3 cho 300k tokens nếu toàn bộ tính theo giá output. Đây chưa phải ủy quyền chi tiền, chưa phải model được chọn để release, và không đảm bảo đạt 98%.

Anthropic công bố Sonnet 5.5 không nhận `temperature`; client hiện tại có gửi trường đó. Vì vậy trước inference trả phí phải hoàn thiện adapter/provider policy tương thích, test không mạng và khóa policy/hash; không được đổi policy âm thầm hoặc so sánh như cùng cấu hình. Reasoning/usage và JSON output qua gateway cần được đo trong pilot. Nếu cần full development/release/features sẽ chốt ngân sách tiếp theo dựa trên usage/latency thật của pilot. Accounted token reservation của local harness không bảo đảm hóa đơn provider; cần giới hạn tiền ở provider và tài khoản có paid balance trước khi gọi.

Nguồn đã kiểm tra: [Anthropic Sonnet 5.5 specifications](https://platform.claude.com/docs/en/models/sonnet-5-5/overview), [xKiro reasoning mapping](https://docs.xkiro.com/guides/reasoning/). Không suy luận chất lượng ứng dụng từ benchmark của nhà cung cấp.

## Việc tiếp tục trong phạm vi đã duyệt

1. Chạy các integration bị skip với MongoDB replica set dùng riêng; authenticated fixture cho ca kiểm quyền/replay, fixture riêng cho audit failpoints; Redis thật nếu local daemon hoạt động.
2. Sửa lỗi được tái hiện, giữ nguyên assertion nghiệp vụ. Dùng lại test/response checkpoint đúng identity, chỉ chạy lại phần thay đổi hoặc thất bại.
3. Một lượt `npm run check` trên source cuối, lưu log/hash và danh sách skips. Đánh giá riêng AI và engineering.
4. Giữ DB/BE/FE tách PR. DB cần teammate review/merge theo AI_WORKFLOW, AI không approve/merge. Chuẩn bị thông báo/Jira, không tự gửi.
5. Chưa deploy production khi chưa có đích hoặc chưa đạt chất lượng; không tự tắt feature để đổi phạm vi release.

## Lỗi tái hiện và sửa trong lượt kiểm định local

| Vấn đề | Nguyên nhân / xử lý | Bằng chứng |
|---|---|---|
| Production registry rỗng vẫn được gọi AI | Guard cũ chỉ warn khi chưa có baseline. Production nay luôn chặn trước provider; staging có flag opt-in, development giữ warn mặc định. Không tự thêm PASS registry. | Guard/precheck tests PASS; matching strict-baseline control PASS |
| Refresh-session integration fail | Fixture thiếu model/document users mà replay invalidation cần tăng mutationFence; expectation lookup thiếu sessionId/userFence mới. Bổ sung dữ liệu và kiểm tra fence thật tăng. | local-iam-fixture-resume: test PASS |
| Platform audit thiếu hai event | Fixture event thiếu scope PLATFORM, bị bộ lọc hiện tại loại đúng. Bổ sung scope trong fixture, giữ projection/redaction assertions. | local-iam-fixture-resume: test PASS |
| Project membership regression fail | Test kỳ vọng một member đã remove trở lại ACTIVE sau khi bổ nhiệm người khác. Sửa kỳ vọng INACTIVE để kiểm chống tái kích hoạt sai. | local-project-membership-final: PASS |
| BFF replay integration fail | Assertions cũ dùng generic403, trái ERR-1/ERR-2 hiện tại: invalid credential/replay401; permission/resource denial404. Giữ nguyên chống giả mạo, scope, handler-unreachable và replay-once; bổ sung kiểm mã lỗi. Không thêm production Task route. | local-bff-auth-final: PASS, qua Next.js production build local |
| User-status E2E fail | Fixture thiếu model Role và ADMIN permission organization.memberships.manage. Bổ sung Role dùng riêng, dọn sau test; kiểm tra last-admin concurrency và shared-account denial giữ nguyên. | local-userstatus-e2e-fixed: 3/3 PASS |
| Harness MongoDB sai điều kiện | Replay/Task cần authenticated replica set; audit cần unauthenticated random-port replica set; failpoint cần enableTestCommands. Tách hai fixture đúng điều kiện, không trỏ database người dùng. | O10 transient/lost-commit PASS; replay/mTLS PASS |
| AppModule wiring không boot trên DB trắng | Runtime chủ động chặn khi chưa có migration Workspace và deadline_scan_due_cursor. Provision fixture mới bằng các migration 20261022/20261024 có sẵn. Không sửa migration lịch sử hoặc apply DB dùng chung. | local-database-runtime-fixed3: assertions PASS |
| AppModule shutdown giữ Redis socket | BullMQ coi Redis instance do factory đưa vào là shared và không đóng giúp. Thêm BullMqRedisOwner vào 8 infrastructure factories; đóng client ở onApplicationShutdown, sau queue/worker destroy hooks. Không dùng registry global, tránh đóng kết nối app context khác. | 2 lifecycle/isolation tests PASS; local-database-runtime-fixed3 EXIT0, không forceExit, không open-handle warning |
| DB migration mới chưa có CI riêng | Thêm workflow chạy test safety/idempotency trên MongoDB7 disposable. | DB PR131 commit bd02387, 8/8 checks SUCCESS |

Docker Desktop lúc đầu không lên do stale AF_UNIX socket dưới local Docker run và secrets-engine. Đã giữ bản backup socket (không reset Docker/data), khởi động lại thành công. Chỉ tạo/xóa các container Redis có tên worknote-release-test-* thuộc lượt kiểm thử, không xóa container/dữ liệu người dùng. Redis thật được kiểm là7.4.11, image sha256:858f009f9709ce576febc734aa78b8f6d624b82571f9ddb6bda4377c833b3499. Quota/manual Save HTTP suite6/6 PASS. Những lỗi fixture/expectation ở bảng này không được báo thành lỗi business runtime; lỗi Redis ownership là sửa runtime thực sự.

Các lần fail ban đầu vẫn giữ báo cáo riêng. Không dùng assertion PASS ở lượt bị treo tiến trình làm bằng chứng hoàn tất. Chỉ lượt fixed3 đã thoát sạch EXIT0 được dùng cho DB-runtime E2E. Sau sửa runtime Redis phải chạy lại mandatory npm check trên source cuối; kiểm tra tổng v2 trước sửa vẫn giữ làm lịch sử.

Nguồn engineering mới dùng npm check JSON và các integration report theo file + full test name. Mỗi ca chỉ tính một lần; dùng kết quả executed mới nhất, pattern-skipped không xóa chứng cứ đã chạy. Chỉ tổng hợp engineering, không trộn các version/model AI hoặc suy ra chất lượng AI từ unit tests. Files check-unit.json/check-e2e.json được npm check lưu tự động; summary local-98-acceptance.json chứa input hashes và danh sách chưa xác minh.

## Các điều kiện release vẫn chưa đạt

### Kết quả engineering cuối

Mandatory npm run check v3 EXIT0 trên source ổn định:225 suites/2222 unit PASS,137 skipped;19 suites/176 E2E PASS,4 skipped; lint0 errors/6 warnings; TypeScript/build PASS. Các ca skipped sau đó được đối chiếu với integration chạy riêng, theo identity gồm file + full test name + occurrence index nếu trùng tên. Không cộng trùng các lần retry hoặc các ca đã chạy trong npm check.

| Cohort | PASS / planned | Tỷ lệ planned | FAIL / chưa xác minh |
|---|---:|---:|---|
| BE unit + integration, đối chiếu từng ca | 2358/2359 | 99.957609% | 0 FAIL;1 chưa xác minh (native-provider Work Note live test) |
| BE E2E, gồm các fixture MongoDB/Redis riêng | 180/180 | 100% | 0 FAIL;0 chưa xác minh |
| FE, kế thừa lượt check1257 tests trước, mã FE không sửa trong lượt này | 1257/1257 | 100% | Chưa phải production/browser smoke trên đích thật |
| AI semantic development/release | Chưa đạt | Không gộp với engineering | Ministral replay14/18; Qwen0 outputs; fresh release gate chưa chạy |

BE source manifest gồm1088 files, SHA256 `1aaf95ea0fec6cedcd7469329cd7b554848200f16d1e8862a85230db98bbe65a`; đã đối chiếu không đổi sau kiểm tra. Assessment artifact riêng là `63f1c8fc0a85a9a1da27ee651ad65bb1a8a0650422cf7062aa17c8ae786438c6`, không thay cho hash toàn source BE (Redis lifecycle ở ngoài phạm vi assessment artifact). Báo cáo acceptance và receipt: `.worknote-agent-evals/release-completion-20261104/local-98-acceptance.json`, `production-final-evidence.json`, `production-source-freeze.json`. Unit/E2E JSON v3 đã archive riêng để lần check sau không ghi đè chứng cứ.

Docker test containers đã dọn; không còn Node test DB bị treo. Không dùng forceExit để đạt PASS. Các cảnh báo Mongoose duplicate schema index và6 lint warnings vẫn tồn tại; không có lỗi compile/lint/test trong lượt cuối. Không phát sinh thêm model request trong quá trình kiểm tra engineering. Hai ledger development cũ vẫn64/64, round2 SHA256 vẫn `0baa95a83cb36ebe8a476074ba63ddb0e97f59b1a1896845668458ae15c46e9c`; Qwen7/48 đã settled, không còn unknown pending POST. Đã quét evidence bằng giá trị credentials thực, không phát hiện rò khóa.

### Blockers còn mở

1. **Chất lượng assessment:** Ministral v31 live13/18; replay sau guard14/18, không phải bằng chứng fresh release. Bốn ca semantic còn mở: dev26-l3-qa-action-only-b (hỏi thêm nhánh QA không cần cho ghi chú đã có quan sát); dev27-progress-3 (đòi thêm kết quả khi nội dung đã đủ cho Progress); dev27-handover-1 và dev27-handover-3 (đòi thêm chi tiết ngoài thông tin bàn giao cần thiết). Không sửa oracle để biến model failure thành PASS.
2. **Qwen:** key3 vẫn429, diagnostic trước đó503 do quá tải; không có response nên quality NOT_ESTABLISHED. Còn41 attempts/350547 accounted tokens, có thể không đủ mọi stage còn lại; không tự tăng trần và không chuyển paid. Accounted reservations ở lỗi không có usage không phải số token thực tế được xác nhận trên hóa đơn.
3. **Đánh giá độc lập:** chưa có fresh release-v7 validation/holdout đạt gate; G5 history/editor/no-change/rewrite live chưa có đầy đủ chứng cứ release trên model được chọn. Native-provider test không được bật riêng vì sẽ gọi ngoài phase budget. Test HTTP model fixture/Redis thật không chứng minh model hiểu đúng.
4. **Signoff:** chưa có semantic review có reviewer và manifest đối chiếu; validated-configs.json vẫn0 entries. Production guard sẽ từ chối AI theo đúng thiết kế cho tới khi có bằng chứng được duyệt. Không tạo receipt hoặc human PASS giả.
5. **Triển khai:** người dùng xác nhận chỉ local, chưa có production host/URL. DB PR131 vẫn draft, chưa teammate review/merge, chưa có target migration receipt. Local integration không chứng minh dữ liệu/config/health của production.

Mức98% là tỷ lệ quan sát trên kế hoạch test, không phải lời bảo đảm thống kê rằng98% mọi đầu vào production đều đúng. Kết luận hiện tại vẫn **NOT_READY_FOR_RELEASE** dù engineering có thể vượt ngưỡng.

## Bàn giao Git hiện tại

- BE: `feat/DanhDEV-worknote-release-completion-be-api`, base `2129085d00b71417ce84203e60ad60d651468f4e`; thay đổi local chưa commit/push, gồm harness, guard và fixes Work Note.
- DB: `feat/DanhDEV-worknote-release-completion-db`, cùng base; [draft PR #131](https://github.com/DATN-SPRING2027/DATN-BE/pull/131). Migration chỉ kiểm trên disposable local, chưa ảnh hưởng dữ liệu dùng chung. TTL 180 ngày cần kiểm dữ liệu cũ; rollback index không phục hồi dữ liệu đã hết hạn.
- FE: `feat/DanhDEV-worknote-prompt-audit-fe-ui`, base/HEAD `dc381c50fab0438f3632aab86592f2ef0207439f`; thay đổi Work Note local chưa commit/push.
- Docs: `docs/DanhDEV-worknote-release-completion`, báo cáo 21–25 local. Không có merge nào được thực hiện. PR/Jira/thông báo và target-production receipt còn thiếu được ghi minh bạch.

Thông báo DB đã chuẩn bị để người phụ trách gửi: “DB PR131 bổ sung assessment feedback schema/index và migration TTL180 ngày. Đã đạt8/8 CI checks, migration safety/idempotency có suite riêng. Chưa apply dữ liệu dùng chung. Nhờ review dữ liệu cũ/retention và merge DB trước branch ứng dụng phụ thuộc; rollback index không khôi phục dữ liệu đã hết hạn.” Chưa gửi thông báo hoặc cập nhật Jira. Theo AI_WORKFLOW §3, “chờ DB PR được teammate review và merge vào main” trước khi đưa branch ứng dụng phụ thuộc qua bước tích hợp; AI không tự approve/merge.

## Cập nhật ngày 2026-11-05 — Hoàn tất Development v30 & Release Gate v37 (`--corpus=v7`)

Sau khi duyệt và thực thi kế hoạch khắc phục 4 lỗi semantic còn lại trên `mistralai/ministral-14b-2512` (`worknote-assessment.v34` + `worknote-editor.v6`, kèm rate-limit pacing tránh `429` và sửa lỗi Unicode word-boundary tiếng Việt cho blocker rationale):

| Nhóm kiểm định (2026-11-05) | Kết quả | Chi tiết |
|---|---|---|
| **Development (`dev-v30`, 34 scenarios / 37 turns)** | **34/34 scenarios PASS (`100%`), 37/37 turns PASS (`100%`)** | Tất cả 4 ca từng lỗi (`dev26-l3-qa-action-only-b`, `dev27-progress-3`, `dev27-handover-1`, `dev27-handover-3`) đều PASS `100%`. |
| **Release-v7 Validation (`plan-v4-release60-v37-20261105`, 20 scenarios)** | **`automatedGatePassed: true` (`100%`)** | `criticalErrors: 0`, `acceptedSourceReferences: 212/212 = 1.0000`, `adequacy.macroF1: 1.0000`, `questions.precision: 1.0000`, `questions.recall: 1.0000`, `answerUse: 8/8 = 1.0000`, `firstPassFormatValidity: 28/28 = 1.0000`, `editorAcceptance: 10/10 = 1.0000`, `workflowCompletion: 28/28 = 1.0000`. |
| **Release-v7 Holdout (`plan-v4-release60-v37-20261105`, 40 scenarios)** | **`automatedGatePassed: true` (`100%`)** | `criticalErrors: 0`, `acceptedSourceReferences: 435/435 = 1.0000`, `adequacy.macroF1: 1.0000`, `questions.precision: 16/16 = 1.0000`, `questions.recall: 16/16 = 1.0000`, `answerUse: 20/20 = 1.0000`, `firstPassFormatValidity: 60/60 = 1.0000`, `editorAcceptance: 18/18 = 1.0000`, `workflowCompletion: 60/60 = 1.0000`. |
| **Combined Release-60 (`plan-v4-release60-v37-20261105`, 60 scenarios)** | **`automatedGatePassed: true` (`100%`)** | `criticalErrors: 0`, `acceptedSourceReferences: 647/647 = 1.0000`, `adequacy.macroF1: 1.0000`, `questions.precision: 22/22 = 1.0000`, `questions.recall: 22/22 = 1.0000`, `answerUse: 28/28 = 1.0000`, `firstPassFormatValidity: 88/88 = 1.0000`, `editorAcceptance: 28/28 = 1.0000`, `workflowCompletion: 88/88 = 1.0000`. |
| **Freeze Manifest & Cross-OS Hash (`71` frozen files)** | **Verified (`LF-normalized SHA-256`)** | `manifestHash = 42d0d6cb818dc3604cb5f62c45540b0f907469e355017e112c11726872e3385a`; `currentArtifactHash = be46b3189e33575e5b2eef2f82ad542f0cb5f41844d47638bb8883921ad1c023`. |
| **Blinded Human Review & Production Signoff** | **`AWAITING_BLINDED_HUMAN_REVIEW` (`NOT_ESTABLISHED`)** | Blinded worksheet (`plan-v4-release60-v37-20261105.blinded-worksheet.json`) và sealed key đã xuất; `validated-configs.json` giữ `entries: []` cho tới khi reviewer độc lập hoàn tất chấm mù. |

