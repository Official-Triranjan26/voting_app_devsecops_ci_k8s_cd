# Troubleshooting Log

> This is a factual project log, not a list of hypothetical incidents.
> Add an entry only after the problem has actually occurred and been
> investigated. Do not invent root causes, command output, fixes, or
> incident impact.

## 1. Current recorded incidents

**No project-specific incidents have been confirmed yet.**

The project is currently at the planning / pre-implementation baseline.
The user has previous experience troubleshooting other development and
infrastructure tasks, but those should not be represented as incidents
from this voting-platform project unless they are encountered again and
recorded in this repository.

## 2. Incident entry template

Copy this section for each real issue.

``` markdown
## YYYY-MM-DD — Short incident title

### Environment
- Stage:
- Local / kind / AWS EKS:
- Component:
- Version / image tag:
- Namespace (if Kubernetes):

### Symptoms
What did you observe? Include exact error messages and relevant status.

### Impact
What functionality was affected? Was this local development or a deployed environment?

### Investigation
Commands and observations, in order:
1.
2.
3.

### Root cause
The verified underlying cause. Distinguish evidence from assumptions.

### Resolution
Exact changes or commands used to fix the issue.

### Verification
How was the fix tested? Include relevant command output or test result.

### Prevention / follow-up
What should change to prevent recurrence?

### Lessons learned
What concept or operational lesson did this incident teach?
```

## 3. Useful investigation command reference

These are reference commands, not claims that they have already been
run. Check the current context and namespace before executing them.

### Docker Compose

``` bash
docker compose ps
docker compose logs
docker compose logs <service>
docker compose config
docker inspect <container>
docker network ls
docker volume ls
```

### Kubernetes

``` bash
kubectl get pods -A
kubectl get events -A --sort-by=.metadata.creationTimestamp
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous
kubectl get deployments,replicasets,services -n <namespace>
kubectl get endpoints -n <namespace>
kubectl get pvc,pv -n <namespace>
kubectl describe pvc <pvc-name> -n <namespace>
kubectl top pods -n <namespace>
kubectl rollout status deployment/<deployment-name> -n <namespace>
kubectl rollout history deployment/<deployment-name> -n <namespace>
```

### Helm

``` bash
helm list -A
helm status <release-name> -n <namespace>
helm history <release-name> -n <namespace>
helm lint <chart-path>
helm template <release-name> <chart-path> -f <values-file>
```

### Argo CD

Use the Argo CD CLI or UI to inspect: - Application sync status. -
Application health. - Comparison/diff. - Sync operation details. -
Repository access errors. - Reconciliation events.

Do not record a command as executed unless it was actually executed.

### Terraform

``` bash
terraform fmt -check -recursive
terraform validate
terraform init
terraform plan
terraform state list
terraform output
```

Be careful with `terraform apply`, `terraform destroy`, state
manipulation, and commands that change cloud resources. Review the plan
and confirm the target account/region/workspace before applying or
destroying.

### AWS / EKS

``` bash
aws sts get-caller-identity
aws eks describe-cluster --name <cluster-name> --region <region>
kubectl get nodes
kubectl get ingress -A
```

Confirm AWS account and region before making changes.

## 4. Planned failure exercises (not incidents yet)

These are intentional tests to perform during the roadmap. Once
performed, record the actual observations and results as incident or
exercise entries.

  -----------------------------------------------------------------------
  Planned exercise                    What to investigate
  ----------------------------------- -----------------------------------
  A unit test fails in CI             Job dependencies and publish
                                      prevention

  A dummy secret is committed to a    Gitleaks detection and remediation
  test branch                         

  A vulnerable test image is scanned  Trivy severity gate

  Invalid container image is deployed ImagePullBackOff and events

  Application starts with invalid     Logs, environment variables,
  configuration                       ConfigMaps/Secrets

  Container exceeds memory limit      OOMKilled, resource limits and
                                      metrics

  PostgreSQL pod is recreated         PVC attachment and data persistence

  Service selector is incorrect       Endpoints and service discovery

  Manual cluster drift is introduced  Argo CD OutOfSync and
                                      reconciliation

  GitOps update references a bad      Sync/health failure and Git revert
  image                               

  ALB target becomes unhealthy        Target health, readiness, ports and
                                      security groups

  Terraform configuration is changed  Plan review and infrastructure
                                      drift
  -----------------------------------------------------------------------

## 5. Logging standards

-   Record dates and the stage where the issue occurred.
-   Preserve exact error messages where safe.
-   Redact passwords, tokens, access keys, personal information, and
    other secrets.
-   Separate observed facts from hypotheses.
-   Record the command and relevant output, not just "checked logs".
-   Explain why the fix worked.
-   Include a verification step.
-   Prefer prevention actions that address the root cause rather than
    adding a superficial workaround.
