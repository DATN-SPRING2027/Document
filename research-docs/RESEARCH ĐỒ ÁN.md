# **CONTINUUM AI**

## **AI-Powered Organizational Knowledge Continuity Platform**

**Loại hệ thống:** Enterprise Knowledge Management / Knowledge Continuity / AI-assisted Onboarding  
**Đối tượng sử dụng:** Doanh nghiệp có nhiều tri thức nội bộ, quy trình vận hành và sự phụ thuộc vào nhân sự có kinh nghiệm  
**Mục tiêu tổng quát:** Biến kiến thức phân tán và kinh nghiệm cá nhân thành trí nhớ tổ chức có thể tìm kiếm, xác minh, duy trì và tái sử dụng.

Các ví dụ về Payment Service chuyển từ MongoDB sang PostgreSQL trong tài liệu này là tình huống minh họa cho temporal knowledge và decision memory, không phải quyết định công nghệ của Continuum AI. Stack MVP đã chốt nằm trong [Tech.md](../research-tech/Tech.md).

---

# **1\. Tổng quan dự án**

&nbsp;

## **1.1. Giới thiệu**

Trong hầu hết doanh nghiệp, kiến thức cần thiết để vận hành không tồn tại tại một vị trí duy nhất.

Một phần kiến thức nằm trong:

* tài liệu nội bộ;  
* SOP;  
* Google Drive;  
* SharePoint;  
* Wiki;  
* Confluence;  
* email;  
* ticket;  
* project management system;  
* source code;  
* issue tracker;  
* biên bản họp;  
* tài liệu hướng dẫn;  
* chính sách doanh nghiệp.

Tuy nhiên, một lượng lớn kiến thức quan trọng lại tồn tại dưới dạng kinh nghiệm cá nhân của nhân viên.

Ví dụ:

> Khi hệ thống X xảy ra lỗi Y thì cần kiểm tra thành phần nào trước?

> Tại sao công ty từng quyết định không sử dụng giải pháp A?

> Khách hàng B thường yêu cầu quy trình xử lý đặc biệt nào?

> Trong trường hợp nào SOP chính thức không hoàn toàn phù hợp?

> Ai là người thực sự hiểu hệ thống cũ?

> Một thao tác nguy hiểm nhưng tài liệu hiện tại chưa đề cập là gì?

Những thông tin dạng này thường không được ghi lại đầy đủ.

Khi một nhân viên có kinh nghiệm nghỉ việc, chuyển bộ phận hoặc không còn tham gia dự án, doanh nghiệp có nguy cơ mất một phần kiến thức mà người đó đang nắm giữ.

Continuum AI được xây dựng nhằm giải quyết vấn đề đó.

Hệ thống đóng vai trò như một **Organizational Memory Platform – nền tảng trí nhớ tổ chức**, trong đó AI hỗ trợ doanh nghiệp:

1. thu thập kiến thức;  
2. tổ chức kiến thức;  
3. phát hiện kiến thức còn thiếu;  
4. khai thác kiến thức ngầm từ nhân viên;  
5. xác minh kiến thức;  
6. phát hiện kiến thức lỗi thời hoặc mâu thuẫn;  
7. tìm kiếm và sử dụng lại kiến thức;  
8. hỗ trợ nhân viên mới;  
9. hỗ trợ chuyển giao công việc;  
10. đánh giá rủi ro phụ thuộc tri thức vào cá nhân.

---

# **2\. Vấn đề cần giải quyết**

## **2.1. Knowledge Fragmentation**

Thông tin của doanh nghiệp thường phân tán trên nhiều nền tảng.

Ví dụ:

Google Drive

Confluence

Jira

Slack

GitHub

Email

PDF

Word

Excel

Meeting Notes

Internal Wiki

&nbsp;

Nhân viên không biết:

* tài liệu nào là tài liệu chính thức;  
* tài liệu nào mới nhất;  
* thông tin nằm ở đâu;  
* nội dung nào đã lỗi thời;  
* ai đang sở hữu kiến thức;  
* phiên bản nào còn hiệu lực.

Điều này làm tăng thời gian tìm kiếm thông tin và khiến cùng một câu hỏi được hỏi đi hỏi lại nhiều lần.

---

# **3\. Tacit Knowledge – tri thức ngầm**

Không phải mọi kiến thức đều tồn tại dưới dạng tài liệu.

Một Senior Engineer có thể biết:

> “Khi hệ thống xuất hiện lỗi này thì không nên restart ngay, vì restart có thể làm mất trạng thái transaction.”

Nhưng kiến thức đó có thể chưa bao giờ được viết trong documentation.

Tương tự, một nhân viên chăm sóc khách hàng có thể biết:

> “Khách hàng A luôn yêu cầu báo cáo trước 15 giờ thứ Sáu, dù hợp đồng chỉ nói cuối tuần.”

Đây là kiến thức hình thành từ kinh nghiệm thực tế.

Continuum AI gọi nhóm thông tin này là:.

**Tacit Knowledge – tri thức ngầm.**

Một mục tiêu quan trọng của hệ thống là chuyển:

Knowledge in people's heads

&nbsp;

thành:

Verified Organizational Knowledge

&nbsp;

mà không đơn giản lưu toàn bộ cuộc hội thoại thành văn bản.

---

# **4\. Knowledge Dependency**

Một vấn đề nghiêm trọng khác xảy ra khi một quy trình quan trọng phụ thuộc quá nhiều vào một cá nhân.

Ví dụ:

Production Deployment

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── Nguyễn A

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── Deployment

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── Rollback

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── Monitoring

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── Incident Handling

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── Legacy Infrastructure

&nbsp;

Nếu Nguyễn A nghỉ việc, doanh nghiệp có thể vẫn còn source code và tài liệu nhưng mất:

* kinh nghiệm xử lý sự cố;  
* nguyên nhân của các quyết định cũ;  
* hiểu biết về ngoại lệ;  
* mối liên hệ giữa các hệ thống;  
* kinh nghiệm vận hành thực tế.

Continuum AI vì vậy không chỉ quản lý tài liệu.

Hệ thống quản lý:

> **mối quan hệ giữa người – kiến thức – quy trình – hệ thống – quyết định – sự cố.**

---

# **5\. Knowledge Staleness**

Kiến thức doanh nghiệp thay đổi theo thời gian.

Ví dụ:

2025:

Payment Service → MongoDB

&nbsp;

2026:

Payment Service → PostgreSQL

&nbsp;

Nếu một tài liệu cũ vẫn được retrieval bởi AI, hệ thống có thể đưa ra câu trả lời đúng về mặt nội dung nhưng sai đối với hiện tại.

Do đó Continuum AI phải quản lý:

Knowledge Version

Knowledge Validity

Knowledge Owner

Valid From

Valid Until

Superseded Knowledge

Deprecated Knowledge

&nbsp;

---

# **6\. Knowledge Conflict**

Hai Team Member có thể đưa ra hai cách xử lý khác nhau.

Ví dụ:

**Team Member A**

> Deploy production sau 22:00.

**Team Member B**

> Không được deploy production sau 22:00.

Hệ thống không được tự động chọn một câu trả lời.

Thay vào đó Continuum AI phải tạo:

Knowledge Conflict

&nbsp;

và yêu cầu người có thẩm quyền xác nhận.

Sau khi xác nhận, một kiến thức mới mới được chuyển sang trạng thái:

VERIFIED

&nbsp;

---

# **7\. Mục tiêu hệ thống**

## **7.1. Mục tiêu chính**

Continuum AI hướng tới việc xây dựng một **Knowledge Continuity Layer** cho doanh nghiệp.

Thay vì chỉ trả lời:

> “Tài liệu nói gì?”

hệ thống phải có khả năng hiểu:

> Công ty biết những gì?

> Kiến thức đó đến từ đâu?

> Ai chịu trách nhiệm?

> Kiến thức có còn hiệu lực không?

> Có bằng chứng nào xác nhận không?

> Có thông tin nào đang mâu thuẫn không?

> Có quy trình quan trọng nào thiếu documentation không?

> Có quy trình nào đang phụ thuộc quá nhiều vào một nguồn kiến thức không?

---

# **8\. Mục tiêu nghiệp vụ**

Hệ thống được thiết kế để giảm:

### **Time-to-Information**

Thời gian một nhân viên cần để tìm được thông tin cần thiết.

### **Time-to-Competence**

Thời gian nhân viên mới cần để có thể tự thực hiện công việc.

### **Expert Interruption**

Số lần chuyên gia hoặc nhân viên lâu năm phải trả lời lại cùng một câu hỏi.

### **Knowledge Loss**

Lượng kiến thức có nguy cơ mất khi nhân viên nghỉ việc.

### **Knowledge Concentration**

Mức độ một quy trình chỉ được hiểu bởi một số rất ít cá nhân.

### **Knowledge Staleness**

Lượng kiến thức không còn phù hợp với trạng thái hiện tại của doanh nghiệp.

---

# **9\. Phạm vi hệ thống**

Continuum AI bao gồm năm lớp chức năng chính.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;CONTINUUM AI

&nbsp;

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Organizational Knowledge

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;┌──────────────────┼──────────────────┐

&nbsp;│                  │                  │

&nbsp;▼                  ▼                  ▼

Capture           Manage             Consume

Knowledge         Knowledge          Knowledge

&nbsp;│                  │                  │

&nbsp;▼                  ▼                  ▼

Documents       Verification       AI Assistant

Interview       Versioning         Search

Systems         Conflict           Onboarding

Meetings        Ownership          Offboarding

Tickets         Freshness          Training

&nbsp;

---

# **10\. Actor và role trong phạm vi project**

Continuum AI MVP tập trung vào một software project có nhiều team. Mọi leader và member đều phải đóng góp, cập nhật và chuyển giao knowledge liên quan đến responsibility của mình trong suốt quá trình project hoạt động.

## **10.1. Project Manager**

Project Manager quản lý continuity trên toàn project và nhiều team:

* theo dõi project knowledge coverage, gap, freshness và concentration;  
* khởi tạo handover khi leader hoặc member rời project hay đổi responsibility;  
* gán hoặc phê duyệt successor;  
* điều phối transfer giữa nhiều team;  
* xác nhận handover readiness hoặc waiver có audit reason.

Project Manager vẫn chịu resource ACL và không mặc nhiên đọc mọi confidential knowledge.

---

## **10.2. Team Leader**

Team Leader chịu trách nhiệm continuity trong team được giao:

* định nghĩa required knowledge của team, module và process;  
* gán Knowledge Owner và scoped SME;  
* theo dõi gap, conflict, freshness và overdue update;  
* quản lý handover của team member;  
* đề xuất successor;  
* xác nhận team handover package.

---

## **10.3. Team Member**

Mọi Team Member đều là knowledge consumer và knowledge contributor:

* tìm kiếm và hỏi AI trên knowledge được phép;  
* tạo hoặc cập nhật decision, procedure, incident, lesson learned, known issue, workaround và dependency;  
* xác nhận claim do AI trích xuất từ công việc của mình;  
* báo knowledge thiếu, lỗi thời hoặc mâu thuẫn;  
* tham gia review và AI interview;  
* hoàn thành handover items khi rời project hoặc chuyển responsibility.

Member không được tự activate knowledge chỉ vì họ là người tạo nội dung.

---

## **10.4. Project Administrator**

Project Administrator quản lý kỹ thuật trong project:

* project/team membership và persistent role;  
* connector và data source;  
* permission policy và resource ACL;  
* ingestion configuration;  
* session/service credential revocation;  
* technical và security audit.

Project Administrator không mặc nhiên là SME hoặc Knowledge Owner và không tự động được đọc confidential source content.

---

# **11\. Scoped assignments**

## **11.1. Subject Matter Expert assignment**

SME là assignment cho một domain, module, process hoặc knowledge requirement cụ thể. SME có thể trả lời gap, tham gia AI interview, review conflict và verify knowledge trong đúng assignment scope.

## **11.2. Knowledge Owner assignment**

Knowledge Owner chịu trách nhiệm đối với Knowledge Object, knowledge requirement, process, module hoặc source cụ thể. Owner có thể approve, reject, edit, deprecate, supersede, assign reviewer và đặt review cycle trong phạm vi được giao.

## **11.3. Successor assignment**

Successor là member được gán tiếp quản responsibility, module hoặc process từ predecessor. Successor nhận scoped handover package, knowledge path và quyền hỏi AI trong phạm vi chuyển giao. Hệ thống không sao chép toàn bộ permission của predecessor cho successor.

---

# **12\. Membership lifecycle states**

`ONBOARDING` và `OFFBOARDING` là trạng thái membership, không phải global RBAC role.

* `ONBOARDING` kích hoạt successor learning path hoặc project onboarding plan.  
* `OFFBOARDING` kích hoạt responsibility analysis, coverage analysis, required handover items, AI interview và access-revocation schedule.

---

# **13\. Authorization model**

Effective permission được tính từ:

```text
Persistent role
+ Project and team membership scope
+ SME, Owner or Successor assignment
+ Source and resource ACL
+ Membership lifecycle state
- Explicit deny
```

Permission phải được kiểm tra trước retrieval. Frontend route guard chỉ phục vụ UX; backend là authority cuối cùng.

---

# **14\. Khái niệm Organizational Knowledge Object**

Đơn vị cơ bản của hệ thống không phải là document.

Đơn vị cơ bản là:

# **Knowledge Object**

Ví dụ một document 30 trang có thể chứa:

1 Policy

4 Procedures

6 Rules

3 Exceptions

2 Decisions

5 Responsibilities

&nbsp;

Các thành phần này được AI trích xuất thành từng Knowledge Object độc lập.

Ví dụ:

Knowledge Object

&nbsp;

Type:

OperationalRule

&nbsp;

Title:

Payment timeout handling

&nbsp;

Condition:

Payment timeout occurs

AND

success\_rate \> 98%

&nbsp;

Action:

Do not immediately rollback

&nbsp;

Reason:

Possible upstream payment gateway latency

&nbsp;

Source:

Incident \#123

Expert Interview \#42

&nbsp;

Owner:

Payment Team

&nbsp;

Status:

Verified

&nbsp;

---

# **15\. Các loại Knowledge Object**

Hệ thống có thể quản lý:

Policy

Procedure

Rule

Exception

Decision

Lesson Learned

Best Practice

Warning

Incident Knowledge

FAQ

Responsibility

Dependency

Definition

Business Rule

Operational Guideline

&nbsp;

Việc phân loại giúp AI hiểu cách sử dụng knowledge thay vì coi tất cả thông tin là những đoạn văn giống nhau.

---

# **16\. Knowledge Lifecycle**

Mỗi knowledge sẽ đi qua một vòng đời.

DISCOVERED

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

EXTRACTED

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

PROPOSED

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

UNDER REVIEW

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;┌───┴────┐

&nbsp;▼        ▼

VERIFIED  REJECTED

&nbsp;│

&nbsp;▼

ACTIVE

&nbsp;│

&nbsp;├─────────────┐

&nbsp;▼             ▼

SUPERSEDED   DEPRECATED

&nbsp;

---

# **17\. Proposed Knowledge**

Knowledge do AI trích xuất không được coi là sự thật ngay lập tức.

Nó chỉ có trạng thái:

PROPOSED

&nbsp;

AI phải lưu kèm:

source

evidence

confidence

extractor

timestamp

&nbsp;

Knowledge Owner hoặc SME có quyền verify.

---

# **18\. Verified Knowledge**

Sau khi được người có thẩm quyền xác nhận, knowledge chuyển thành:

VERIFIED

&nbsp;

Verified Knowledge được ưu tiên cao hơn:

* raw document;  
* chat message;  
* unverified extraction;  
* historical knowledge.

---

# **19\. Knowledge Versioning**

Knowledge được quản lý theo version.

Ví dụ:

Refund Policy v1

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

Refund Policy v2

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

Refund Policy v3

&nbsp;

Mỗi version có:

valid\_from

valid\_until

created\_by

verified\_by

reason\_for\_change

&nbsp;

Knowledge cũ vẫn được lưu để phục vụ historical analysis nhưng không được coi là current truth.

---

# **20\. Knowledge Source**

Mỗi knowledge phải có nguồn gốc.

Nguồn có thể là:

Document

Email

Chat

Ticket

Incident

Meeting

Interview

Manual Input

Source Code

Policy

Decision Record

&nbsp;

Ví dụ:

Knowledge

&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;├── Supported by → SOP v4

&nbsp;&nbsp;&nbsp;├── Supported by → Incident \#129

&nbsp;&nbsp;&nbsp;└── Confirmed by → Nguyễn A

&nbsp;

Điều này cho phép AI trả lời kèm evidence.

---

# **21\. Knowledge Graph**

Knowledge Graph là lớp thể hiện các quan hệ trong tổ chức.

Các entity chính gồm:

Person

Team

Role

Process

System

Knowledge

Document

Decision

Incident

Project

Client

Skill

Policy

&nbsp;

---

# **22\. Quan hệ Knowledge Graph**

Ví dụ:

Person

&nbsp;KNOWS\_ABOUT

&nbsp;Process

&nbsp;

Team

&nbsp;OWNS

&nbsp;System

&nbsp;

Process

&nbsp;DEPENDS\_ON

&nbsp;System

&nbsp;

Knowledge

&nbsp;DOCUMENTED\_IN

&nbsp;Document

&nbsp;

Incident

&nbsp;REVEALED

&nbsp;Knowledge

&nbsp;

Decision

&nbsp;CHANGED

&nbsp;System

&nbsp;

Team Member

&nbsp;HAS\_SKILL

&nbsp;Skill

&nbsp;

---

# **23\. Temporal Knowledge Graph**

Quan hệ phải có yếu tố thời gian.

Ví dụ:

Payment Service

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│ USES

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;MongoDB

&nbsp;valid\_until \= 2025-08

&nbsp;

và:

Payment Service

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│ USES

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

PostgreSQL

valid\_from \= 2025-08

&nbsp;

Nhờ đó hệ thống có thể xử lý câu hỏi:

> Payment Service hiện sử dụng database nào?

khác với:

> Payment Service sử dụng database nào vào tháng 4/2025?

---

# **24\. Module 1 – Enterprise Knowledge Ingestion**

Module này chịu trách nhiệm thu thập dữ liệu từ hệ sinh thái doanh nghiệp.

Nguồn ban đầu có thể gồm:

PDF

DOCX

TXT

Markdown

Web Page

Google Drive

Confluence

GitHub

Jira

Slack

Microsoft Teams

&nbsp;

Hệ thống phải giữ metadata gốc như:

author

created\_at

updated\_at

source\_system

source\_url

permission

version

&nbsp;

---

# **25\. Document Processing**

Document sau khi ingest được xử lý:

Document

&nbsp;&nbsp;&nbsp;↓

Parser

&nbsp;&nbsp;&nbsp;↓

OCR if required

&nbsp;&nbsp;&nbsp;↓

Structure Detection

&nbsp;&nbsp;&nbsp;↓

Section Extraction

&nbsp;&nbsp;&nbsp;↓

Chunking

&nbsp;&nbsp;&nbsp;↓

Metadata Extraction

&nbsp;&nbsp;&nbsp;↓

Embedding

&nbsp;

Tài liệu gốc vẫn được giữ để citation.

---

# **26\. Knowledge Extraction Engine**

Sau ingestion, AI phân tích nội dung để tìm các Knowledge Object.

Ví dụ tài liệu:

> Nếu server API không phản hồi trong vòng 30 giây, kỹ thuật viên phải kiểm tra Redis trước khi restart service.

AI có thể tạo:

Type:

Procedure

&nbsp;

Trigger:

API response timeout \> 30 seconds

&nbsp;

Step:

Check Redis

&nbsp;

Constraint:

Before restarting service

&nbsp;

---

# **27\. AI Knowledge Assistant**

Đây là giao diện hỏi đáp chính.

Người dùng có thể hỏi:

> Quy trình refund là gì?

> Tôi phải liên hệ ai khi Payment Service lỗi?

> Tại sao công ty chuyển khỏi MongoDB?

> Deployment hiện tại được thực hiện như thế nào?

> Có những incident tương tự lỗi này trước đây không?

AI không chỉ dùng vector similarity.

Hệ thống sử dụng nhiều retrieval strategy.

---

# **28\. Hybrid Retrieval**

Pipeline đề xuất:

User Question

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

Intent Detection

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

Query Planner

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;┌────┼───────────────┐

&nbsp;▼    ▼               ▼

BM25 Vector         Graph

&nbsp;│    │               │

&nbsp;└────┴──────┬────────┘

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Reranker

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Evidence Filter

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Context Builder

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;LLM

&nbsp;

---

# **29\. Query Classification**

Ví dụ:

**Question**

> Chính sách nghỉ phép là gì?

Routing:

BM25 \+ Vector

&nbsp;

---

**Question**

> Ai đang hiểu rõ Payment Service?

Routing:

Graph Search

&nbsp;

---

**Question**

> Tại sao team chuyển từ Redis Pub/Sub sang Kafka?

Routing:

Decision Graph

\+

Document Retrieval

&nbsp;

---

**Question**

> Những system nào bị ảnh hưởng nếu Authentication Service ngừng hoạt động?

Routing:

Graph Traversal

&nbsp;

---

# **30\. Evidence-based Answer**

AI phải cung cấp:

Answer

Confidence

Sources

Knowledge Status

Last Verified Date

Owner

&nbsp;

Ví dụ:

> Deployment production hiện được thực hiện thông qua GitHub Actions sau khi có approval từ Platform Team.

**Sources**

* Deployment SOP v4  
* CI/CD Architecture  
* Platform Policy

**Verified:** 10/08/2026  
**Owner:** Platform Team

---

# **31\. Insufficient Evidence Handling**

Nếu evidence không đủ, AI phải tránh hallucination.

Ví dụ:

Confidence: LOW

&nbsp;

Reason:

Only one outdated source found.

&nbsp;

Current verified knowledge:

Not available.

&nbsp;

AI có thể đề xuất:

Ask Knowledge Owner

&nbsp;

hoặc:

Create Knowledge Gap

&nbsp;

---

# **32\. Knowledge Gap Detection**

Knowledge Gap là kiến thức mà tổ chức cần nhưng chưa có nguồn đáng tin cậy.

Hệ thống phát hiện gap thông qua:

Repeated unanswered questions

Missing process documentation

Conflicting answers

Unverified knowledge

Old documentation

Repeated expert escalation

Incident patterns

&nbsp;

---

# **33\. Ví dụ Knowledge Gap**

Người dùng nhiều lần hỏi:

> Khi settlement thất bại thì phải làm gì?

AI tìm thấy:

12 related Slack discussions

4 support tickets

0 verified SOP

3 different suggested solutions

&nbsp;

Hệ thống tạo:

Knowledge Gap

&nbsp;

Topic:

Failed Settlement Handling

&nbsp;

Severity:

High

&nbsp;

Suggested Owner:

Payment Operations

&nbsp;

Evidence:

12 conversations

4 incidents

&nbsp;

---

# **34\. AI Knowledge Interviewer**

AI Knowledge Interviewer là module chuyên khai thác tacit knowledge.

Không giống chatbot thông thường, module này chủ động đặt câu hỏi.

AI trước tiên phân tích:

Known Knowledge

Unknown Knowledge

Process Dependencies

Incident History

Existing Documents

&nbsp;

Sau đó tạo một interview plan.

---

# **35\. Ví dụ AI Interview**

AI phát hiện:

Rollback SOP:

Available

&nbsp;

Emergency rollback:

Missing

&nbsp;

Manual recovery:

Missing

&nbsp;

Incident escalation:

Partially documented

&nbsp;

AI có thể hỏi SME:

> Trong các incident gần đây, có một số trường hợp service health check thất bại nhưng team không rollback ngay. Anh/chị có thể giải thích điều kiện nào khiến team giữ production thay vì rollback không?

---

# **36\. Interview Processing**

Conversation:

AI

&nbsp;↕

Expert

&nbsp;

được chuyển thành:

Transcript

&nbsp;&nbsp;&nbsp;&nbsp;↓

Claim Extraction

&nbsp;&nbsp;&nbsp;&nbsp;↓

Knowledge Object Extraction

&nbsp;&nbsp;&nbsp;&nbsp;↓

Contradiction Detection

&nbsp;&nbsp;&nbsp;&nbsp;↓

Evidence Linking

&nbsp;&nbsp;&nbsp;&nbsp;↓

Proposed Knowledge

&nbsp;&nbsp;&nbsp;&nbsp;↓

Expert Confirmation

&nbsp;

Transcript không tự động trở thành truth.

---

# **37\. Knowledge Conflict Detection**

AI kiểm tra knowledge mới với knowledge hiện tại.

Ví dụ:

Existing:

Restart service immediately.

&nbsp;

New Knowledge:

Never restart service before checking Redis.

&nbsp;

AI tạo:

Potential Conflict

&nbsp;

và yêu cầu xác minh.

---

# **38\. Knowledge Verification Center**

Knowledge Owner có dashboard gồm:

Pending Knowledge

Conflicts

Expired Knowledge

Upcoming Reviews

Reported Issues

AI Suggestions

&nbsp;

Mỗi item có thể:

Approve

Reject

Edit

Request Clarification

Assign Reviewer

Mark Deprecated

&nbsp;

---

# **39\. Knowledge Freshness Engine**

Mỗi knowledge có thể có review interval.

Ví dụ:

Security Policy:

90 days

&nbsp;

Infrastructure Guide:

180 days

&nbsp;

Company Policy:

365 days

&nbsp;

Khi tới review date:

ACTIVE

&nbsp;↓

REVIEW REQUIRED

&nbsp;

AI có thể so sánh knowledge với nguồn mới để phát hiện khả năng đã lỗi thời.

---

# **40\. Knowledge Continuity Radar**

Đây là module dành cho management.

Nó cho thấy những khu vực mà tổ chức đang có nguy cơ mất tri thức.

Ví dụ dashboard:

| Process | Criticality | Coverage | Freshness | Knowledge Concentration | Risk |
| ----- | ----- | ----- | ----- | ----- | ----- |
| Payroll | Critical | 92% | Good | Low | Low |
| Deployment | Critical | 60% | Medium | High | High |
| Refund | High | 81% | Good | Medium | Medium |
| Legacy Billing | High | 31% | Poor | Very High | Critical |

---

# **41\. Knowledge Concentration**

Knowledge Concentration phản ánh một process đang phụ thuộc vào bao nhiêu nguồn độc lập.

Ví dụ:

Process A

&nbsp;

Knowledge owners:

Nguyễn A

Nguyễn B

Lê C

&nbsp;

risk thấp hơn:

Process B

&nbsp;

Knowledge owners:

Nguyễn A

&nbsp;

Tuy nhiên hệ thống đánh giá:

Process Risk

&nbsp;

không đánh giá:

Employee Value

&nbsp;

---

# **42\. Knowledge Coverage**

Một process có thể có nhiều knowledge requirement.

Ví dụ:

Production Deployment

&nbsp;

Deployment Procedure           ✓

Rollback                      ✓

Emergency Rollback            ✗

Monitoring                    ✓

Security Approval             ✓

Manual Recovery               ✗

Incident Escalation           △

&nbsp;

Từ đó hệ thống tính coverage.

---

# **43\. Successor Onboarding Module**

Khi một thành viên mới tiếp nhận responsibility hoặc thay người cũ, Project Manager / Team Leader tạo Successor assignment. Hệ thống xác định:

Successor

&nbsp;↓

Project và Team Membership

&nbsp;↓

Handover Scope / Responsibility

&nbsp;↓

Required Knowledge

&nbsp;↓

Required Skills

&nbsp;

Ví dụ:

Backend Engineer

&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;├── Authentication

&nbsp;&nbsp;&nbsp;├── Database

&nbsp;&nbsp;&nbsp;├── Coding Standard

&nbsp;&nbsp;&nbsp;├── Deployment

&nbsp;&nbsp;&nbsp;├── Monitoring

&nbsp;&nbsp;&nbsp;└── Incident Response

&nbsp;

---

# **44\. Personalized Learning Path**

AI xây dựng learning path dựa trên:

Responsibility Requirements

\+

Current Successor Knowledge

\+

Team Knowledge

\+

Process Criticality

&nbsp;

Hai Successor cùng job title không nhất thiết có cùng takeover plan vì phạm vi responsibility và knowledge gap có thể khác nhau.

---

# **45\. AI Mentor**

Successor có thể hỏi:

> Tôi đang làm module Payment, cần đọc những gì?

AI có thể đưa ra:

1\. Payment Architecture

2\. Payment API Guideline

3\. Refund Process

4\. Settlement Incident History

5\. Payment Deployment Procedure

&nbsp;

với lý do và thứ tự ưu tiên.

---

# **46\. Scenario-based Training**

Hệ thống không chỉ sử dụng quiz lý thuyết.

Ví dụ:

> Payment API latency tăng từ 100ms lên 2s nhưng CPU vẫn bình thường. Redis connection pool đang đạt 98%. Bạn sẽ kiểm tra gì trước?

Successor đưa ra câu trả lời.

AI đánh giá dựa trên:

Verified Knowledge

Incident History

SOP

Best Practices

&nbsp;

---

# **47\. Competency Tracking**

Hệ thống có thể theo dõi:

Knowledge Viewed

Questions Asked

Scenario Completed

Scenario Accuracy

Knowledge Areas Covered

Human Verification

&nbsp;

Không nên chỉ sử dụng:

course completion %

&nbsp;

làm thước đo duy nhất.

---

# **48\. Member Handover / Offboarding Module**

Khi một Team Member hoặc Team Leader chuẩn bị rời project, chuyển team hoặc đổi responsibility, Project Manager / Team Leader khởi tạo handover và hệ thống chạy:

Departing Member (lifecycle state: OFFBOARDING)

&nbsp;↓

Knowledge Graph Analysis

&nbsp;↓

Connected Critical Processes

&nbsp;↓

Existing Knowledge Coverage

&nbsp;↓

Missing Knowledge

&nbsp;↓

Knowledge Transfer Plan và Successor Assignment

&nbsp;

---

# **49\. Departure Knowledge Assessment**

Ví dụ:

Senior DevOps Engineer

&nbsp;

Production Deployment       93%

Monitoring                  87%

Cloud Billing               70%

Legacy Infrastructure       31%

VPN Setup                   18%

&nbsp;

AI ưu tiên interview về:

Legacy Infrastructure

VPN Setup

&nbsp;

thay vì yêu cầu Departing Member viết lại mọi thứ.

---

# **50\. Knowledge Transfer Interview**

AI tạo những câu hỏi chính xác dựa trên gap.

Ví dụ:

> Trong Legacy Monitoring hiện tại, những lỗi nào không thể phát hiện bằng dashboard?

> Có thao tác maintenance nào hiện chỉ anh/chị biết thực hiện?

> Nếu monitoring server mất hoàn toàn, recovery sequence hiện tại là gì?

---

# **51\. Decision Memory**

Continuum AI phải lưu lại lý do doanh nghiệp đưa ra quyết định.

Ví dụ:

Decision:

Migrate MongoDB → PostgreSQL

&nbsp;

Context:

Transaction consistency problems

&nbsp;

Alternatives:

MongoDB

PostgreSQL

CockroachDB

&nbsp;

Selected:

PostgreSQL

&nbsp;

Reason:

Transaction support

Operational familiarity

Lower migration risk

&nbsp;

Related:

Incident \#241

ADR-019

&nbsp;

Sau này AI có thể trả lời:

> Tại sao công ty không tiếp tục sử dụng MongoDB?

---

# **52\. Incident Memory**

Incident là nguồn kiến thức rất quan trọng.

Hệ thống có thể liên kết:

Incident

&nbsp;↓

Root Cause

&nbsp;↓

Resolution

&nbsp;↓

Lesson Learned

&nbsp;↓

Affected System

&nbsp;↓

Related Process

&nbsp;

Một incident đã giải quyết trong quá khứ trở thành knowledge cho các sự cố tương lai.

---

# **53\. Permission Model**

Knowledge của doanh nghiệp không phải ai cũng được truy cập.

Permission hiệu lực được xác định từ:

Persistent Project Role

Project Membership

Team Membership

Scoped SME / Knowledge Owner / Successor Assignment

Membership Lifecycle State

Knowledge Object ACL

Source Document ACL

Explicit Deny

&nbsp;

---

# **54\. Permission-aware Retrieval**

Permission phải được kiểm tra trước khi retrieval.

User Query

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Identity

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Authorization

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Allowed Knowledge Scope

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Retrieval

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

LLM

&nbsp;

Không được:

Retrieve everything

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

LLM

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Remove restricted data

&nbsp;

vì nội dung nhạy cảm đã được đưa vào model context.

---

# **55\. Source Permission Inheritance**

Nếu document gốc chỉ cho phép Finance Team truy cập:

Document

permission \= Finance

&nbsp;

Knowledge được extract từ document mặc định phải kế thừa:

Knowledge

permission \= Finance

&nbsp;

trừ khi Knowledge Owner thay đổi rõ ràng.

---

# **56\. Audit Logging**

Các hành động quan trọng phải được ghi audit:

Knowledge created

Knowledge edited

Knowledge verified

Knowledge rejected

Permission changed

Data exported

Connector added

AI answer generated

Sensitive knowledge accessed

&nbsp;

Audit record gồm:

actor

action

resource

timestamp

ip/device where applicable

before\_value

after\_value

&nbsp;

---

# **57\. Kiến trúc hệ thống tổng thể**

Sơ đồ dưới đây mô tả các trách nhiệm logic, không yêu cầu triển khai mỗi khối thành một microservice riêng. MVP dùng NestJS cho Continuum Core API, MongoDB cho domain state, SAG/LanceDB cho retrieval index và Redis/BullMQ cho background jobs.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;CLIENT LAYER

&nbsp;

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Web / Mobile / Chat

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;API GATEWAY

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;┌────────────┼─────────────┐

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│            │             │

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼            ▼             ▼

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Auth         Knowledge      Admin

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Service        Service       Service

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;AI ORCHESTRATOR

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;┌───────────────┼────────────────┐

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│               │                │

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼               ▼                ▼

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Retrieval       Knowledge        Interview

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Engine         Extraction        Engine

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│               │                │

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└───────────────┼────────────────┘

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;KNOWLEDGE LAYER

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;┌───────────────┼────────────────┐

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼               ▼                ▼

&nbsp;&nbsp;&nbsp;MongoDB           LanceDB        Graph Layer

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└───────────────┼────────────────┘

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;INGESTION PIPELINE

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;┌────────────────┼───────────────┐

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼                ▼               ▼

&nbsp;&nbsp;&nbsp;Documents         SaaS Apps       Internal Data

&nbsp;

---

# **58\. AI Orchestrator**

AI Orchestrator chịu trách nhiệm quyết định:

cần dùng model nào

cần retrieval nào

có cần graph query không

có cần tool execution không

có cần permission check không

có cần human verification không

&nbsp;

Nó không phải một autonomous agent hoàn toàn.

Trong MVP nên sử dụng deterministic workflow ở phần quan trọng.

---

# **59\. Data Layer**

Hệ thống có thể chia thành các nhóm dữ liệu.

### **Identity Data**

Project

User

Team

Project Membership

Team Membership

Persistent Role Assignment

SME Assignment

Knowledge Owner Assignment

Successor / Handover Assignment

Membership Lifecycle State

Permission

&nbsp;

### **Source Data**

Document

Document Version

Source

Connector

Chunk

&nbsp;

### **Knowledge Data**

Knowledge Object

Knowledge Version

Claim

Evidence

Knowledge Owner

Verification

&nbsp;

### **Graph Data**

Entity

Relationship

Temporal Relationship

&nbsp;

### **Learning Data**

Learning Path

Knowledge Requirement

Assessment

Scenario

Progress

&nbsp;

### **Analytics Data**

Query Log

Knowledge Usage

Gap

Coverage

Risk

&nbsp;

---

# **60\. Logical Database Structure**

Ví dụ:

organizations

&nbsp;

users

&nbsp;

teams

&nbsp;

roles

&nbsp;

permissions

&nbsp;

documents

&nbsp;

document\_versions

&nbsp;

document\_chunks

&nbsp;

knowledge\_objects

&nbsp;

knowledge\_versions

&nbsp;

knowledge\_sources

&nbsp;

knowledge\_verifications

&nbsp;

knowledge\_conflicts

&nbsp;

entities

&nbsp;

knowledge_relations

&nbsp;

processes

&nbsp;

knowledge\_requirements

&nbsp;

knowledge\_gaps

&nbsp;

interviews

&nbsp;

interview\_sessions

&nbsp;

interview\_claims

&nbsp;

learning\_paths

&nbsp;

assessments

&nbsp;

incidents

&nbsp;

decisions

&nbsp;

audit\_logs

&nbsp;

---

# **61\. Vector Storage**

Vector index được sử dụng cho:

document chunks

knowledge objects

incident descriptions

questions

decision records

&nbsp;

Không nên sử dụng vector database như nguồn truth chính.

Vector database chỉ phục vụ:

semantic retrieval

&nbsp;

Nguồn truth nằm trong structured data layer.

---

# **62\. Graph Storage**

Trong giai đoạn đầu, graph nghiệp vụ của Continuum có thể được lưu trong MongoDB qua các collection có reference và index theo project/team scope, ví dụ:

entities

knowledge_relations

&nbsp;

Không bắt buộc sử dụng Neo4j ngay.

Khi graph traversal trở nên lớn và phức tạp, hệ thống có thể migrate sang graph database chuyên dụng.

---

# **63\. File Storage**

Raw documents nên được lưu trong object storage.

Ví dụ:

S3

Cloudflare R2

MinIO

&nbsp;

Database chỉ lưu metadata và object path.

---

# **64\. AI Model Strategy**

Hệ thống không nên phụ thuộc hoàn toàn vào một LLM.

AI Provider Layer nên hỗ trợ:

Model A

Model B

Model C

&nbsp;

theo abstraction:

LLM Gateway

&nbsp;

để có thể thay đổi provider dựa trên:

cost

latency

context size

privacy

quality

&nbsp;

---

# **65\. AI Task Classification**

Không phải mọi task cần model mạnh nhất.

Ví dụ:

| Task | Model requirement |
| ----- | ----- |
| Intent classification | Small |
| Entity extraction | Small/Medium |
| Query rewrite | Small |
| Knowledge extraction | Medium |
| Interview reasoning | Strong |
| Conflict analysis | Strong |
| Final complex answer | Strong |
| Embedding | Embedding model |

---

# **66\. Human-in-the-loop**

AI được phép:

extract

suggest

detect

classify

summarize

recommend

&nbsp;

nhưng các hành động có ảnh hưởng lớn đến organizational truth phải có human confirmation.

Ví dụ:

Verify knowledge

Change policy

Resolve conflict

Deprecate critical procedure

Modify permission

&nbsp;

---

# **67\. Yêu cầu hiệu năng**

Đối với câu hỏi thông thường, hệ thống nên hướng tới:

Search retrieval:

\< 2 seconds

&nbsp;

Normal AI response:

2–8 seconds

&nbsp;

Complex graph reasoning:

5–15 seconds

&nbsp;

Background processing như ingestion hoặc extraction có thể chạy asynchronous.

---

# **68\. Yêu cầu khả năng mở rộng**

Kiến trúc phải có khả năng hỗ trợ:

10 users

100 users

1,000 users

10,000 users

&nbsp;

mà không phải thay đổi toàn bộ kiến trúc.

Các workload nặng như:

OCR

embedding

document extraction

knowledge extraction

&nbsp;

nên được xử lý qua worker queue.

---

# **69\. Reliability**

Nếu AI provider unavailable:

Knowledge Search

&nbsp;

vẫn nên hoạt động ở mức cơ bản.

Nếu extraction pipeline thất bại, raw document không được mất.

Job phải hỗ trợ:

retry

dead letter

status tracking

idempotency

&nbsp;

---

# **70\. Security**

Hệ thống phải hỗ trợ tối thiểu:

TLS

JWT/OAuth

RBAC

Encryption at Rest

Encryption in Transit

Audit Logs

Permission-aware Retrieval

Secret Management

Session Management

Rate Limiting

&nbsp;

---

# **71\. Privacy**

Interview transcript có thể chứa thông tin cá nhân hoặc confidential information.

Do đó hệ thống phải cho phép:

retention policy

raw transcript deletion

knowledge anonymization

PII removal

access restriction

&nbsp;

Knowledge được giữ lại nên ưu tiên mô tả kiến thức tổ chức thay vì thông tin cá nhân không cần thiết.

---

# **72\. Observability**

Hệ thống phải theo dõi:

API latency

LLM latency

LLM cost

retrieval latency

token usage

failed jobs

connector errors

embedding queue

knowledge extraction failures

&nbsp;

Ngoài technical metrics cần có AI metrics:

answer confidence

citation coverage

retrieval quality

knowledge acceptance rate

conflict rate

&nbsp;

---

# **73\. Knowledge Quality Metrics**

Hệ thống cần đo:

Verified Knowledge Ratio

&nbsp;

Knowledge Freshness

&nbsp;

Knowledge Coverage

&nbsp;

Unresolved Knowledge Gaps

&nbsp;

Knowledge Conflict Rate

&nbsp;

Knowledge Usage Rate

&nbsp;

---

# **74\. Business Metrics**

Các metric quan trọng hơn chatbot accuracy gồm:

### **Time-to-Information**

Trước:

15 minutes

&nbsp;

Sau:

2 minutes

&nbsp;

### **Expert Interruption Rate**

Số câu hỏi SME nhận trực tiếp.

### **Time-to-Competence**

Thời gian nhân viên mới có thể tự xử lý công việc.

### **Knowledge Coverage**

Tỷ lệ critical process đã có verified knowledge.

### **Knowledge Reuse**

Một knowledge được sử dụng bao nhiêu lần.

---

# **75\. Continuity Risk Model**

Một mô hình conceptual:

Continuity Risk

\=

Process Criticality

×

Knowledge Concentration

×

Knowledge Gap

×

Knowledge Staleness

&nbsp;

Trong đó:

**Process Criticality**

Mức độ quan trọng của process.

**Knowledge Concentration**

Tri thức tập trung vào bao nhiêu nguồn.

**Knowledge Gap**

Mức thiếu hụt documentation/verified knowledge.

**Knowledge Staleness**

Mức độ knowledge có nguy cơ lỗi thời.

---

# **76\. Main Workflow – Knowledge Ingestion**

Data Source

&nbsp;&nbsp;&nbsp;↓

Connector

&nbsp;&nbsp;&nbsp;↓

Document Processing

&nbsp;&nbsp;&nbsp;↓

Chunking

&nbsp;&nbsp;&nbsp;↓

Embedding

&nbsp;&nbsp;&nbsp;↓

Knowledge Extraction

&nbsp;&nbsp;&nbsp;↓

Entity Extraction

&nbsp;&nbsp;&nbsp;↓

Relationship Extraction

&nbsp;&nbsp;&nbsp;↓

Proposed Knowledge

&nbsp;&nbsp;&nbsp;↓

Verification

&nbsp;&nbsp;&nbsp;↓

Active Knowledge

&nbsp;

---

# **77\. Main Workflow – Project Member / Successor Question**

Project Member hoặc Successor

&nbsp;&nbsp;&nbsp;↓

Question

&nbsp;&nbsp;&nbsp;↓

Identity, Project/Team Membership, Assignment và Resource ACL

&nbsp;&nbsp;&nbsp;↓

Intent Detection

&nbsp;&nbsp;&nbsp;↓

Query Planning

&nbsp;&nbsp;&nbsp;↓

Hybrid Retrieval

&nbsp;&nbsp;&nbsp;↓

Evidence Reranking

&nbsp;&nbsp;&nbsp;↓

Knowledge Validation

&nbsp;&nbsp;&nbsp;↓

LLM

&nbsp;&nbsp;&nbsp;↓

Answer \+ Citation

&nbsp;

---

# **78\. Main Workflow – Knowledge Gap Resolution**

Repeated Question

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

No Verified Answer

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Gap Detection

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Knowledge Gap

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Team Leader xác nhận phạm vi và giao Knowledge Owner / SME

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Knowledge Owner / SME trả lời hoặc tham gia AI Interview

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Knowledge Extraction

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Human Verification bởi người có thẩm quyền trong phạm vi

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Gap Resolved

&nbsp;

---

# **79\. Main Workflow – Successor Takeover**

Successor được Project Manager / Team Leader chỉ định

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Team Membership và phạm vi handover được gán

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Hệ thống tổng hợp Knowledge Transfer Package theo phạm vi

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Successor thực hiện Initial Readiness Assessment

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Knowledge Gap theo handover assignment

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Takeover Learning Path

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

AI Assistant với citation và kiểm tra quyền trước retrieval

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Scenario Assessment

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Takeover Readiness Progress

&nbsp;

---

# **80\. Main Workflow – Member Handover / Offboarding**

Project Manager / Team Leader khởi tạo handover

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Departing Member được gắn lifecycle state OFFBOARDING

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Phân tích knowledge, responsibility và dependency của thành viên

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Kiểm tra mức độ bao phủ và freshness của knowledge

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Tạo handover items cho knowledge còn thiếu

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Knowledge Owner / Departing Member cập nhật tài liệu hoặc tham gia AI Interview

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Team Leader / SME xác minh theo phạm vi

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Knowledge Transfer Package được gán cho Successor

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

Successor xác nhận tiếp nhận; Project Manager / Team Leader đóng handover

&nbsp;

---

# **81\. Những chức năng không thuộc MVP**

Giai đoạn đầu không nên xây:

Autonomous AI Agent thực hiện nghiệp vụ quan trọng

&nbsp;

Fine-tuning LLM riêng cho mỗi doanh nghiệp

&nbsp;

Full LMS

&nbsp;

Employee performance scoring

&nbsp;

Automatic organizational restructuring

&nbsp;

Automatic policy modification

&nbsp;

Full Business Process Management system

&nbsp;

Những chức năng này làm tăng scope nhưng không giúp kiểm chứng core value proposition.

---

# **82\. MVP đề xuất**

MVP nên tập trung vào:

Project, User & Membership Management

&nbsp;

Persistent Role, Team & Scoped Assignment Management

&nbsp;

Document Upload

&nbsp;

Google Drive Integration

&nbsp;

Document Parsing

&nbsp;

OCR

&nbsp;

Vector Search

&nbsp;

AI Knowledge Assistant

&nbsp;

Citation

&nbsp;

Knowledge Object Extraction

&nbsp;

Knowledge Verification

&nbsp;

Knowledge Graph

&nbsp;

Knowledge Gap Detection

&nbsp;

AI Knowledge Interview

&nbsp;

Knowledge Continuity Dashboard

&nbsp;

Successor Takeover

&nbsp;

Member Handover / Offboarding

&nbsp;

---

# **83\. Điểm khác biệt cốt lõi**

Continuum AI không định vị là:

Document Chatbot

&nbsp;

cũng không chỉ là:

Company Wiki

&nbsp;

hay:

AI LMS

&nbsp;

mà là:

# **Organizational Knowledge Continuity System**

Sự khác biệt nằm ở vòng lặp:

KNOWLEDGE EXISTS

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

KNOWLEDGE DISCOVERED

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

KNOWLEDGE STRUCTURED

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

KNOWLEDGE VERIFIED

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

KNOWLEDGE USED

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

KNOWLEDGE GAP DISCOVERED

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

NEW KNOWLEDGE CAPTURED

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓

ORGANIZATIONAL MEMORY IMPROVES

&nbsp;

---

# **84\. Giá trị cuối cùng của hệ thống**

Sau một thời gian hoạt động, hệ thống không đơn giản biết:

> Công ty đang có những file nào?

Nó bắt đầu hiểu:

Công ty có những process nào.

&nbsp;

Process nào phụ thuộc vào system nào.

&nbsp;

Team nào chịu trách nhiệm.

&nbsp;

Ai có expertise ở lĩnh vực nào.

&nbsp;

Quyết định nào đã được đưa ra.

&nbsp;

Tại sao quyết định đó tồn tại.

&nbsp;

Incident nào từng xảy ra.

&nbsp;

Bài học nào được rút ra.

&nbsp;

Knowledge nào còn hiệu lực.

&nbsp;

Knowledge nào đang lỗi thời.

&nbsp;

Knowledge nào đang thiếu.

&nbsp;

Knowledge nào đang mâu thuẫn.

&nbsp;

Process nào đang có continuity risk.

&nbsp;

---

# **85\. Tầm nhìn hệ thống**

Ở giai đoạn đầu:

Continuum AI

\=

Knowledge Management

\+

AI Search

\+

Knowledge Capture

&nbsp;

Ở giai đoạn tiếp theo:

Continuum AI

\=

Organizational Memory

&nbsp;

Và về dài hạn:

Continuum AI

\=

Enterprise Context Layer

&nbsp;

cho cả:

Human Employees

\+

AI Agents

&nbsp;

Khi AI Agent cần thực hiện một hành động cho doanh nghiệp, nó không thể chỉ dựa trên general knowledge của LLM.

Nó cần hiểu:

company policies

process

responsibility

permissions

historical decisions

exceptions

dependencies

current organizational state

&nbsp;

Continuum AI có thể trở thành lớp context cung cấp toàn bộ thông tin đó.

---

# **86\. Định nghĩa cuối cùng của dự án**

**Continuum AI là một nền tảng quản trị và duy trì tri thức tổ chức sử dụng Artificial Intelligence, Retrieval-Augmented Generation, Knowledge Graph và Human-in-the-loop Verification nhằm thu thập, cấu trúc, xác minh, liên kết và tái sử dụng tri thức doanh nghiệp.**

Khác với hệ thống quản lý tài liệu truyền thống, Continuum AI không xem document là đơn vị tri thức duy nhất mà xây dựng một lớp Organizational Memory gồm kiến thức, quy trình, quyết định, sự cố, hệ thống, con người và mối quan hệ giữa chúng.

Hệ thống có khả năng chủ động phát hiện knowledge gap, knowledge conflict, knowledge staleness và knowledge concentration; từ đó sử dụng AI Knowledge Interviewer để khai thác tri thức ngầm từ các Subject Matter Expert trước khi kiến thức đó bị mất.

Organizational Memory sau khi được human verification có thể được sử dụng để hỗ trợ nhân viên tìm kiếm thông tin, giải quyết công việc, đào tạo nhân viên mới, chuyển giao kiến thức khi nhân viên nghỉ việc và đánh giá rủi ro liên tục đối với các process quan trọng.

Mục tiêu cuối cùng của Continuum AI không đơn thuần là giúp nhân viên **tìm thông tin nhanh hơn**, mà là giúp tổ chức:

> **duy trì khả năng vận hành và khả năng học hỏi ngay cả khi con người, công nghệ và quy trình liên tục thay đổi.**

&nbsp;
