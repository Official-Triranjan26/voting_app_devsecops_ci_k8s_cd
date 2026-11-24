# Development Roadmap --- DevOps Voting Platform

## 1. Goal and working approach

Build a secure, automated, GitOps-driven application platform using
Docker Example Voting App, Kubernetes, Terraform, and AWS EKS.

The roadmap is designed around learning and independent implementation.
For every stage follow:

**Learn → Design → Implement manually → Test → Break deliberately →
Troubleshoot → Document → Explain.**

The user wants to understand each command and configuration and make
changes manually wherever practical. Codex should guide, review,
explain, and troubleshoot rather than silently completing the project.

**Estimated effort:** approximately 130--165 hours, including
implementation, testing, troubleshooting, and documentation. This is an
estimate, not a deadline.

## 2. Stage overview

  ------------------------------------------------------------------------------
  Stage            Name                          Estimate Main outcome
  ---------------- ---------------- --------------------- ----------------------
  0                Foundation and                  6--8 h Working Compose app
                   application                            and understood
                   understanding                          architecture

  1                CI pipeline and               10--12 h Automated tests, image
                   container                              builds, and GHCR
                   registry                               publishing

  2                DevSecOps                     12--16 h Enforced secret,
                   integration                            Dockerfile, and image
                                                          security checks

  3                Local Kubernetes              18--22 h Complete application
                   and Helm                               deployed to kind using
                                                          Helm

  4                GitOps with Argo              12--15 h Git-driven automated
                   CD                                     deployment and
                                                          reconciliation

  5                Monitoring and                14--18 h Dashboards, actionable
                   centralized                            alert, and searchable
                   logging                                logs

  6                Terraform and                 20--24 h Reproducible AWS VPC,
                   AWS                                    EKS, and ECR
                   infrastructure                         infrastructure

  7                Migration to AWS              14--18 h Application running on
                   EKS                                    EKS through GitOps

  8                Production                    14--20 h Reliability/security
                   hardening and                          controls, incidents,
                   finalization                           load test, and demo
  ------------------------------------------------------------------------------

At 10 hours/week: roughly 13--17 weeks. At 15 hours/week: roughly 9--11
weeks. At 20 hours/week: roughly 7--9 weeks.

## 3. Stage 0 --- Foundation and application understanding

**Estimate:** 6--8 hours\
**Objective:** Understand the workload before adding delivery and
infrastructure tooling.

### Activities

1.  Fork Docker Example Voting App.
2.  Inspect the README, source tree, Dockerfiles, and Compose
    configuration.
3.  Run the application with `docker compose up --build`.
4.  Verify the Vote → Redis → Worker → PostgreSQL → Result flow.
5.  Inspect ports, environment variables, networks, volumes, and service
    dependencies.
6.  Draw the architecture using Mermaid.
7.  Create the user's repository structure, initial README, ADR
    template, and initial runbook structure.

### Success criteria

-   Application starts successfully with Compose.
-   Voting and result display work.
-   All five components and their communication paths can be explained.
-   The user can draw the architecture from memory.
-   Initial repository documentation is committed.

## 4. Stage 1 --- CI pipeline and container registry

**Estimate:** 10--12 hours\
**Objective:** Automate tests, image builds, tagging, and publishing.

### Activities

1.  Learn GitHub Actions workflows, triggers, runners, jobs, steps,
    permissions, artifacts, and caching.
2.  Create CI workflow(s) for relevant application components.
3.  Add available unit tests; add focused tests where useful and
    practical.
4.  Add integration/smoke verification for the application flow.
5.  Build custom application images.
6.  Use Docker BuildKit and layer caching.
7.  Tag application images with the Git commit SHA.
8.  Publish successful application images to GHCR.
9.  Pin upstream Redis/PostgreSQL versions or digests rather than
    rebuilding them without reason.

### Success criteria

-   Relevant code changes trigger CI.
-   Tests run before image publishing.
-   Failed tests prevent publishing.
-   Application images build and publish to GHCR.
-   Each build is traceable to a Git commit.
-   The user can explain job dependencies, caching, tags, and failure
    behavior.

## 5. Stage 2 --- DevSecOps integration

**Estimate:** 12--16 hours\
**Objective:** Detect and prevent common security and container hygiene
problems.

### Activities

1.  Integrate Gitleaks for secret scanning.
2.  Integrate Hadolint for Dockerfile linting.
3.  Integrate Trivy for image vulnerability scanning.
4.  Initial Trivy policy: CRITICAL blocks; HIGH warns/reports; MEDIUM
    and LOW are reported. Revisit this policy based on findings.
5.  Configure Dependabot for application dependencies, Docker base
    images where supported, and GitHub Actions.
6.  Harden custom images: non-root user, minimal/pinned base images,
    multi-stage builds where suitable, `.dockerignore`, and reduced
    unnecessary packages.
7.  Set least-privilege GitHub Actions permissions.
8.  Document exceptions and remediation.

### Success criteria

-   A dummy secret in a test branch is detected.
-   A deliberately poor Dockerfile triggers a lint finding.
-   A known critical test vulnerability blocks the image gate.
-   Findings are triaged and remediated or justified.
-   Custom application containers run as non-root where feasible.
-   Dependency update PRs can be generated.
-   Security workflow permissions are restricted.

## 6. Stage 3 --- Local Kubernetes and Helm

**Estimate:** 18--22 hours\
**Objective:** Deploy and operate the five components on a local
Kubernetes cluster.

### Activities

1.  Create a kind cluster.
2.  Learn and write raw Kubernetes YAML before templating.
3.  Deploy Vote, Result, Worker, Redis, and PostgreSQL.
4.  Configure Deployments, Services, and an appropriate PostgreSQL
    StatefulSet/PVC design.
5.  Configure ConfigMaps and Secrets; remember base64 is not encryption.
6.  Configure persistent storage and test database data survival after
    pod recreation.
7.  Configure startup, readiness, and liveness probes appropriately.
8.  Set CPU/memory requests and limits.
9.  Practice scaling, rolling updates, rollout history, and rollback.
10. Configure internal service discovery and application communication.
11. Configure a local Ingress controller and expose Vote/Result.
12. Convert raw manifests into a Helm chart.
13. Add development and production values files.

### Success criteria

-   All five components run and communicate.
-   Vote and Result are accessible.
-   Deleting a stateless pod leads to recovery.
-   PostgreSQL data survives pod recreation.
-   Probes and resource policies behave as expected.
-   Rolling update and rollback are demonstrated.
-   Helm lint, template, install, upgrade, and uninstall work.
-   Environment-specific values are separated.

## 7. Stage 4 --- GitOps with Argo CD

**Estimate:** 12--15 hours\
**Objective:** Make Git the source of truth for application desired
state.

### Activities

1.  Install Argo CD on kind.
2.  Create GitOps application and environment configuration.
3.  Configure Argo CD to deploy the Helm chart.
4.  Separate CI artifact creation from CD deployment.
5.  After successful CI and publishing, update the image tag in GitOps
    configuration.
6.  Let Argo CD detect and reconcile the change.
7.  Configure development and production values.
8.  Deliberately introduce manual cluster drift and observe Argo CD.
9.  Revert a bad GitOps commit to roll back the deployment.

### Success criteria

-   Successful application change produces a GitOps image-reference
    update.
-   Failed CI does not update the deployment reference.
-   Argo CD deploys the new image from Git.
-   Normal application deployment does not require manual
    `kubectl apply`.
-   Drift is visible and can be reconciled.
-   Git revert restores the previous desired version.

## 8. Stage 5 --- Monitoring and centralized logging

**Estimate:** 14--18 hours\
**Objective:** Observe cluster/application health and investigate
failures.

### Activities

1.  Install kube-prometheus-stack.
2.  Understand Prometheus, Grafana, Alertmanager, Node Exporter, and
    kube-state-metrics.
3.  Build dashboards for cluster health, application health where
    metrics exist, and resource utilization.
4.  Configure a small set of actionable alerts: unavailable
    replicas/pods, repeated restarts, sustained resource pressure, node
    unavailability, and application availability where measurable.
5.  Route at least one alert to Slack.
6.  Install Loki and configure log collection.
7.  Query application logs through Grafana.
8.  Simulate failures and correlate alerts, metrics, events, and logs.

### Success criteria

-   Prometheus collects cluster metrics.
-   Useful dashboards show node/pod health and resource usage.
-   A deliberate failure triggers an appropriate alert.
-   Slack receives the notification.
-   Application logs can be searched in Loki.
-   The user can explain how metrics and logs helped diagnose a failure.

**Career milestone:** Begin targeted job applications after this stage
while continuing the remaining project work.

## 9. Stage 6 --- Terraform and AWS infrastructure

**Estimate:** 20--24 hours\
**Objective:** Provision cloud infrastructure reproducibly with
Terraform.

### Activities

1.  Learn providers, resources, data sources, variables, outputs,
    locals, modules, dependencies, and state.
2.  Create a Terraform repository/module structure.
3.  Bootstrap an S3 backend with encryption, versioning, restricted
    access, and supported state locking (consider S3 native lockfile
    support).
4.  Design a VPC with public/private subnets, route tables, Internet
    Gateway, and deliberate egress/NAT strategy.
5.  Provision EKS and worker capacity.
6.  Create ECR repositories.
7.  Configure IAM roles and least-privilege policies.
8.  Add `terraform fmt`, `terraform validate`, and Checkov to CI.
9.  Review plans before applying.
10. Document costs, state recovery, and teardown.

### Success criteria

-   Terraform code is formatted and validates.
-   Checkov runs in CI and configured policy failures are visible.
-   AWS infrastructure can be provisioned from code.
-   Remote state and locking work.
-   Network architecture and IAM permissions can be explained.
-   Terraform plan shows expected changes.
-   Infrastructure can be destroyed and recreated cleanly.
-   Orphaned resources are checked after teardown.

## 10. Stage 7 --- Migration to AWS EKS

**Estimate:** 14--18 hours\
**Objective:** Move the proven local Kubernetes/GitOps workload to AWS.

### Activities

1.  Configure kubectl access to EKS.
2.  Configure GitHub OIDC trust and an appropriately scoped IAM role.
3.  Publish/migrate application images to ECR.
4.  Configure EKS image pull access.
5.  Install/configure AWS Load Balancer Controller.
6.  Expose Vote and Result using an ALB.
7.  Configure EBS CSI and persistent storage for PostgreSQL.
8.  Install/configure Argo CD on EKS.
9.  Connect the existing GitOps flow to EKS.
10. Verify application behavior, persistence, ingress, monitoring, and
    rollback.

### Success criteria

-   All five components run on EKS.
-   Vote and Result are accessible through the ALB.
-   Application images are pulled from ECR.
-   GitHub Actions uses OIDC, not long-lived AWS keys.
-   Argo CD deploys application changes.
-   PostgreSQL storage survives pod recreation.
-   Monitoring/logging works on EKS.
-   Git revert rolls back an application release.

## 11. Stage 8 --- Production hardening and finalization

**Estimate:** 14--20 hours\
**Objective:** Demonstrate operational maturity, reliability, security,
and the ability to explain the system.

### Activities

1.  Configure HPA and validate metrics/requests.
2.  Configure PDBs and understand their limits.
3.  Add NetworkPolicies and verify actual allowed/blocked traffic.
4.  Improve workload security: non-root, read-only filesystem where
    feasible, dropped capabilities, seccomp, service accounts, and RBAC.
5.  Configure AWS Budget and billing alerts.
6.  Evaluate Spot instances only for suitable workloads.
7.  Run k6 load tests and record methodology/results.
8.  Document 2--3 real incident investigations, such as
    CrashLoopBackOff, ALB 502, or database connectivity.
9.  Complete README, architecture, ADRs, runbooks, deployment and cost
    documentation.
10. Record a concise five-minute demo.

### Success criteria

-   HPA scales under a reproducible load test.
-   PDBs are configured and their behavior is understood.
-   NetworkPolicies enforce intended communication boundaries.
-   Workload security settings are verified.
-   AWS budget alert is configured.
-   k6 results and limitations are documented.
-   At least 2--3 real incident reports are complete.
-   Another developer can follow the README to reproduce the project.
-   The user can demonstrate and defend the architecture in an
    interview.

## 12. Explicitly out of initial scope

Do not add these during the core roadmap unless a concrete need emerges:

-   Kyverno
-   Cosign
-   Argo Rollouts
-   Distributed tracing
-   Chaos Mesh / dedicated chaos tooling
-   Karpenter
-   External Secrets Operator
-   RDS migration
-   Custom domain

The aim is a well-understood, working project, not the largest possible
tool list.

## 13. Definition of overall completion

The project is ready for portfolio/interview use when:

-   A clean code change passes tests and security gates.
-   Versioned images are published.
-   GitOps configuration is updated only after successful CI.
-   Argo CD deploys and reconciles the desired state.
-   The application runs on EKS and is accessible through ALB.
-   Infrastructure is managed through Terraform.
-   GitHub-to-AWS authentication uses OIDC.
-   Monitoring, alerting, and centralized logs are functional.
-   A rollback and multiple troubleshooting exercises have been
    demonstrated.
-   Documentation accurately describes the real implementation.
-   The user can explain key decisions, trade-offs, failure modes, and
    cost considerations.

Completion does not guarantee a particular salary or job offer. It
provides concrete evidence of practical skills to support the user's
career transition.
