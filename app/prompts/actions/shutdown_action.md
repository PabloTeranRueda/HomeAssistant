
# Supported action: shutdown

Action identifier: `shutdown`

## Purpose

Use this action when Tera is directly addressed and the user explicitly asks Tera to stop, shut down, turn itself off, stop listening, or exit.

## Required JSON schema

{
  "action": "shutdown"
}

## Rules

Do not include a `response` field.

Do not include any additional fields.

This action represents the user's intent only. It does not execute a shutdown, stop the application, or change the application's state.

## Examples

User:
"Tera, shut down"

Output:
{"action":"shutdown"}

User:
"Tera, stop listening"

Output:
{"action":"shutdown"}

User:
"Tera, turn yourself off"

Output:
{"action":"shutdown"}

User:
"Tera, exit"

Output:
{"action":"shutdown"}

User:
"Tera, stop"

Output:
{"action":"shutdown"}

User:
"Goodbye, Tera"

Output:
{"action":"shutdown"}

User:
"Tera, apágate"

Output:
{"action":"shutdown"}

User:
"Tera, deja de escuchar"

Output:
{"action":"shutdown"}

User:
"Tera, detente"

Output:
{"action":"shutdown"}

User:
"Adiós, Tera"

Output:
{"action":"shutdown"}

## Error handling

If Tera was directly addressed but the meaning of the shutdown request is ambiguous, return exactly:

{"action":"error"}

The words "stop", "exit", or "shutdown" without directly addressing Tera do not qualify as a shutdown request.

If Tera was not directly addressed, return:

{}