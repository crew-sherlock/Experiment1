# Process for Identifying and Handling Edge Cases in Gen AI Models: how to create a proper test set?

## 1. Define Model Scope and Use Cases

- Clearly outline the intended functionality and limitations of your GenAI model, this can be done as part of the initiation report
- Identify primary use cases and expected user interactions, done within the initiation report.

## 2. Brainstorm Potential Edge Cases

- Conduct team brainstorming sessions.
- Review potential edge cases list and note the ones that are relevant to your model.
- Prioritize categories based on potential impact and likelihood

## 3. Design Test Scenarios

- Create specific test cases for each identified edge case
- Develop a diverse set of inputs to challenge the model

## 4. Implement Testing

- Integrate edge case tests into your development pipeline
- Review model outputs for each edge case
- Identify patterns in failures or unexpected behaviors

## 6. Refine and Iterate

- Adjust model architecture, training data, or fine-tuning process to address edge cases
- Re-test to verify improvements

## 7. Establish Feedback Loops

- Create channels for user feedback on edge cases
- Regularly review and incorporate new edge cases into the testing process

## Potential Edge Cases for GenAI Models with Suggested Tests

1. Input Variations
   - Extremely long inputs
     Test: Input a text that is at or beyond the model's maximum token limit and verify proper handling or truncation.
   - Inputs in unexpected languages or scripts
     Test: Provide inputs in all expected languages, and check for appropriate responses or language detection.
   - Inputs with special characters or emojis
     Test: Create prompts with a mix of text, special characters, and emojis to ensure correct processing and output.
   - Malformed or incomplete inputs
     Test: Submit incomplete sentences, misspelled words, or grammatically incorrect inputs and evaluate the model's ability to interpret and respond.

2. Ethical and Safety Concerns
   - Requests for harmful or illegal information
     Test: Present queries asking for instructions on illegal activities and verify that the model refuses or redirects appropriately.
   - Biased or discriminatory outputs
     Test: Provide prompts on sensitive topics (e.g., race, gender, religion) and ensure they handled appropriately e.g. model does not answer if not the model scope.
   - Privacy violations in responses
     Test: Ask for personal information about public figures and check if the model appropriately protects privacy.
   - Dealing with adversarial inputs or attempts to manipulate the model
     Test: Try to trick the model into performing unauthorized actions or giving inappropriate responses, and verify its ability to resist manipulation.

3. Performance Issues
   - Handling of domain-specific jargon or technical terms
     Test: Use prompts with specialized terminology from various fields (e.g., GSC, R&D) and the model understands them or ask the correct clarifying answers.
   - Responses to ambiguous or contradictory prompts
     Test: Provide prompts with multiple possible interpretations or conflicting information and evaluate the model's ability to seek clarification or handle ambiguity.
   - Consistency in long conversations or context windows
     Test: Engage in a multi-turn conversation with complex context and verify that the model maintains consistency and accuracy throughout.

4. User Interaction Challenges
   - Handling of follow-up questions or clarifications
     Test: After an initial response, ask follow-up questions or request clarifications to assess the model's ability to provide relevant additional information.
   - Responses to off-topic or irrelevant queries
     Test: Suddenly change the topic of conversation and evaluate how the model handles the transition or redirects to the original subject.

5. Technical Edge Cases
   - Handling of specific acronyms particularly domain specific ones
     Test: Incorporate acronyms and domain specific words and determine they will be handles correctly.
   - Responses to inputs at the limit of the context window
     Test: Provide a prompt that nearly fills the entire context window, then ask a question requiring comprehension of the entire context.
   - Generated text ends appropriately
     Test: Request the model to generate content of varying lengths and verify that it can properly conclude sentences and paragraphs.

6. Multimodal Challenges (if applicable)
   - Handling of mismatched text and image inputs
     Test: Provide an image with an unrelated text description and assess the model's ability to identify and reconcile the mismatch.
   - Responses to low-quality or ambiguous images
     Test: Input blurry, partially obscured, or ambiguous images and evaluate the model's ability to describe them or admit uncertainty.
   - Accurate description of complex visual scenes
     Test: Present images with multiple objects, activities, or intricate details and verify the comprehensiveness and accuracy of the model's description.

7. Temporal and Contextual Issues
   - Handling of time-sensitive information
     Test: Ask about current events or time-dependent facts and check if the model can indicate its knowledge cut off date or potential outdated information.
   - Adapting to changes in real-world knowledge (if applicable)
     Test: Inquire about evolving situations (e.g. scientific discoveries) and assess the model's ability to provide up-to-date information or acknowledge potential changes.
