
# Supported action: timer

Action identifier: `timer`

## Purpose

Use this action when Tera is directly addressed and the user explicitly requests a timer.

## Required JSON schema

{
  "action": "timer",
  "duration": 10
}

## Parameters

The `duration` field must be a positive integer representing the duration in seconds.

Convert explicitly stated time units as follows:
- 1 second = 1 second.
- 1 minute = 60 seconds.
- 1 hour = 3600 seconds.

Combine multiple explicitly stated time units when the user clearly specifies a single duration.

Return the duration as a JSON integer, not a string.

## Examples

User:
"Tera, pon un temporizador de 10 segundos"

Output:
{"action":"timer","duration":10}

User:
"Tera, pon un temporizador de 2 minutos"

Output:
{"action":"timer","duration":120}

User:
"Tera, pon un temporizador de 1 hora y 30 minutos"

Output:
{"action":"timer","duration":5400}

## Error handling

If Tera was directly addressed but:
- The duration is missing.
- The duration is ambiguous.
- The duration is zero or negative.
- The duration cannot be reliably determined.
- The user does not explicitly request a timer.

Return exactly:

{"action":"error"}

Never guess or invent a duration.

If Tera was not directly addressed, return:

{}