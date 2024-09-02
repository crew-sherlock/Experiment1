# User Story 89856 – Structured Way to Evaluate GenAI output

Date: 2024-08-12

## Status

Accepted

## 1. Initial Planning and Stakeholder Identification

### Who: Product team + Senior stakeholders

* Define Objectives: Clearly define the purpose of the Gen AI model and the expected outcomes based on the problem statement/opportunity.

• Identify Stakeholders: Identify key stakeholders, including business owners, developers, and end-users.

• Set Expectations: Discuss the scope, timeline, and deliverables with all stakeholders. Establish criteria for successful chatbot responses.

### AIGA Assets

• Risk Assessment of Gen AI project as part of the Accountability Report

• Template for success criteria metrics for stakeholders.

## 2. Data Collection and Storage

### Who: Product team + Stakeholders

• Gather Requirements: Collect specific requirements from stakeholders regarding the model's functionality and content.

• Collect Data: Gather data from existing customer interactions, FAQs, and other resources relevant to the Gen AI's domain.

• Pre-process Data: Clean and store the data.

### AIGA Assets

• Pipeline for anonymization, if required, requirements identified from the Accountability Report as risks and mitigation Actions

• Document Loading pipeline

• AIGA Starter

## 3. Initial Gen AI Development

### Who: Product team

• Develop Initial Gen AI Responses: Create an initial set of responses based on the collected data and stakeholder input.

• Test with Sample Data: Test the Gen AI model with sample inputs to ensure it provides relevant responses as detailed by success criteria from stakeholders

### AIGA Assets

• Index Creation and AML pipeline.

• RAG Experimentation Repository

• Capture of edge cases

## 4. Validation Process

### Who: Product team + Stakeholders

• Review and Approval by Stakeholders: Share the initial responses with stakeholders for feedback and approval.

• Create Validation Criteria: Develop a set of criteria to evaluate the Gen AI's responses, including accuracy, relevance, tone, and completeness and scoring metric.

• Golden Response Dataset: Begin building a golden response dataset/ground truth by curating approved and validated responses.

### AIGA Assets

• Method to exchange model response rating data with stakeholders for response ratings.

• Golden data generation script

## 5. Iterative Refinement

### Who: Product team + Testers/Users + Stakeholders

• Conduct User Testing: Involve a small group of users in testing the model to identify gaps and areas for improvement.

• Collect Feedback: Gather feedback from both stakeholders and users on the model's performance.

• Refine Responses: Use the feedback to refine responses, improve the language model, and update the golden response dataset.

• Continuous Iteration: Repeat the testing and refinement process iteratively until the model meets the quality standards set by stakeholders.

### AIGA Assets

• Fine tuning prompts within the inference flow.

## 6. Final Validation and Launch Preparation

### Who: Product team + Stakeholders

• Final Stakeholder Review: Conduct a final review with stakeholders to ensure all concerns are addressed and the Gen AI meets the defined criteria.

• Golden Response Dataset Finalization: Finalize the golden response dataset as a reference for future updates and training.

• Train and Optimize: Optimize the Gen AI using the finalized dataset, ensuring it performs well under varied conditions.

### AIGA Assets

• Stress testing e.g. high load, strange queries.

## 7. Documentation and Knowledge Sharing

### Who: Product team

• Document the Process: Document the entire process, including decisions made, data sources used, and the criteria for response validation.

• Share Best Practices: Share learnings and best practices with the team and stakeholders to ensure knowledge transfer and consistency in future projects.

### AIGA Assets

• Template for documentation to cover data sources, validation criteria etc
