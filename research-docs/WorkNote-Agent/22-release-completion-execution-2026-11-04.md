# 22 — Thực thi kế hoạch hoàn thiện release (2026-11-04)

Trạng thái chốt vòng2: ENGINEERING_PASS (local configured checks), AUTOMATED_QUALITY_FAIL, RELEASE_NOT_READY. Vòng2 đã hết64/64 attempts. Đây là báo cáo thực hiện có giới hạn ngân sách; không phải chứng nhận release hoặc human approval.
Nguồn chỉ đạo: [kế hoạch đã được người dùng chấp thuận](21-release-completion-plan-2026-11-04.md). Người dùng cũng cho phép XKIRO_API_KEY2 khi gặp 429. Vòng 1 không có 429; vòng 2 đã dùng fallback khóa phụ, chi tiết ở §8.

## 1. Kết quả theo gate

| Gate | Trạng thái thực tế | Bằng chứng / điều còn thiếu |
|---|---|---|
| G0 snapshot/delivery | Snapshot và gói DB riêng đã chuẩn bị; delivery chưa hoàn tất | 61 file đầu vào + 10 artifact lịch sử được lưu kèm hash; branch BE/docs mới; DB worktree riêng. Các thay đổi DB kế thừa vẫn còn ở working tree BE, chưa được chuyển thành chuỗi PR/merge độc lập |
| G1 evaluator/harness | Core fixes đã triển khai và test; còn oracle/policy review | Tách parser acceptance khỏi scripted dependency/transport; workflow completeness; strict class n; editor acceptance; immutable freeze; holdout chỉ sau validation PASS; journal/replay/lock; cần adjudicate QA failure reporting vs task contradiction và ký duyệt nhãn release trước freeze |
| G2 development | FAIL; vòng 2 đã hết trần HTTP | v30: 24/34; v31 probe: 13/18, 0 critical trong probe nhưng còn 5 fail. Sau live sửa guard coverage câu ghép và replay 1 ca PASS; 4 lỗi semantic đã biết còn mở, full candidate mới chưa đo |
| G3 corpus release mới | Chưa freeze | Có 24 development mới và corpus development tổng 34; chưa tạo/chạy holdout v7 khi G2 còn FAIL. Loader/CLI v7 đã chuẩn bị, file corpus v7 chưa tồn tại |
| G4 independent release gate | Chưa chạy | Bị chặn bởi G2; giữ nguyên evidence v26, không chạy lại holdout đã lộ để tuyên bố độc lập |
| G5 live history/workflows/no-change | Chưa chạy theo release plan mới | Corpus cũ còn là đầu vào cần review/leakage check; không coi validator hoặc unit PASS là live quality PASS |
| G6 review/registry/DB/CI | Chuẩn bị một phần | Registry vẫn rỗng, human review NOT_ESTABLISHED; migration test DB tạm PASS; reusable CI gate có test, chưa gắn caller production; DB đích/owner/receipt chưa có |
| G7 staging/rollout | Chưa thực hiện | Chưa có artifact quality PASS, target deployment, phê duyệt runtime hoặc quan sát canary |

## 2. Thay đổi đã thực hiện

### Evaluator và bằng chứng

- Thêm evaluator version. Trường raw_model_output kế thừa thực tế chứa output đã parse, trước state guard; raw response riêng được giữ trong rawSyntheticResponse/journal. Không coi label raw này là semantic grading trên dữ liệu chưa parse.
- First-pass validity đo parser chấp nhận response thật; không gọi SCRIPTED_QUESTION_NOT_PRODUCED hoặc HTTP 429 là lỗi JSON. Semantic parser rejection vẫn làm first-pass accepted output thất bại; metric này không phải chỉ JSON syntax validity.
- Bổ sung workflowCompletion để lỗi dây chuyền, missing/unexpected/duplicate turn không biến mất khỏi kết quả end-to-end.
- Chế độ strictRelease kiểm tra đủ workflow, n >= 8 cho cả ba lớp, editor acceptance >= 0.95 cùng các ngưỡng cũ.
- Mở rộng frozen file set cho scripts evaluator/harness, client, dependency lock và config. Manifest cũ không bị ghi đè; freeze trùng phase bị từ chối.
- Coordinator kiểm tra lại validation theo strictRelease trước holdout. Thêm loader/CLI cho development v27/v28 và release v7; không có corpus v7 thì fail thay vì tự dùng corpus cũ.

### Chống chạy lặp và quản lý khóa

- HTTP journal lưu response tổng hợp ở atomic temp/rename, khóa theo process và kiểm tra request hash; replay không gọi HTTP lại. POST không rõ kết quả giữ pending và chặn retry tự động.
- Thử replay 12 lượt single-turn + 14 lượt gồm multi-turn: không tăng ledger từ 52 attempts, tái hiện cùng failure list. Đây là kiểm chứng recovery của evaluation transport, không phải chạy model mới.
- Routing evaluation-only: chỉ primary 429 mới đổi secondary; không đổi với 401/403/500 hoặc global/shared scope; sau khi secondary cũng 429 trả lỗi và checkpoint. Mọi request đi qua cùng budget. Giá trị khóa được redact, log chỉ alias/status.
- Ledger phase dùng ghi file atomic và thời gian chờ lock ngắn để các shard chia sẻ cùng cap. Source hash/corpus hash/model/policy gắn journal; không dùng response cache làm quality evidence của phiên bản khác.

### Parser/model

- Test tái hiện xác nhận guard không nhận “nghiêm cấm” là phủ định, gây hạ SUPPORTED xuống PARTIAL khi tác giả báo tuân thủ điều cấm. Đã thêm nhận diện cấm/forbid/prohibit, kèm đối chứng giữ PARTIAL cho bằng chứng phủ định trái yêu cầu khẳng định.
- V28 giữ cấu trúc prompt và bổ sung quy tắc scope QA, lịch sử hết hiệu lực, hai phủ định cùng chiều và không hỏi lại nhu cầu đã trả lời.
- V29 thử rút gọn system prompt theo purpose để giảm chồng chéo. Probe cho thấy regression nên đã REJECT và khôi phục prompt/protocol/fingerprint v28 từ snapshot. V29 source và kết quả vẫn được giữ riêng.
- Không tự nâng adequacy lên đủ để làm metric tốt hơn; registry PASS không được thêm entry.

### DB và deployment preparation

- Worktree DB: E:/DATN/worktrees/worknote-release-completion-db; branch feat/DanhDEV-worknote-release-completion-db.
- Migration inspect bổ sung aggregate counts tổng record, recordedAt sai/thiếu, số record đủ tuổi TTL. Apply chặn ngày sai; record cũ yêu cầu --ack-existing-expiry. Runbook nêu tác động xóa của TTL và giới hạn rollback.
- Migration vẫn chỉ non-production loopback. Chưa sửa guard để chạy DB remote; chưa có migration receipt của DB đích.
- Thêm assertion/CLI và reusable workflow kiểm tra artifact, per-surface registry, automated PASS, non-provisional và semantic review receipt. CLI buộc expected surface riêng assessment/editor/rewrite. Không tự tạo receipt PASS; chưa có production caller.

## 3. Báo cáo live chất lượng

Model yêu cầu: mistralai/ministral-14b, combined. Trong 50 response có HTTP journal (v28/v29), provider báo cùng model mistralai/ministral-14b. Các batch không đổi model hoặc provider policy. V27 có 14 call trước khi journal được tích hợp; không suy diễn provider-reported label từ metadata không được lưu.

| Batch | Phạm vi | Kết quả | Ý nghĩa |
|---|---|---|---|
| V27 | 10 L1–L5 / 14 turns | 6/10 scenario không có runtime failure | Development, không release evidence |
| V28 | 34 scenario / 38 turns | 26/34 scenario đạt, 8 còn lỗi | Development theo corpus có errata ghi rõ |
| V29 probe | 12 scenario được chọn trước / 12 turns | 4/12 đạt; có regression | Probe chọn lọc; không so Macro-F1 trực tiếp với toàn bộ V28 |

V27 corpus gốc có ca dev26-l1-compound-multianswer-b#2 yêu cầu câu hỏi trái quy tắc đã tồn tại: tác giả xác nhận chưa chạy thử nhu cầu vừa được hỏi, clarificationLedger không cho hỏi lại. Errata ở development mới đổi question required -> none, vẫn giữ adequacy thiếu. Corpus gốc và kết quả gốc giữ nguyên; không coi thay oracle này là cải thiện model. Holdout không đổi nhãn.

Một ca development QA báo outcome thất bại so với Task có thể xung đột giữa rubric “ghi nhận outcome” và nhãn CONTRADICTORY. Đã đánh dấu cần policy adjudication; chưa đổi oracle sau chạy hoặc dùng sự mơ hồ đó để công bố PASS.

### V28 — Metrics tổng trên 38 turns

| Metric | Kết quả | Ngưỡng | Verdict |
|---|---:|---:|---|
| Runtime critical | 0 | 0 | PASS trong tập development này |
| Source reference validity | 172/172 = 1.000 | 1.000 | PASS |
| Adequacy Macro-F1 | 0.7731 | >= 0.90 | FAIL |
| Question precision | 14/(14+2) = 0.8750 | >= 0.90 | FAIL |
| Question recall | 14/(14+1) = 0.9333 | >= 0.90 | PASS |
| Answer usage | 4/4 = 1.000 | >= 0.95 | PASS, n nhỏ |
| First-pass accepted output | 38/38 = 1.000 | >= 0.98 | PASS |
| Workflow completion | 38/38 | 100% | PASS |

Lớp CONTRADICTORY chỉ n=4: cảnh báo thiếu mẫu. Đây không phải release corpus đủ n.

Tám scenario V28 còn lỗi:

| Case | Lỗi đã quan sát |
|---|---|
| dev26-l3-qa-action-only-b | NOTE_ADEQUACY — còn đánh giá thiếu khi một ca QA đã có outcome |
| dev27-progress-3 | Note báo blocked rõ lý do nhưng model tạo BLOCKING; runtime hạ về UNDETERMINED |
| dev27-decision-1 | Model coi 48 giờ vi phạm yêu cầu tối thiểu 36 giờ |
| dev27-decision-2 | Model coi 48 giờ là vi phạm thay vì hỏi rationale còn thiếu |
| dev27-handover-1 | Hỏi thừa bước tiếp theo đã có trong note |
| dev27-handover-3 | Đòi thêm implementation/Task criteria dù handover đã có trạng thái và next steps |
| dev27-incident-3 | NOTE_ADEQUACY; cần đọc transcript, không suy diễn một nguyên nhân duy nhất từ mã lỗi |
| dev27-auto-1 | NOTE_ADEQUACY; cần đọc transcript/purpose resolution |

### V29 — Vì sao bị loại

Tám ca lỗi: dev26-l3-qa-action-only-b, dev27-decision-1, dev27-handover-1, dev27-handover-3, dev27-auto-1, dev27-decision-3, dev27-completion-1, dev26-l4-criteria-violation-b. dev27-completion-1 bị UNSUPPORTED_REQUIREMENT; các ca còn lại kết luận adequacy/câu hỏi sai. Guard điều cấm được giữ; không đổi parser theo regression prompt để ép PASS.

## 4. Re-audit v26

- Validation: metric cũ 27/28 “format” thực tế là 27/27 accepted model responses; một lượt bị scripted dependency failure. Workflow vẫn 27/28 và precision/recall/answer usage vẫn FAIL.
- Holdout: first-pass accepted output 36/37 thay vì 36/38; vẫn <0.98. Ba false-sufficient giữ nguyên. Các lỗi HTTP bị loại khỏi model-format denominator nhưng vẫn là lý do chưa hoàn tất stage.
- Báo cáo re-audit được lưu riêng, original checkpoint/hash không sửa. Không coi đây là lượt đo live mới.

## 5. Ngân sách và hành động tiếp theo

Ledger release-completion-dev-20261104: 64/64 HTTP attempts, tất cả đã settled, 787615 reported/accounted tokens; cap token 2000000. Không có 429, không sử dụng khóa phụ live. Tiền phí NOT_ESTABLISHED; không gọi token accounting là hóa đơn provider.

Không có call live tiếp theo sau cap. Để tiếp tục G2 cần quyết định vòng development mới với budget/candidate rõ ràng hoặc thay model với gate/policy tương ứng; không reset ledger cũ. G3/G4 chưa được tiêu ngân sách holdout khi G2 còn FAIL. Sau khi G2 đạt phải quay lại đầy đủ các gate G3–G7, không nhảy thẳng sang deploy vì engineering PASS.

## 6. Bằng chứng lưu trong workspace

Gốc evidence: DATN-BE/.worknote-agent-evals/release-completion-20261104/.

- input-snapshot/inventory.json: snapshot 61 file đầu vào, hash/HEAD/branch.
- historical-evidence/inventory.json: 10 artifact v25/v26 lịch sử.
- reaudit-v26-evaluator-v2.json: tính lại có version, không ghi đè v26.
- dev-v28-aggregate.json + dev-v28-mechanisms.json / purpose-a.json / purpose-b.json: quality và từng row.
- v28-source-snapshot/manifest.json: artifact hash 6df5272ed7ac41e47216c55045569bef96ad68af8d6e767a8fa89413e520dbe7.
- v29-probe-aggregate.json + v29-probe-0.json / 1.json và v29-rejected-source-snapshot/: candidate đã bị loại.
- HTTP journals tại .worknote-agent-evals/release-completion-dev-20261104.<scope>.<identity>.http-journal.json; chứa synthetic response đã redact, không chứa Authorization header.
- development-oracle-errata-20261104.json ở scripts/work-note-agent: căn cứ thay đổi development oracle.
- dev-v30-aggregate.json + ba shard: full development v30; v30-reference-diagnosis.json ghi các quote bị chép sai.
- v31-probe.json + v31-source-snapshot/: probe live v31 và source trước sửa guard.
- joint-coverage-offline-replay.json + v31-grounding-source-snapshot/: một ca replay sau sửa guard, không phải live gate mới.
- round2-closed-evidence/manifest.json + bản copy ledger/journals: đóng vòng2, 64 attempts đã settled, model provenance và hash.

## 7. Kiểm tra kỹ thuật và bàn giao

V28 trước vòng probe: BE check exit 0; 221 suites / 2182 unit tests pass, 15 suites / 137 tests skip; e2e 19 suites / 176 tests pass, 2 suites / 4 tests skip. FE check exit 0: 181 files / 1257 tests PASS, lint 0 errors / 6 warnings, build PASS. Deployment gate thêm 7 test PASS riêng; migration DB tạm 2/2 PASS gồm các assertion dữ liệu cũ/ngày sai.

Lượt check tổng thể tiếp theo: lint 0 errors / 6 warnings, typecheck PASS, unit 222 suites / 2192 tests PASS (15 suites / 137 tests skip). E2E FAIL 2 tests: iam-secret và iam-bootstrap-env, child.status=null sau timeout 30000ms; 17 suites / 174 tests PASS và 2 suites / 4 tests skip. Source v30 được sửa trong thời gian lượt tổng thể này còn chạy, nên kết quả này không chứng nhận một snapshot v30 bất biến. Bộ kiểm tra mục tiêu v30 sau thay đổi cuối: 5 suites / 79 tests PASS, fingerprint khớp và lint prompt PASS.

Chẩn đoán E2E: lượt chạy lại tái hiện cùng 2 timeout; chạy riêng child với timeout dài thu được JWT_SECRET_REQUIRED đúng kỳ vọng sau 45054ms (ts-node typecheck), và 23202ms khi transpile-only. Harness E2E đã tách kiểm tra runtime khỏi typecheck gate riêng, dùng TS_NODE_TRANSPILE_ONLY=true, timeout child 60s / test 65s và assertion child.error/child.signal để lỗi timeout được phân biệt rõ. Không sửa logic IAM hay làm yếu assertion JWT_SECRET/env bootstrap. Kiểm tra mục tiêu hai test sau sửa: 2/2 PASS, tổng 29.707s. Chờ lượt check cuối trên source ổn định trước kết luận ENGINEERING_PASS.

Không có commit/push/merge, áp dụng migration DB đích hoặc deployment trong đợt này. Source đang là working tree; HEAD không chứng nhận các file mới.

Lượt cuối trên artifact sau guard 0e6093...: npm run check EXIT0; lint 0 errors / 6 warnings, typecheck và hai nhóm Node safety tests PASS; unit 223 suites / 2205 tests PASS, 15 suites / 137 tests skip (546.831s); E2E 19 suites / 176 tests PASS, 2 suites / 4 tests skip (178.389s); build PASS. Đây là ENGINEERING_PASS trong cấu hình test local hiện tại, không chứng minh các integration/environment còn skip hoặc release quality.

Log được lưu ở engineering-v31-guard-final-check.log và engineering-round2-db-check.log; engineering-final-evidence.json xác nhận source artifact khớp snapshot, ledger đóng không đổi, log không chứa giá trị hai credential. Local dist1345 files có digest17e5910943e84cc1b3664d9865c77f808f2dd4449b11f46a395737f45dbf4a2b; chưa có production image/deployment receipt. Không lấy lượt check đã ABORT làm bằng chứng PASS.

## 8. Chấp thuận vòng development 2

Sau khi xem kết quả và giới hạn 64/64 của vòng 1, người dùng đã chấp thuận rõ: “Mở thêm một vòng sửa với model hiện tại: tối đa 64 attempts / 2 triệu tokens”. Vòng mới dùng ledger release-completion-dev-round2-20261104; ledger cũ không reset/đổi trần. Model vẫn mistralai/ministral-14b, combined.

Giả thuyết candidate v30: few-shot hiện chọn nhầm ví dụ khác purpose (QA có ví dụ thiếu actor của COMPLETION; HANDOVER có ví dụ completion; OTHER không có ví dụ riêng), và ví dụ QA với Task rỗng chưa báo outcome nhưng được gán đủ, trái quy tắc F14 mới. Vòng 2 sẽ sửa tính nhất quán của example packs và conditional stop rule theo rubric, rồi kiểm tra cùng bộ development đầy đủ. Không dùng holdout để tune. Trần mới được cấp trước khi gọi live, không coi đây là retry miễn phí hoặc mở lại kết quả v28/v29.

### V30 — Snapshot và chính sách đo đã chốt trước live

- Model/architecture: mistralai/ministral-14b / combined; analysis policy không đổi; editor-limit=0 trong development.
- Prompt task-note-assessment/2026-11-04.v30; artifactHash=9d08c73207637581061b8c71e7f323276183a8bd7ef31ebeb66dfd0c6cb31ba9. Lưu 68 file trong v30-source-snapshot/ trước call đầu.
- Corpus dev-v30: 34 scenarios / 38 analysis turns, corpusHash=505cc0510d4087f125d6c6d1ac71dd898bbe307d1788378a1284e2c5c4ac5563. Dry-run ceiling 38 HTTP attempts; trần phase 64 / 2000000 tokens, mọi retry/429 fallback cùng ledger.
- Giữ system prompt dài v28; sửa final stop theo purpose, định nghĩa chiều bất đẳng thức min/max, chọn few-shot cùng purpose cho explicit purpose và bổ sung đối chứng QA observed failure, handover actionable, decision hợp lệ/vi phạm, OTHER reference/vague. Split assessor cùng dùng example packs cũng bump version, nhưng không coi kết quả combined là bằng chứng split.
- Erratum development thứ hai ghi trong corpus trước live: dev27-qa-3 kỳ vọng ENOUGH_FOR_PURPOSE thay CONTRADICTORY vì chỉ báo lỗi QA quan sát được, không claim hoàn thành Task. Rubric QA có requireWholeTaskCoverage=false, chấp nhận outcome lỗi. Coverage Task vẫn có thể CONTRADICTORY. Sửa này khiến điểm historical v28 giảm, không biến v28 thành PASS; corpus cũ/release label giữ nguyên.
- Không sửa source thuộc artifact trong lúc các shard live chạy. Kết quả live và ledger sẽ được bổ sung sau khi đủ cả ba shard; chưa tuyên bố candidate PASS từ preflight/unit.

### V30 — Kết quả vòng development 2, batch đầy đủ

Kết quả 24/34 scenarios PASS, 10 FAIL; 38 analysis rows. Tất cả dùng artifactHash ở trên. V30 FAIL G2; không chạy validation/holdout. Không so sánh trực tiếp số pass với v28 như một cải thiện thuần model vì corpus dev-v30 có erratum QA đã khai báo trước.

| Metric runtime | V30 | Ngưỡng | Kết luận |
|---|---:|---:|---|
| Critical theo evaluator | 2 (1 INVALID_SOURCE_REFERENCE, 1 false-sufficient) | 0 | FAIL; invalid reference bị parser chặn, không phải nguồn giả được runtime chấp nhận |
| Accepted source refs trên output đã parse | 173/173 | 1.00 | PASS cho các refs được chấp nhận; không xóa lỗi INVALID_SOURCE_REFERENCE khỏi critical |
| Adequacy Macro-F1 | 0.8221 | >=0.90 | FAIL |
| Question precision | 13/(13+5)=0.7222 | >=0.90 | FAIL |
| Question recall | 13/(13+2)=0.8667 | >=0.90 | FAIL |
| Answer use | 4/4 | >=0.95 | PASS, mẫu nhỏ |
| First-pass accepted output | 36/38=0.9474 | >=0.98 | FAIL |
| Workflow completion | 36/38 | 100% | FAIL |

CONTRADICTORY n=3, INSUFFICIENT n=16, SUFFICIENT n=19. Editor không chạy, human semantic acceptance NOT_ESTABLISHED. Latency analysis p50=34474ms / p95=49658ms, n=38; chưa có SLO release để kết luận hiệu năng.

| Ca fail | Nguyên nhân quan sát từ transcript |
|---|---|
| dev26-l3-qa-action-only-b | Đã có PNG 8MB trả HTTP 413/FILE_TOO_LARGE nhưng hỏi kết quả tệp <=5MB mà tác giả nói chưa chạy; sai phạm vi QA |
| dev26-l5-progress-history-conflict-a | INVALID_SOURCE_REFERENCE: model chép “đối soát” thành “đối sát” trong 6 refs ở requirements/claim/coverage/gap. ID tồn tại nhưng quote không còn nguyên văn. Parser chặn đúng hợp đồng; không phải JSON syntax error |
| dev27-progress-3 | Raw ENOUGH nhưng đồng thời tạo BLOCKING scope.completed_part cho trạng thái blocked đã có lý do; runtime hạ UNDETERMINED |
| dev27-decision-2 | “Chốt lưu bản nháp 48 giờ.” không báo rationale nhưng trả ENOUGH; false-sufficient và thiếu câu hỏi bắt buộc |
| dev27-handover-1 | Hỏi bước tiếp theo dù note đã nêu thêm index ở staging và đo trên bộ dữ liệu mẫu |
| dev27-handover-3 | Hỏi chi tiết thao tác dù note đã bàn giao giải phóng log rồi chạy migration ở nhánh đã nêu |
| dev27-incident-1 | HTTP 502 + staging + thời điểm sau đăng nhập đã có, vẫn yêu cầu mô tả triệu chứng chi tiết hơn |
| dev27-incident-3 | Mảng rỗng + local + chuyển dự án/quyền xem đã có, vẫn hỏi lại hiện tượng |
| dev27-completion-1 | UNSUPPORTED_REQUIREMENT: text requirement kết thúc dấu chấm trong khi quote cắt ở dấu chấm phẩy; parser yêu cầu literal match. Không đổi parser để bỏ qua mọi khác biệt nội dung |
| dev27-auto-1 | Raw ENOUGH nhưng kèm BLOCKING/câu hỏi về phần test để ca sau; runtime hạ UNDETERMINED |

Budget sau batch: 41/64 attempts settled; 467758 reported tokens; 619936 accounted tokens (bao gồm reservation của 3 phản hồi 429 không có usage), cap 2000000. Mỗi shard gặp primary 429 một lần và chuyển secondary thành công, tổng 3 primary 429 + 38 phản hồi model. Không in giá trị key. Retry-After được lưu trong routing events; không thử lại primary đã hết quota trong cùng shard.

### V31 — Probe tiếp theo trong 23 attempts còn lại (định nghĩa trước live)

Giả thuyết: nhiều rubric/purpose trong cùng system prompt làm model đòi thông tin ngoài purpose và bỏ qua consistency. Thay system bằng grounding chung + chỉ rubric purpose được chọn; AUTO vẫn có toàn bộ rubric để phân giải. Giữ example packs v30, model, provider policy và parser. Nhấn mạnh rationale phải do tác giả báo, không lấy từ Task; requirement.text/quote giữ cả dấu câu, sourceId chỉ lấy request cuối. Đây là candidate mới, không được gộp các ca v30 PASS vào v31.

Probe đã chốt 18 scenarios / 22 analysis turns: cả bốn ca multi-turn L1/L2, cả 10 ca v30 FAIL và bốn đối chứng QA thiếu outcome, Decision hợp lệ/vi phạm, Incident mơ hồ. Max local 23 HTTP attempts (22 logical + tối đa một primary429->secondary), cùng ledger round2 cap64/2M. Không đủ ngân sách để đo full34/38 v31 sau probe này; dù probe xanh vẫn chưa đủ G2 trên toàn bộ candidate.

Test tái hiện purpose isolation trước sửa: 7 FAIL / 1 PASS; sau sửa phải kiểm tra lại cùng bộ mục tiêu và fingerprints trước snapshot/live. Test mới runner cả hai key429 chứng minh trước sửa vẫn thử các ca kế tiếp khi --no-fail-fast; đã thêm điều kiện dừng ngay cho cả analysis/editor. Lượt v30 không gặp secondary429 nên lỗi dừng này không làm thay đổi kết quả batch đã lưu.

Preflight cuối V31: 6 suites / 104 tests PASS; lint prompt/example/runner/evaluator-spec PASS, fingerprints cập nhật. Snapshot 68 file lưu tại v31-source-snapshot/, artifactHash=aae8f96861e79b96de88f667f2583c063e286dc568db2083f33368829fa9a24e. CorpusHash giữ dev-v30 đã chốt; prompt task-note-assessment/2026-11-04.v31. Dry-run 18 scenarios / 22 analysis calls / 0 editor, max local23 + global64/2M; bắt đầu live sau preflight. npm run check được chạy lại trên source V31 ổn định, chưa có verdict khi probe còn chạy.

### V31 — Kết quả probe và trần ngân sách cuối

13/18 scenarios PASS, 5 FAIL; đủ 22 analysis turns. Đây là probe chọn có chủ đích, không phải full34/38; không pool với v30 hoặc coi 13/18 là release pass rate. Cả bốn ca multi-turn L1/L2 và bốn đối chứng đã chọn đều PASS. Năm lỗi v30 gồm historical quote, Decision rationale, hai Incident và AUTO đã PASS trong probe v31; chưa chứng minh độ ổn định trên family mới.

| Metric runtime probe v31 | Giá trị | Ngưỡng release để tham chiếu | Verdict |
|---|---:|---:|---|
| Critical | 0 | 0 | PASS trong probe |
| Accepted source refs | 115/115 | 1.00 | PASS |
| Adequacy Macro-F1 | 0.8353 | >=0.90 | FAIL |
| Question precision | 9/(9+4)=0.6923 | >=0.90 | FAIL |
| Question recall | 9/(9+0)=1.0000 | >=0.90 | PASS |
| Answer use | 4/4 | >=0.95 | PASS, mẫu nhỏ |
| First-pass accepted output | 22/22 | >=0.98 | PASS |
| Workflow completion | 22/22 | 100% | PASS |

CONTRADICTORY n=1 / INSUFFICIENT n=10 / SUFFICIENT n=11, không đạt n>=8 mỗi lớp. Editor không chạy; human semantic review NOT_ESTABLISHED.

| Ca fail v31 | Lỗi còn thấy trong transcript |
|---|---|
| dev26-l3-qa-action-only-b | Tiếp tục hỏi test tệp <=5MB dù ca PNG 8MB đã có HTTP413/FILE_TOO_LARGE; đòi nghiệm thu toàn Task thay scope QA |
| dev27-progress-3 | Trạng thái blocked đã có lý do quyền staging, nhưng hỏi khi nào có quyền/cách khác để kiểm thử; không phải thông tin bắt buộc của Progress |
| dev27-handover-1 | Hỏi cách thêm index/kết quả đo và thêm gap về bảo đảm thứ tự thời gian, vượt thông tin bàn giao cần thiết đã có |
| dev27-handover-3 | Hỏi chi tiết cách giải phóng log/chạy migration dù note đã nêu next steps, nhánh và blocker; cùng lỗi đòi mức chi tiết ngoài rubric |
| dev27-completion-1 | Model literal refs đã hợp lệ, raw ENOUGH và coverage SUPPORTED. Parser hạ requirement tổng hợp thành PARTIAL vì quote dài nối hai claim FULL nhưng không có một claim riêng lẻ chứa toàn quote; runtime vì vậy UNDETERMINED |

Phase round2 đóng ở 64/64 attempts settled: 60 model responses HTTP200 + 4 primary429 được secondary tiếp nối thành công, 0 secondary429. Provider báo đúng mistralai/ministral-14b trên cả 60 response. Reported tokens=668534, khớp tổng usage trong journals; accounted tokens=868654/2000000 gồm 4 reservation cho phản hồi429 không có usage. Không thêm call sau trần64; token cap còn dư không cấp quyền tăng HTTP cap. Không gọi accounted tokens là tiền phí provider.

Đã copy nguyên ledger và 4 journals vào round2-closed-evidence/, manifest chứa SHA256 và model/status counts. Ledger gốc giữ nguyên; ledger vòng1 vẫn64/64 riêng, không reset hoặc ghép trần.

### Sửa guard sau live — chỉ test/replay offline

Test mới tái hiện compound coverage trước sửa: 1 positive FAIL / 3 negative PASS. Guard được đổi để chấp nhận quote được bao phủ liên tục bởi nhiều AUTHOR_REPORT/FULL claims cùng sourceId, chỉ cho phép khoảng trắng giữa các đoạn. Thiếu đoạn có chữ/dấu câu, claim PARTIAL hoặc khác sourceId vẫn không được ghép; polarity veto giữ nguyên. Đây là kiểm tra provenance nguyên văn, không tự chứng minh entailment của Task hoặc tự nâng model coverage PARTIAL thành SUPPORTED.

Bộ kiểm tra guard/protocol/state/fingerprint sau sửa: 4 suites / 130 tests PASS; lint PASS. Replay đúng raw response dev27-completion-1 đã lưu: coverage toàn SUPPORTED, runtime ENOUGH_FOR_PURPOSE/ready_to_edit, grade PASS; HTTP attempts=0. Không sửa v31-probe.json để biến live13/18 thành14/18, không tính replay này là một model response mới hoặc release gate.

Prompt vẫn task-note-assessment/2026-11-04.v31 vì nội dung prompt không đổi ở bước guard. Artifact sau sửa=0e6093d1442236b7efb091c525e53dd9a3f802fd7017e0bc8fabae31e76069d8; lưu69 file tại v31-grounding-source-snapshot/. Artifact live cũ aae8... vẫn được giữ riêng. Candidate hiện tại chưa có full live development; bốn lỗi semantic kể trên vẫn chưa được sửa bằng bằng chứng live.

Lượt npm run check V31 ban đầu được chủ động ABORT trong unit phase để sửa lỗi guard vừa tái hiện, không ghi là PASS hoặc một lỗi test mới. Đã bắt đầu lại npm run check trên artifact sau sửa; kết quả cuối sẽ chốt ở §7. DB worktree: chạy lại migration MongoDB7.0.24 tạm, 2/2 tests PASS (4889.9ms), không áp dụng DB đích.

## 9. Trạng thái bàn giao sau vòng 2

| Kết luận | Trạng thái |
|---|---|
| ENGINEERING_PASS | PASS local: check EXIT0, 2205 unit /176 E2E PASS, build PASS; 137 unit/4 E2E skip vẫn được báo; DB tạm2/2 PASS |
| AUTOMATED_QUALITY_PASS | FAIL: full v30 không đạt; probe v31 không đạt; artifact sau sửa guard chưa có full live |
| HUMAN_REVIEW_PASS | NOT_ESTABLISHED |
| DB_READY | DB tạm PASS; DB đích/migration mechanism/receipt chưa có |
| RELEASE_READY | FALSE |
| DEPLOYED | FALSE |

Bốn lỗi semantic còn mở ở dev26-l3-qa-action-only-b, dev27-progress-3, dev27-handover-1, dev27-handover-3. Giữ expected labels, source guards và ngưỡng release; không ép ENOUGH để làm xanh development. Cần một candidate giải quyết đủ các nhóm này và đo full34/38 cùng artifact trước G3/G4. Không được dùng phần token còn dư của phase đã hết64 attempts để gọi thêm hoặc mở phase khác không có chấp thuận.

Đề xuất bước quyết định sau báo cáo: chọn tiếp tục model hiện tại hay đánh giá candidate với model khác, rồi chốt model/provider policy và ngân sách mới trước live. Kết quả này chưa chứng minh model khác chắc chắn PASS. Sau G2 vẫn phải hoàn tất fresh corpus/freeze, validation/holdout, feature measurements, semantic review, registry/DB/CI và staging/rollout theo kế hoạch; không rút bỏ gate để release sớm.

Sau báo cáo, người dùng chọn “Chuẩn bị đánh giá model khác; chốt model và ngân sách trước khi chạy”. Đã lập [đề xuất model/ngân sách](23-alternative-model-evaluation-proposal-2026-11-04.md), chỉ đọc catalog/usage và dry-run; chưa gọi inference hoặc cấp phase mới. Quyết định này không tự cho phép đổi runtime model hay tiêu thêm ngân sách.

Cập nhật sau đó: người dùng đã duyệt phase Qwen48 attempts/650000 tokens, yêu cầu tối ưu đánh dấu và thêm key3. Đã triển khai cache/checkpoint, replay22 lượt với0 HTTP; check cuối2218 unit/176 E2E và build PASS. Qwen mới dùng5/48 attempts,0 reported tokens, chưa có output model vì503/429; giữ nguyên trần, không chạy full. Chi tiết và nguồn mới nhất tại [báo cáo checkpoint/tối ưu](24-incremental-evaluation-and-qwen-checkpoint-2026-11-04.md).
