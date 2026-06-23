```text
██╗  ██╗███████╗██╗     ██╗      ██████╗
██║  ██║██╔════╝██║     ██║     ██╔═══██╗
███████║█████╗  ██║     ██║     ██║   ██║
██╔══██║██╔══╝  ██║     ██║     ██║   ██║
██║  ██║███████╗███████╗███████╗╚██████╔╝
╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝
```

# 이선우

백엔드와 AI 검색 시스템을 다룹니다.  
Spring Boot, FastAPI, RAG, vLLM 쪽 작업을 주로 하고 있습니다.

[![Email](https://img.shields.io/badge/Email-sunwoomjc@widiservice.com-111111?style=flat-square&logo=gmail&logoColor=white)](mailto:sunwoomjc@widiservice.com)
[![GitHub](https://img.shields.io/badge/GitHub-sunwoo8478-111111?style=flat-square&logo=github&logoColor=white)](https://github.com/sunwoo8478)
[![Views](https://komarev.com/ghpvc/?username=sunwoo8478&color=111111&style=flat-square&label=views)](https://github.com/sunwoo8478)

---

## About

기능을 만드는 것뿐 아니라, 배포 후에도 문제를 찾을 수 있는 구조를 좋아합니다.  
요즘은 상담 도메인의 질문을 RAG 파이프라인으로 잘 연결하는 일과, GPU 서버에서 LLM 응답 속도를 안정적으로 만드는 일을 하고 있습니다.

- 서울노동권익센터 AI 상담 챗봇 개발
- Gemma 3 12B 기반 RAG 파이프라인 개선
- A100 GPU 서버에서 vLLM 서빙 및 부하 테스트
- Spring Boot, FastAPI, React 기반 서비스 구현

## Projects

| Project | Description | Stack |
| --- | --- | --- |
| 서울노동권익센터 AI 노무상담 챗봇 | 노동 상담 데이터를 기반으로 답변 근거를 찾고 상담 연계까지 이어지는 챗봇입니다. 비공개 프로젝트입니다. | Spring Boot, React, MariaDB, vLLM, Ollama |
| [korean-chatbot](https://github.com/sunwoo8478/korean-chatbot) | 한국어 공공데이터 문서를 검색하고 답변 근거를 함께 보여주는 RAG 서비스입니다. | FastAPI, PostgreSQL, pgvector, React |
| [PayFit ERP](https://github.com/sunwoo8478/ERP) | 근태, 급여 계산, 법정 공제, 명세서 발급 흐름을 하나로 묶은 HR 시스템입니다. | Kotlin, Spring Boot, PostgreSQL, TypeScript |

## Stack

| Area | Tools |
| --- | --- |
| Backend | Java, Kotlin, Spring Boot, Spring Security, FastAPI |
| AI / Search | RAG, vLLM, Ollama, bge-m3, BGE-Reranker |
| Data | MariaDB, PostgreSQL, pgvector, Redis |
| Frontend | React, TypeScript, Vite |
| Ops | Docker, GitHub Actions, Linux, Grafana, KT Cloud GPU |

## Notes

| Topic | Focus |
| --- | --- |
| API | 요청과 응답이 명확한 구조 |
| Search | 실패 케이스를 수집하고 개선할 수 있는 검색 흐름 |
| LLM Serving | TTFT, 처리량, 동시 요청 수를 실제로 측정하는 운영 |
| Data | 인덱스, 트랜잭션, 마이그레이션을 고려한 설계 |
| Logs | 문제가 생겼을 때 위치를 좁힐 수 있는 기록 |

<details>
<summary>GitHub activity</summary>

<br>

<div align="center">

![GitHub Streak](https://streak-stats.demolab.com/?user=sunwoo8478&theme=dark&hide_border=true&locale=ko&date_format=Y.m.j)

<img src="./assets/github-stats-card.svg" width="100%" alt="이선우 GitHub 지표">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/sunwoo8478/sunwoo8478/output/snake-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/sunwoo8478/sunwoo8478/output/snake.svg">
  <img alt="snake animation" src="https://raw.githubusercontent.com/sunwoo8478/sunwoo8478/output/snake.svg">
</picture>

</div>

</details>
