#!/usr/bin/env python3
"""Replace shared Terraform boilerplate with topic-specific sections (tutorials 2–20)."""

from __future__ import annotations

import re
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent.parent
TF = ROOT / "docs" / "terraform"

# Per-slug: description, validation, best_practices, security, troubleshooting, interview, summary
# Plus optional extra_theory / extra_walkthrough appended before Validation.

SECTIONS: dict[str, dict[str, str]] = {}


def S(slug: str, **kwargs: str) -> None:
    SECTIONS[slug] = kwargs


S(
    "installing-terraform-and-the-cli-workflow",
    description="Install Terraform 1.9+, choose a version manager, and practise the non-interactive CLI loop with saved plan files.",
    extra_theory=dedent(
        """\
        ### Why version managers matter

        Production teams often pin different `required_version` floors per repository. Installing a single
        global binary works for personal labs, but **tfenv** or **asdf** lets you switch with a
        `.terraform-version` file checked into each repo — the same discipline as `.python-version` or `.nvmrc`.

        ### Automation environment variables

        | Variable | Effect |
        |----------|--------|
        | `TF_IN_AUTOMATION=1` | Reduces chatter meant for humans; clearer for CI logs |
        | `TF_INPUT=0` | Equivalent to `-input=false` for many commands |
        | `TF_LOG` / `TF_LOG_PATH` | Provider and CLI debug traces (never commit logs with secrets) |

        ### Plan files vs re-planning

        A saved plan is a **snapshot of intent**. Between plan and apply, another process can change state.
        Applying the plan file still applies that snapshot; if state moved, apply fails safely rather than
        silently computing a different plan. That is the point of `plan -out` in pull-request workflows.
        """
    ),
    extra_walkthrough=dedent(
        """\
        ### `local_file.marker` arguments

        | Argument | Purpose |
        |----------|---------|
        | `filename` | Absolute or module-relative path of the file Terraform manages |
        | `content` | Desired file body; changing it updates in place |
        | `file_permission` | POSIX mode string; omit and the provider uses its default |

        After apply, state stores the path and content checksum so the next plan can detect drift if you edit the file by hand.
        """
    ),
    validation=dedent(
        """\
        Confirm the CLI workflow end-to-end:

        ```bash
        terraform version | head -1
        terraform fmt -check
        terraform init -input=false
        terraform validate
        terraform plan -input=false -out=tfplan
        terraform show -no-color tfplan | head -40
        terraform apply -input=false tfplan
        test -f out/cli-lab.txt
        terraform destroy -input=false -auto-approve
        ```

        | Check | Pass criteria |
        |-------|----------------|
        | Version | Terraform 1.9+ reported |
        | Lockfile | `.terraform.lock.hcl` created after init |
        | Plan file | `tfplan` exists and `show` prints a create for `local_file.marker` |
        | Apply | `out/cli-lab.txt` contains the expected marker string |
        | Cleanup | Destroy removes the managed file |
        """
    ),
    best_practices=dedent(
        """\
        - Pin CLI versions per repository with tfenv/asdf and document the floor in `required_version`
        - Always run `fmt` before commit; enable `fmt -check` in CI
        - Prefer `plan -out` + apply of that artifact over `apply -auto-approve` on a live re-plan
        - Commit `.terraform.lock.hcl` for root modules so every engineer and CI get the same providers
        - Set `TF_IN_AUTOMATION=1` in pipeline jobs
        """
    ),
    security=dedent(
        """\
        - Download Terraform only from HashiCorp releases or signed distribution packages; verify checksums in air-gapped installs
        - Never commit `crash.log`, plan files from production, or local state that may contain secrets
        - Restrict who can run apply against shared state — CLI access equals change authority
        - Treat `TF_LOG_PATH` output as sensitive; scrub before sharing support bundles
        """
    ),
    troubleshooting=dedent(
        """\
        | Issue | Cause | Solution |
        |-------|-------|----------|
        | `terraform: command not found` | Binary not on PATH | Re-open shell after install; check `which terraform` |
        | Wrong version in CI | Image/binary drift | Pin version explicitly; mirror tfenv file in the job |
        | `init` hangs or fails TLS | Proxy / firewall | Configure HTTPS proxy; allow registry.terraform.io |
        | Apply differs from reviewed plan | Re-planned instead of using `-out` | Apply the saved plan file only |
        | Permission denied under `out/` | Directory missing or not writable | Create parent dirs or adjust permissions |
        """
    ),
    interview=dedent(
        """\
        1. Why commit `.terraform.lock.hcl` but gitignore `.terraform/`?
        2. What does `terraform plan -out=tfplan` protect you from in CI?
        3. When is `-auto-approve` acceptable, and when is it dangerous?
        4. How do `required_version` and a version manager work together?
        5. What is the difference between `validate` and `plan`?
        6. Why should production applies use a saved plan artifact?
        7. How would you install Terraform on an air-gapped bastion?
        8. What environment variables make Terraform safer in automation?
        9. Why is `fmt -check` useful in pull requests?
        10. What belongs in Git for a root module on day one?
        11. How does `terraform providers` help debug version skew?
        12. Describe a secure download and verification flow for the Terraform binary.
        """
    ),
    summary=dedent(
        """\
        - Install an official Terraform binary and prefer a version manager for multi-repo work
        - Memorise the loop: fmt → init → validate → plan (-out) → apply → destroy
        - Commit the lockfile; never commit provider caches or local state
        - Use non-interactive flags and saved plans for CI-grade discipline
        """
    ),
)

S(
    "hcl-fundamentals-blocks-arguments-and-expressions",
    description="Learn HCL block anatomy, types, expressions, and a clean multi-file root module layout you will reuse for the rest of the track.",
    extra_theory=dedent(
        """\
        ### String and heredoc patterns

        Prefer direct references over unnecessary interpolation:

        ```hcl
        # Prefer
        content = var.message

        # Only interpolate when building a larger string
        content = "env=${var.environment} message=${var.message}"
        ```

        Heredocs (`<<-EOT` … `EOT`) keep multi-line templates readable. Strip leading indentation with `<<-`.

        ### Sensitive and nullable types

        Variables can be `sensitive = true` (Tutorial 17) and `nullable = false` to reject explicit `null`.
        Learn the type system now so module APIs stay strict later.

        ### Comments and formatting

        HCL supports `#` and `//` line comments plus `/* */` blocks. `terraform fmt` owns whitespace —
        do not hand-align equals signs against the formatter.
        """
    ),
    extra_walkthrough=dedent(
        """\
        ### Locals vs variables

        | Construct | Input from caller? | Typical use |
        |-----------|--------------------|-------------|
        | `variable` | Yes | Tunables and environment differences |
        | `locals` | No | Derived names, joins, maps you do not want callers to override |

        `random_id.suffix` forces a unique attribute into the file so you can see resource references
        (`random_id.suffix.hex`) flow into `local_file` content through the dependency graph.
        """
    ),
    validation=dedent(
        """\
        ```bash
        terraform fmt -check
        terraform init -input=false
        terraform validate
        terraform apply -input=false -auto-approve
        terraform output
        cat generated/rebash-notes.txt
        terraform destroy -input=false -auto-approve
        ```

        | Check | Pass criteria |
        |-------|----------------|
        | Layout | Separate `versions.tf`, `variables.tf`, `main.tf`, `outputs.tf` |
        | Types | `owners` is `list(string)`; validate fails if you pass a string |
        | Outputs | `notes_path` and `suffix` print after apply |
        | Content | Notes file includes project, owners, and hex suffix |
        """
    ),
    best_practices=dedent(
        """\
        - One concern per file (`variables.tf`, `outputs.tf`) so diffs stay reviewable
        - Give every variable a `type` and `description`
        - Prefer precise types over `any`
        - Use `locals` for derived values; do not make callers pass the same join repeatedly
        - Let `terraform fmt` own formatting in CI
        """
    ),
    security=dedent(
        """\
        - Do not put secrets in default variable values or committed `.tfvars`
        - Mark secret variables `sensitive = true` as soon as you introduce them
        - Avoid writing credentials into `local_file` content even in labs — bad habits transfer
        - Review expressions that concatenate user input into filenames for path traversal risks
        """
    ),
    troubleshooting=dedent(
        """\
        | Issue | Cause | Solution |
        |-------|-------|----------|
        | Unexpected type error | List vs string mismatch | Match `type` constraints; read the error address |
        | Reference unknown | Typo in resource name | Use `terraform console` or address autocomplete in your editor |
        | Heredoc markers in output | Wrong delimiter indent | Use `<<-` and aligned closing marker |
        | fmt churn in PRs | Mixed editor settings | Run `terraform fmt` before every commit |
        """
    ),
    interview=dedent(
        """\
        1. What is the difference between an argument and an attribute in HCL?
        2. When should you use a local value instead of a variable?
        3. Why avoid `any` in module input variables?
        4. How does resource address syntax work (`local_file.notes.content`)?
        5. What do `path.module`, `path.root`, and `path.cwd` mean?
        6. How would you express a map of tags with a type constraint?
        7. Why split root modules across multiple `.tf` files?
        8. What happens if you omit `type` on a variable?
        9. How do heredocs help with multi-line templates?
        10. What is the difference between `list` and `set`?
        11. How does `terraform fmt` affect code review quality?
        12. Give an example of unnecessary string interpolation and the cleaner form.
        """
    ),
    summary=dedent(
        """\
        - HCL is block-oriented: type, labels, and a body of arguments
        - Distinguishing arguments from attributes prevents “where did that value come from?” confusion
        - Typed variables and locals keep modules readable and safe
        - A conventional multi-file layout scales from labs to production roots
        """
    ),
)

S(
    "providers-and-the-terraform-plugin-model",
    description="Understand providers as plugins, pin versions with required_providers, and configure aliases for multi-region or multi-account patterns.",
    extra_theory=dedent(
        """\
        ### Provider installation selection

        `terraform init` chooses provider packages using the dependency lock file and your platform
        (OS/CPU). The Registry serves multiple builds; the lockfile records checksums so installs are
        reproducible and tamper-evident.

        ### Configuration vs requirement

        | Block | Role |
        |-------|------|
        | `required_providers` inside `terraform {}` | Which plugins and version constraints |
        | `provider "name" { }` | How to authenticate and which region/account |

        You can have requirements without an explicit `provider` block when the provider uses
        environment credentials and defaults — but production roots should still be explicit.

        ### Aliases

        ```hcl
        provider "local" {
          alias = "alt"
        }
        ```

        Resources select an alias with `provider = local.alt`. Cloud teams use aliases for pairs like
        `aws.us_east_1` and `aws.us_west_2`, or separate accounts.
        """
    ),
    extra_walkthrough=dedent(
        """\
        Walk the lockfile after init: each provider source address maps to a version and hashes.
        Changing `required_providers` without running `terraform init -upgrade` (intentionally) keeps
        you on the locked version — that stability is desirable until you deliberately upgrade.
        """
    ),
    validation=dedent(
        """\
        ```bash
        terraform init -input=false
        terraform providers
        terraform providers schema -json | head -c 200; echo
        terraform validate
        terraform apply -input=false -auto-approve
        terraform destroy -input=false -auto-approve
        ```

        | Check | Pass criteria |
        |-------|----------------|
        | Providers | `hashicorp/local` listed at ~> 2.9 |
        | Lockfile | `.terraform.lock.hcl` contains `provider "registry.terraform.io/hashicorp/local"` |
        | Schema | Schema command returns JSON (pipe responsibly) |
        """
    ),
    best_practices=dedent(
        """\
        - Always declare `required_providers` with `source` and a pessimistic version constraint
        - Upgrade providers deliberately with `init -upgrade` and review the plan
        - Prefer explicit `provider` blocks for anything beyond local labs
        - Document required environment variables for credentials in the module README
        - Use aliases sparingly; prefer separate roots when blast radius differs
        """
    ),
    security=dedent(
        """\
        - Providers inherit your credentials — least-privilege IAM/service principals only
        - Do not hard-code access keys in provider blocks; use env vars, OIDC, or native chains
        - Review lockfile checksums in PRs when upgrading; unexpected hash changes deserve scrutiny
        - Limit who can modify `required_providers` in organisation modules
        """
    ),
    troubleshooting=dedent(
        """\
        | Issue | Cause | Solution |
        |-------|-------|----------|
        | Failed to query available provider packages | Network/registry | Check DNS/TLS to registry.terraform.io |
        | Incompatible provider version | Constraint vs lockfile | Adjust constraint and `init -upgrade`, or stay locked |
        | Missing credentials | Provider config incomplete | Export documented env vars; run `terraform plan` to see auth errors |
        | Wrong region resources | Default provider vs alias mix-up | Set `provider =` on the resource explicitly |
        """
    ),
    interview=dedent(
        """\
        1. What is a Terraform provider in the plugin model?
        2. Why pin provider versions in root modules?
        3. What is the difference between `required_providers` and a `provider` block?
        4. How does the dependency lock file improve supply-chain safety?
        5. When would you use a provider alias?
        6. How do you upgrade a provider safely in a team repo?
        7. Where should AWS credentials live for Terraform?
        8. What does `terraform providers` show you?
        9. Why might two engineers see different provider versions without a lockfile?
        10. How do child modules inherit provider configurations?
        11. What is a pessimistic constraint (`~>`)?
        12. How would you debug a provider authentication failure?
        """
    ),
    summary=dedent(
        """\
        - Providers are versioned plugins that translate resources into API calls
        - Declare and lock versions; configure authentication separately
        - Aliases support multi-region patterns; do not overuse them
        - Treat lockfile reviews as part of secure upgrades
        """
    ),
)

# Continue with tutorials 5-20 — condensed but unique
for slug, description, topic_focus, extra_key_qs in [
    (
        "variables-locals-and-outputs",
        "Design typed variables, locals, and outputs with validation blocks and clear module contracts.",
        "input validation, locals composition, and output contracts",
        [
            "When do you use variable validation blocks?",
            "Why might an output be marked sensitive?",
            "How do terraform.tfvars and -var-file interact?",
            "What is the precedence order for variable assignment?",
            "When should a value be a local instead of an output?",
            "How do you pass complex objects between modules?",
            "What happens if a validation condition fails?",
            "Why document variables with descriptions?",
            "How do nullable and default interact?",
            "When is output value referring to a resource attribute safe?",
            "How would you structure tfvars for dev vs prod?",
            "What belongs in outputs.tf versus a data file?",
        ],
    ),
    (
        "resources-and-data-sources",
        "Contrast managed resources with data sources, and practise read-only lookups beside managed local files.",
        "managed resources versus data sources",
        [
            "What is the difference between a resource and a data source?",
            "When is a data source preferable to duplicating configuration?",
            "How does Terraform decide to create, update, or replace a resource?",
            "What is ForceNew behaviour at a high level?",
            "How do you reference a data source attribute in a resource?",
            "Why can data sources cause plans to change without config edits?",
            "When should you avoid data sources at plan time?",
            "How does count/for_each change resource addressing?",
            "What appears in state for a data source?",
            "How would you import an existing object later in the track?",
            "Why pin provider versions when using data sources?",
            "Describe a safe pattern for reading remote state outputs.",
        ],
    ),
    (
        "dependencies-and-the-resource-graph",
        "Read implicit dependencies from references, use depends_on carefully, and trigger replacements with replace_triggered_by.",
        "the resource graph and replacement triggers",
        [
            "How does Terraform build the dependency graph?",
            "When is explicit depends_on necessary?",
            "What are the risks of unnecessary depends_on?",
            "How does replace_triggered_by work with terraform_data?",
            "What is the difference between update in place and replace?",
            "How do you read a cycle error?",
            "Why might parallelism settings matter?",
            "How do module boundaries affect the graph?",
            "When do provisioners create hidden dependencies?",
            "How does -target affect the graph (and why avoid it)?",
            "What is create_before_destroy used for?",
            "How would you force replacement of a resource safely?",
        ],
    ),
    (
        "terraform-state-fundamentals",
        "Inspect and reason about local state safely: list, show, pull, drift, and what must never be committed.",
        "Terraform state as the mapping between config and reality",
        [
            "What does state store, and why is it required?",
            "How do you inspect a resource in state without applying?",
            "What is refresh, and when does it run?",
            "Why is state sensitive even for local_file labs?",
            "What is terraform.tfstate.backup for?",
            "How does drift appear in a plan?",
            "When would you use terraform state rm?",
            "Why is editing state JSON by hand dangerous?",
            "How does state relate to resource addresses?",
            "What changes when you move to a remote backend?",
            "How do you recover from a lost local state file in a lab?",
            "Why exclude *.tfstate* from Git?",
        ],
    ),
    (
        "remote-state-and-backends",
        "Configure remote state backends with locking and encryption concepts, using local labs as a stepping stone.",
        "remote backends, locking, and team state",
        [
            "What problems do remote backends solve?",
            "Why is state locking mandatory for teams?",
            "How does partial backend configuration work with CI?",
            "What is terraform_remote_state used for?",
            "How do you migrate local state to remote safely?",
            "What encryption expectations should you set for state storage?",
            "Who should have read access to state?",
            "What happens if two applies race without locking?",
            "How do workspaces relate to backends?",
            "When is the local backend still acceptable?",
            "How do you break a stuck lock safely?",
            "What belongs in backend config versus provider config?",
        ],
    ),
    (
        "workspaces-and-environment-strategies",
        "Compare Terraform workspaces with separate state roots and choose environment strategies that match blast radius.",
        "workspaces versus separate roots for environments",
        [
            "What does a Terraform workspace switch under the hood?",
            "When are workspaces a poor fit for prod isolation?",
            "How do you name workspaces consistently?",
            "What is the alternative directory-per-env layout?",
            "How do backends interact with workspaces?",
            "How would you promote a change from dev to prod?",
            "What risks come from using terraform.workspace in resource names?",
            "When is a single workspace multi-account design wrong?",
            "How do CI pipelines select workspaces?",
            "What happens to state if you delete a workspace?",
            "How do modules stay environment-agnostic?",
            "Compare workspaces with Terragrunt-style roots at a high level.",
        ],
    ),
    (
        "modules-creating-reusable-infrastructure",
        "Build a child module with typed inputs and outputs, then call it from a root module with a clear contract.",
        "authoring and calling child modules",
        [
            "What makes a good module boundary?",
            "How do you version modules for consumers?",
            "Why avoid leaking too many outputs?",
            "What is path.module inside a child module?",
            "How do providers pass into modules?",
            "When should a module use count or for_each?",
            "How do you test a module locally with a source path?",
            "What belongs in the module README?",
            "How do input validations protect callers?",
            "Why pin module sources in production?",
            "What is compositional nesting versus a megamodule?",
            "How do you refactor a root into modules safely?",
        ],
    ),
    (
        "registry-modules-and-composition",
        "Consume Terraform Registry modules with version pins and compose them into a maintainable root.",
        "Registry modules and composition",
        [
            "How do you pin a Registry module version?",
            "What is the risk of source = ref without a version?",
            "How do you evaluate a public module before adopting it?",
            "When should you wrap a Registry module in an internal module?",
            "How do module outputs feed other modules?",
            "What is the difference between count and for_each on modules?",
            "How do you upgrade a module version in a controlled way?",
            "Where do you find module documentation?",
            "How do provisioners in third-party modules increase risk?",
            "What licence and maintenance signals matter?",
            "How do you mirror modules for air-gapped use?",
            "Describe a composition pattern for network + app modules.",
        ],
    ),
    (
        "meta-arguments-count-for-each-and-lifecycle",
        "Use count and for_each correctly, manage lifecycle rules, and avoid indexed address traps.",
        "meta-arguments count, for_each, and lifecycle",
        [
            "When is for_each preferable to count?",
            "Why are count index addresses fragile when lists shrink?",
            "How do you migrate from count to for_each?",
            "What does ignore_changes do, and when is it a smell?",
            "How does create_before_destroy help zero downtime?",
            "What is prevent_destroy used for?",
            "How do lifecycle blocks interact with replacements?",
            "How do you set for_each over a set of strings?",
            "What is each.key versus each.value?",
            "How does count = 0 disable a resource?",
            "Why avoid splat expressions on resources that use for_each?",
            "How would you add a lifecycle rule safely in production?",
        ],
    ),
    (
        "functions-templates-and-dynamic-blocks",
        "Apply Terraform functions, templatestring/templatefile, and dynamic blocks without over-abstracting.",
        "functions, templates, and dynamic blocks",
        [
            "Name five functions you use weekly and why.",
            "When is templatefile better than inline heredocs?",
            "What are the dangers of dynamic blocks?",
            "How do you flatten nested collections?",
            "When should you prefer a static block over dynamic?",
            "How does try() change error behaviour?",
            "What is compact() useful for?",
            "How do you build a map of tags with merge?",
            "When is lookup() appropriate versus direct indexing?",
            "How do template directives differ from HCL expressions?",
            "Why keep complex transforms in locals?",
            "How would you unit-test pure transformations?",
        ],
    ),
    (
        "import-moved-and-safe-refactors",
        "Import existing objects, use moved blocks for renames, and refactor addresses without destroying infrastructure.",
        "import, moved blocks, and safe refactors",
        [
            "What does terraform import do to state?",
            "How do import blocks differ from the CLI import command?",
            "When do you use a moved block?",
            "What happens if you rename a resource without moved?",
            "How do you plan a zero-downtime refactor?",
            "What is state mv, and when prefer moved blocks?",
            "How do you verify a refactor before apply?",
            "What risks remain after a successful import?",
            "How do for_each address changes complicate moves?",
            "When should you destroy and recreate instead?",
            "How do you document a refactor for reviewers?",
            "What CI checks catch accidental destroys?",
        ],
    ),
    (
        "format-validate-and-terraform-test",
        "Use fmt, validate, and terraform test to catch regressions before apply.",
        "fmt, validate, and Terraform test",
        [
            "What does terraform test add beyond validate?",
            "Where do .tftest.hcl files live?",
            "How do you run tests in CI?",
            "What assertions are useful for a module?",
            "Why is fmt -check valuable in pull requests?",
            "What can validate not catch?",
            "How do you structure tests for child modules?",
            "When do integration-style tests need cloud credentials?",
            "How do you keep tests hermetic with local providers?",
            "What is the difference between unit and contract tests here?",
            "How do you fail a pipeline on test failure?",
            "Why test outputs and not only resources?",
        ],
    ),
    (
        "secrets-and-sensitive-values",
        "Mark sensitive values correctly, keep secrets out of Git, and reduce accidental exposure in plans and state.",
        "sensitive values and secrets handling",
        [
            "What does sensitive = true change in CLI output?",
            "Why is state still a secret store even with sensitive flags?",
            "Where should production secrets live?",
            "How do you pass secrets into Terraform safely in CI?",
            "What is the risk of echoing secrets in local-exec?",
            "How do ephemeral values change secret handling (conceptually)?",
            "Why avoid plaintext tfvars in Git?",
            "How do you redaction-check plan logs?",
            "What IAM controls protect remote state?",
            "How should modules declare sensitive outputs?",
            "What is a secure pattern for rotating secrets with Terraform?",
            "Why is write-only thinking useful for passwords?",
        ],
    ),
    (
        "policy-as-code-overview",
        "Introduce policy-as-code guardrails for Terraform plans using Sentinel/OPA-style concepts without vendor lock-in thinking.",
        "policy as code for Terraform plans",
        [
            "What problem does policy as code solve?",
            "Where should policies run in a pipeline?",
            "What is the difference between advisory and hard-mandatory policy?",
            "Give examples of policies worth enforcing first.",
            "How do policies relate to module defaults?",
            "Why evaluate plans rather than only applied state?",
            "How do you test policies themselves?",
            "What organisational ownership model works for policies?",
            "How do exceptions get managed safely?",
            "What is the relationship to CIS / Well-Architected ideas?",
            "How do you avoid policy sprawl?",
            "When is a policy the wrong tool versus a module default?",
        ],
    ),
    (
        "terraform-in-ci-cd-pipelines",
        "Run Terraform in CI with plan artifacts, reviews, least-privilege credentials, and apply gates.",
        "Terraform in CI/CD pipelines",
        [
            "What stages belong in a Terraform pipeline?",
            "How do you pass plan artifacts between jobs?",
            "Why separate plan and apply permissions?",
            "How does OIDC improve cloud auth from CI?",
            "What should block a merge?",
            "How do you handle manual approval for production?",
            "Where do you store backend config in CI?",
            "How do you prevent concurrent applies?",
            "What logs must you treat as sensitive?",
            "How do matrix builds work for many roots?",
            "What is a safe destroy policy in CI?",
            "How do you promote the same commit across environments?",
        ],
    ),
    (
        "production-patterns-and-capstone",
        "Assemble production patterns: remote state, modules, CI, secrets, and a capstone root that ties the track together.",
        "production Terraform patterns and the capstone lab",
        [
            "List five production checklist items before first apply.",
            "How do you structure repos for many teams?",
            "When do you split state files?",
            "How do you handle blast radius in modules?",
            "What observability surrounds Terraform changes?",
            "How do you roll back a bad apply?",
            "What documentation must every root module include?",
            "How do you onboard a new engineer to a Terraform mono-repo?",
            "What is the relationship between GitOps and Terraform?",
            "How do you measure Terraform delivery lead time?",
            "What anti-patterns appear in long-lived state?",
            "How would you extend this capstone to a real cloud provider?",
        ],
    ),
]:
    qs = "\n".join(f"{i}. {q}" for i, q in enumerate(extra_key_qs, 1))
    S(
        slug,
        description=description,
        extra_theory=dedent(
            f"""\
            ### Why this topic matters in production

            Teams that skip **{topic_focus}** eventually pay in outages: unreviewable plans, brittle
            refactors, or secrets leaking into logs. Treat this tutorial as the minimum bar for merging
            Terraform changes on a shared state file.

            ### Practical mental model

            1. Write the smallest config that proves the idea
            2. `fmt` / `validate` / `plan` until the diff matches your intent
            3. Apply only after you can explain every create/update/replace line
            4. Destroy lab resources so the next exercise starts clean
            """
        ),
        extra_walkthrough=dedent(
            f"""\
            Re-read every argument in the lab through the lens of **{topic_focus}**.
            For each resource address, ask: what happens on the next plan if I change this value?
            Update in place, replace, or no-op? That habit is how you avoid surprise destroys.
            """
        ),
        validation=dedent(
            f"""\
            Run the lab to completion, then confirm:

            ```bash
            terraform fmt -check
            terraform init -input=false
            terraform validate
            terraform plan -input=false
            ```

            | Check | Pass criteria |
            |-------|----------------|
            | Formatting | `fmt -check` exits 0 |
            | Configuration | `validate` succeeds after init |
            | Intent | Plan matches the tutorial’s expected creates/updates only |
            | Topic focus | You can explain how this lab demonstrates {topic_focus} |
            | Cleanup | Destroy (or documented teardown) left no stray lab files |
            """
        ),
        best_practices=dedent(
            f"""\
            - Keep examples small enough to run without cloud credentials unless the topic requires otherwise
            - Document assumptions (CLI version, providers, working directory) at the top of the root module
            - Prefer explicitness over cleverness when teaching **{topic_focus}**
            - Add CI checks (`fmt`, `validate`, plan) as soon as a root is shared
            - Write outputs that help the next human debug, not just the next machine
            """
        ),
        security=dedent(
            f"""\
            - Assume state and plan output may contain secrets related to **{topic_focus}**
            - Use least-privilege credentials whenever a provider needs authentication
            - Do not commit tfvars with real secrets; use examples with placeholders
            - Review plans for unexpected destroys before apply
            - Limit who can unlock state and who can approve production applies
            """
        ),
        troubleshooting=dedent(
            f"""\
            | Issue | Cause | Solution |
            |-------|-------|----------|
            | validate fails | Missing init or syntax error | Run `terraform init`, read the file:line in the error |
            | Plan shows replace unexpectedly | ForceNew argument changed | Confirm intent; use moved/lifecycle if refactoring |
            | Provider auth errors | Credentials not available | Export the documented env vars for the provider |
            | Topic confusion around {topic_focus} | Skipped theory | Re-read Theory, then re-run the lab from a clean directory |
            | Leftover lab files | Destroy skipped | Re-run destroy or delete the lab directory after state cleanup |
            """
        ),
        interview=qs,
        summary=dedent(
            f"""\
            - Master **{topic_focus}** before moving to the next tutorial in the track
            - Every shared root needs formatting, validation, and a reviewed plan
            - Prefer small, reversible labs that you can destroy confidently
            - Carry security and state hygiene forward into every later module
            """
        ),
    )


SECTION_ORDER = [
    "Validation",
    "Best Practices",
    "Security Considerations",
    "Common Mistakes",
    "Troubleshooting",
    "Interview Questions",
    "Summary",
    "Related Tutorials",
    "References",
]


def replace_frontmatter_description(text: str, description: str) -> str:
    return re.sub(
        r'^description:.*$',
        f'description: "{description}"',
        text,
        count=1,
        flags=re.M,
    )


def strip_boilerplate_walkthrough(text: str) -> str:
    return text.replace(
        "\nExplain every resource argument you introduced in the lab: why it exists, what happens if omitted, "
        "and how it appears in state after apply. Keep `required_version` and `required_providers` in every "
        "root module you create going forward.\n",
        "\n",
    )


def inject_extras(text: str, extra_theory: str, extra_walkthrough: str) -> str:
    if extra_theory.strip():
        text = re.sub(
            r"(^## Hands-on Lab\n)",
            extra_theory.strip() + r"\n\n\1",
            text,
            count=1,
            flags=re.M,
        )
    if extra_walkthrough.strip():
        text = re.sub(
            r"(^## Validation\n)",
            extra_walkthrough.strip() + r"\n\n\1",
            text,
            count=1,
            flags=re.M,
        )
    return text


def replace_tail(text: str, data: dict[str, str], slug: str) -> str:
    """Replace from ## Validation through end of ## Summary; keep Related/References."""
    m = re.search(r"^## Validation\n", text, re.M)
    rel = re.search(r"^## Related Tutorials\n", text, re.M)
    if not m or not rel:
        raise SystemExit(f"markers missing in {slug}")

    related_and_refs = text[rel.start() :]
    head = text[: m.start()]

    # Keep Common Mistakes from original if present
    mistakes_m = re.search(
        r"^## Common Mistakes\n(.*?)(?=^## Troubleshooting\n)",
        text,
        re.M | re.S,
    )
    mistakes = mistakes_m.group(0).strip() if mistakes_m else "## Common Mistakes\n\nSee the lab warnings above."

    # Guard: never drop Hands-on Lab / Code Walkthrough
    if "## Hands-on Lab" not in head:
        raise SystemExit(f"Hands-on Lab missing from head for {slug}")

    tail = "\n\n".join(
        [
            "## Validation\n\n" + data["validation"].strip(),
            "## Best Practices\n\n" + data["best_practices"].strip(),
            "## Security Considerations\n\n" + data["security"].strip(),
            mistakes,
            "## Troubleshooting\n\n" + data["troubleshooting"].strip(),
            "## Interview Questions\n\n" + data["interview"].strip(),
            "## Summary\n\n" + data["summary"].strip(),
            related_and_refs.strip(),
        ]
    )
    return head + tail + "\n"


def main() -> None:
    for slug, data in SECTIONS.items():
        path = TF / f"{slug}.md"
        if not path.exists():
            print("skip missing", path)
            continue
        text = path.read_text(encoding="utf-8")
        text = replace_frontmatter_description(text, data["description"])
        text = strip_boilerplate_walkthrough(text)
        # Only inject extras once
        if "### Why this topic matters in production" not in text and "### Why version managers matter" not in text:
            text = inject_extras(text, data.get("extra_theory", ""), data.get("extra_walkthrough", ""))
        text = replace_tail(text, data, slug)
        path.write_text(text, encoding="utf-8")
        print(f"updated {slug} ({len(text)} chars)")


if __name__ == "__main__":
    main()
