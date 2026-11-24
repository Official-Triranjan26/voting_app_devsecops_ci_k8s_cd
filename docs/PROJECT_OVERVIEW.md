# Project Overview --- DevOps Voting Platform

## 1. Project purpose

Build a portfolio-quality DevOps/DevSecOps platform around Docker's
Example Voting App. The application is the workload used to demonstrate
the engineering practices; the main value of the project is the delivery
platform built around it.

The project should demonstrate that the developer can design, automate,
secure, deploy, operate, troubleshoot, and explain a multi-service
application on Kubernetes and AWS.

**Career objective:** support a transition into DevOps / Cloud
Engineering roles, targeting approximately 8--10 LPA in India. The user
has around two years of Qt/C++ Windows application development
experience, an AWS Developer Associate certification, and some MERN
development/freelancing experience. Position the profile as a software
developer transitioning into DevOps/Cloud engineering, not as an
experienced senior DevOps engineer.

## 2. Project selected

**Docker Example Voting App** (upstream open-source project).

It is a five-component sample application:

  Component    Technology       Responsibility
  ------------ ---------------- ------------------------------------
  Vote         Python / Flask   Accepts votes from users
  Redis        Redis            Temporarily stores incoming votes
  Worker       .NET             Processes votes and writes results
  PostgreSQL   PostgreSQL       Stores processed vote data
  Result       Node.js          Displays voting results

The expected high-level data flow is:

1.  A user submits a vote through the Vote web application.
2.  Vote publishes/stores the vote in Redis.
3.  The Worker consumes the vote from Redis.
4.  Worker writes the processed result to PostgreSQL.
5.  Result reads from PostgreSQL and displays the updated result.

The application is initially run with Docker Compose. The upstream
project commonly exposes the Vote application on port `8080` and Result
on port `8081`; verify the checked-out Compose configuration rather than
assuming these values never change.

The upstream repository also contains Kubernetes specifications. Treat
those as learning references, not as production-ready manifests to copy
without review. The upstream README notes that the sample is not
intended to represent a perfectly architected production application.

## 3. Project objectives

The finished project should demonstrate:

-   CI automation with GitHub Actions.
-   Automated tests and quality gates.
-   Container image building, versioning, caching, and publishing.
-   DevSecOps checks and remediation.
-   Kubernetes workload management and Helm packaging.
-   GitOps deployment and reconciliation with Argo CD.
-   AWS infrastructure provisioning with Terraform.
-   Secure GitHub-to-AWS authentication using OIDC.
-   EKS deployment, ECR image hosting, ALB ingress, and persistent
    storage.
-   Metrics, dashboards, alerting, and centralized logs.
-   Operational troubleshooting, incident documentation, and cost
    awareness.

The project must be independently understandable and reproducible. The
user should be able to explain and justify important implementation
decisions rather than merely demonstrate that the application runs.

## 4. Target architecture

### Delivery flow

``` text
Developer change
      |
      v
GitHub repository
      |
      v
GitHub Actions CI
  - checkout
  - tests
  - lint / quality checks
  - build application images
  - scan images
      |
      v
GHCR (initial development stages)
      |
      | Later: publish/migrate images to ECR
      v
GitOps configuration in the repository
  - versioned image references
  - Helm values / environment configuration
      |
      v
Argo CD
  - observes Git desired state
  - detects drift
  - reconciles Kubernetes resources
      |
      v
Kubernetes
  - local: kind
  - cloud: AWS EKS
```

GitHub Actions is responsible for CI and artifact creation. It may
update the GitOps configuration after all required checks and publishing
succeed. Argo CD is responsible for application deployment and
reconciliation. Do not make the normal application deployment path
depend on GitHub Actions running `kubectl apply`.

### Infrastructure and operations

Terraform provisions AWS infrastructure independently of application
delivery:

``` text
Terraform
  |
  +-- VPC
  |    +-- public subnets
  |    +-- private subnets
  |    +-- route tables
  |    +-- Internet Gateway
  |    +-- NAT Gateway (where required)
  |
  +-- EKS cluster and worker capacity
  +-- ECR repositories
  +-- IAM roles and policies
  +-- supporting security/network configuration

EKS
  +-- Vote
  +-- Redis
  +-- Worker
  +-- PostgreSQL
  +-- Result
  +-- Argo CD
  +-- AWS Load Balancer Controller
  +-- EBS CSI driver

Observability
  +-- Prometheus
  +-- Grafana
  +-- Alertmanager
  +-- Loki
```

Prometheus/Grafana/Alertmanager provide metrics, dashboards and alerts.
Loki provides centralized log querying. Add application-level metrics
only where the application exposes them or instrumentation is
deliberately added; do not imply that cluster metrics automatically
provide request latency or application error rates.

## 5. Technology decisions (current baseline)

  -----------------------------------------------------------------------
  Area                                Selected technology
  ----------------------------------- -----------------------------------
  Application                         Docker Example Voting App

  Local application runtime           Docker Compose

  CI                                  GitHub Actions

  Secret scanning                     Gitleaks

  Dockerfile linting                  Hadolint

  Image vulnerability scanning        Trivy

  Dependency updates                  Dependabot

  Initial registry                    GHCR

  AWS registry                        ECR

  Local Kubernetes                    kind

  Packaging                           Helm

  GitOps                              Argo CD

  Infrastructure as Code              Terraform

  Cloud platform                      AWS EKS

  AWS authentication from GitHub      OIDC / assumed IAM role

  Ingress                             AWS Load Balancer Controller / ALB

  Persistent block storage            EBS CSI

  Metrics and alerting                kube-prometheus-stack (Prometheus,
                                      Grafana, Alertmanager)

  Logging                             Loki

  Load testing                        k6

  Terraform security checks           Checkov
  -----------------------------------------------------------------------

## 6. Repository structure (target; adapt as implementation evolves)

``` text
devops-voting-platform/
├── app/                         # Application source and Dockerfiles
├── tests/                       # Unit, integration and end-to-end tests, as appropriate
├── docker/                      # Shared Docker configuration, if needed
├── helm/
│   └── voting-app/
├── gitops/
│   ├── applications/
│   └── environments/
├── infra/
│   ├── modules/
│   └── environments/
├── monitoring/
│   ├── prometheus/
│   ├── grafana/
│   ├── alerts/
│   └── loki/
├── .github/
│   └── workflows/
├── docs/
│   ├── adr/
│   ├── architecture.md
│   ├── runbook.md
│   ├── incidents.md
│   ├── security.md
│   ├── deployment.md
│   └── cost-analysis.md
├── Makefile
├── README.md
└── .gitignore
```

This is a target layout, not a claim that all directories or files
already exist. Preserve the upstream application structure where
practical and avoid needless restructuring.

## 7. Engineering principles

1.  Prefer understanding and implementing manually over blindly copying
    generated configurations.
2.  Keep CI, infrastructure provisioning, GitOps deployment, and runtime
    responsibilities separate.
3.  Use immutable Git-SHA image tags for application releases; do not
    deploy `latest`.
4.  Pin third-party image versions/digests where practical. Redis and
    PostgreSQL are upstream images and do not need custom builds without
    a concrete reason.
5.  Never commit real credentials, `.env` files, Terraform state, or
    generated secrets.
6.  Use least privilege for GitHub Actions, AWS IAM, Kubernetes RBAC,
    and service accounts.
7.  Test failure paths deliberately and document root causes.
8.  Keep AWS costs controlled; destroy temporary infrastructure and
    check for orphaned resources.
9.  Make decisions explicit in ADRs and operational procedures explicit
    in runbooks.
10. Prefer a small number of well-understood tools over adding tools
    merely to enlarge the technology list.

## 8. Scope boundaries

The project is a portfolio and learning platform, not a claim of a fully
production-certified voting service. Do not over-engineer the sample
application or imply that a demo deployment is suitable for real
elections or other high-stakes use.

Initially deferred / future improvements:

-   Kyverno
-   Cosign / image signing
-   Argo Rollouts
-   Distributed tracing
-   Chaos engineering tools/tests
-   Karpenter
-   External Secrets Operator
-   RDS migration
-   Custom domain

Only add these if the core roadmap is complete and there is a clear
learning or architectural reason.

## 9. How Codex should assist

The user is learning and wants to make changes manually. Codex should
act as a technical mentor and reviewer:

-   Explain commands, concepts, architecture, and trade-offs.
-   Help inspect the current repository and identify likely issues.
-   Review code/configuration and suggest precise changes.
-   Explain the expected effect before proposing edits.
-   Prefer small, reviewable changes.
-   Do not silently modify files or run destructive commands unless
    explicitly asked.
-   Do not assume a task requires a code change: many requests are
    explanations, documentation, troubleshooting plans, or reviews.
-   When suggesting commands, explain what they do and whether they are
    destructive.
-   Verify actual repository state before claiming something is
    implemented.
-   Keep this project context synchronized by updating
    `IMPLEMENTATION_STATUS.md`, `ARCHITECTURE_DECISIONS.md`,
    `TROUBLESHOOTING_LOG.md`, and the relevant roadmap status when
    meaningful changes occur.
