# Implementation Status

> **Status accuracy rule:** This file records only what has been
> confirmed. Do not mark a task complete merely because it is planned,
> discussed, or described in project documentation.

## 1. Current overall status

**Current stage: Pre-implementation / Stage 0 not yet confirmed
complete.**

The project choice, technology baseline, high-level architecture,
development phases, and working practices have been discussed and agreed
as the current plan. The available context does not confirm that the
project repository has been forked or that any project stage has been
completed.

Do not infer implementation progress from the user's general Kubernetes
learning. The user has previously studied Kubernetes fundamentals and
practiced concepts such as Pods, ReplicaSets, Deployments, rollouts,
Services, environment variables, ConfigMaps, Secrets, Volumes, and HPA.
This is prior learning, not proof that the voting application has been
deployed to Kubernetes.

## 2. Confirmed planning decisions

-   Project selected: Docker Example Voting App.
-   CI: GitHub Actions rather than Jenkins.
-   Initial image registry: GHCR.
-   AWS image registry: ECR.
-   Security tools: Gitleaks, Hadolint, Trivy, Dependabot.
-   Local Kubernetes: kind.
-   Kubernetes packaging: Helm.
-   GitOps: Argo CD.
-   Infrastructure as Code: Terraform.
-   Cloud platform: AWS EKS.
-   GitHub-to-AWS authentication: OIDC; no long-lived AWS access keys.
-   Monitoring: kube-prometheus-stack (Prometheus, Grafana,
    Alertmanager).
-   Logging: Loki.
-   Terraform checks: `terraform fmt`, `terraform validate`, Checkov.
-   Load testing: k6.
-   Deferred: Kyverno, Cosign, Argo Rollouts, tracing, chaos tooling,
    Karpenter, External Secrets, RDS, custom domain.

## 3. Stage tracking

  --------------------------------------------------------------------------
  Stage             Description       Status            Evidence / notes
  ----------------- ----------------- ----------------- --------------------
  0                 Foundation and    Not started /     Fork, Compose run,
                    application       unverified        architecture diagram
                    understanding                       and repo setup are
                                                        not confirmed

  1                 CI pipeline and   Pending           GitHub Actions
                    container                           build/test/publish
                    registry                            not confirmed

  2                 DevSecOps         Pending           Gitleaks, Hadolint,
                    integration                         Trivy and Dependabot
                                                        not confirmed

  3                 Local Kubernetes  Pending           Voting app
                    and Helm                            deployment to kind
                                                        and Helm chart not
                                                        confirmed

  4                 GitOps with Argo  Pending           Local Argo CD
                    CD                                  workflow not
                                                        confirmed

  5                 Monitoring and    Pending           Dashboards, alerts,
                    logging                             Slack and Loki not
                                                        confirmed

  6                 Terraform and AWS Pending           Terraform modules,
                    infrastructure                      remote state, VPC
                                                        and EKS not
                                                        confirmed

  7                 Migration to AWS  Pending           ECR, OIDC, ALB, EBS
                    EKS                                 CSI and EKS
                                                        application not
                                                        confirmed

  8                 Production        Pending           HPA, PDB,
                    hardening and                       NetworkPolicies, k6,
                    finalization                        incidents and demo
                                                        not confirmed
  --------------------------------------------------------------------------

## 4. Current next action

Start Stage 0:

1.  Fork the upstream Docker Example Voting App into the user's own
    GitHub account.
2.  Inspect the upstream repository structure and README.
3.  Run the application using Docker Compose.
4.  Verify the Vote, Redis, Worker, PostgreSQL, and Result data flow.
5.  Inspect Dockerfiles, ports, environment variables, volumes, and
    dependencies.
6.  Create the project repository structure without unnecessarily
    breaking the upstream app.
7.  Write the first architecture diagram and initial README.
8.  Create an ADR template and initial runbook structure.

Only update Stage 0 to complete after the success criteria in
`DEVELOPMENT_ROADMAP.md` are demonstrated.

## 5. User's relevant background

-   Approximately two years of Qt/C++ Windows application development
    experience.
-   AWS Developer Associate certification.
-   Some MERN development/freelancing experience.
-   Currently developing skills in Linux, networking, AWS, Docker,
    CI/CD, Jenkins, and Kubernetes.
-   Career target: DevOps Engineer, Cloud Engineer, Build/Release
    Engineer, or junior SRE roles; avoid senior-level roles.
-   Target compensation discussed: approximately 8--10 LPA, up from
    around 4 LPA.

The project should help bridge the practical experience gap. It does not
by itself guarantee a particular job title or salary.

## 6. Update protocol for Codex

After a meaningful work session:

1.  Inspect the actual repository and command/test results.
2.  Update only the tasks that were actually completed.
3.  Record the current stage and the next concrete task.
4.  Add new technical decisions to `ARCHITECTURE_DECISIONS.md`.
5.  Add real problems, root causes, fixes, commands, and lessons to
    `TROUBLESHOOTING_LOG.md`.
6.  Keep the roadmap status synchronized.
7.  Distinguish clearly between:
    -   **Done:** implemented and verified.
    -   **In progress:** currently being implemented.
    -   **Pending:** planned but not started.
    -   **Blocked:** cannot proceed; explain the blocker.
    -   **Unverified:** may exist, but evidence has not been checked.

Never fabricate test results, deployment status, screenshots, metrics,
incidents, or completion evidence.
