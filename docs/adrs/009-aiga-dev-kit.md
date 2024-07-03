# 9. AIGA dev kit integration

Date: 2024-07-02

## Status

Accepted

## Context

AIGA will require using the dev kit to provision resource, at the moment the dev kit workflow is not standardize and not automated.
It makes it hard to automate it as part of AIGA, we would like to have some standards in order to connect the dev kit with AIGA, even if not in a full automated way.

## Requirements for the dev kit

How will the dev kit Integrate/connect with AIGA.

The current flow of requesting a dev kit is:
Raise a ticket -> More information is requested -> Request approved -> Create Resources -> Receive an email with the information (keyvault, models names, region etc.).

Problem - no conventions and standardization, for both request and response there are often missing details which require many iterations:

- No standardize way for the request.
- No standardize way for the response.

## Conclusions

We won't be able to fully automate the work with the dev kit during this time, however, we would like to try and have a reliable, managed process to ease the use of the dev kit while using AIGA.
By creating interfaces on the request and response side, with appropriate instructions, we will be able to ease the user usage with the dev kit and downsize the amount of cycles it takes to get the request approved.

## Action items

- Create conventions for dev kit request and response which will meet AIGA requirements.
