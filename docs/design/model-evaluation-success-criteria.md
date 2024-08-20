# Success Criteria for a Gen AI Model

## Introduction

This document provides a structured approach for stakeholders to critique and evaluate the output of a Gen AI model. It includes evaluation criteria, scoring methods, and guidelines for providing comprehensive feedback. The scoring criteria is agreed at the beginning of the process and it is used to create and evaluate the Proof of Concept (PoC). The goal of this critique is to provide constructive feedback that will help improve the model's performance and ensure it meets stakeholder needs and expectations.

## Evaluation Process for Stakeholders

1. Familiarize yourself with the model's intended purpose and objectives.
2. Review the model's output across multiple test cases or scenarios.
3. Score the practical applicability of the answer on a scale of 1-5 (see Scoring Guide below).
4. Provide specific examples and comments for each scenario where the model answer is not <4.

## Evaluation Criteria

The model answers will be evaluated through the use of other LLMs, the metrics assessed by LLMs are Groundedness, Accuracy and Relevance. The human validation will assess the practical applicability of the model answer, see below for the definition of each evaluation criteria.

### LLM Calculated Metric - Groundedness

* Does the output align with established facts and knowledge?
* Are claims and statements supported by reliable sources or evidence?
* Is there a clear distinction between factual information and opinions or speculations?

### LLM Calculated Metric - Accuracy

* How precise and correct is the information provided by the system?
* Are there any factual errors or misrepresentations in the output?
* Does the system maintain consistency in its responses across different queries?

### LLM Calculated Metric - Relevance

* How closely does the output match the user's query or intent?
* Is the information provided directly applicable to the user's needs?
* Does the output prioritize the most important or useful information for the given context?

### Human Validation - Practical Applicability

* How useful is the output for its intended purpose?
* Can the information or suggestions be readily implemented or applied?

## Scoring Guide

Use the following scale to score each model answer:

1 - Poor: Fails to meet expectations

2 - Fair: Partially meets expectations with significant room for improvement

3 - Good: Meets expectations but with some areas for improvement

4 - Very Good: Exceeds expectations in most areas

5 - Excellent: Consistently exceeds expectations

## Evaluation Form Example

| Model Prompt | Gen AI Model answer | Practical Applicability Score (1-5) | Comments/ Examples |
|--------------|---------------------|-------------------------------------|-------------------|
| What are the critical quality attributes (CQAs) that must be monitored during the granulation process in tablet manufacturing, and how do they influence the final product's efficacy? | Critical Quality Attributes (CQAs) in the granulation process of tablet manufacturing include particle size distribution, moisture content, and granule density. These attributes are crucial as they directly affect the compressibility of the granules, tablet hardness, disintegration time, and ultimately, the drug's bioavailability. | 5 | |
| What is the primary purpose of lyophilization in pharmaceutical manufacturing? | Lyophilization, or freeze-drying, is primarily used to stabilize and preserve sensitive pharmaceutical compounds by removing water content, ensuring the product's efficacy and shelf life without the need for refrigeration. | 2 | Describes the two methods but does not compare the two and how they affect the product's quality |
| What is the role of a clean room in pharmaceutical production? | A clean room is used to keep the manufacturing area clean. | 2 | The answer is overly simplistic and lacks important details.|
