# Recovered Scientific Reference Preservation Record

```text
document_status =
ACCEPTED_RECOVERED_SCIENTIFIC_REFERENCE

document_role =
NON_AUTHORIZING_SCIENTIFIC_REFERENCE

authorization_effect =
NONE

current_state_control =
NO

controlling_governance_effect =
NONE

scientific_execution_authority =
NONE

relationship_to_GOV_DEC_0021 =
CORROBORATING_PROPORTIONALITY_BASIS_ONLY

SCIENTIFIC_RIGOR_RELAXED =
NO

SOURCE_EXCLUSIVITY_RELAXED =
YES

LITERATURE_REPORT_AUTHORIZED_GOV_DEC_0021 =
NO

GOV_DEC_0021_OWNER_AUTHORIZATION_REMAINS_SEPARATE =
YES

LITERATURE_REFERENCE_CONTROLS_CURRENT_CLASSIFICATION =
NO

RECOVERED_SOURCE_CONTENT_PRESERVED =
YES
```

This file preserves an Owner-provided recovered scientific-reference artifact.
Its research findings provide historical scientific context for the
proportionality judgment later reflected in GOV-DEC-0021, but this file is not
an Owner decision, governance decision, authorization source, current-state
controller, classification controller, or scientific-execution authority.

The recovered source content below is preserved as historical research content.
No new web research, citation updating, publication-status updating, or silent
reconciliation with later project findings was performed in this preservation
transaction.

---

# Completion pass — reconciled literature audit

I used the original audit specification as the controlling evidence standard: historical membership, ticker identity, share classes, predecessor/successor links, primary listing, delistings, and security-master use are **NOT\_DOCUMENTED unless the paper explicitly establishes them**.

The central correction to the prior report is this: **the literature supports dropping the arbitrary requirement of exactly 120 securities, but it does not support replacing it with an equally arbitrary “minimum of 60.”** The evidence supports a rule-driven universe whose size follows from the selection protocol.

## 1. Reconciled evidence base

**EXACT\_PAPER\_COUNT = 20**
**EXACT\_PEER\_REVIEWED\_COUNT = 19**
**EXACT\_PREPRINT\_COUNT = 1**

Every study counted below contributes to the aggregate results; no additional unnamed study is included.

| #Paper / publication statusRL methodSecurities / universeUniverse construction and data |                                                                                                                                                                                                                                     |                                                   |                                                                            |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1                                                                                       | Yang, Liu, Zhong & Walid, **“Deep Reinforcement Learning for Automated Stock Trading: An Ensemble Strategy,” ICAIF 2020**, peer reviewed. DOI **10.1145/3383455.3422540**                                                           | A2C, PPO, DDPG ensemble                           | **30**, DJIA                                                               | Fixed Dow-30 constituents as of Jan. 1, 2016; WRDS/Compustat; growing training window + rolling validation. The 2016 membership list is applied to earlier observations. ([Quantum FinAI Lab](https://openfin.engineering.columbia.edu/sites/openfin.engineering.columbia.edu/files/content/publications/ensemble.pdf "https://openfin.engineering.columbia.edu/sites/openfin.engineering.columbia.edu/files/content/publications/ensemble.pdf"))                                                                                   |
| 2                                                                                       | Wu et al., **“Adaptive stock trading strategies with deep reinforcement learning methods,” Information Sciences 2020**, peer reviewed. DOI **10.1016/j.ins.2020.05.066**                                                            | GDPG, GDQN                                        | **15 stocks**                                                              | Fixed experimental stock set across multiple market conditions/countries; approximately eight years of historical observations reported. Full identity reconstruction not documented. ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0020025520304692?utm_source=chatgpt.com "Adaptive stock trading strategies with deep reinforcement learning methods - ScienceDirect"))                                                                                                                                |
| 3                                                                                       | Ye et al., **“Reinforcement-Learning Based Portfolio Management with Augmented Asset Movement Prediction States,” AAAI 2020**, peer reviewed. DOI **10.1609/aaai.v34i01.5462**                                                      | RL portfolio agent                                | **9 high-tech stocks**                                                     | Fixed technology-stock set; Reuters news plus market data; chronological train/test period covering roughly 2006–2013. ([ML Anthology](https://mlanthology.org/aaai/2020/ye2020aaai-reinforcement/ "https://mlanthology.org/aaai/2020/ye2020aaai-reinforcement/"))                                                                                                                                                                                                                                                                  |
| 4                                                                                       | Théate & Ernst, **“An application of deep reinforcement learning to algorithmic trading,” ESWA 2021**, peer reviewed. DOI **10.1016/j.eswa.2021.114632**                                                                            | TDQN                                              | **30 instruments evaluated**                                               | Pre-specified multi-instrument test bench; not a dynamically reconstructed security universe. ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0957417421000737 "https://www.sciencedirect.com/science/article/abs/pii/S0957417421000737"))                                                                                                                                                                                                                                                                  |
| 5                                                                                       | Hirchoua, Ouhbi & Frikh, **“Deep reinforcement learning based trading agents: Risk curiosity driven learning for financial rules-based policy,” ESWA 2021**, peer reviewed. DOI **10.1016/j.eswa.2020.114553**                      | PPO-related policy-gradient framework             | **8 real stocks**                                                          | Fixed evaluation stocks; historical-security reconstruction not documented. ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0957417420311970 "https://www.sciencedirect.com/science/article/pii/S0957417420311970"))                                                                                                                                                                                                                                                                                            |
| 6                                                                                       | Wu et al., **“Portfolio management system in equity market neutral using reinforcement learning,” Applied Intelligence 2021**, peer reviewed. DOI **10.1007/s10489-021-02262-0**                                                    | RL portfolio management                           | **50**, Taiwan 50                                                          | Taiwan-50 constituent pool; Taiwan Stock Exchange OHLC data; approximately 2015–17 train and 2017–19 test. ([Springer Link](https://link.springer.com/article/10.1007/s10489-021-02262-0?utm_source=chatgpt.com "Portfolio management system in equity market neutral using reinforcement learning \| Applied Intelligence \| Springer Nature Link"))                                                                                                                                                                               |
| 7                                                                                       | Wang et al., **“DeepTrader,” AAAI 2021**, peer reviewed. DOI **10.1609/aaai.v35i1.16144**                                                                                                                                           | Actor-critic portfolio management                 | **30 DJIA; 49 HSI; 80 CSI100**                                             | Fixed index-derived experimental sets; WRDS/Wind reported in associated implementation materials. Incomplete-data stocks were removed, but that is not equivalent to including delisted securities. ([AAAI Publications](https://ojs.aaai.org/index.php/AAAI/article/view/16144 "https://ojs.aaai.org/index.php/AAAI/article/view/16144"))                                                                                                                                                                                          |
| 8                                                                                       | Li, Wang & Zhou, **“Ensemble Investment Strategies Based on Reinforcement Learning,” Scientific Programming 2022**, peer reviewed. DOI **10.1155/2022/7648810**                                                                     | PPO, A2C, SAC ensemble                            | **40 A-shares**                                                            | 40 sufficiently liquid stocks from CSI100; Wind data; three-month retraining/validation sequence; explicit transaction costs. ([Wiley Online Library](https://onlinelibrary.wiley.com/doi/10.1155/2022/7648810 "https://onlinelibrary.wiley.com/doi/10.1155/2022/7648810"))                                                                                                                                                                                                                                                         |
| 9                                                                                       | Brim & Flann, **“Deep reinforcement learning stock market trading, utilizing a CNN with candlestick images,” PLOS ONE 2022**, peer reviewed. DOI **10.1371/journal.pone.0263181**                                                   | DRL/CNN                                           | **30**                                                                     | Thirty large S&P 500 stocks; Alpha Vantage; historical train period and 2020 test period. ([PLOS](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0263181 "https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0263181"))                                                                                                                                                                                                                                                                       |
| 10                                                                                      | Kong & So, **“Empirical Analysis of Automated Stock Trading Using Deep Reinforcement Learning,” Applied Sciences 2023**, peer reviewed. DOI **10.3390/app13010633**                                                                 | A2C, DDPG, PPO; expanded actor-critic comparisons | **30 each**: DJIA, KOSPI, JPX                                              | Fixed 30-stock sets; Korea/Japan pools selected by market capitalization; FinanceDataReader/yfinance; rolling 63-day validation and model selection. ([MDPI](https://www.mdpi.com/2076-3417/13/1/633 "https://www.mdpi.com/2076-3417/13/1/633"))                                                                                                                                                                                                                                                                                    |
| 11                                                                                      | Lee & Moon, **“Offline Reinforcement Learning for Automated Stock Trading,” IEEE Access 2023**, peer reviewed. DOI **10.1109/ACCESS.2023.3324458**                                                                                  | Offline actor-critic; PPO/SAC comparisons         | **9, 30, 50** depending dataset                                            | Several fixed benchmark datasets: 9 technology names, Dow-30, 50 U.S. stocks and 30-stock international subsets. ([Directory of Open Access Journals](https://doaj.org/article/8d8658e82d124958bceadd119b268dab?utm_source=chatgpt.com "Offline Reinforcement Learning for Automated Stock Trading – DOAJ"))                                                                                                                                                                                                                        |
| 12                                                                                      | Jang & Seong, **“Deep reinforcement learning for stock portfolio optimization by connecting with modern portfolio theory,” ESWA 2023**, peer reviewed. DOI **10.1016/j.eswa.2023.119556**                                           | DDPG                                              | **29 stocks**                                                              | Historical datasets for stocks included in Dow Jones indices, 2008–2019; full historical-membership/security-master construction not documented. ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S095741742300057X "https://www.sciencedirect.com/science/article/pii/S095741742300057X"))                                                                                                                                                                                                                       |
| 13                                                                                      | Zou et al., **“A novel Deep Reinforcement Learning based automated stock trading system using cascaded LSTM networks,” ESWA 2024**, peer reviewed. DOI **10.1016/j.eswa.2023.122801**                                               | CLSTM-PPO                                         | **120 distinct stocks total**, but **30 per market experiment**            | 30 Dow + 30 SSE50 + 30 Sensex + 30 FTSE100. The paper therefore contains 120 names collectively, **not a single 120-stock U.S. portfolio and not a claim that 120 is required**. U.S. data inherit Yang et al.; other markets use Wind. ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0957417423033031?utm_source=chatgpt.com "A novel Deep Reinforcement Learning based automated stock trading system using cascaded LSTM networks - ScienceDirect"))                                                       |
| 14                                                                                      | Li & Hai, **“Deep Reinforcement Learning Model for Stock Portfolio Management Based on Data Fusion,” Neural Processing Letters 2024**, peer reviewed. DOI **10.1007/s11063-024-11582-4**                                            | Multi-agent DQN                                   | **34 SSE stocks** plus index series                                        | Fixed Chinese-equity sample; Resset data; historical-identity reconstruction not documented. ([Springer Link](https://link.springer.com/article/10.1007/s11063-024-11582-4 "Deep Reinforcement Learning Model for Stock Portfolio Management Based on Data Fusion \| Neural Processing Letters \| Springer Nature Link"))                                                                                                                                                                                                           |
| 15                                                                                      | Cheng & Sun, **“Multiagent-based deep reinforcement learning framework for multi-asset adaptive trading and portfolio management,” Neurocomputing 2024**, peer reviewed. DOI **10.1016/j.neucom.2024.127800**                       | Multi-agent TD3                                   | **3 Taiwan-50 stocks**                                                     | Hand-selected high-market-cap/high-volume stocks from different sectors; fixed sample. ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S092523122400571X?utm_source=chatgpt.com "Multiagent-based deep reinforcement learning framework for multi-asset adaptive trading and portfolio management - ScienceDirect"))                                                                                                                                                                                             |
| 16                                                                                      | Zhang et al., **“Reinforcement Learning with Maskable Stock Representation for Portfolio Management in Customizable Stock Pools,” WWW 2024**, peer reviewed. DOI **10.1145/3589334.3645615**                                        | EarnMore / maskable RL                            | Up to **420 S&P-500-pool names**; smaller customizable subsets also tested | Yahoo Finance; explicitly tackles changing/customizable stock pools, with several expanding chronological train/test splits. It models stock-pool removals, but this is **not equivalent to complete security-master reconstruction**. ([Nanyang Technological University](https://personal.ntu.edu.sg/boan/papers/WWW24_EarnMore.pdf "Reinforcement Learning with Maskable Stock Representation for Portfolio Management in Customizable Stock Pools"))                                                                            |
| 17                                                                                      | Aritonang, Wiryono & Faturohman, **“Hidden-layer configurations in reinforcement learning models for stock portfolio optimization,” Intelligent Systems with Applications 2025**, peer reviewed. DOI **10.1016/j.iswa.2024.200467** | A2C, DDPG, PPO, TD3                               | **45 stocks**                                                              | Fixed actively traded Indonesian stock set; historical-security genealogy not documented. ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2667305324001418 "https://www.sciencedirect.com/science/article/pii/S2667305324001418"))                                                                                                                                                                                                                                                                              |
| 18                                                                                      | Wang et al., **“FinRL Contests: Data-Driven Financial Reinforcement Learning Agents for Stock and Crypto Trading,” Artificial Intelligence for Engineering 2025**, peer reviewed. DOI **10.1049/aie2.12004**                        | FinRL RL baselines                                | **30 DJIA** in the relevant stock task                                     | Standardized contest data/task; includes pre-submission and genuinely later post-submission evaluation. The framework discusses data bias, but the 30-stock contest task does not document complete historical security-master reconstruction. ([IET](https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/aie2.12004?utm_source=chatgpt.com "FinRL Contests: Data‐Driven Financial Reinforcement Learning Agents for Stock and Crypto Trading - Wang - 2025 - Artificial Intelligence for Engineering - Wiley Online Library")) |
| 19                                                                                      | Huang et al., **“Explainable reinforcement learning with adaptive feature selection for stock trading,” Applied Soft Computing 2026**, peer reviewed. DOI **10.1016/j.asoc.2025.114543**                                            | TwinTRPO + RF/SHAP/XGBoost feature selection      | **8 Chinese A-share stocks**                                               | Fixed individual-stock experimental sample. Particularly relevant because supervised models augment RL, although they are feature-selection components rather than participation gates. ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1568494625018563?utm_source=chatgpt.com "Explainable reinforcement learning with adaptive feature selection for stock trading - ScienceDirect"))                                                                                                                        |
| 20                                                                                      | Abbade & Costa, **“Realistic Market Impact Modeling for Reinforcement Learning Trading Environments,” arXiv 2026**, substantive preprint. DOI **10.48550/arXiv.2603.29086**                                                         | A2C, PPO, DDPG, SAC, TD3                          | **NASDAQ-100**                                                             | Explicit **static circa-2021 NASDAQ-100 composition**, daily 2010–2026, with 2025 reserved for final OOS. Authors explicitly acknowledge mild survivorship bias. ([arXiv](https://arxiv.org/html/2603.29086v2 "Realistic Market Impact Modeling for Reinforcement Learning Trading Environments"))                                                                                                                                                                                                                                  |

### Corrected historical-identity and validation audit

`ND = NOT_DOCUMENTED`, not “No.” That distinction is important.

| #Historical membershipDelisted securities explicitly includedSurvivorship discussion / full controlTicker / share-class / successor / primary-listing reconstructionWalk-forward / rollingFinal untouched test |                                                 |        |                                             |                   |                                  |                                                |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- | ------ | ------------------------------------------- | ----------------- | -------------------------------- | ---------------------------------------------- |
| 1                                                                                                                                                                                                              | **NO** — fixed 2016 DJIA list                   | ND     | No / No                                     | ND / ND / ND / ND | **YES**                          | **NO** — rolling selection continues           |
| 2                                                                                                                                                                                                              | ND                                              | ND     | No / No                                     | ND / ND / ND / ND | ND                               | UNCLEAR                                        |
| 3                                                                                                                                                                                                              | ND                                              | ND     | No / No                                     | ND / ND / ND / ND | NO                               | UNCLEAR                                        |
| 4                                                                                                                                                                                                              | ND                                              | ND     | No / No                                     | ND / ND / ND / ND | NO                               | UNCLEAR                                        |
| 5                                                                                                                                                                                                              | ND                                              | ND     | No / No                                     | ND / ND / ND / ND | ND                               | UNCLEAR                                        |
| 6                                                                                                                                                                                                              | ND                                              | ND     | No / No                                     | ND / ND / ND / ND | NO                               | UNCLEAR                                        |
| 7                                                                                                                                                                                                              | ND                                              | ND     | No / No                                     | ND / ND / ND / ND | NO                               | UNCLEAR                                        |
| 8                                                                                                                                                                                                              | ND                                              | ND     | No / No                                     | ND / ND / ND / ND | **YES**                          | **NO** — rolling model selection               |
| 9                                                                                                                                                                                                              | ND                                              | ND     | No / No                                     | ND / ND / ND / ND | NO                               | UNCLEAR                                        |
| 10                                                                                                                                                                                                             | ND                                              | ND     | No / No                                     | ND / ND / ND / ND | **YES**                          | **NO** — repeated rolling selection            |
| 11                                                                                                                                                                                                             | ND                                              | ND     | No / No                                     | ND / ND / ND / ND | NO                               | UNCLEAR                                        |
| 12                                                                                                                                                                                                             | ND                                              | ND     | No / No                                     | ND / ND / ND / ND | ND                               | UNCLEAR                                        |
| 13                                                                                                                                                                                                             | ND                                              | ND     | No / No                                     | ND / ND / ND / ND | ND                               | UNCLEAR                                        |
| 14                                                                                                                                                                                                             | ND                                              | ND     | No / No                                     | ND / ND / ND / ND | ND                               | UNCLEAR                                        |
| 15                                                                                                                                                                                                             | ND                                              | ND     | No / No                                     | ND / ND / ND / ND | ND                               | UNCLEAR                                        |
| 16                                                                                                                                                                                                             | **PARTIAL** — changing/custom pools are modeled | ND     | Not explicit / Partial at most              | ND / ND / ND / ND | **PARTIAL** — expanding splits   | UNCLEAR                                        |
| 17                                                                                                                                                                                                             | ND                                              | ND     | No / No                                     | ND / ND / ND / ND | ND                               | UNCLEAR                                        |
| 18                                                                                                                                                                                                             | ND for the specific contest universe            | ND     | **Yes / Partial at framework level**        | ND / ND / ND / ND | PARTIAL across contest protocols | **YES** for post-submission contest evaluation |
| 19                                                                                                                                                                                                             | ND                                              | ND     | No / No                                     | ND / ND / ND / ND | ND                               | UNCLEAR                                        |
| 20                                                                                                                                                                                                             | **NO** — explicitly static circa-2021 list      | **ND** | **Yes / No** — acknowledged, not eliminated | ND / ND / ND / ND | **NO**                           | UNCLEAR\*                                      |

\*Abbade & Costa reserve 2025 for “true OOS and final evaluation,” but their HPO objective explicitly uses OOS Sharpe across epochs before the final period. I therefore do **not** upgrade this to “untouched final test” under the project's stricter frozen-model meaning. ([arXiv](https://arxiv.org/html/2603.29086v2 "Realistic Market Impact Modeling for Reinforcement Learning Trading Environments"))

This corrects the prior report's overly generous classification of ordinary chronological test sets as “final untouched tests.” A stated test period is **not enough** to prove that model specification, hyperparameters, feature choices and thresholds were frozen before that period.

## 2. Corrected aggregate findings

Using one representative equity-universe count per paper, the observed study sizes are centered much lower than 120. The reconciled median is **30 securities**. A practical recurring range is roughly **30–50**, although credible papers range from very small fixed samples to 80, 100, and EarnMore's much larger customizable stock pool. ([Quantum FinAI Lab](https://openfin.engineering.columbia.edu/sites/openfin.engineering.columbia.edu/files/content/publications/ensemble.pdf?utm_source=chatgpt.com "Deep Reinforcement Learning for Automated Stock Trading: An Ensemble Strategy"))

The important nuance about 120 is:

> **Zou et al. use 120 distinct names across the study, but conduct the market experiments as four 30-stock universes.**

That is evidence that **120 names can appear in a credible paper**; it is **not evidence for a scientifically necessary 120-security portfolio threshold**. ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0957417423033031?utm_source=chatgpt.com "A novel Deep Reinforcement Learning based automated stock trading system using cascaded LSTM networks - ScienceDirect"))

Corrected counts:

```text
TOTAL_CREDIBLE_PAPERS_REVIEWED = 20

PEER_REVIEWED_PAPERS = 19
PREPRINT_PAPERS = 1

FULL_HISTORICAL_INDEX_MEMBERSHIP_RECONSTRUCTION = 0 / 20
PARTIAL_DYNAMIC_MEMBERSHIP_HANDLING = 1 / 20

HISTORICAL_TICKER_IDENTITY_RECONSTRUCTED = 0 / 20
SHARE_CLASS_HISTORY_RECONSTRUCTED = 0 / 20
SUCCESSOR_PREDECESSOR_HISTORY_RECONSTRUCTED = 0 / 20
PRIMARY_LISTING_HISTORY_RECONSTRUCTED = 0 / 20

DELISTED_SECURITIES_EXPLICITLY_INCLUDED = 0 / 20
EXPLICIT_SURVIVORSHIP_BIAS_DISCUSSION = 2 / 20
FULL_PAPER_SPECIFIC_SURVIVORSHIP_CONTROL = 0 / 20

EXPLICIT_FULL_SECURITY_MASTER_RECONSTRUCTION = 0 / 20

WALK_FORWARD_OR_ROLLING_VALIDATION =
3 YES
2 PARTIAL
15 NO_OR_NOT_DOCUMENTED

FINAL_UNTOUCHED_TEST_SET_UNDER_STRICT_PROJECT_DEFINITION =
1 YES
3 NO
16 UNCLEAR
```

The zero counts for ticker/share-class/successor/listing reconstruction mean **“no paper documents doing it,” not “we proved the authors never performed any such preprocessing.”** That is exactly the evidentiary distinction required by the audit.

Commercial/institutional data are also more common than the earlier report implied. WRDS/Compustat appears in Yang et al.; Wind appears in Li et al., DeepTrader-related data, and Zou et al.; Resset is used by Li & Hai; public sources such as Yahoo Finance, FinanceDataReader and Alpha Vantage are also common. ([Quantum FinAI Lab](https://openfin.engineering.columbia.edu/sites/openfin.engineering.columbia.edu/files/content/publications/ensemble.pdf?utm_source=chatgpt.com "Deep Reinforcement Learning for Automated Stock Trading: An Ensemble Strategy"))

---

# 3. A — What published precedent actually supports

Published precedent strongly supports **pre-specified fixed or index-derived universes** without comprehensive point-in-time security-master reconstruction. Examples include 30 Dow stocks in Yang et al.; 40 liquid CSI100 stocks in Li et al.; 30-stock DJIA/KOSPI/JPX experiments in Kong & So; 29 Dow-related stocks in Jang & Seong; 45 actively traded Indonesian stocks in Aritonang et al.; and static NASDAQ-100 in Abbade & Costa. ([Quantum FinAI Lab](https://openfin.engineering.columbia.edu/sites/openfin.engineering.columbia.edu/files/content/publications/ensemble.pdf?utm_source=chatgpt.com "Deep Reinforcement Learning for Automated Stock Trading: An Ensemble Strategy"))

Published precedent also supports **considerably smaller samples than 120**. The surveyed peer-reviewed literature contains credible experiments with 3, 8, 9, 15, 29, 30, 34, 40, 45, 50 and 80 securities, as well as 100-stock and larger/customizable-pool cases. ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S092523122400571X?utm_source=chatgpt.com "Multiagent-based deep reinforcement learning framework for multi-asset adaptive trading and portfolio management - ScienceDirect"))

What precedent **does not establish** is a statistical or methodological minimum number of stocks. None of these papers demonstrates that `N=30`, `N=60`, `N=100`, or `N=120` is a minimum necessary for valid RL research.

```text
MINIMUM_UNIVERSE_SIZE_SUPPORTED_BY_LITERATURE =
NOT_ESTABLISHED
```

Therefore the previous recommendation of “approximately 60 stocks” was too categorical.

```text
STATUS_OF_60 =
PROJECT_DESIGN_COMPROMISE / ARBITRARY_BUT_REASONABLE
NOT_LITERATURE_SUPPORTED_MINIMUM
```

---

# 4. B — What is scientifically necessary for this project's question

The project is not primarily testing whether it has reconstructed the complete U.S. equity population. It is testing:

```text
DO_SUPERVISED_RF_OR_XGBOOST_PARTICIPATION_GATES
ADD_INCREMENTAL_VALUE
AROUND_QUALIFIED_RL_POLICIES?
```

For that question, the decisive scientific requirements are **comparability and leakage control**, not an exact cross-sectional count.

PPO/SAC/RecurrentPPO and their gated variants should face the **same ex-ante universe**, same observations, same transaction-cost model, same train/validation periods, and same untouched final evaluation. Otherwise a difference attributed to the RF/XGBoost gate could instead arise from changing asset availability, data selection, or tuning. Yang, Li et al. and Kong & So demonstrate how rolling model-selection designs can be structured, while the FinRL contest illustrates the additional value of genuinely later evaluation. ([Quantum FinAI Lab](https://openfin.engineering.columbia.edu/sites/openfin.engineering.columbia.edu/files/content/publications/ensemble.pdf?utm_source=chatgpt.com "Deep Reinforcement Learning for Automated Stock Trading: An Ensemble Strategy"))

For the project's primary claim, I would retain:

- **ex-ante universe rules and formation cutoff;**
- **no current-constituent/current-ticker backcasting that inserts future information;**
- **no outcome-driven removal or replacement of securities;**
- **stable security-level identity where needed to distinguish different share classes;**
- **no automatic predecessor/successor return stitching;**
- **point-in-time exchange/listing eligibility during the governed experimental window;**
- **explicit treatment of a sampled security that delists, merges, converts or otherwise terminates during the experiment;**
- **fail-closed handling when an unresolved identity question could actually change eligibility or historical returns;**
- **frozen RL model/gate/threshold before the common final test;**
- realistic costs, repeated seeds and regime robustness.

Those controls are methodologically stronger than what is documented in most surveyed RL papers, but they directly protect the internal validity of the gate comparison. The fact that Abbade & Costa explicitly acknowledge the survivorship bias caused by a static 2021 NASDAQ-100 composition demonstrates why simply following common precedent is not necessarily best practice. ([arXiv](https://arxiv.org/html/2603.29086v2 "Realistic Market Impact Modeling for Reinforcement Learning Trading Environments"))

### Is the current 20-security sample scientifically useless?

No. Published peer-reviewed work exists with substantially fewer securities: Cheng & Sun use three selected Taiwan-50 stocks, Hirchoua et al. evaluate eight real stocks, and Ye et al. use nine technology stocks. ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S092523122400571X?utm_source=chatgpt.com "Multiagent-based deep reinforcement learning framework for multi-asset adaptive trading and portfolio management - ScienceDirect"))

But **20 would narrow external validity**. It could support:

> “Within this pre-specified, historically certified liquid U.S.-equity sample, does supervised gating improve qualified RL policies?”

It would be weaker support for:

> “Supervised gating improves RL trading across the general U.S. equity universe.”

So the reason to expand beyond 20 is **breadth and generalizability**, not satisfaction of a published numerical minimum.

---

# 5. C — Rigor that would strengthen the paper even though precedent does not require it

The project can legitimately exceed prevailing practice. Particularly valuable extra controls would be point-in-time eligibility, explicit terminal/delisting treatment, persistent security-level IDs, documented share-class treatment, and a reproducible archived formation snapshot. Those address weaknesses that many papers simply leave undocumented.

EarnMore is especially useful precedent here: it shows that a top-tier peer-reviewed paper can make **stock-pool definition and changing availability themselves explicit parts of the experimental design** rather than assuming a permanent fixed ticker list. ([Nanyang Technological University](https://personal.ntu.edu.sg/boan/papers/WWW24_EarnMore.pdf "Reinforcement Learning with Maskable Stock Representation for Portfolio Management in Customizable Stock Pools"))

However, some parts of the project's current reconstruction standard are probably disproportionate **if they cannot affect the governed experiment**. Examples are reconstructing an exhaustive ticker genealogy long before the study period, resolving every predecessor/successor relationship when no history will be stitched across that event, and reconstructing remote historical primary-listing changes outside the eligibility/return window.

The distinction should therefore be:

```text
FAIL_CLOSED_IF_UNRESOLVED_FACT_CAN_CHANGE =
ELIGIBILITY
SECURITY_IDENTITY
RETURN_HISTORY
SHARE_CLASS
LISTING_STATUS_DURING_STUDY
TERMINAL_EVENT_TREATMENT

DOCUMENT_BUT_DO_NOT_BLOCK_IF_UNRESOLVED_FACT =
CANNOT_CHANGE_ANY_OF_THE_ABOVE
AND_IS_OUTSIDE_THE_GOVERNED_WINDOW
```

That retains scientific rigor without allowing historical-identity archaeology to become an unrelated research objective.

---

# 6. Best universe design

I would **not** choose pure Design B with an invented lower target such as exactly 60.

I would choose a **Design D + Design B hybrid**:

```text
HYBRID_D_PLUS_B =

1. Apply frozen positive-certification rules
   to the candidate population.

2. Include ALL securities positively certified
   by the predetermined formation cutoff.

3. Do NOT force the count to equal 120, 80, 60,
   or any other post-hoc target.

4. Freeze that resulting universe before
   PPO / SAC / RecurrentPPO qualification and
   RF/XGBoost gating experiments.

5. Hold the primary experimental universe fixed
   during comparison, except for pre-specified
   terminal-event handling.

6. Preserve strong point-in-time identity controls
   where they can change inclusion or returns.
```

This gets the strongest part of Design D—**no arbitrary target forcing**—while retaining the strongest part of Design B—**a fixed, historically defensible comparison universe once the experiment begins**.

A practical project planning objective of perhaps **30–80 certified securities** is reasonable because it gives more cross-sectional and sectoral heterogeneity while remaining well within the empirical scale represented by published RL work. But it must be labeled a **project-specific breadth objective**, not a statistical minimum. Papers using 30, 40, 45, 50 and 80 stocks demonstrate that those scales are entirely normal research settings. ([Quantum FinAI Lab](https://openfin.engineering.columbia.edu/sites/openfin.engineering.columbia.edu/files/content/publications/ensemble.pdf?utm_source=chatgpt.com "Deep Reinforcement Learning for Automated Stock Trading: An Ensemble Strategy"))

If certification stalls at 20 after reasonable effort, I would **not weaken point-in-time integrity merely to hit a larger N**. Use the 20 and narrow the claim, then add a robustness universe later if feasible.

---

# 7. Owner-level disposition

```text
TOTAL_CREDIBLE_PAPERS_REVIEWED =
20

EXACT_PAPER_COUNT =
20

EXACT_PEER_REVIEWED_COUNT =
19

EXACT_PREPRINT_COUNT =
1

EXACT_PAPER_COUNT_RECONCILED =
YES


120_THRESHOLD_SUPPORTED =
NO


LITERATURE_SUPPORTED_MINIMUM_N =
NOT_ESTABLISHED


PROJECT_SPECIFIC_RECOMMENDED_N_OR_RANGE =
NO_FORCED_N

OPERATIONAL_BREADTH_OBJECTIVE =
APPROXIMATELY_30_TO_80_IF_FEASIBLE

CURRENT_20_STATUS =
SCIENTIFICALLY_USABLE_FOR_A_NARROW_SAMPLE_SPECIFIC_CLAIM
BUT_LESS_DESIRABLE_FOR_BROAD_CROSS_SECTIONAL_GENERALIZATION


IS_60_A_LITERATURE_DERIVED_MINIMUM =
NO


FULL_HISTORICAL_SECURITY_MASTER_RECONSTRUCTION_REQUIRED_BY_PRECEDENT =
NO


WOULD_DROPPING_EXACT_120_MATERIALLY_WEAKEN_PUBLICATION =
NO

CONDITION =
THE_PAPER_MUST_SCOPE_ITS_CLAIMS_TO_THE_PRE_SPECIFIED_CERTIFIED_SAMPLE
AND_PRESERVE_INTERNAL_VALIDITY_AND_SURVIVORSHIP_CONTROLS


WHICH_SURVIVORSHIP_CONTROLS_SHOULD_BE_RETAINED =

NO_CURRENT_CONSTITUENT_OR_TICKER_BACKCASTING_WHERE_IT_CREATES_FUTURE_INFORMATION

EX_ANTE_FORMATION_AND_ELIGIBILITY_RULES

POINT_IN_TIME_SECURITY_EXISTENCE_AND_LISTING_ELIGIBILITY_DURING_THE_STUDY_WINDOW

DISTINCT_SHARE_CLASS_HANDLING_WHERE_RELEVANT

NO_AUTOMATIC_SUCCESSOR_PREDECESSOR_RETURN_STITCHING

EXPLICIT_DELISTING_MERGER_AND_TERMINAL_EVENT_TREATMENT_FOR_INCLUDED_SECURITIES

NO_OUTCOME_DRIVEN_SECURITY_REMOVAL

FAIL_CLOSED_WHEN_UNRESOLVED_IDENTITY_CAN_CHANGE_INCLUSION_OR_RETURNS

FROZEN_PRIMARY_UNIVERSE_BEFORE_MODEL_COMPARISON

COMMON_FINAL_UNTOUCHED_TEST_FOR_RL_AND_GATED_VARIANTS


WHICH_CURRENT_CONTROLS_ARE_PROBABLY_DISPROPORTIONATE_TO_THE_PRIMARY_QUESTION =

FORCING_EXACTLY_120_CERTIFIED_SECURITIES

EXHAUSTIVE_TICKER_GENEALOGY_OUTSIDE_THE_GOVERNED_SAMPLE_WINDOW

EXHAUSTIVE_PREDECESSOR_SUCCESSOR_RECONSTRUCTION_WHEN_NO_HISTORY_IS_STITCHED

FULL_REMOTE_PRIMARY_LISTING_HISTORY_WHEN_IT_CANNOT_CHANGE_STUDY_PERIOD_ELIGIBILITY

FAIL_CLOSED_ON_METADATA_AMBIGUITIES_THAT_CANNOT_CHANGE_SECURITY_IDENTITY,
ELIGIBILITY_OR_RETURNS


BEST_FINAL_UNIVERSE_DESIGN =
HYBRID_DESIGN_D_PLUS_B

ALL_POSITIVELY_CERTIFIED_SECURITIES_AT_A_FROZEN_FORMATION_CUTOFF,
FOLLOWED_BY_A_FIXED_PRIMARY_EXPERIMENTAL_UNIVERSE,
WITH_NO_FORCED_EXACT_N


RECOMMENDED_OWNER_DECISION =

SUPERSEDE_THE_EXACT_120_SECURITY_REQUIREMENT.

RETAIN_THE_CORE_POINT_IN_TIME_AND_NO_BACKCASTING_CONTROLS.

CONTINUE_POSITIVE_CERTIFICATION_WITHOUT_LOWERING_EVIDENCE_STANDARDS
SOLELY_TO_REACH_A_NUMERIC_TARGET.

AT_THE_PREDECLARED_FORMATION_CUTOFF,
FREEZE_ALL_SECURITIES_THAT_PASS_THE_RULES
AND_USE_THE_IDENTICAL_UNIVERSE_FOR
PPO_SAC_RECURRENT_PPO_AND_RF_XGBOOST_GATING_COMPARISONS.

TREAT_30_TO_80_AS_A_PROJECT_PLANNING_OBJECTIVE,
NOT_A_LITERATURE_DERIVED_MINIMUM.

IF_THE_FINAL_CERTIFIED_COUNT_REMAINS_NEAR_20,
PROCEED_WITH_A_NARROW_SAMPLE_SPECIFIC_CLAIM
PLUS_STRONG_ROBUSTNESS_ANALYSIS
RATHER_THAN_WEAKENING_HISTORICAL_INTEGRITY_TO_FORCE_N_120.
```

**Bottom line:** published precedent clearly does **not** require 120 securities or full historical security-master reconstruction. The scientifically strongest adjustment is also **not** “change 120 to 60.” It is to eliminate the forced count altogether, let frozen positive-certification rules determine `N`, and then freeze that universe for the RL-versus-gating experiment. That preserves the controls most relevant to causal attribution while avoiding a large data-acquisition burden that the literature does not justify as necessary.