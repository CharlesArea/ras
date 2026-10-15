"""Reusable report template catalog and starter block blueprints."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


TEMPLATE_CATALOG: dict[str, dict[str, Any]] = {
    "executive-brief": {
        "display_name": "Executive brief",
        "description": "A concise management readout with a supported finding and next action.",
        "blocks": [
            ("executive-summary", "executive_summary", "Executive summary", "State the supported finding, implication, and next action."),
            ("decision", "recommendation", "Recommended next action", "Turn the supported finding into an actionable next step."),
        ],
    },
    "decision-memo": {
        "display_name": "Decision memo",
        "description": "A structured choice between options with trade-offs, recommendation, and decision ask.",
        "blocks": [
            ("executive-summary", "executive_summary", "Executive summary", "Frame the decision and the answer in one page."),
            ("options", "comparison", "Options and trade-offs", "Compare the available paths against the decision criteria."),
            ("recommendation", "recommendation", "Recommendation and decision ask", "State the recommended path, rationale, owner, and timing."),
        ],
    },
    "research-synthesis": {
        "display_name": "Research synthesis",
        "description": "An evidence-led synthesis that separates findings, limitations, and implications.",
        "blocks": [
            ("executive-summary", "executive_summary", "Executive summary", "State the answer supported by the evidence set."),
            ("evidence", "finding", "Evidence and findings", "Organize the strongest findings with source references."),
            ("limitations", "narrative", "Limitations and gaps", "Make uncertainty, omitted material, and evidence gaps explicit."),
            ("implications", "recommendation", "Implications", "Translate the synthesis into practical implications."),
        ],
    },
    "analytical-deep-dive": {
        "display_name": "Analytical deep dive",
        "description": "A long-form analysis organized around baseline, drivers, evidence, and implications.",
        "blocks": [
            ("executive-summary", "executive_summary", "Executive summary", "Answer the central analytical question before the detail."),
            ("baseline", "narrative", "Baseline and definitions", "Set the period, comparison group, and key definitions."),
            ("drivers", "finding", "Drivers and evidence", "Explain the mechanisms supported by the evidence."),
            ("implications", "recommendation", "Implications and outlook", "Convert analysis into planning implications and risks."),
        ],
    },
    "comparative-evaluation": {
        "display_name": "Comparative evaluation",
        "description": "A before/after, option, vendor, or policy comparison with explicit criteria.",
        "blocks": [
            ("executive-summary", "executive_summary", "Executive summary", "State the comparison result and the main caveat."),
            ("criteria", "narrative", "Evaluation criteria", "Define the criteria and evidence used for the comparison."),
            ("comparison", "comparison", "Comparison", "Show the differences in a structured table or visual."),
            ("conclusion", "recommendation", "Conclusion", "State the preferred interpretation or next action."),
        ],
    },
    "proposal-business-case": {
        "display_name": "Proposal and business case",
        "description": "A case for change with benefits, costs, risks, and an approval path.",
        "blocks": [
            ("executive-summary", "executive_summary", "Executive summary", "State the case for change and the requested decision."),
            ("case-for-change", "finding", "Case for change", "Describe the problem, opportunity, or cost of inaction."),
            ("economics", "comparison", "Benefits, costs, and risks", "Make the value logic, assumptions, and trade-offs explicit."),
            ("recommendation", "recommendation", "Approval and next steps", "State the requested approval and the first delivery steps."),
        ],
    },
    "strategy-roadmap": {
        "display_name": "Strategy roadmap",
        "description": "A strategy translated into priorities, milestones, measures, and ownership.",
        "blocks": [
            ("executive-summary", "executive_summary", "Executive summary", "State the strategy and the outcome it is intended to create."),
            ("priorities", "finding", "Strategic priorities", "Describe the few priorities that guide choices."),
            ("roadmap", "timeline", "Roadmap and milestones", "Sequence the work with timing, dependencies, and owners."),
            ("measures", "metric_panel", "Measures and governance", "Define how progress will be monitored and reviewed."),
        ],
    },
    "status-progress": {
        "display_name": "Status and progress review",
        "description": "A recurring operating review for progress, blockers, risks, and next steps.",
        "blocks": [
            ("executive-summary", "executive_summary", "Executive summary", "State overall status and the most important change since last review."),
            ("progress", "finding", "Progress and completed work", "Record what moved forward and what evidence supports the status."),
            ("risks", "risk", "Risks and blockers", "Make current risks, dependencies, and decisions visible."),
            ("next-steps", "recommendation", "Next steps", "List the committed actions, owners, and dates."),
        ],
    },
    "performance-kpi": {
        "display_name": "Performance and KPI review",
        "description": "A metric-led review with trends, context, variance, and operating action.",
        "blocks": [
            ("executive-summary", "executive_summary", "Executive summary", "State the headline performance and the operating implication."),
            ("kpi-trend", "chart", "KPI trend", "Show the reported trend without implying unsupported causation."),
            ("variance", "finding", "Variance and drivers", "Explain the meaningful changes and evidence behind them."),
            ("actions", "recommendation", "Actions and owners", "Convert the KPI readout into operating actions."),
        ],
    },
    "audit-assessment": {
        "display_name": "Audit assessment",
        "description": "A formal assessment of controls, findings, evidence gaps, and remediation.",
        "blocks": [
            ("executive-summary", "executive_summary", "Executive summary", "State the overall assessment and material findings."),
            ("scope", "narrative", "Scope and criteria", "Define the assessed scope, period, and criteria."),
            ("findings", "finding", "Findings and evidence", "Record findings with severity, evidence, and impact."),
            ("remediation", "recommendation", "Remediation plan", "Set corrective actions, owners, and target dates."),
        ],
    },
    "compliance-risk": {
        "display_name": "Compliance and risk review",
        "description": "A risk-focused review of obligations, exposures, controls, and mitigations.",
        "blocks": [
            ("executive-summary", "executive_summary", "Executive summary", "State the material exposure and the recommended response."),
            ("obligations", "narrative", "Obligations and scope", "Identify the applicable requirements and boundaries."),
            ("risk-register", "risk", "Risk register", "Describe risks, likelihood, impact, controls, and owners."),
            ("actions", "recommendation", "Mitigations and next steps", "Set the practical response and escalation path."),
        ],
    },
    "technical-architecture": {
        "display_name": "Technical architecture",
        "description": "A system explanation with boundaries, interfaces, data flow, and operational concerns.",
        "blocks": [
            ("executive-summary", "executive_summary", "Executive summary", "State the architecture decision and the key constraint."),
            ("architecture", "diagram", "Architecture and request path", "Show the major components and their relationships."),
            ("interfaces", "narrative", "Interfaces and data contracts", "Describe boundaries, dependencies, and data movement."),
            ("operations", "recommendation", "Operations and next steps", "State reliability, security, and implementation priorities."),
        ],
    },
    "incident-postmortem": {
        "display_name": "Incident postmortem",
        "description": "A blameless incident record covering impact, timeline, root cause, and follow-up.",
        "blocks": [
            ("executive-summary", "executive_summary", "Executive summary", "State what happened, impact, and current status."),
            ("timeline", "timeline", "Incident timeline", "Sequence the observed events and response actions."),
            ("root-cause", "finding", "Root cause and contributing factors", "Separate direct cause, contributing factors, and evidence."),
            ("actions", "recommendation", "Corrective actions", "Set prevention, detection, and recovery actions with owners."),
        ],
    },
    "investigation-root-cause": {
        "display_name": "Investigation and root cause",
        "description": "A structured investigation that keeps hypotheses, evidence, and conclusions separate.",
        "blocks": [
            ("executive-summary", "executive_summary", "Executive summary", "State the current conclusion and confidence level."),
            ("evidence", "finding", "Evidence record", "List the observations and source material that constrain the inquiry."),
            ("hypotheses", "comparison", "Hypotheses and tests", "Compare candidate explanations and the evidence for each."),
            ("conclusion", "recommendation", "Conclusion and follow-up", "State what is supported, unresolved, and next."),
        ],
    },
    "policy-sop": {
        "display_name": "Policy and SOP",
        "description": "A repeatable operating standard with scope, procedure, controls, and exceptions.",
        "blocks": [
            ("executive-summary", "executive_summary", "Purpose and scope", "State who the policy serves and what it covers."),
            ("policy", "narrative", "Policy requirements", "Describe the rules, roles, and required behaviors."),
            ("procedure", "timeline", "Procedure", "Sequence the repeatable steps and decision points."),
            ("controls", "recommendation", "Controls and exceptions", "Describe monitoring, escalation, and approved exceptions."),
        ],
    },
    "case-study": {
        "display_name": "Case study",
        "description": "A documented example that connects context, intervention, result, and lessons learned.",
        "blocks": [
            ("executive-summary", "executive_summary", "Executive summary", "State the case and the lesson in a short readout."),
            ("context", "narrative", "Context and challenge", "Describe the setting, constraints, and starting point."),
            ("intervention", "timeline", "Intervention and execution", "Describe what changed and how the work unfolded."),
            ("lessons", "recommendation", "Results and lessons", "State the observed result, limits, and transferable lessons."),
        ],
    },
}


def template_ids() -> list[str]:
    return list(TEMPLATE_CATALOG)


def get_template(template_id: str) -> dict[str, Any]:
    try:
        return deepcopy(TEMPLATE_CATALOG[template_id])
    except KeyError as exc:
        raise ValueError(f"Unknown RAS template: {template_id}") from exc


def template_summary(template_id: str) -> dict[str, Any]:
    template = get_template(template_id)
    return {
        "id": template_id,
        "display_name": template["display_name"],
        "description": template["description"],
        "block_ids": [item[0] for item in template["blocks"]],
    }


__all__ = ["TEMPLATE_CATALOG", "get_template", "template_ids", "template_summary"]
