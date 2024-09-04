# ADR 17: Method to Share AIGA Responses and Receive Scoring from Stakeholders

## Context

Our organization is implementing the AIGA system to improve efficiency during the development of Gen AI models. To ensure the quality and relevance of the AI-generated responses from the Gen AI models we are developing, we need a systematic method to share these responses with stakeholders for review and scoring. This feedback is crucial for continuous and iterative improvement of the AI model.

Key considerations include:

- Version control of AI responses
- Ease of collaboration among stakeholders
- Data privacy and security
- Integration with existing workflows
- Scalability to accommodate multiple projects and stakeholders

## Decision

After careful consideration of our requirements and available resources, we have decided to use Microsoft Teams as the primary platform for sharing AIGA responses and collecting stakeholder feedback.

Specifically, we will:

1. Create a dedicated MS Teams channel for each AIGA project with a standard folder structure.
2. Use Teams' file sharing capabilities to distribute AI model-generated responses.
3. Utilize Teams' collaborative features (comments, mentions, etc.) for stakeholders to provide feedback and scoring.
4. Implement a structured naming convention and folder organization within Teams for version control.
5. Leverage Teams' integration with other Microsoft tools (e.g., Forms for structured feedback, Power Automate for workflow automation) to enhance the feedback process in the short-term.

This an intermediate decision, with a future possibility of having a custom web application.

## Status

Accepted

## Consequences

### Positive

- MS Teams is widely used within our organization, ensuring high adoption rates and minimal training requirements of stakeholders (our key user group). This is advantageous as a frictionless solution would support adequate human validation support.
- Built-in security features of MS Teams align with our data privacy needs. CSI folders can be created for sensitive data.
- Collaborative features enable real-time feedback and discussions among stakeholders.
- Integration with other Microsoft tools allows for potential future enhancements to the feedback process.
- Version control can be managed through Teams' file history and naming conventions of files during the saving process.

### Negative

- Requires creation of new Teams channels for each project, which may lead to proliferation of channels.
- May not be as customizable as a purpose-built solution.
- Stakeholders need to actively check Teams for new content, unlike email notifications.
- Limited advanced analytics capabilities for feedback data without additional tools or integrations.

## Alternatives Considered

1. **Email-based System**
   - Pros: Familiar to all users, easy to implement
   - Cons: Lacks real-time collaboration, potential for lost or overlooked emails, difficult version control

2. **Custom Web Application**
   - Pros: Highly customizable, could provide advanced analytics
   - Cons: Expensive to develop and maintain, longer implementation time, additional security considerations and contains similar limitations to real-time collaboration between stakeholders.

3. **Third-party Collaboration Tools** (e.g., Slack, Confluence)
   - Pros: Purpose-built for collaboration, may offer more features
   - Cons: Additional cost (for licenses and time for stakeholders to gain access), potential integration challenges, new tool for many users to learn, privacy concerns for CSI data.

## Review Date

This decision will be reviewed in 7 months (March 2025) to assess its effectiveness and consider any necessary adjustments based on user feedback and evolving needs.
