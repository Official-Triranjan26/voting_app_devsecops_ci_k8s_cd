# Architecture Decisions

This file records the current architectural baseline and the reasoning
behind it. Decisions are provisional until implemented and validated.
When implementation reveals a better approach, add a new decision or
superseding ADR rather than silently rewriting history.

## Decision summary

  ---------------------------------------------------------------------------------
  ID                      Decision                          Current status
  ----------------------- --------------------------------- -----------------------
  ADR-001                 GitHub Actions over Jenkins for   Accepted as project
                          this project                      baseline

  ADR-002                 AWS OIDC over long-lived access   Accepted as project
                          keys                              baseline

  ADR-003                 Argo CD for GitOps deployment     Accepted as project
                                                            baseline

  ADR-004                 Trivy severity policy             Accepted as initial
                                                            policy; tune with
                                                            evidence

  ADR-005                 Helm for Kubernetes packaging     Accepted as project
                                                            baseline

  ADR-006                 GHCR initially, ECR on AWS        Accepted as project
                                                            baseline

  ADR-007                 Prometheus/Grafana/Alertmanager   Accepted as project
                          and Loki                          baseline

  ADR-008                 Terraform remote state in S3      Accepted as project
                                                            baseline

  ADR-009                 PostgreSQL persistence strategy   To validate during
                                                            Kubernetes design

  ADR-010                 AWS VPC and EKS network design    To validate during
                                                            Terraform design
  ---------------------------------------------------------------------------------

------------------------------------------------------------------------

## ADR-001 --- GitHub Actions over Jenkins

**Status:** Accepted

### Context

The project needs CI automation for tests, Docker builds, security
checks, and publishing images. The user has some Jenkins
learning/background, but does not want to operate a separate Jenkins
server for this portfolio project.

### Decision

Use GitHub Actions.

### Reasons

-   Integrated with the GitHub repository and pull requests.
-   No Jenkins controller/server to provision and maintain.
-   Supports hosted runners and workflow caching.
-   Supports OIDC federation to AWS.
-   Commonly encountered in modern engineering job descriptions.

### Alternatives considered

-   **Jenkins:** valuable to learn and already part of the user's
    background, but adds server administration and maintenance for this
    project's needs.
-   **GitLab CI:** capable, but GitHub Actions fits the chosen
    repository hosting workflow.

### Consequences

-   Learn workflow, jobs, steps, runners, permissions, artifacts,
    caching, and environments.
-   Keep workflow permissions minimal.
-   Jenkins knowledge remains useful and can be discussed as an
    alternative, not as the project's selected CI platform.

------------------------------------------------------------------------

## ADR-002 --- AWS OIDC over long-lived access keys

**Status:** Accepted

### Context

GitHub Actions needs permission to publish images to ECR and perform
specifically authorized AWS operations.

### Decision

Use GitHub's OIDC identity token to assume a restricted AWS IAM role. Do
not store long-lived AWS access keys in GitHub repository secrets.

### Reasons

-   Avoids long-lived credentials.
-   Uses short-lived role credentials.
-   Supports trust policies restricted to the intended GitHub
    repository, branch, or environment.
-   Demonstrates modern cloud identity and least-privilege practices.

### Consequences

-   Configure the AWS IAM OIDC provider and role trust policy.
-   Restrict the `sub` claim to the intended repository/ref or protected
    environment.
-   Grant only the AWS permissions required by each workflow.
-   Set explicit GitHub Actions `permissions`, including
    `id-token: write` only where needed.
-   Never treat OIDC as a reason to grant broad administrator
    permissions.

------------------------------------------------------------------------

## ADR-003 --- Argo CD for GitOps

**Status:** Accepted

### Context

The project needs a deployment approach where the desired application
state is stored in Git and the cluster continuously reconciles toward
that state.

### Decision

Use Argo CD to deploy and reconcile Helm-based application configuration
from the GitOps directory.

### Reasons

-   Makes Git the reviewable source of truth for desired application
    state.
-   Provides synchronization and health visibility.
-   Detects configuration drift.
-   Supports rollback by reverting the Git change.
-   Separates CI artifact creation from CD reconciliation.

### Alternatives considered

-   **GitHub Actions with direct `kubectl apply`:** simpler initially,
    but mixes CI and cluster deployment permissions and does not provide
    the same continuous reconciliation model.
-   **Flux:** a valid GitOps alternative, but Argo CD is the selected
    tool for this project.

### Consequences

-   GitHub Actions builds, tests, scans, publishes images, and updates
    the GitOps image reference only after successful gates.
-   Argo CD deploys the desired state.
-   Do not use routine direct `kubectl apply` as the application
    deployment mechanism.
-   Manual cluster changes are for deliberate troubleshooting exercises
    and should be reconciled or reverted.

------------------------------------------------------------------------

## ADR-004 --- Trivy severity policy

**Status:** Accepted as an initial policy

### Context

The project needs vulnerability scanning without making the pipeline
unusable due to every low-severity finding or unfixed upstream issue.

### Decision

Initial policy: - CRITICAL: fail the pipeline. - HIGH: report/warn
initially. - MEDIUM and LOW: report.

Review the policy after observing actual scan results.

### Reasons

-   Critical issues should block publication.
-   Initial warning treatment for HIGH provides visibility while
    allowing findings to be triaged.
-   A later policy can block HIGH vulnerabilities when the team
    understands the impact and remediation options.

### Consequences

-   Record scan output and remediation.
-   Distinguish fixed from unfixed vulnerabilities.
-   Do not blindly suppress findings.
-   Exceptions must be justified, scoped, and reviewed.
-   A test image with a known critical vulnerability should demonstrate
    that the gate works.

------------------------------------------------------------------------

## ADR-005 --- Helm for Kubernetes packaging

**Status:** Accepted

### Context

The application has multiple components and needs repeatable deployment
configuration across local development and AWS environments.

### Decision

Write and understand raw Kubernetes manifests first, then package the
application using Helm with environment-specific values.

### Reasons

-   Reusable templates reduce duplicated manifests.
-   Values files support environment differences.
-   Helm provides install, upgrade, rollback-history, and release
    management capabilities.
-   Argo CD can deploy Helm charts from Git.

### Consequences

-   Do not start by copying a complex chart without understanding the
    underlying resources.
-   Keep templates readable and values explicit.
-   Validate using `helm lint` and `helm template`.
-   Separate environment-specific settings from shared templates.
-   Do not store real credentials in committed values files.

------------------------------------------------------------------------

## ADR-006 --- GHCR initially, ECR for AWS

**Status:** Accepted

### Context

The project begins locally and should avoid requiring AWS infrastructure
before the local delivery workflow is proven.

### Decision

Use GHCR during early CI and local Kubernetes stages. Use ECR for the
AWS EKS stage.

### Reasons

-   GHCR is convenient for a GitHub-hosted project.
-   Local stages can be completed without provisioning EKS.
-   ECR integrates naturally with AWS IAM and EKS.
-   The migration provides a useful cloud integration exercise.

### Consequences

-   Use immutable Git-SHA tags for custom application images.
-   Pin third-party Redis and PostgreSQL image versions/digests where
    practical.
-   Do not build custom Redis/PostgreSQL images unless a real
    requirement exists.
-   Migrate the selected application image versions to ECR for EKS.

------------------------------------------------------------------------

## ADR-007 --- Prometheus, Grafana, Alertmanager, and Loki

**Status:** Accepted

### Context

The project needs metrics, dashboards, alerting, and centralized logs
for Kubernetes operations and troubleshooting.

### Decision

Use kube-prometheus-stack for Prometheus, Grafana, Alertmanager, and
standard Kubernetes exporters; use Loki for log aggregation and
querying.

### Reasons

-   Common Kubernetes observability stack.
-   Prometheus supports metrics collection and alert rules.
-   Grafana provides dashboards and a shared interface for metrics and
    logs.
-   Alertmanager routes notifications.
-   Loki provides centralized log querying.

### Consequences

-   Build useful dashboards, not just install the tools.
-   Start with a small number of actionable alerts.
-   Configure log retention and cost controls.
-   Distinguish cluster metrics from application metrics.
-   Add application instrumentation only where useful and supported.

------------------------------------------------------------------------

## ADR-008 --- Terraform remote state in S3

**Status:** Accepted

### Context

Terraform will provision shared AWS infrastructure. Local-only state is
unsuitable for a reproducible, recoverable project workflow.

### Decision

Use an S3 backend with encryption, versioning, and state locking. Prefer
the S3 backend's supported native lockfile mechanism (`use_lockfile`)
where compatible with the selected Terraform version and setup.

### Reasons

-   Centralized state storage.
-   State versioning supports recovery.
-   Locking reduces concurrent state modification risk.
-   Keeps state out of the Git repository.

### Consequences

-   Bootstrap the backend separately before using it for the main
    infrastructure.
-   Never commit state or state backups.
-   Restrict access to the state bucket.
-   Do not assume state contains no secrets.
-   Document recovery and cleanup carefully.
-   DynamoDB locking is an older pattern; do not add it automatically if
    native S3 lockfiles are being used.

------------------------------------------------------------------------

## ADR-009 --- PostgreSQL persistence strategy

**Status:** To validate during Stage 3

### Context

PostgreSQL needs persistent storage for the application to retain
processed votes when a pod is recreated.

### Current direction

Use a PVC-backed PostgreSQL workload on local kind and later evaluate a
StatefulSet with an appropriate StorageClass on EKS.

### Alternatives

-   Deployment plus PVC for a simple single-instance local learning
    setup.
-   StatefulSet plus PVC for stable identity and storage association.
-   Managed RDS as a future alternative, deliberately outside the
    initial scope.

### Questions to resolve

-   What does the upstream application require?
-   Is one database replica sufficient for this portfolio workload?
-   What are the backup and restore expectations?
-   How will storage behave across pod recreation and node/AZ
    constraints?
-   What is the cleanup and data-retention policy?

A PVC is not a backup strategy. Document backup/recovery limitations.

------------------------------------------------------------------------

## ADR-010 --- AWS VPC and EKS network design

**Status:** To validate during Stage 6

### Current direction

Use a dedicated VPC with public subnets for internet-facing
load-balancer resources and private subnets for EKS worker nodes,
subject to EKS and load-balancer subnet-discovery requirements.

### Design considerations

-   Internet Gateway and public route tables.
-   NAT Gateway or another deliberate egress strategy for private
    workloads.
-   Availability Zone coverage.
-   EKS control-plane connectivity and endpoint access.
-   Security groups and network ACLs where appropriate.
-   ALB subnet tagging/discovery.
-   Cost impact of NAT Gateways and load balancers.

Do not implement a network diagram without validating actual routing,
subnet tags, security-group rules, and AWS service requirements.

------------------------------------------------------------------------

## ADR maintenance rules

For every new decision: 1. Record the context/problem. 2. List realistic
alternatives. 3. Explain the selected option and why. 4. Record
trade-offs and consequences. 5. Mark the decision as proposed, accepted,
superseded, or rejected. 6. Do not rewrite history when a decision
changes; add a superseding decision.
