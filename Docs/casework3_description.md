# ISYE 6202 Supply Chain Facilities

**Professor**: Benoit Montreuil  

**Casework 3**  
**FeMoaSa Manufacturing & Warehousing Facility Design**

- **Due date**: Due at the latest on **November 12th, 2025, at 23h55**
- **Team**: To be realized solo or in teams of up to 6 students, with no impact on evaluation
- **Weight**: 20%

A worksheet is provided with all Tables and Basic Layouts depicted in this document.

Deliverables should be well documented, with joined files as pertinent (software, spreadsheets, drawings, simulations, etc.), yet not forcing to rely on the joined files to evaluate the core of your deliverables.

---

## Overall Context and Mission

FaMoaSa는 고객사 전용 공장과 창고를 구축하는 **부품 제조 서비스 제공업체**로,  
고객사의 조립 공장 인근에 공장과 창고를 설치하여, 요구되는 제품을 **신속하고 안정적으로 적시(in-time)** 방식으로 공급하는 데 특화되어 있다.

지금까지 FaMoaSa는 자사가 구축한 공장들을 대부분 **job shop**으로 간주해 왔으며,  
그에 따라 항상 **기능 중심(function organization)** 구조로 공장을 설계해 왔다.

최근 FaMoaSa의 리더들은 다음과 같은 이유로 인해 자사의 제조 및 물류 역량과 서비스 성과 잠재력을 제한하고 있을 수 있다는 사실을 인지하게 되었다.

1. 공장을 기능 조직으로만 설계해 왔으나, 특정 경우에 더 적절할 수 있는 **다양한 조직 설계 옵션**이 존재한다는 점  
2. 공장 조직 방식은 각 고객사 인근에 일반적으로 위치하는 **창고의 규모와 성능**에 영향을 미친다는 점

FaMoaSa는 현재 고객사 A와 B를 위해 구축한 공장과 창고를 **테스트베드(testbed)**로 선택하여,  
대체 조직 설계가 미치는 영향을 평가하고자 한다.

이 공장은 남북 방향 고속도로를 따라 건설되어 있으며,  
고객사 A의 제품 조립 공장은 북쪽으로 90마일,  
고객사 B의 제품 조립 공장은 남쪽으로 110마일 떨어져 있다.  

현재 FaMoaSa는 고객사 A와 B 각각에 전용으로 운영되는 **두 개의 창고**를 가지고 있으며,  
각 창고는 해당 고객사의 조립 공장 부지 인근에 위치해 있다.

FaMoaSa는 이 테스트베드를 활용하여 **대체적인 시설 조직 설계(facility organization designs)**의 잠재력을 엄밀하게 평가하는 데 도움을 요청하고 있다.  
리더십은 귀하의 팀이 FaMoaSa 내부의 역사와 기존 패러다임에 물들지 않은 **“fresh look”**을 제공하기를 원하며, 그 때문에 이 연구를 수행하는 동안 일정 부분 거리를 두고자 한다.

따라서, 귀하의 팀에게는 이 테스트베드를 위한 핵심 기능 및 기술 사양만이 제공되고,  
FaMoaSa의 고객사 A와 B에 관한 정보나,  
3년 전 FaMoaSa 팀이 이 고객사를 위해 설계·구축한 공장에 대한 정보는 **일절 제공되지 않는다.**

---

## Year +1 Demand Forecast and Performance Expectations from Client

FaMoaSa의 테스트베드 공장은 미국에 위치해 있으며,  
다음 두 고객사를 위한 부품을 생산한다.

- 고객사 A: 제품 **A1 ~ A3** 조립 공장
- 고객사 B: 제품 **B1 ~ B2** 조립 공장

두 고객사는 Year +1 기간(1월 1일부터 12월 21일까지, 12개월)에 대해 다음과 같은 수요 예측 정보를 제공하였다.

1. 먼저, 각 제품별 **예상 연간 수요(annual demand forecast)**  
2. 둘째, Year +1 동안 각 제품별 실제 조립 수량에는 불확실성이 존재하므로,  
   제공된 예측값을 중심으로 한 **Year +1 실제 수요의 기대 표준편차(expected standard deviation)**

> (원문에는 여기서 각 제품에 대한 연간 수요와 표준편차를 포함한 **수치 표(Table)**가 제시된다. 해당 표는 수치 그대로 활용하면 된다.)

3. 셋째, 두 고객사 모두 조립 공장 수요에 **계절성(seasonality)**이 없다고 보기 때문에,  
   각 제품의 **예상 평균 주간 수요(average weekly demand)**를 제공했으며,  
   이는 단순히 연간 수요 예측을 52주로 나눈 값이다.

4. 넷째, 실제 조립 생산량은 이 주간 평균값 주변에서 변동할 것이므로,  
   각 제품의 Year +1 **주간 수요 변동계수(coefficient of variation of weekly demand)**를 제공했다.

5. 다섯째, 두 고객사의 주간 조립 일정은 매우 평탄화(smoothing)되어 있어,  
   주간 수요는 **주 5일, 하루 2교대, 각 교대 8시간**으로 고르게 분배된다고 명시하였다.

---

FaMoaSa의 고객사 A와 B는, 각각 다음 제품들을 조립한다.

- 고객사 A: A1, A2, A3  
- 고객사 B: B1, B2  

이들 제품은 모두 FaMoaSa 부품 공장이 공급하는 **20개 부품(Parts)**으로부터 조립된다.

아래는 이들 제품에 대한 **Product–Parts 매트릭스**이다.

> (원문에는 각 제품(A1~A3, B1~B2)과 20개 부품(P1~P20) 사이의 관계를 나타내는 매트릭스(표)가 제시된다.)

---

고객사 A와 B는 각각 각 부품에 대해 다음과 같은 **버퍼 재고(buffer)**를 유지한다.

- 고객사 A: 각 부품별로 **4시간 동안 99% 자율성(autonomy)**을 보장하는 버퍼  
- 고객사 B: 각 부품별로 **12시간 동안 99% 자율성**을 보장하는 버퍼  

두 고객사는 자신의 조립 공장이 운영되는 교대 시간 동안,  
FaMoaSa 부품 공장으로부터 **지속적인 보충(replenishment)**을 요청한다.

보충 주기:

- 고객사 A: **매 1시간**마다 보충  
- 고객사 B: **매 4시간**마다 보충  

요구되는 서비스 수준:

- On-Time In-Full(**OTIF**) 보충 서비스 수준 **99.5%**

이를 초과하는 0.5% 이상의 지연 보충이 발생할 경우 **금전적 페널티**가 부과되며,  
어떤 제품이든 조립이 중단되면 **추가 페널티**가 발생한다.

따라서, 부품 공장은 이 **서비스 수준 협약(Service Level Agreement, SLA)**을  
**강건하게(robustly)** 충족하도록 설계되어야 한다.

---

## Testbed Factory Specifications

FaMoaSa의 부품 공장은 다음과 같이 운영된다.

- 하루 8시간 기준 **1교대 또는 2교대**
- 주 5일 운영

반면, 창고는 두 고객사와 동일하게:

- 하루 8시간, **2교대**
- 주 5일 운영

FaMoaSa는 주요 혼란(disruptions) 상황에서는 초과근무(overtime)나 추가 교대(extra shifts)를 활용할 수 있다고 알고 있으나,  
정상적인 운영에서는 **추가 근무 시간이나 추가 근무일이 필요하지 않도록** 공장을 설계하고자 한다.

아래에는 FaMoaSa가 제조하는 부품들에 대한 정보가 제공된다.

- 각 부품 ID(Identifier)  
- X, Y, Z(높이, inch 단위) 치수  
- 무게(lbs)  
- 단위당 재료비(Materials cost, Price per unit)

> (원문 표 예시: P1 ~ P20까지 각 부품의 Dimensions(X, Y, Z), Weight, Price/unit가 행 단위로 제시된다.)

---

각 부품의 재료(Materials)는 FaMoaSa의 **자재 공급 센터(Materials Supply Center, MSC)**에서  
부품 공장으로 **100개 단위 키트(100-part kits)** 형태로 공급된다.

- 각 키트의 총 무게와 부피는 개별 부품 무게 및 부피 합의 **150%**

여러 다른 FaMoaSa 공장과 마찬가지로,  
테스트베드 공장은 MSC로부터 각 부품별로 **주 1회** inbound 공급을 받는다.  
MSC는 공장에서 **250마일** 떨어져 있다.

공장은 **99.9% 강건성을 갖는 2주치 재고(two-week materials inventory)**를 유지하는 것을 목표로 한다.

---

부품 포트폴리오를 생산하기 위해, FaMoaSa는 **A부터 M까지 13개 공정(processes A to M)**을 수행할 수 있는 설비를 갖추어야 한다.

다음 표는 각 부품별 제조 공정을 제공하며, 각 단계에서 수행해야 할 작업 유형을 나타낸다.

- 각 부품의 자재 키트(materials kit)는 제조 공정의 첫 단계의 입력물로 투입되며,  
  부품이 공정을 통과하는 동안 함께 이동한다.

> (원문 표 예시: P1~P20에 대해 Step1~Step7까지 어떤 공정(A,B,C,…M)이 수행되는지 행렬 형태로 제시된다.)

---

각 공정 단계에서, 아래 표는 **단위당 처리 시간(process time in minutes per unit)**을 제공한다.

FaMoaSa는 모든 장비에 대해 다음을 가정한다.

- **효율(Efficiency)**: 90%  
- **신뢰성(Reliability)**: 98%  
- 각 작업에서 **품질(quality)**: 100%

> (원문에는 각 부품별, 각 공정 단계별 처리 시간이 분 단위로 제시된 표가 포함된다.)

---

각 공정(operation)을 수행하기 위해서는 **전문화된 장비(specialized equipment)**가 필요하며,  
이들 장비는 **전문 작업자(expert operators)**에 의해 운영되어야 한다.

다음 표는 시장에서 사용 가능한 장비 포트폴리오를 제시한다.

- 각 장비는 수행할 수 있는 공정(operation) 조합을 나타내는 **문자 코드(letter code)**로 식별된다.  
  - 예: `CD` 장비는 공정 C와 D를 수행 가능
- 표에는 각 장비 유형에 대해 다음 정보가 포함된다.
  - 설치 가격(Installed price)  
  - 공장 내에서 장비를 재배치(relocate)할 때마다 발생하는 예상 비용(Relocation cost)  
  - 장비의 기대 수명(Useful life, years)  
  - 각 장비 유닛당 요구되는 작업자 수와 타입(Operators: C1, C2, C3)

> (원문 표 예시: A, B, C, D, AB, AC, CD, ABC, ABCD, E, F, G, EF, EG, FG, EFG, H, I, J, IJ, K, L, M, KL, KM, LM, KLM에 대해 Installed price, Relocation cost, Useful life, Number of operators 구성이 제시된다.)

---

각 장비 유형은 상이한 수준의 **인력 구성(staffing level)**을 요구한다.

FaMoaSa는 세 종류의 작업자(operator)를 보유한다.

- C1  
- C2  
- C3  

위 장비 표에는 각 장비가 특정 센터에 설치되었을 때,  
각 작업자 유형별로 얼마나 요구되는지가 명시되어 있다.

예를 들어,

- A 장비는
  - C1 작업자 1명  
  - C2 작업자 0.25명 (1/4 FTE)  
  의 상주(full-time equivalent)를 필요로 한다.

작업자의 분수 단위(Fraction) 인력은 **같은 센터 내에서는 공유 가능**하지만,  
서로 다른 센터 간에는 공유할 수 없다.  
(단, 홀로그래픽 공장과 같이 작은 인접 센터들 사이에서는 예외적으로 공유 가능)

경험에 따르면, 작업자들은 휴일, 병가, 휴가를 고려하여  
연간 52주 중 **49주 근무**하는 것으로 가정한다.

다음 표는 각 작업자 유형에 대한 **시간당 비용(hourly cost)**을 제공하며,  
여기에는 급여(salary), 복리후생(benefits), 지원 비용(support)이 포함된다.

- C1: $40 / hour  
- C2: $75 / hour  
- C3: $100 / hour

---

이후에는 각 장비 카테고리(A–B–C–D, E–F–G, H–I–J, K–L–M)에 대한 **레이아웃 도식(layout schematics)**이 제공된다.

각 도식은 다음을 나타낸다.

- 장비 유닛의 형상(shape)  
- 작업자의 전형적인 위치  
- 자재/부품의 inbound 구역  
- 재공품(work-in-process) 또는 완제품의 outbound 구역  
- 유지보수 공간(maintenance access)으로 비워 둬야 하는 영역

이 도식들은 **참고용(indicative)**이며,  
타당하다면 이를 개선 또는 변경할 수 있다.

---

도식에서:

- 실선(full lines)은 다른 장비 유닛과 공유할 수 없는 **엄격한 경계(rigid boundaries)**를 의미한다.  
- 점선(dotted lines)은 적절한 경우 인접 장비 유닛과 **공유 가능한 영역(sharable areas)**을 의미한다.

---

### Material Handling

위에서 정의된 각 장비 구역(zone) 내에서의 자재 입출(inbound to outbound) 취급은  
해당 장비에 할당된 **작업자(operator)**가 수행한다.

센터 간 또는 비인접 장비 구역 간의 자재 키트 및 부품 운송은  
**핸들러(handler)**에 의해 수행되며, 이들의 비용은 다음과 같다.

- 시간당 $40 (C1 작업자와 동일)

귀하는 다음 항목에 대해 제안하고, 대략적인 가격을 조사해야 한다.

- 취급/저장 장치(handling/storage units)  
- 차량(vehicles)  
- 랙(racking) 등

---

### Building and Financial Assumptions

- 공장 건물 구현(implementation) 비용: **$250 / ft²**  
- 장비는 수명 종료 시 무시할 만한 잔존 가치(negligible residual value)로 가정  
- FaMoaSa는 재고를 포함한 금융 비용(financial expenses)에 대해 **10% 이자율**을 사용

---

## Task 1

고객의 수요 예측 정보와 서비스 성능 기대치를 활용하여,  
Year +1 기간 동안 전체 FaMoaSa 공장에서 **각 부품별 수요 충족 역량(demand fulfillment capacity)** 계획을 수립하라.

---

## Task 2

Year +1 기간에 대해 각 부품에 대한 **완제품 저장 용량(finished storage capacity)** 계획을 수립하고,  
각 부품의 저장량을 다음 장소들 사이에 어떻게 배분할지 제안하라.

- 공장 내 출고 저장(outbound storage in the factory)  
- 고객사 A 인근 창고  
- 고객사 B 인근 창고  

이를 통해 서비스 수준 협약(SLA)이 강건하게 준수되도록 해야 한다.

- 세 위치 모두를 반드시 사용해야 하는 것은 아니다.

가정:

- 부품은 **표준 랙(standard racking)**에 보관하며, 자동 저장·취급 설비는 사용하지 않는다.
- 고객사 인근 저장 건물(near-client storage buildings)을 사용할 경우:
  - 내부 사용 가능 높이(usable height): 20 feet  
  - 건물 비용: $200 / ft²  

---

## Task 3

Year +1 계획 기간 동안 고객사의 수요를 충족시키기 위한  
다음 **여덟 가지 대체 부품 공장(Alternative parts factories)**를 고려하라.

### (a) Function organization

- 공장을 **단일 공정 전용 센터(elementary-process-dedicated centers)**들의 네트워크로 구성  
- 각 공정마다 하나의 센터  
- receiving, inbound storage, outbound storage, shipping에 특화된 센터 포함

### (b) Process organization

- 공장을 **복합 공정 전용 센터(composite-process-dedicated centers)**들의 네트워크로 구성  
- 각 복합 프로세스마다 하나의 센터  
- receiving, inbound storage, outbound storage, shipping 포함

### (c) Parts organization

- 공장을 **부품 전용 센터(part-dedicated centers)**들의 네트워크로 구성  
- 각 부품당 하나의 센터  
- receiving, storage, shipping 공정을 각각의 부품 센터에 포함시켜도 되고,  
  이 공정들에 대해 다른 조직 구조를 제안해도 된다.

### (d) Group organization

- 공장을 **부품 그룹 전용 생산 센터(parts-group-dedicated production centers)**들의 네트워크로 구성  
- 각 부품은 정확히 하나의 그룹 센터에 할당  
- receiving, inbound/outbound storage, shipping 공정을 각 그룹 센터에 포함시키거나,  
  이들 공정에 대한 별도의 조직 구조를 제안해도 된다.

### (e) Product organization

- 공장을 **제품 전용 생산 센터(product-dedicated production centers)**들의 네트워크로 구성  
- 각 센터는 해당 고객 제품에 필요한 모든 부품을 생산  
- receiving, inbound/outbound storage, shipping 공정을 각 제품 센터에 포함시키거나,  
  이들에 대해 다른 조직을 제안할 수 있다.

### (f) Fractal organization

- 공장을 **프랙탈 센터(fractal centers)**들의 네트워크로 구성  
- 각 프랙탈 센터는 모든 제품을 생산할 수 있으며,  
  공장이 제공해야 할 전체 수요 충족 능력의 약 `1/f` 수준을 담당  
- receiving, inbound/outbound storage, shipping을 각 프랙탈 센터에 포함시키거나,  
  이들 공정에 대해 다른 조직을 제안할 수 있다.

### (g) Holographic organization

- 공장을 **소규모, 집중 공정 센터(small, focused process centers)**들의 네트워크로 구성  
  - elementary 또는 composite processes 포함 가능  
- 이들 센터 대부분은 공장 전반에 여러 인스턴스로 분산 배치되며,  
  전체적으로 요구되는 용량으로 모든 제품을 생산할 수 있어야 한다.

### (h) Free-style organization

- (a)~(g)로부터 학습한 내용을 바탕으로,  
  위에서 사용된 센터 타입을 자유롭게 조합하거나,  
  수업에서 제시된 프레임워크 내에서 새로운 유형의 센터를 도입해도 된다.
- 이 Free-style 설계는 귀하의 평가 기준에 따라 **가장 높은 성능을 기대하는 설계**이거나,  
  최소한 **상위 세 개 설계** 중 하나여야 한다.

---

### 선택 조건

위 여덟 가지 중 **다섯 가지 공장 조직 타입**을 선택하여 설계를 수행하되, 다음 조건을 만족해야 한다.

- (a) Function organization 기반 공장은 **필수**
- (f) Fractal 또는 (g) Holographic 중 적어도 하나 포함
- (h) Free-style organization 기반 공장은 **필수**

선택한 다섯 가지에 대해, 왜 선택했는지 **정당화(Justify)** 해야 한다.

---

### 각 설계에 대해 제공해야 할 내용

선택된 다섯 개 시설 설계(facility designs)에 대해, 다음 정보를 제공하라.

1. **네트워크 조직 구조(network organization)**  
   - 네트워크 다이어그램  
   - 공장 및 사용되는 인근 창고(near-client warehouse-s)의 각 센터의 mission

2. **센터별 및 전체 리소스 요구 계획(resource requirements plan)**  
   - 생산, 저장, 물류(handling)를 위한 장비 및 인력(Equipment and personnel)

3. **각 센터 및 전체 공장·인근 창고 레이아웃(Layout)**

4. **센터 내부(intra-center)의 작업 및 흐름 패턴, 활용도(Utilization profile)**  
   - 분석 방법을 명확히 설명  
   - 레이아웃 위에 결과를 테이블 및 도식(Schematic) 형태로 오버레이

5. **센터 간(inter-center) 흐름, 이동 거리(travel distances), 트래픽(traffic)**  
   - 흐름 다이어그램(graphical flow diagrams)  
   - 히트맵(heatmaps)  
   - 표(tabular results)

6. **예상 공장 및 창고의 핵심 성능 지표(Key performance indicators)**

7. **전체 예상 투자비 및 직접 운영비(Overall expected investment and direct operating costs)**  
   - 생산, 저장, 물류에서 발생하는 비용 포함

이렇게 생성한 대체 시설 설계들을 **체계적으로 비교(contrast)하고 순위화(rank)** 하며,  
FaMoaSa에 제공할 핵심 인사이트와,  
본 프로젝트에서 얻은 주요 학습 내용을 중점적으로 논의하라.

---

## Year +2 to +5 Demand Forecast and Performance Expectations from Client

Year +2에서 Year +5까지의 계획 기간 동안,  
FaMoaSa 테스트베드 공장은 다음 제품들에 대한 부품 생산 능력을 확장해야 한다.

- 고객사 A: **신규 제품 A4**
- 고객사 B: **신규 제품 B3, B4**

고객사들은 Year +2~+5에 대해 다음 정보를 제공하였다.

1. 각 제품에 대한 **전체 예상 수요(overall expected demand)**  
2. Year +2~+5 기간 동안의 실제 수요에 대한 **예상 표준편차(expected standard deviation)**  
   - 제공된 예측값 주변에서의 변동

> (원문에는 각 제품(A1~A4, B1~B4)에 대한 Year +2~+5 수요 및 표준편차가 표로 제시된다.)

3. 여전히 계절적 패턴은 없다고 가정하여, Year +1과 마찬가지로  
   각 제품에 대한 **예상 평균 주간 수요(average weekly demand)**를 제공한다.

4. 주간 평균 수요 주변에서 실제 조립 생산에는 변동이 발생하므로,  
   각 제품에 대한 Year +2~+5 기간의 **주간 수요 변동계수(coefficient of variation of weekly demand)**를 제공한다.

5. 주간 조립 일정은 계속해서 다음과 같이 평탄화될 것이라고 명시되어 있다.
   - 주 5일  
   - 하루 1~2교대  
   - 각 교대 8시간

FaMoaSa의 고객사들은 Year +2~+5 기간 동안의 세 신규 제품(A4, B3, B4)도  
Year +1과 동일한 **20개 부품**으로부터 조립한다.

> (이들 제품에 대한 Product–Parts 매트릭스가 원문 표로 제시된다.)

고객사들은 Year +2~+5 기간 동안에도 Year +1과 동일한 **서비스 성능(Service performance)**을 요구한다.  
따라서, 부품 공장과 창고는 동일한 서비스 수준 협약(SLA)을 강건하게 충족하도록 설계되어야 한다.

---

## Task 4

다음의 세 가지 설계를 고려하라.

i. Task 2.a에서 개발한 **Function-organization 기반 공장 설계**  
ii. Task 2.b ~ 2.g에서 도출한 설계들 중 **가장 높은 성능을 보이는 설계(Top-ranked)**  
iii. Task 2.h에서 개발한 **Free-style 공장 설계**

### (a)

각 설계에 대해, 조직 유형(type)을 유지한 상태에서  
Year +2, +3, +4, +5 동안의 수요를 충족할 수 있도록  
다음 요소를 어떻게 진화시킬지에 대한 제안을 개발하라.

- 조직 구조(organization)  
- 장비(equipment) 집합  
- 인력(pool of personnel)  
- 레이아웃(layout)

각 설계에 대해 다음을 제공해야 한다.

1. 각 연도에 대해 계획된 **네트워크 조직 구조(network organization)**  
   - 네트워크 다이어그램  
   - 각 센터의 mission  
   - 필요하다면 연도별 변화(evolution)를 명확히 표현

2. 연도별 센터별 및 전체 **리소스 요구 계획(resource requirements plan)**  
   - 생산, 저장, 물류(handling)를 위한 장비 및 인력

3. 연도별 각 센터 및 전체 공장·창고 레이아웃

4. 연도별 **재레이아웃(relayout) 계획**  
   - 수요 변화 및 센터·장비·인력 구성이 변함에 따라  
     공장과 창고에서 수행해야 할 모든 변경 사항 식별  
   - 모든 재레이아웃 활동을 생생하게 보여주는 그래픽 표현 포함

5. 각 연도에 대해, 각 센터 내부의  
   - 작업 및 흐름 패턴(work and flow patterns)  
   - 활용도(utilization profile)  
   를 추정하고, 결과를 레이아웃 위에 테이블과 도식 형태로 오버레이

6. 각 연도에 대해, 센터 간(inter-center)  
   - 흐름(flow)  
   - 이동 거리(travel distances)  
   - 트래픽(traffic)  
   을 추정하고, 이를 그래픽 흐름도, 히트맵, 표로 제시

7. 각 연도별 및 전체 기간에 대해,  
   예상되는 공장 및 창고의 **핵심 성능 지표(key performance indicators)**를 제시

8. 연도별 및 전체 기간에 대해,  
   생산, 저장, 물류에 의해 발생하는 비용을 포함한  
   예상 투자비(investment)와 직접 운영비(direct operating costs)를 제시

### (b)

생성된 대안 설계들을 **체계적으로 비교(contrast)하고 순위를 매긴 뒤(rank)**,  
그 결과를 논의하라.

---

## Task 5

FaMoaSa에 제공할 **Executive Summary**를 작성하라.

- 길이: 최대 2페이지  
- 포함 내용:
  - 전체 평가 요약(overall assessments)  
  - 주요 인사이트(insights)  
  - 추천 사항(recommendations)  
  - 설득력 있는 그림(Figures) 및/또는 표(Tables)

---

## Task 6

본 케이스워크를 수행하면서 팀이 얻게 된  
**핵심 학습 내용(key learnings)**을 정리하라.

---

I hope this casework proves to be a challenging, stimulating, and worthwhile learning experience.  
**Professor Benoit Montreuil**
